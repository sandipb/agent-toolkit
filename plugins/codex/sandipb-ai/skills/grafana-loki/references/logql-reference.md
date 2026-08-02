# LogQL Quick Reference

## Query Structure

```
{stream_selector} | line_filters | parser | label_filters | line_format | ...
```

## Stream Selectors (ALWAYS required, ALWAYS first)

```logql
{label="value"}           # exact match
{label!="value"}          # not equal
{label=~"regex"}          # regex match
{label!~"regex"}          # regex not match
```

Multiple selectors: `{app="nginx", env="prod", cluster="us-east"}`

**CRITICAL**: Always use the most specific stream selectors possible. Every label narrows the
search before any line processing occurs.

## Line Filters (applied BEFORE parsing - very fast)

```logql
|= "exact string"        # line contains
!= "exact string"        # line does not contain
|~ "regex"               # line matches regex
!~ "regex"               # line does not match regex
|> "<_> error <_>"       # pattern match (fast structured matching)
!> "<_> error <_>"       # pattern not match
```

**Order matters**: Place the most selective filter first. Each filter reduces data for the next stage.

## Parsers

```logql
| json                              # parse JSON logs
| json field1, field2               # parse only specific JSON fields (faster)
| logfmt                            # parse key=value logs
| logfmt field1, field2             # parse specific logfmt fields (faster)
| regexp "(?P<name>pattern)"        # extract with regex
| pattern "<_> <method> <path> <_>" # extract with pattern syntax
| unpack                            # unpack packed JSON labels
```

## Label Filters (applied AFTER parsing)

```logql
| status_code >= 400
| duration > 10s
| method = "GET"
| level =~ "error|warn"
| size > 1KB
| ip = ip("192.168.0.0/16")      # IP matching
```

**Supported units**: duration (ns, us, ms, s, m, h), bytes (b, kib, mib, gib, KB, MB, GB)

## Formatting

```logql
| line_format "{{.status}} {{.method}} {{.path}}"    # reformat line
| label_format dst="{{.src}}"                         # rename/transform label
| decolorize                                          # strip ANSI color codes
| drop label1, label2                                 # remove labels
| keep label1, label2                                 # keep only these labels
```

## Metric Queries

### Log range aggregations (produce metrics from logs)

```logql
rate({app="nginx"}[5m])                          # logs per second
count_over_time({app="nginx"}[5m])               # total count in range
bytes_over_time({app="nginx"}[5m])               # bytes in range
bytes_rate({app="nginx"}[5m])                     # bytes per second
absent_over_time({app="nginx"}[5m])               # 1 if no logs in range
```

### Unwrap range aggregations (produce metrics from extracted values)

```logql
rate({app="nginx"} | json | unwrap duration [5m])
sum_over_time({app="nginx"} | json | unwrap bytes_sent [5m])
avg_over_time({app="nginx"} | json | unwrap response_time [5m])
min_over_time(...)
max_over_time(...)
stdvar_over_time(...)
stddev_over_time(...)
first_over_time(...)
last_over_time(...)
quantile_over_time(0.99, {app="nginx"} | json | unwrap latency [5m])
```

### Vector aggregations (aggregate across series)

```logql
sum(rate({app="nginx"}[5m])) by (host)
avg(...) by (label)
min(...) by (label)
max(...) by (label)
count(...) by (label)
stddev(...) by (label)
stdvar(...) by (label)
bottomk(3, ...)
topk(10, ...)
sort(...)
sort_desc(...)
```

### Grouping

```logql
sum by (host) (rate({app="nginx"}[5m]))
sum without (instance) (rate({app="nginx"}[5m]))
```

## Binary Operations

```logql
# Arithmetic: + - * / % ^
# Comparison: == != > >= < <=  (add bool for 0/1 instead of filter)
# Logical: and or unless

# Example: error rate > 5%
sum(rate({app="nginx"} |= "error" [5m])) / sum(rate({app="nginx"}[5m])) > 0.05
```

## Useful Functions

```logql
label_replace(expr, "dst", "replacement", "src", "regex")
vector(scalar)           # convert scalar to vector
```

## Pipeline Errors

```logql
| __error__ = ""         # only successfully parsed lines
| __error__ != ""        # lines that failed parsing
| __error_details__ ...  # error detail
```

## Comments

```logql
# This is a comment (works in multi-line queries)
{app="nginx"} # inline comment
```

## Time Ranges & Step

LogQL uses Go duration format: `ns`, `us`, `ms`, `s`, `m`, `h`, `d`, `w`, `y`

## Structured Metadata

Structured metadata fields are automatically available as labels without parsing:

```logql
{app="nginx"} | trace_id="abc123"          # filter on structured metadata
{app="nginx"} | pod="myservice-abc-123"    # no parser needed
```

**IMPORTANT**: Structured metadata filters MUST appear BEFORE parser expressions for bloom filter acceleration to work.
