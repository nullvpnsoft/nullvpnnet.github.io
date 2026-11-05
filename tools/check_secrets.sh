#!/usr/bin/env bash
# =============================================================================
# check_secrets.sh — credential-leak gate for this repository
#
# Scans files for credential-looking content and credential-shaped filenames.
# Exit codes: 0 = clean, 1 = findings, 2 = usage error.
#
# Usage:
#   tools/check_secrets.sh [path ...]   # default: all tracked/staged files
#
# Waivers:
#   .secretsallow — one POSIX-extended regex per line, matched against the
#   file path. Keep waivers narrow (path-scoped) and review them regularly.
#
# Notes:
#   - The scanner excludes itself and .githooks/ to avoid self-matches.
#   - Findings are printed REDACTED on purpose so logs never re-leak a value.
# =============================================================================
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 2
SELF="tools/check_secrets.sh"
ALLOW="$ROOT/.secretsallow"
FAIL=0
SCANNED=0

# ---------- file collection ----------
declare -a FILES=()
if [ "$#" -gt 0 ]; then
  FILES=("$@")
elif git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  mapfile -t FILES < <(git ls-files)
else
  mapfile -t FILES < <(find . -type f -not -path './.git/*' -not -path './node_modules/*')
fi

# ---------- waivers ----------
declare -a WAIVERS=()
if [ -f "$ALLOW" ]; then
  while IFS= read -r line; do
    line="${line%%#*}"
    [ -z "${line//[[:space:]]/}" ] && continue
    WAIVERS+=("$(printf '%s' "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')")
  done < "$ALLOW"
fi

waived() {
  local f="$1" w
  for w in ${WAIVERS[@]+"${WAIVERS[@]}"}; do
    printf '%s\n' "$f" | grep -Eq -- "$w" && return 0
  done
  return 1
}

# ---------- patterns ----------
# High-signal credential formats (case-sensitive).
HIGH='(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|cfat_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk_live_[A-Za-z0-9]{10,}|rk_live_[A-Za-z0-9]{10,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|_authToken[[:space:]]*[=:])'

# Generic assignment secrets (case-insensitive): password="...", api_key: '...'
Q='["'"'"']'
GENERIC='(api[_-]?key|api[_-]?secret|client[_-]?secret|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd)'${Q}'?[[:space:]]*[:=][[:space:]]*'${Q}'[^'${Q}']{8,}'

# Credential-shaped FILENAMES
NAME_RE='(^|/)\.env($|\.)|\.pem$|\.key$|(^|/)id_rsa|(^|/)id_ed25519|\.p12$|\.pfx$|\.kdbx$|(^|/)credentials[^/]*\.json$|\.session$|(^|/)\.secrets(/|$)'

redact() { # file:line:content → file:line:[redacted]
  sed -E 's/^([^:]+:[0-9]+:).{0,40}.*/\1[redacted]/'
}

report() { # label, grep-output
  printf '  ✖ [%s] %s\n' "$1" "$(printf '%s\n' "$2" | redact | head -n 20)"
  FAIL=1
}

scan_file() {
  local f="$1" out
  [ "$f" = "$SELF" ] && return 0
  case "$f" in .githooks/*) return 0 ;; esac
  waived "$f" && return 0
  [ -f "$f" ] || return 0
  # Skip binary files (grep -I)
  if ! LC_ALL=C grep -qI . "$f" 2>/dev/null; then return 0; fi
  SCANNED=$((SCANNED + 1))
  out=$(grep -nE "$HIGH" -- "$f" 2>/dev/null) && report HIGH "$out"
  out=$(grep -inE "$GENERIC" -- "$f" 2>/dev/null) && report generic "$out"
  return 0
}

echo "== secrets scan: ${#FILES[@]} candidate file(s) =="

for f in ${FILES[@]+"${FILES[@]}"}; do
  if printf '%s\n' "$f" | grep -Eqi "$NAME_RE"; then
    if waived "$f"; then continue; fi
    echo "  ✖ [filename] $f looks like a key/env file — do not commit it"
    FAIL=1
    continue
  fi
  scan_file "$f"
done

if [ "$FAIL" -eq 1 ]; then
  echo "✖ check_secrets: FAILED — remove the secret(s) or add a narrow .secretsallow waiver"
  exit 1
fi
echo "✅ check_secrets: clean — $SCANNED file(s) content-scanned"
exit 0
