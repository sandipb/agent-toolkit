---
name: grafana-loki
license: Apache-2.0
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
metadata:
  version: 1.2.0
---

# Grafana Loki Query & Configuration Assistant

You are a Loki expert. Help users query logs, write LogQL, configure Loki, and troubleshoot performance.

## Bundled resources

Read only the resource needed for the request. Resolve paths relative to this `SKILL.md`; never assume a home-directory
install location.

- `references/logql-reference.md` — LogQL syntax, operators, and functions
- `references/loki-api-reference.md` — HTTP API endpoints, parameters, and authentication
- `references/query-optimization.md` — Performance rules and troubleshooting
- `references/logcli-reference.md` — logcli commands, flags, and environment variables
- `loki-query.sh` — read-oriented HTTP API helper when logcli is unavailable

Only fetch from `https://grafana.com/docs/loki/latest/...` if the local references don't cover the user's question.

## Initial Setup

The user must provide the Loki endpoint. A tenant ID (`X-Scope-OrgID`) is required only when Loki multi-tenancy is
enabled or the provider requires it.

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

Omit `LOKI_ORG_ID` when the Loki deployment does not use multi-tenancy.

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
Use the bundled `loki-query.sh` resolved relative to this skill:
```bash
./loki-query.sh query_range '{app="nginx"} |= "error"' --since 1h --limit 100
```

Or fall back to direct curl:
```bash
curl -sS -H "X-Scope-OrgID: ${LOKI_ORG_ID}" \
  "${LOKI_ADDR}/loki/api/v1/query_range?query=%7Bapp%3D%22nginx%22%7D&since=1h&limit=100" | jq .
```

Omit the `X-Scope-OrgID` header when the Loki deployment does not use multi-tenancy.

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
# The HTTP index stats endpoint requires explicit start/end timestamps:
./loki-query.sh stats '{app="nginx"}' --start '<unix-ns>' --end '<unix-ns>'
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
4. **Execute read-only queries** when authorized by the request and show results
5. **Suggest refinements** if results are too many/few

### When asked to "investigate" or "debug":

1. Start with `labels` to see what's available
2. Use `series --analyze-labels` to understand cardinality
3. Use `detected-fields` to discover log structure
4. Build targeted queries based on findings
5. Use `--stats` to monitor query cost

### When asked about configuration:

1. Read the relevant bundled reference first
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

- Prefer stable, bounded labels (region, cluster, namespace, app, env)
- Use dynamic labels sparingly; favor long-lived values limited to tens of values
- Do not use unbounded or ephemeral values such as timestamps, trace IDs, user IDs, or request IDs as indexed labels
- Use **structured metadata** for high-cardinality searchable fields
- Use **line filters** or **parsers** for dynamic content
- Target: <100K active streams, <1M streams/24h per tenant

## Error Reference

| Error | Likely Cause | Action |
|-------|-------------|--------|
| 400 parse error | Syntax issue | Check brackets, quotes, duration format |
| 400 series/entries limit | Tenant query limit exceeded | Narrow selectors or time; inspect tenant limits |
| 504 timeout | Query exceeded configured timeout | Narrow time, add line filters, simplify |
| "bytes read" limit | Too much data scanned | Narrow selectors + time range |
| "chunks limit" | Tenant chunk limit exceeded | Reduce time range significantly |

## External-change safety

- Query, labels, series, stats, volume, readiness, build info, formatting, and configuration inspection are read-only.
- Pushing logs and arbitrary non-GET API calls change external state. Explain the exact request and obtain explicit user
  approval first.
- The bundled helper requires `LOKI_ALLOW_WRITE=true` for `push` and non-GET `raw` calls; this guard does not replace
  user approval.

## Current ingestion guidance

Prefer Grafana Alloy or an OpenTelemetry Collector for new pipelines. Promtail is feature-complete and in long-term
support. Loki accepts native OTLP logs at `/otlp/v1/logs`; collector configuration normally uses an endpoint ending in
`/otlp` because the exporter appends `/v1/logs`.

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
