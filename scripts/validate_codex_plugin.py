#!/usr/bin/env python3
"""Run the bundled Codex plugin validator without a machine-specific path."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


validator = Path.home() / ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py"
plugin = Path(__file__).resolve().parents[1] / "plugins/codex/sandipb-agents"

if validator.is_file():
    subprocess.run([sys.executable, str(validator), str(plugin)], check=True)
else:
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    required = {"name", "version", "description", "author", "skills", "interface"}
    missing = required - manifest.keys()
    if missing:
        raise SystemExit(f"Codex manifest missing fields: {sorted(missing)}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise SystemExit("Codex manifest version must be strict semantic versioning")
    skills = (plugin / manifest["skills"]).resolve()
    if skills != (plugin / "skills").resolve() or not skills.is_dir():
        raise SystemExit("Codex manifest skills must resolve to the plugin skills directory")
    if not manifest["interface"].get("defaultPrompt"):
        raise SystemExit("Codex manifest interface.defaultPrompt is required")
