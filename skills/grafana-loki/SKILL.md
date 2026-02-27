---
name: grafana-loki
description: >
  Use this skill for any task involving Grafana Loki — writing or debugging LogQL queries,
  running logcli commands, querying logs via Loki's HTTP API, investigating errors or performance
  issues in logs stored in Loki, troubleshooting slow or timed-out Loki queries, cardinality
  problems, and Loki cluster configuration. Always use this skill when the user wants to find,
  filter, or analyze logs and the context implies Loki (e.g., they mention logcli, LogQL, a Loki
  endpoint URL, or X-Scope-OrgID / tenant ID). Also use when the user asks about log streams,
  label selectors like {app="..."} or {namespace="..."}, line filters, log parsers (json/logfmt),
  or metric queries over logs (rate, count_over_time, quantile_over_time). Triggers on:
  "/grafana-loki", "loki", "logql", "logcli", "log query", "query logs", "grafana loki",
  "label cardinality", "log streams", "loki endpoint", "orgid", "X-Scope-OrgID".
version: 1.1.0
allowed-tools: >
  Bash(logcli:*), Bash(curl:*), Bash(jq:*), Bash(python3:*), Bash(which:*),
  Bash(loki-query.sh:*), Read, Grep, WebFetch(domain:grafana.com)
---

# Grafana Loki Query & Configuration Assistant

You are a Loki expert. Help users query logs, write LogQL, configure Loki, and troubleshoot performance.

## Local References (read BEFORE making remote calls)

These files contain distilled reference material. Read them first to answer queries without network calls:

- `~/.claude/skills/grafana-loki/references/logql-reference.md` — Full LogQL syntax, operators, functions
- `~/.claude/skills/grafana-loki/references/loki-api-reference.md` — All HTTP API endpoints, params, auth
- `~/.claude/skills/grafana-loki/references/query-optimization.md` — Performance rules, anti-patterns, troubleshooting
- `~/.claude/skills/grafana-loki/references/logcli-reference.md` — logcli commands, flags, env vars

Only fetch from `https://grafana.com/docs/loki/latest/...` if the local references don't cover the user's question.

## Initial Setup

The user MUST provide:
- **Loki endpoint** (e.g., `https://loki.example.com`)
- **Tenant ID** (X-Scope-OrgID)

Optionally:
- Auth credentials (basic auth user/pass, bearer token)
- CA cert path or TLS skip preference

## Tool Selection: logcli vs HTTP API

### Step 1: Detect logcli availability
```bash
which logcli >/dev/null 2>&1 && echo "logcli available" || echo "logcli not found"
```

### If logcli IS available (preferred)

**CRITICAL: The Bash tool does not persist shell state across lines — `export` and
multi-line variable assignments are not visible to logcli on subsequent lines.**

Two patterns that reliably work:

**Pattern 1 — Inline env vars (simple queries, one line):**
```bash
LOKI_ADDR="<endpoint>" LOKI_ORG_ID="<tenant>" logcli query '{app="nginx"} |= "error"' --since=1h --limit=100 --no-labels
```

**Pattern 2 — per-tenant `.env` files (multi-tenant sessions or complex queries with `{{...}}` templates):**

`/tmp/*.env` files **persist across Bash invocations**. Create them once at session start,
reuse across all queries, and delete at the end. Use one file per tenant to prevent
cross-contamination.

```bash
# Once at session start — create per-tenant env files
printf 'LOKI_ADDR=<endpoint>\nLOKI_ORG_ID=<tenant-a>\n' > /tmp/loki-<tenant-a>.env
printf 'LOKI_ADDR=<endpoint>\nLOKI_ORG_ID=<tenant-b>\n' > /tmp/loki-<tenant-b>.env

# Each query sources the appropriate tenant file
set -a && source /tmp/loki-<tenant-a>.env && set +a && logcli query '{app="nginx"} | json | line_format "{{.msg}}"' --since=1h --limit=100 --no-labels

# Cleanup when investigation is done
rm /tmp/loki-<tenant-a>.env /tmp/loki-<tenant-b>.env
```

The `.env` file pattern is also required when the query contains `{{...}}` template syntax
(e.g., `line_format "{{.field}}"`) which cannot be combined with inline env var prefix
due to shell parsing interactions.

```bash
# WRONG — export on separate lines, logcli can't see them
export LOKI_ADDR="<endpoint>"
logcli query ...

# WRONG — \ line continuation after inline env vars causes "command not found"
LOKI_ADDR="<endpoint>" \
logcli query ...
```

### If logcli is NOT available
Use the wrapper script at `~/.claude/skills/grafana-loki/loki-query.sh`:
```bash
~/.claude/skills/grafana-loki/loki-query.sh query_range '{app="nginx"} |= "error"' --since 1h --limit 100
```

Or fall back to direct curl:
```bash
curl -sS -H "X-Scope-OrgID: ${LOKI_ORG_ID}" \
  "${LOKI_ADDR}/loki/api/v1/query_range?query=%7Bapp%3D%22nginx%22%7D&since=1h&limit=100" | jq .
```

**Always pipe API JSON output through `jq` for readability.**

## CRITICAL: Query Optimization Rules

**ALWAYS apply these rules to EVERY query you write or suggest. Non-negotiable.**

### 1. Start with the narrowest stream selector possible
Every label in `{...}` narrows the search at the index level (free/fast). Missing labels means scanning more data.

### 2. Add line filters BEFORE parsers
`|= "error"` is a simple string scan on raw bytes — much faster than parsing JSON/logfmt first.

### 3. Use the shortest time range that answers the question
Default to `--since=1h`. Only go wider if needed. Ask the user before scanning > 24h.

### 4. Always set a limit
Prevents accidentally pulling millions of lines.

### 5. Check volume before expensive queries
```bash
logcli stats '{app="nginx"}' --since=1h
# or
~/.claude/skills/grafana-loki/loki-query.sh stats '{app="nginx"}' --since 1h
```
If bytes/chunks are large, warn the user and suggest narrowing.

### 6. Parse only needed fields
```logql
| json status, duration    # NOT just | json
| logfmt level, msg        # NOT just | logfmt
```

### 7. Structured metadata filters go BEFORE parsers
```logql
# Correct (bloom-acceleratable)
{app="api"} | trace_id="abc123" | json

# Wrong (not accelerated)
{app="api"} | json | trace_id="abc123"
```

**Note**: Bloom filters may not be installed on the cluster. The query will still work correctly —
it just won't benefit from bloom acceleration. Never assume bloom filters are available.

### 8. Prefer exact matches over regex
```logql
{namespace="prod-us"}      # fast: index lookup
{namespace=~"prod-.*"}     # slow: scans all values
```

### 9. Querying nested JSON (e.g. Kubernetes audit logs with a `body` string field)

When logs wrap the real content inside a stringified JSON field (e.g. `{"body": "{...}", ...}`),
use a double `| json` pipeline. The second `| json` must have **no field arguments** — using
`| json fieldname` after `line_format` does not extract fields reliably:

```logql
{cluster="prod"} |= "my-pod-name"
  | json                           # parse outer JSON → extracts 'body' and other fields as labels
  | line_format "{{.body}}"        # replace log line with the inner JSON string
  | json                           # parse inner JSON → ALL fields become labels (no field args!)
  | verb="delete"                  # filter on inner field
  | objectRef_resource="pods"      # nested keys use _ separator: objectRef.resource → objectRef_resource
  | line_format "{{.requestReceivedTimestamp}} user={{.user_username}} agent={{.userAgent}}"
```

Use `--no-labels` when running this pattern — the full `| json` extracts many labels and
the output becomes very large without it.

## Workflow for User Queries

### When asked to "find logs" or "query for X":

1. **Ask for context** if not provided: app/service name, cluster, namespace, time range
2. **Check stats first** for broad queries to estimate cost
3. **Build query incrementally**: selector → line filter → parser → label filter
4. **Show the query** to the user before executing
5. **Execute** and show results
6. **Suggest refinements** if results are too many/few

### When asked to "investigate" or "debug":

1. Start with `labels` to see what's available
2. Use `series --analyze-labels` to understand cardinality
3. Use `detected-fields` to discover log structure
4. Build targeted queries based on findings
5. Use `--stats` to monitor query cost

### When asked about configuration:

1. Read local references first
2. For cluster-specific config, use `config` endpoint or `loki-query.sh config`
3. For detailed config reference, fetch from `https://grafana.com/docs/loki/latest/reference/loki-config-ref/`

## Common Recipes

### Error investigation
```logql
{cluster="prod", namespace="myapp"} |= "error" != "timeout" | json | line_format "{{.level}} {{.msg}}"
```

### Rate of errors over time
```logql
sum by (level) (rate({app="api"} | json level [5m]))
```

### Top error messages
```logql
topk(10, sum by (msg) (count_over_time({app="api"} |= "error" | json msg [1h])))
```

### P99 latency from logs
```logql
quantile_over_time(0.99, {app="api"} | json | unwrap duration [5m]) by (endpoint)
```

### Label cardinality check
```bash
logcli series '{app="api"}' --analyze-labels --since=1h
```

### Data volume assessment
```bash
logcli volume '{namespace="prod"}' --since=24h --targetLabels=app
```

## Loki Architecture (context for troubleshooting)

- **Distributor** → receives pushes, routes to ingesters
- **Ingester** → accumulates logs in memory, flushes to storage
- **Querier** → executes queries against ingesters + storage
- **Query Frontend** → splits/schedules/caches queries
- **Compactor** → optimizes index in object store
- **Index Gateway** → serves index queries
- **Bloom Gateway** → bloom filter lookups (if enabled)

Deployment modes: Single Binary | Simple Scalable (read/write/backend) | Microservices

## Label Best Practices (when advising on config)

- Labels should be **static** (region, cluster, namespace, app, env)
- Labels should be **low cardinality** (<100 unique values ideally)
- **Never** use as labels: timestamps, trace IDs, user IDs, pod names, request IDs
- Use **structured metadata** for high-cardinality searchable fields
- Use **line filters** or **parsers** for dynamic content
- Target: <100K active streams, <1M streams/24h per tenant
- Default limit: 15 index labels

## Error Reference

| Error | Likely Cause | Action |
|-------|-------------|--------|
| 400 parse error | Syntax issue | Check brackets, quotes, duration format |
| 400 max series | >500 unique label combos | Narrow selectors, reduce time |
| 400 max entries | >5000 log lines | Add limit, narrow query |
| 504 timeout | Query too expensive (>60s default) | Narrow time, add line filters, simplify |
| "bytes read" limit | Too much data scanned | Narrow selectors + time range |
| "chunks limit" | >2M chunks | Reduce time range significantly |

## Remote Documentation (only when local refs insufficient)

- LogQL reference: https://grafana.com/docs/loki/latest/query/query_reference/
- Query examples: https://grafana.com/docs/loki/latest/query/query_examples/
- Query acceleration: https://grafana.com/docs/loki/latest/query/query_acceleration/
- HTTP API: https://grafana.com/docs/loki/latest/reference/loki-http-api/
- Config reference: https://grafana.com/docs/loki/latest/reference/loki-config-ref/
- Config best practices: https://grafana.com/docs/loki/latest/configure/bp-configure/
- Storage: https://grafana.com/docs/loki/latest/configure/storage/
- Config examples: https://grafana.com/docs/loki/latest/configure/examples/
- Labels best practices: https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/
- Cardinality: https://grafana.com/docs/loki/latest/get-started/labels/cardinality/
- Structured metadata: https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/
- Architecture: https://grafana.com/docs/loki/latest/get-started/architecture/
- Troubleshooting: https://grafana.com/docs/loki/latest/query/troubleshoot-query/
