# Loki HTTP API Reference

## Authentication

Multi-tenant header: `X-Scope-OrgID: <tenant-id>`
Multiple tenants: `X-Scope-OrgID: tenant1|tenant2`
Basic auth: `-u username:password`

## Core Query Endpoints

### Range Query (logs + metrics)
```
GET /loki/api/v1/query_range
```
| Param | Description | Default |
|-------|-------------|---------|
| `query` | LogQL query (required) | |
| `limit` | Max entries | 100 |
| `start` | Start time (epoch ns, float s, RFC3339) | 1h ago |
| `end` | End time | now |
| `since` | Lookback duration (e.g. `5m`, `1h`) | |
| `step` | Query resolution step (metric queries) | |
| `interval` | Return entries at given interval (log queries) | |
| `direction` | `forward` or `backward` | backward |

### Instant Query (metrics only)
```
GET /loki/api/v1/query
```
| Param | Description | Default |
|-------|-------------|---------|
| `query` | LogQL query (required) | |
| `limit` | Max entries | 100 |
| `time` | Evaluation time | now |
| `direction` | `forward` or `backward` | backward |

## Discovery Endpoints

### List Labels
```
GET /loki/api/v1/labels
```
Params: `start`, `end`, `since`, `query` (optional stream selector to scope)

### Label Values
```
GET /loki/api/v1/label/<name>/values
```
Params: `start`, `end`, `since`, `query` (optional stream selector to scope)

### Series
```
GET /loki/api/v1/series
POST /loki/api/v1/series  (Content-Type: application/x-www-form-urlencoded)
```
Params: `match[]` (repeatable), `start`, `end`, `since`

## Statistics & Volume

### Index Stats
```
GET /loki/api/v1/index/stats
```
Params: `query`, `start`, `end`
Returns: streams, chunks, entries, bytes counts (approximation)

### Volume
```
GET /loki/api/v1/index/volume
```
Params: `query`, `start`, `end`, `limit`, `targetLabels`, `aggregateBy`
Requires: `volume_enabled: true`

### Volume Range
```
GET /loki/api/v1/index/volume_range
```
Same as volume + `step` parameter

## Detected Fields
```
GET /loki/api/v1/detected_fields
```
Params: `query`, `start`, `end`, `field_limit` (default 100), `line_limit` (default 1000), `step`

## Patterns
```
GET /loki/api/v1/patterns
```
Params: `query`, `start`, `end`, `step`
Requires: `pattern_ingester.enabled: true`

## Tail (WebSocket)
```
GET /loki/api/v1/tail
```
Params: `query`, `delay_for` (0-5s), `limit`, `start`

## Management

### Push Logs
```
POST /loki/api/v1/push
```
Content-Type: `application/json` or `application/x-protobuf`
Optional: `Content-Encoding: gzip`

JSON body:
```json
{
  "streams": [{
    "stream": {"label": "value"},
    "values": [["<unix_ns>", "log line", {"metadata_key": "metadata_value"}]]
  }]
}
```

### Delete Logs
```
POST /loki/api/v1/delete
```
Params: `query`, `start`, `end`, `max_interval`
Returns: 204 on success

```
GET /loki/api/v1/delete       # list deletion requests
DELETE /loki/api/v1/delete    # cancel (params: request_id, force)
```

### Format Query
```
GET/POST /loki/api/v1/format_query
```
Param: `query`

## Status Endpoints

```
GET /ready                        # readiness probe (200 when ready)
GET /metrics                      # prometheus metrics
GET /config                       # current config (param: mode=diffs|defaults)
GET /services                     # running services
GET /loki/api/v1/status/buildinfo # version info
GET /log_level                    # current log level
POST /log_level                   # change log level (param: log_level)
```

## Ring Endpoints

```
GET /distributor/ring
GET /indexgateway/ring
GET /ruler/ring
GET /compactor/ring
```

## Ruler Endpoints (requires enable_api: true)

```
GET    /loki/api/v1/rules                          # all rules
GET    /loki/api/v1/rules/{namespace}               # namespace rules
GET    /loki/api/v1/rules/{namespace}/{group}       # specific group
POST   /loki/api/v1/rules/{namespace}               # create/update (YAML body)
DELETE /loki/api/v1/rules/{namespace}/{group}       # delete group
DELETE /loki/api/v1/rules/{namespace}               # delete namespace
GET    /prometheus/api/v1/rules                     # prometheus-compatible
GET    /prometheus/api/v1/alerts                    # prometheus-compatible
```

## Timestamp Formats (all endpoints)

- Unix nanoseconds (integer string): `"1700000000000000000"`
- Floating-point seconds: `"1700000000.123"`
- RFC3339: `"2024-01-15T10:30:00Z"`
- RFC3339Nano: `"2024-01-15T10:30:00.123456789Z"`

## Response Format

All query responses include a `data.stats` object with detailed execution metrics:
ingester/store breakdown, bytes processed, chunks scanned, etc.
