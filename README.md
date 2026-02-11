# AI Coding Agent Skills Directory

A public collection of reusable skills for AI coding agents (Claude Code, OpenCode, GitHub
Copilot, Cursor, etc.).

**Note**: Skills were originally created for [Claude Code](https://github.com/anthropics/claude-code)
but follow a generic format that can be adapted for other AI coding assistants.

## What are Skills?

Skills are specialized capability packages that enhance AI coding agents with domain-specific
knowledge and tools. Each skill includes:
- Trigger conditions (keywords, commands)
- Allowed tools and permissions
- Expert instructions and reference material
- Helper scripts and utilities

## Available Skills

### grafana-loki

Query and analyze logs using Grafana Loki.

**Capabilities:**
- Write and execute LogQL queries
- Query via `logcli`, HTTP API, or helper script
- Optimize queries for performance
- Analyze label cardinality and data volume
- Investigate errors and patterns in logs

**Triggers:** `/grafana-loki`, "loki", "logql", "logcli", "log query"

**Installation (Claude Code):**
```bash
cp -r skills/grafana-loki ~/.claude/skills/
```

**Includes:**
- Complete LogQL syntax reference
- Loki HTTP API documentation
- Query optimization guide
- logcli command reference
- Bash wrapper script for API calls

## Installing Skills

### For Claude Code

1. Clone this repository:
   ```bash
   git clone https://github.com/sandipb/skills-directory.git
   ```

2. Copy desired skills to your Claude skills directory:
   ```bash
   cp -r skills-directory/skills/<skill-name> ~/.claude/skills/
   ```

3. Restart Claude Code or start a new session to load the skill.

### For Other AI Coding Agents

The SKILL.md format and structure can be adapted to your agent's configuration system. Check your
agent's documentation for how to add custom capabilities or context.

## Verifying Installation (Claude Code)

In Claude Code, skills appear in the system reminder at the start of conversations:
```
The following skills are available for use with the Skill tool:
- <skill-name>: <description>
```

## Contributing

Contributions welcome! When adding new skills:
- Ensure no personally identifying information (PII)
- Use placeholder domains and credentials in examples
- Include comprehensive reference documentation
- Test locally before submitting
- Update this README with the new skill

See [AGENTS.md](AGENTS.md) for detailed contributor guidelines.

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.
