#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Summarize Fireworks billing usage exported by firectl."""

from __future__ import annotations

import argparse
import csv
import subprocess
import tempfile
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

MAX_RANGE_DAYS = 31
REQUIRED_COLUMNS = {"usage_type", "prompt_tokens", "completion_tokens"}
CommandRunner = Callable[[list[str]], str]


def run_firectl_command(args: list[str]) -> str:
    """Run firectl without invoking a shell and return stdout."""
    try:
        result = subprocess.run(
            ["firectl", *args],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
    except FileNotFoundError:
        raise SystemExit(
            "Error: firectl was not found. Install it from "
            "https://docs.fireworks.ai/tools-sdks/firectl/firectl"
        ) from None
    except subprocess.TimeoutExpired:
        raise SystemExit("Error: firectl timed out after 120 seconds.") from None
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "unknown error").strip()
        raise SystemExit(f"Error running firectl: {detail}") from None
    return result.stdout.strip()


def check_authentication(command_runner: CommandRunner = run_firectl_command) -> None:
    """Verify that firectl has a usable authenticated profile."""
    try:
        command_runner(["whoami"])
    except SystemExit as exc:
        raise SystemExit(
            f"{exc}\nAuthenticate with `firectl signin`, then retry."
        ) from None


def parse_date(value: str) -> date:
    """Parse an ISO calendar date for argparse."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected an ISO date (YYYY-MM-DD)") from exc


def resolve_range(start: date | None, end: date | None) -> tuple[date, date]:
    """Resolve and validate an inclusive-start, exclusive-end date range."""
    today = datetime.now(UTC).date()
    resolved_end = end or today
    resolved_start = start or (resolved_end - timedelta(days=1))
    days = (resolved_end - resolved_start).days
    if days <= 0:
        raise ValueError("start date must be earlier than end date")
    if days > MAX_RANGE_DAYS:
        raise ValueError(
            f"date range cannot exceed {MAX_RANGE_DAYS} days; split longer ranges"
        )
    return resolved_start, resolved_end


def _integer(row: dict[str, str], column: str, row_number: int) -> int:
    value = (row.get(column) or "0").strip()
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"invalid integer in {column!r} at CSV row {row_number}: {value!r}"
        ) from exc


def _number(row: dict[str, str], column: str, row_number: int) -> float:
    value = (row.get(column) or "0").strip()
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"invalid number in {column!r} at CSV row {row_number}: {value!r}"
        ) from exc


def summarize_csv(path: Path, start: date, end: date) -> str:
    """Summarize supported usage fields from a Fireworks billing CSV."""
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"billing CSV is missing required columns: {names}")

        totals = {"prompt": 0, "completion": 0, "accelerator_seconds": 0.0}
        by_model: dict[str, dict[str, float | int]] = defaultdict(
            lambda: {"prompt": 0, "completion": 0, "accelerator_seconds": 0.0}
        )
        usage_types: dict[str, int] = defaultdict(int)
        rows = 0

        for row_number, row in enumerate(reader, start=2):
            rows += 1
            prompt = _integer(row, "prompt_tokens", row_number)
            completion = _integer(row, "completion_tokens", row_number)
            accelerator = (
                _number(row, "accelerator_seconds", row_number)
                if "accelerator_seconds" in columns
                else 0.0
            )
            model = (
                (row.get("model_bucket") or "").strip()
                or (row.get("base_model_name") or "").strip()
                or "Unknown"
            )
            usage_type = (row.get("usage_type") or "Unknown").strip() or "Unknown"

            totals["prompt"] += prompt
            totals["completion"] += completion
            totals["accelerator_seconds"] += accelerator
            by_model[model]["prompt"] += prompt
            by_model[model]["completion"] += completion
            by_model[model]["accelerator_seconds"] += accelerator
            usage_types[usage_type] += 1

    lines = [
        f"Period: {start.isoformat()} (inclusive) to {end.isoformat()} (exclusive)",
        f"Rows: {rows:,}",
        (
            f"Total: {totals['prompt']:,} prompt tokens, "
            f"{totals['completion']:,} completion tokens, "
            f"{totals['accelerator_seconds']:,.2f} accelerator seconds"
        ),
    ]
    if rows == 0:
        lines.append("No usage recorded.")
        return "\n".join(lines)

    lines.append("\nBy model:")
    for model, stats in sorted(by_model.items()):
        lines.append(
            f"  {model}: {stats['prompt']:,} prompt tokens, "
            f"{stats['completion']:,} completion tokens, "
            f"{stats['accelerator_seconds']:,.2f} accelerator seconds"
        )
    lines.append("\nRows by usage type:")
    for usage_type, count in sorted(usage_types.items()):
        lines.append(f"  {usage_type}: {count:,}")
    return "\n".join(lines)


def get_usage(
    start: date | None = None,
    end: date | None = None,
    command_runner: CommandRunner = run_firectl_command,
) -> str:
    """Export and summarize Fireworks billing usage."""
    resolved_start, resolved_end = resolve_range(start, end)
    with tempfile.TemporaryDirectory(prefix="fireworks-billing-") as directory:
        csv_path = Path(directory) / "billing-metrics.csv"
        command_runner(
            [
                "billing",
                "export-metrics",
                "--start-time",
                resolved_start.isoformat(),
                "--end-time",
                resolved_end.isoformat(),
                "--filename",
                str(csv_path),
            ]
        )
        if not csv_path.is_file():
            raise ValueError("firectl did not create the requested billing CSV")
        return summarize_csv(csv_path, resolved_start, resolved_end)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize Fireworks billing usage")
    subparsers = parser.add_subparsers(dest="command", required=True)
    usage_parser = subparsers.add_parser(
        "usage", aliases=["spend"], help="summarize exported billing usage"
    )
    usage_parser.add_argument("--start-time", type=parse_date, metavar="YYYY-MM-DD")
    usage_parser.add_argument("--end-time", type=parse_date, metavar="YYYY-MM-DD")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        start, end = resolve_range(args.start_time, args.end_time)
        check_authentication()
        print(get_usage(start, end))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
