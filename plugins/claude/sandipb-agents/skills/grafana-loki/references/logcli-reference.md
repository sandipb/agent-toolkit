# LogCLI Quick Reference

## Environment Variables

```bash
export LOKI_ADDR="http://localhost:3100"   # Loki endpoint
export LOKI_ORG_ID="my-tenant"             # Tenant ID (X-Scope-OrgID)
export LOKI_USERNAME="user"                # Basic auth user
export LOKI_PASSWORD="pass"                # Basic auth password
export LOKI_BEARER_TOKEN="token"           # Bearer token
export LOKI_BEARER_TOKEN_FILE="/path"      # Bearer token file
export LOKI_CA_CERT_PATH="/path"           # CA cert
export LOKI_TLS_SKIP_VERIFY="true"         # Skip TLS verify
export LOKI_CLIENT_CERT_PATH="/path"       # Client cert
export LOKI_CLIENT_KEY_PATH="/path"        # Client key
```

## Commands

### query - Fetch log entries
```bash
logcli query [flags] <logql-query>
```
Key flags:
- `--since=1h` / `--from` + `--to` (RFC3339) - time range
- `--limit=30` - max entries
- `--output=default|raw|jsonl` - output format
- `--forward` - chronological order
- `--tail` / `--follow` - live stream
- `--timezone=Local|UTC`
- `--stats` - show query statistics
- `-q, --quiet` - suppress metadata
- `--no-labels` - hide labels
- `--include-label=name` / `--exclude-label=name`
- `--colored-output` - colorize labels
- `--parallel-duration=12h` - split into parallel jobs
- `--parallel-max-workers=4` - worker count
- `--part-path-prefix=./parts/p` - save parts to files
- `--merge-parts` / `--keep-parts` - manage part files

### instant-query - Point-in-time metric query
```bash
logcli instant-query [flags] <logql-query>
```
- `--now` - evaluation timestamp
- `--limit=30`

### labels - List available labels
```bash
logcli labels [label_name]
```
- `--since=1h` / `--from` + `--to`

### series - List matching streams
```bash
logcli series [flags] <matcher>
```
- `--analyze-labels` - cardinality analysis
- `--since=1h`

### stats - Index statistics
```bash
logcli stats [flags] <query>
```
Returns: streams, chunks, entries, bytes

### volume - Data volume
```bash
logcli volume [flags] <query>
logcli volume_range [flags] <query>   # with --step
```
- `--targetLabels=label1,label2`

### detected-fields - Discover log fields
```bash
logcli detected-fields [flags] <query>
```
- `--field-limit=100` - max fields
- `--line-limit=1000` - lines to scan

### fmt - Format a query
```bash
logcli fmt '<query>'
```

### delete - Manage log deletions
```bash
logcli delete [create|list|cancel] [flags]
```

## Global Flags

```
--addr URL              Loki server address
--org-id ID             Tenant ID
--username USER         Basic auth user
--password PASS         Basic auth password
--bearer-token TOKEN    Bearer token
--ca-cert PATH          CA certificate
--tls-skip-verify       Skip TLS verification
--compress              Request compressed responses
--retries N             Retry count (default 0)
--query-tags TAGS       X-Query-Tags header
--nocache               Add Cache-Control: no-cache
```

## Installation

Binary: Download from https://github.com/grafana/loki/releases
Homebrew: `brew install logcli`
From source:
```bash
git clone https://github.com/grafana/loki.git && cd loki
make logcli && cp cmd/logcli/logcli /usr/local/bin/
```

## Stdin Mode (query saved logs)
```bash
cat logs.jsonl | logcli --stdin query '{app="nginx"} | json | status >= 400'
```
