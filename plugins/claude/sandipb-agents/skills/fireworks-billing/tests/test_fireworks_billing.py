from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "fireworks_billing", SKILL_DIR / "fireworks-billing.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BillingUsageTests(unittest.TestCase):
    def test_summarizes_current_fireworks_schema(self) -> None:
        result = MODULE.summarize_csv(
            SKILL_DIR / "tests/fixtures/billing-metrics.csv",
            date(2026, 2, 17),
            date(2026, 2, 18),
        )
        self.assertIn("150 prompt tokens, 35 completion tokens", result)
        self.assertIn("1,800.00 accelerator seconds", result)
        self.assertIn("Llama: 150 prompt tokens", result)
        self.assertIn("accounts/fireworks/models/custom", result)
        self.assertIn("TEXT_COMPLETION_INFERENCE_USAGE: 2", result)

    def test_empty_export_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text(
                "usage_type,prompt_tokens,completion_tokens,base_model_name\n",
                encoding="utf-8",
            )
            result = MODULE.summarize_csv(path, date(2026, 2, 17), date(2026, 2, 18))
        self.assertIn("Rows: 0", result)
        self.assertIn("No usage recorded.", result)

    def test_changed_schema_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("model,tokens\nfoo,1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required columns"):
                MODULE.summarize_csv(path, date(2026, 2, 17), date(2026, 2, 18))

    def test_range_validation(self) -> None:
        with self.assertRaisesRegex(ValueError, "earlier"):
            MODULE.resolve_range(date(2026, 2, 18), date(2026, 2, 18))
        with self.assertRaisesRegex(ValueError, "31 days"):
            MODULE.resolve_range(date(2026, 1, 1), date(2026, 2, 2))

    def test_export_uses_a_real_temporary_filename(self) -> None:
        fixture = (SKILL_DIR / "tests/fixtures/billing-metrics.csv").read_text(
            encoding="utf-8"
        )
        recorded: list[str] = []

        def fake_runner(arguments: list[str]) -> str:
            recorded.extend(arguments)
            destination = Path(arguments[arguments.index("--filename") + 1])
            destination.write_text(fixture, encoding="utf-8")
            return ""

        result = MODULE.get_usage(date(2026, 2, 17), date(2026, 2, 18), fake_runner)
        self.assertIn("--filename", recorded)
        self.assertNotEqual(recorded[recorded.index("--filename") + 1], "-")
        self.assertIn("Rows: 3", result)


if __name__ == "__main__":
    unittest.main()
