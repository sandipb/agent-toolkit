#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cat >"$TMP_DIR/curl" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" >>"${CURL_LOG:?}"
EOF
chmod +x "$TMP_DIR/curl"

export PATH="$TMP_DIR:$PATH"
export CURL_LOG="$TMP_DIR/curl.log"
export LOKI_ADDR="https://loki.example.com"

fail() { echo "FAIL: $*" >&2; exit 1; }

: >"$CURL_LOG"
"$SKILL_DIR/loki-query.sh" query_range '{app="api"}' --since 1h --limit 10
grep -q 'query_range?' "$CURL_LOG" || fail "query_range did not call curl"
grep -q 'since=1h' "$CURL_LOG" || fail "query_range omitted since"

: >"$CURL_LOG"
if "$SKILL_DIR/loki-query.sh" stats '{app="api"}' --since 1h 2>/dev/null; then
    fail "stats accepted unsupported --since"
fi
[[ ! -s "$CURL_LOG" ]] || fail "invalid stats request reached curl"

if "$SKILL_DIR/loki-query.sh" query_range 2>/dev/null; then
    fail "query_range accepted a missing query"
fi

: >"$CURL_LOG"
if "$SKILL_DIR/loki-query.sh" tail '{app="api"}' 2>/dev/null; then
    fail "tail unexpectedly succeeded"
fi
[[ ! -s "$CURL_LOG" ]] || fail "tail reached plain HTTP curl"

: >"$CURL_LOG"
if "$SKILL_DIR/loki-query.sh" push '{"streams":[]}' 2>/dev/null; then
    fail "push bypassed write guard"
fi
[[ ! -s "$CURL_LOG" ]] || fail "guarded push reached curl"

LOKI_ALLOW_WRITE=true "$SKILL_DIR/loki-query.sh" push '{"streams":[]}'
grep -q -- '-X' "$CURL_LOG" || fail "approved push did not call curl"

echo "ok"
