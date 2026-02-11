#!/usr/bin/env bash
# loki-query.sh - Wrapper for Loki HTTP API calls
# Avoids generating curl commands every time; handles auth, tenant, and common endpoints.
#
# Usage:
#   loki-query.sh <command> [options]
#
# Environment variables (required):
#   LOKI_ADDR     - Loki endpoint URL (e.g. https://loki.example.com)
#   LOKI_ORG_ID   - Tenant ID (X-Scope-OrgID header)
#
# Optional environment variables:
#   LOKI_USERNAME      - Basic auth username
#   LOKI_PASSWORD      - Basic auth password
#   LOKI_BEARER_TOKEN  - Bearer token
#   LOKI_CA_CERT       - CA cert path for TLS
#   LOKI_TLS_SKIP      - Set to "true" to skip TLS verification
#
# Commands:
#   query_range  <logql> [--limit N] [--since DURATION] [--start T] [--end T] [--step S] [--direction forward|backward]
#   query        <logql> [--limit N] [--time T] [--direction forward|backward]
#   labels       [--since DURATION] [--start T] [--end T] [--query SELECTOR]
#   label_values <label_name> [--since DURATION] [--start T] [--end T] [--query SELECTOR]
#   series       <match> [--since DURATION] [--start T] [--end T]
#   stats        <logql> [--start T] [--end T]
#   volume       <logql> [--since DURATION] [--start T] [--end T] [--limit N] [--targetLabels L]
#   volume_range <logql> [--since DURATION] [--start T] [--end T] [--step S] [--targetLabels L]
#   detected_fields <logql> [--since DURATION] [--start T] [--end T] [--field_limit N] [--line_limit N]
#   push         <json_body>
#   ready        - Check if Loki is ready
#   config       [--mode diffs|defaults]
#   buildinfo    - Show build info
#   format       <logql> - Format a LogQL query
#   tail         <logql> [--limit N] [--delay_for N] [--start T]
#   raw          <method> <path> [extra_curl_args...] - Raw API call

set -euo pipefail

# --- Configuration ---
: "${LOKI_ADDR:?Error: LOKI_ADDR environment variable is required}"

# Build auth and TLS flags
CURL_AUTH_FLAGS=()
if [[ -n "${LOKI_USERNAME:-}" && -n "${LOKI_PASSWORD:-}" ]]; then
    CURL_AUTH_FLAGS+=(-u "${LOKI_USERNAME}:${LOKI_PASSWORD}")
elif [[ -n "${LOKI_BEARER_TOKEN:-}" ]]; then
    CURL_AUTH_FLAGS+=(-H "Authorization: Bearer ${LOKI_BEARER_TOKEN}")
fi

CURL_TLS_FLAGS=()
if [[ "${LOKI_TLS_SKIP:-}" == "true" ]]; then
    CURL_TLS_FLAGS+=(-k)
fi
if [[ -n "${LOKI_CA_CERT:-}" ]]; then
    CURL_TLS_FLAGS+=(--cacert "${LOKI_CA_CERT}")
fi

CURL_TENANT_FLAGS=()
if [[ -n "${LOKI_ORG_ID:-}" ]]; then
    CURL_TENANT_FLAGS+=(-H "X-Scope-OrgID: ${LOKI_ORG_ID}")
fi

# Base curl command
_curl() {
    curl -sS --fail-with-body \
        "${CURL_AUTH_FLAGS[@]}" \
        "${CURL_TLS_FLAGS[@]}" \
        "${CURL_TENANT_FLAGS[@]}" \
        "$@"
}

# URL-encode a string
_urlencode() {
    python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"
}

# Parse common flags from remaining args
_parse_time_flags() {
    local -n _params=$1
    shift
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --since)    _params+=("since=$2"); shift 2 ;;
            --start)    _params+=("start=$2"); shift 2 ;;
            --end)      _params+=("end=$2"); shift 2 ;;
            --limit)    _params+=("limit=$2"); shift 2 ;;
            --step)     _params+=("step=$2"); shift 2 ;;
            --direction) _params+=("direction=$2"); shift 2 ;;
            --time)     _params+=("time=$2"); shift 2 ;;
            --query)    _params+=("query=$(_urlencode "$2")"); shift 2 ;;
            --targetLabels) _params+=("targetLabels=$2"); shift 2 ;;
            --aggregateBy) _params+=("aggregateBy=$2"); shift 2 ;;
            --field_limit) _params+=("field_limit=$2"); shift 2 ;;
            --line_limit) _params+=("line_limit=$2"); shift 2 ;;
            --delay_for) _params+=("delay_for=$2"); shift 2 ;;
            --mode)     _params+=("mode=$2"); shift 2 ;;
            *) echo "Unknown flag: $1" >&2; return 1 ;;
        esac
    done
}

# Build query string from params array
_build_qs() {
    local IFS='&'
    echo "$*"
}

# --- Commands ---

cmd_query_range() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/query_range?${qs}"
}

cmd_query() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/query?${qs}"
}

cmd_labels() {
    local params=()
    _parse_time_flags params "$@"
    local qs=""
    if [[ ${#params[@]} -gt 0 ]]; then
        qs="?$(_build_qs "${params[@]}")"
    fi
    _curl "${LOKI_ADDR}/loki/api/v1/labels${qs}"
}

cmd_label_values() {
    local label="$1"; shift
    local params=()
    _parse_time_flags params "$@"
    local qs=""
    if [[ ${#params[@]} -gt 0 ]]; then
        qs="?$(_build_qs "${params[@]}")"
    fi
    _curl "${LOKI_ADDR}/loki/api/v1/label/${label}/values${qs}"
}

cmd_series() {
    local match="$1"; shift
    local params=("match[]=$(_urlencode "$match")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/series?${qs}"
}

cmd_stats() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/index/stats?${qs}"
}

cmd_volume() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/index/volume?${qs}"
}

cmd_volume_range() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/index/volume_range?${qs}"
}

cmd_detected_fields() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    _curl "${LOKI_ADDR}/loki/api/v1/detected_fields?${qs}"
}

cmd_push() {
    local body="$1"
    _curl -X POST \
        -H "Content-Type: application/json" \
        "${LOKI_ADDR}/loki/api/v1/push" \
        -d "$body"
}

cmd_ready() {
    _curl "${LOKI_ADDR}/ready"
}

cmd_config() {
    local params=()
    _parse_time_flags params "$@"
    local qs=""
    if [[ ${#params[@]} -gt 0 ]]; then
        qs="?$(_build_qs "${params[@]}")"
    fi
    _curl "${LOKI_ADDR}/config${qs}"
}

cmd_buildinfo() {
    _curl "${LOKI_ADDR}/loki/api/v1/status/buildinfo"
}

cmd_format() {
    local logql="$1"
    _curl -G --data-urlencode "query=${logql}" "${LOKI_ADDR}/loki/api/v1/format_query"
}

cmd_tail() {
    local logql="$1"; shift
    local params=("query=$(_urlencode "$logql")")
    _parse_time_flags params "$@"
    local qs; qs=$(_build_qs "${params[@]}")
    # Note: tail is WebSocket; curl can do basic connection but wscat/websocat is better
    echo "Note: /tail is a WebSocket endpoint. Use logcli --tail or wscat for streaming." >&2
    echo "Attempting HTTP GET (will show initial data but won't stream):" >&2
    _curl "${LOKI_ADDR}/loki/api/v1/tail?${qs}"
}

cmd_raw() {
    local method="$1"; shift
    local path="$1"; shift
    _curl -X "$method" "${LOKI_ADDR}${path}" "$@"
}

# --- Usage ---
usage() {
    cat <<'USAGE'
Usage: loki-query.sh <command> [options]

Commands:
  query_range      <logql> [flags]    Range query (logs + metrics)
  query            <logql> [flags]    Instant query (metrics)
  labels           [flags]            List labels
  label_values     <name> [flags]     Label values
  series           <match> [flags]    List series
  stats            <logql> [flags]    Index stats
  volume           <logql> [flags]    Volume info
  volume_range     <logql> [flags]    Volume over time
  detected_fields  <logql> [flags]    Discover fields
  push             <json_body>        Push logs
  ready                               Readiness check
  config           [--mode M]         Show config
  buildinfo                           Build info
  format           <logql>            Format query
  tail             <logql> [flags]    Tail logs (WebSocket note)
  raw              <METHOD> <path>    Raw API call

Common flags: --since, --start, --end, --limit, --step, --direction, --query

Environment: LOKI_ADDR (required), LOKI_ORG_ID, LOKI_USERNAME, LOKI_PASSWORD,
             LOKI_BEARER_TOKEN, LOKI_CA_CERT, LOKI_TLS_SKIP

Examples:
  export LOKI_ADDR=https://loki.example.com LOKI_ORG_ID=my-tenant

  # List labels
  loki-query.sh labels --since 1h

  # Query logs
  loki-query.sh query_range '{app="nginx"} |= "error"' --since 1h --limit 100

  # Check data volume before querying
  loki-query.sh stats '{app="nginx"}' --since 1h

  # Instant metric
  loki-query.sh query 'sum(rate({app="nginx"}[5m])) by (status)'

  # Raw API call
  loki-query.sh raw GET /loki/api/v1/rules
USAGE
}

# --- Main ---
if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

COMMAND="$1"; shift

case "$COMMAND" in
    query_range)      cmd_query_range "$@" ;;
    query)            cmd_query "$@" ;;
    labels)           cmd_labels "$@" ;;
    label_values)     cmd_label_values "$@" ;;
    series)           cmd_series "$@" ;;
    stats)            cmd_stats "$@" ;;
    volume)           cmd_volume "$@" ;;
    volume_range)     cmd_volume_range "$@" ;;
    detected_fields)  cmd_detected_fields "$@" ;;
    push)             cmd_push "$@" ;;
    ready)            cmd_ready ;;
    config)           cmd_config "$@" ;;
    buildinfo)        cmd_buildinfo ;;
    format)           cmd_format "$@" ;;
    tail)             cmd_tail "$@" ;;
    raw)              cmd_raw "$@" ;;
    -h|--help|help)   usage ;;
    *)                echo "Unknown command: $COMMAND" >&2; usage; exit 1 ;;
esac
