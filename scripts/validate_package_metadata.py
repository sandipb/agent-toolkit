#!/usr/bin/env python3
"""Validate shared package identity and manual-invocation invariants."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPO / "plugins/codex/sandipb-agents"
CLAUDE_ROOT = REPO / "plugins/claude/sandipb-agents"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    return yaml.safe_load(text.split("\n---\n", 1)[0][4:])


codex = load_json(CODEX_ROOT / ".codex-plugin/plugin.json")
claude = load_json(CLAUDE_ROOT / ".claude-plugin/plugin.json")
codex_market = load_json(REPO / ".agents/plugins/marketplace.json")
claude_market = load_json(REPO / ".claude-plugin/marketplace.json")

for field in ("name", "version", "description", "license"):
    if codex.get(field) != claude.get(field):
        raise SystemExit(f"host manifests disagree on {field}")

if codex_market["plugins"][0]["name"] != codex["name"]:
    raise SystemExit("Codex marketplace and manifest names disagree")
if codex_market["plugins"][0]["source"]["path"] != "./plugins/codex/sandipb-agents":
    raise SystemExit("Codex marketplace source path is incorrect")
if claude_market["plugins"][0]["name"] != claude["name"]:
    raise SystemExit("Claude marketplace and manifest names disagree")
if claude_market["plugins"][0]["source"] != "./plugins/claude/sandipb-agents":
    raise SystemExit("Claude marketplace source path is incorrect")

canonical_edit = frontmatter(REPO / "skills/edit-technical-docs/SKILL.md")
codex_edit = frontmatter(CODEX_ROOT / "skills/edit-technical-docs/SKILL.md")
claude_edit = frontmatter(CLAUDE_ROOT / "skills/edit-technical-docs/SKILL.md")
if "disable-model-invocation" in canonical_edit or "disable-model-invocation" in codex_edit:
    raise SystemExit("Claude invocation metadata leaked into canonical or Codex skill")
if claude_edit.get("disable-model-invocation") is not True:
    raise SystemExit("Claude technical-editing skill must be manual-only")

openai = yaml.safe_load(
    (CODEX_ROOT / "skills/edit-technical-docs/agents/openai.yaml").read_text()
)
if openai.get("policy", {}).get("allow_implicit_invocation") is not False:
    raise SystemExit("Codex technical-editing skill must be manual-only")
