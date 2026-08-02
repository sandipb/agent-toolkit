#!/usr/bin/env python3
"""Validate canonical and generated skills with OpenAI's validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
VALIDATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
ROOTS = (
    REPO / "skills",
    REPO / "plugins/codex/sandipb-ai/skills",
)


def main() -> None:
    for root in ROOTS:
        for skill in sorted(root.iterdir()):
            if skill.is_dir():
                if VALIDATOR.is_file():
                    subprocess.run([sys.executable, str(VALIDATOR), str(skill)], check=True)
                else:
                    validate_portable_skill(skill)


def validate_portable_skill(skill: Path) -> None:
    path = skill / "SKILL.md"
    text = path.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise SystemExit(f"invalid frontmatter: {path}")
    frontmatter = text.split("\n---\n", 1)[0][4:]
    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict) or not data.get("name") or not data.get("description"):
        raise SystemExit(f"name and description are required: {path}")


if __name__ == "__main__":
    main()
