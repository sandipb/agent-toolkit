# Loki Query Optimization Guide

## Golden Rules (ALWAYS follow)

### 1. Narrow Stream Selectors First
```logql
# BAD - scans everything
{job=~".+"} |= "error"

# GOOD - targets specific streams
{cluster="prod", namespace="myapp", job="api-server"} |= "error"
```

### 2. Use Line Filters Before Parsers
Line filters (`|=`, `!=`, `|~`, `!~`) operate on raw text BEFORE parsing. They are extremely fast
because they skip the parsing stage entirely for non-matching lines.

```logql
# BAD - parses ALL lines then filters
{app="nginx"} | json | status >= 400

# GOOD - filters raw text first, then parses only matching lines
{app="nginx"} |= "err" | json | status >= 400

# BEST - multiple line filters progressively narrow
{app="nginx"} |= "err" != "timeout" | json | status >= 400
```

### 3. Minimize Time Range
- Start with `--since=15m` or `--since=1h`, increase only if needed
- Use `--from` / `--to` for precise ranges
- Avoid scanning days/weeks unless absolutely necessary

### 4. Use Limits
- Always set `--limit` (logcli) or `limit` param (API)
- Default is only 30/100, but be explicit
- For investigation, start with `--limit=50` and increase

### 5. Prefer Exact Label Matches Over Regex
```logql
# SLOW - regex requires scanning all label values
{namespace=~"prod-.*"}

# FAST - exact match, direct index lookup
{namespace="prod-us"}
```

### 6. Extract Only Needed Fields
```logql
# SLOW - parses entire JSON object
{app="api"} | json

# FAST - parses only specific fields
{app="api"} | json status, duration, method
```

## Structured Metadata Optimization

If the cluster supports structured metadata, filter on it BEFORE parsers:

```logql
# Accelerated (bloom filters can help)
{app="api"} | trace_id="abc123" | json

# NOT accelerated (filter after parser)
{app="api"} | json | trace_id="abc123"
```

## Bloom Filter Acceleration

Bloom filters accelerate queries when:
1. The cluster has bloom filters enabled (not always the case)
2. Structured metadata is configured
3. Filters use exact string equality: `| key="value"`
4. Filters appear BEFORE parser expressions
5. Simplified regex is used: `| key=~"value1|value2"` (converted to OR)

**Check if available**: Query works either way, but without bloom filters the filter just runs at normal speed.

## Query Anti-Patterns

### Avoid high-cardinality label selectors
```logql
# BAD - pod names are high cardinality
{pod=~"api-.*"}

# GOOD - use the deployment/job label instead
{job="api"} |= "pod-specific-string"
```

### Avoid regex when exact match works
```logql
# BAD
{app=~"nginx"}

# GOOD
{app="nginx"}
```

### Avoid unbounded aggregations
```logql
# BAD - aggregates across ALL labels
sum(rate({app="nginx"}[5m]))

# GOOD - aggregate by specific dimension
sum by (status) (rate({app="nginx"}[5m]))
```

### Avoid very small step intervals on large ranges
```logql
# BAD - 10s steps over 7 days = 60,480 data points
rate({app="nginx"}[5m])  # with step=10s, range=7d

# GOOD - match step to range
rate({app="nginx"}[5m])  # with step=1m for 1d, step=5m for 7d
```

## Troubleshooting Slow Queries

### Common Errors & Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| 504 Gateway Timeout | Query too expensive | Narrow time range, add line filters, more specific selectors |
| "max series" exceeded | Too many unique label combos (500 default) | Add selectors, reduce time, aggregate |
| "max entries" exceeded | Too many log lines (default 5000) | Add `limit`, narrow selectors/time |
| "bytes read" limit | Scanning too much data | Narrow selectors, reduce time, add line filters early |
| "chunks limit" exceeded | >2M chunks scanned | Narrow time range and selectors |

### Diagnosis

1. Use `--stats` flag (logcli) to see bytes processed, chunks scanned
2. Use `logcli stats '{your_selector}'` to estimate query volume
3. Use `logcli volume '{your_selector}' --since=1h` to check data volume
4. Use `logcli series '{your_selector}' --analyze-labels` to find cardinality issues

### Step-by-Step Query Building

1. Start with narrow stream selector + short time range
2. Add the most selective line filter first
3. Test incrementally - add one pipeline stage at a time
4. Only add parsers when you need label extraction
5. Use `--stats` to verify each addition doesn't explode the cost

## Resource-Efficient Patterns

### Counting errors without fetching lines
```logql
count_over_time({app="api"} |= "error" [1h])
```

### Getting just label cardinality info
```bash
logcli series '{app="api"}' --analyze-labels --since=1h
```

### Checking data volume before querying
```bash
logcli stats '{app="api"}' --since=1h
logcli volume '{app="api"}' --since=1h
```

### Parallel queries for large ranges
```bash
logcli query --parallel-duration=1h --parallel-max-workers=4 --since=24h '{app="api"} |= "error"'
```
