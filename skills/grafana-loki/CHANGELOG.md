# Changelog - grafana-loki

All notable changes to the grafana-loki skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-03-02

### Changed
- Local reference file paths and wrapper script path changed from Claude-specific absolute paths
  (`~/.claude/skills/grafana-loki/...`) to skill-relative paths (`./references/...`, `./loki-query.sh`),
  making the skill portable across different AI coding agents
- Added portability note clarifying that local file paths are relative to the directory containing `SKILL.md`

## [1.1.0] - 2026-02-25

### Added
- Section 9: Querying nested JSON — double `| json` pipeline pattern for logs with a
  stringified inner JSON field (e.g. Kubernetes audit logs with a `body` field)
- Critical note that the Bash tool does not persist shell state across invocations, with two
  reliable logcli env var patterns: inline prefix for simple queries, and per-tenant
  `/tmp/*.env` files for multi-tenant sessions or queries with `{{...}}` template syntax

### Changed
- Expanded skill description with additional trigger keywords (`query logs`, `label streams`,
  `loki endpoint`, `orgid`, `X-Scope-OrgID`, etc.) for broader activation coverage

## [1.0.0] - 2024-02-10

### Added
- Initial release of grafana-loki skill
- LogQL query support via logcli, HTTP API, or wrapper script
- Complete LogQL syntax reference
- Loki HTTP API documentation
- Query optimization guide with best practices
- logcli command reference
- Bash wrapper script (loki-query.sh) for API calls without logcli
- Support for basic auth, bearer token, and TLS configuration
- Query statistics and volume analysis commands
- Label cardinality analysis
- Detected fields discovery
