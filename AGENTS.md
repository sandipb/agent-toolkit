# Agent Instructions for skills-directory

This repository is a collection of reusable AI coding agent skills designed for public sharing.

## Repository Purpose

This repo provides ready-to-use skills for AI coding agents (Claude Code, OpenCode, GitHub Copilot,
Cursor, etc.). Each skill is a self-contained package with:
- Skill definition (SKILL.md) that defines triggers, capabilities, and instructions
- Supporting scripts and tools
- Reference documentation to minimize external API calls

**Note**: Skills were originally created for Claude Code but follow a generic format that can be
adapted for other AI coding assistants.

## Skill Structure

Skills are organized under the `skills/` directory:

```
skills/
└── <skill-name>/
    ├── SKILL.md              # Required: skill definition with frontmatter
    ├── CHANGELOG.md          # Required: version history for this skill
    ├── <scripts>             # Optional: helper scripts
    └── references/           # Optional: reference documentation
        └── *.md
```

Each skill is a self-contained package that includes its own changelog.

### SKILL.md Format

Each skill must have a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description shown to users
version: 1.0.0
allowed-tools: Bash(...), Read, Grep, etc.
---

# Skill Instructions

Agent instructions go here...
```

## Installation

### For Claude Code

```bash
cp -r skills/<skill-name> ~/.claude/skills/
```

### For Other AI Coding Agents

The SKILL.md format and structure can be adapted to your agent's configuration system. Check your
agent's documentation for how to add custom capabilities or context.

## Contributing

### Adding New Skills

When adding new skills:
1. Ensure no personally identifying information (PII) is present
2. Use placeholder domains (example.com) and credentials in examples
3. Include comprehensive reference documentation when possible
4. Test the skill locally before submitting
5. Set initial version to `1.0.0` in SKILL.md frontmatter
6. Create `skills/<skill-name>/CHANGELOG.md` with initial release entry
7. Update the repo's main README.md with the new skill description
8. Create a pull request with all changes

### Modifying Existing Skills

**CRITICAL**: Any change to a skill REQUIRES:

1. **Version Bump** in `skills/<skill-name>/SKILL.md` frontmatter:
   - Patch (1.0.0 → 1.0.1): Bug fixes, typo corrections, minor doc updates
   - Minor (1.0.0 → 1.1.0): New features, new reference docs, backwards-compatible changes
   - Major (1.0.0 → 2.0.0): Breaking changes, removed features, incompatible changes

2. **CHANGELOG.md Entry** in `skills/<skill-name>/CHANGELOG.md`:
   - Add new version section with date
   - Document what changed under appropriate categories (Added, Changed, Fixed, etc.)
   ```markdown
   ## [1.1.0] - 2024-02-10

   ### Added
   - Description of new features

   ### Changed
   - Description of changes
   ```

3. **Pull Request Workflow**:
   - **One commit per PR** - All changes must be in a single commit
   - Never commit skill changes directly to main
   - Create a feature branch with descriptive name
   - PR title should reference the skill and version (e.g., "grafana-loki v1.1.0: Add bloom filter support")
   - If changes are needed after initial commit, use `git commit --amend` and `git push --force`
   - When amending, update the commit message if the scope has changed

**Important**: Avoid obvious/mechanical entries in commit messages, changelogs, and PR descriptions:
- ❌ Don't include: "Bumped skill version", "Updated changelog", "Updated version number"
- ✅ Do include: Meaningful changes that users care about (new features, bug fixes, improvements)

**Example workflow for updating a skill:**
```bash
# 1. Create branch
git checkout -b update-grafana-loki-bloom-filters

# 2. Edit skill files
vim skills/grafana-loki/SKILL.md           # Update version: 1.0.0 -> 1.1.0
vim skills/grafana-loki/CHANGELOG.md       # Add version entry

# 3. Commit and create PR (single commit)
git add skills/grafana-loki/
git commit -m "grafana-loki v1.1.0: Add bloom filter documentation"
git push -u origin update-grafana-loki-bloom-filters
gh pr create

# 4. If changes needed after review, amend the commit
vim skills/grafana-loki/references/bloom-filters.md
git add skills/grafana-loki/
git commit --amend  # Update message if scope changed
git push --force
```

## License

All skills in this repository are licensed under Apache License 2.0 (see LICENSE file).
