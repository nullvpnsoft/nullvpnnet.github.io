#!/usr/bin/env bash
# =============================================================================
# deploy_historyless.sh — publish the current working tree to origin/main as a
# SINGLE parentless commit ("orphan snapshot"). The remote repository's git
# history stays at depth 1 FOREVER — GitHub has no native "disable history"
# setting, so this script force-replaces main on every deploy.
#
# Flow:
#   1. git add -A                      (stage everything, incl. new files)
#   2. secrets gate                    (mandatory — cannot be skipped)
#   3. content gates (i18n / links)    (skippable with --skip-gates)
#   4. git write-tree + commit-tree    (parentless commit, no checkout dance)
#   5. git push --force  → origin/main (history reset to depth 1)
#   6. local main re-pointed at the deployed commit
#
# Options:
#   --message "..."   custom commit message (default: "Deploy <UTC> — content <tree>")
#   --skip-gates      skip i18n/link gates (secrets scan CANNOT be skipped)
#
# Requires: GitHub credential at ~/.secrets/gh_token (override with
#           GH_TOKEN_FILE=... ), pushed via an ephemeral GIT_ASKPASS helper —
#           the token is never stored in .git/config or process argv.
#
# Old development history (if any) remains ONLY in this local .git object
# store; the remote never receives it. Run `git gc --prune=now --aggressive`
# locally if you want to shred it on this machine too.
# =============================================================================
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

MSG_ARG=""
SKIP_GATES=0
while [ $# -gt 0 ]; do
  case "$1" in
    --message) MSG_ARG="$2"; shift 2 ;;
    --skip-gates) SKIP_GATES=1; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

echo "[0/5] stamping sitemap lastmod"
# r106: keep <lastmod> truthful automatically — it was hand-edited and could
# go stale between content deploys. Stamp today's date (site timezone, UTC+8)
# on every deploy, BEFORE staging so the stamped file lands in the snapshot.
# Non-fatal by design: a stamping failure must never block a deploy.
TODAY="$(TZ=Asia/Shanghai date +%F 2>/dev/null)"
[ -n "$TODAY" ] || TODAY="$(date +%F)"
if [ -f sitemap.xml ]; then
  sed -i.bak "s|<lastmod>[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]</lastmod>|<lastmod>${TODAY}</lastmod>|g" sitemap.xml \
    && rm -f sitemap.xml.bak || true
  echo "  lastmod -> ${TODAY}"
fi

echo "[1/5] staging working tree"
git add -A

echo "[2/5] secrets gate (mandatory)"
bash tools/check_secrets.sh

if [ "$SKIP_GATES" -eq 0 ] && command -v node >/dev/null 2>&1; then
  echo "[2/5] content gates"
  node tools/check_html_i18n.js >/dev/null && echo "  i18n gate OK"
  node tools/check_links.js >/dev/null && echo "  links gate OK"
else
  echo "[2/5] content gates skipped"
fi

echo "[3/5] building parentless snapshot commit"
TREE=$(git write-tree)
MSG="${MSG_ARG:-Deploy $(date -u '+%Y-%m-%d %H:%M UTC') — content $(git rev-parse --short=12 "$TREE")}"
COMMIT=$(git commit-tree "$TREE" -m "$MSG")
echo "  snapshot commit: $COMMIT"

echo "[4/5] force-pushing → origin/main (history reset to depth 1)"
export GH_TOKEN_FILE="${GH_TOKEN_FILE:-/home/z/.secrets/gh_token}"
export GIT_ASKPASS="${GIT_ASKPASS:-/tmp/nullvpn-askpass.sh}"
if [ ! -x "$GIT_ASKPASS" ]; then
  cat > "$GIT_ASKPASS" <<'EOS'
#!/bin/sh
case "$1" in
  Username*) echo nullvpnnet ;;
  Password*) cat "${GH_TOKEN_FILE:-/home/z/.secrets/gh_token}" ;;
esac
EOS
  chmod +x "$GIT_ASKPASS"
fi
export GIT_TERMINAL_PROMPT=0
git push --force origin "$COMMIT:refs/heads/main"

echo "[5/5] re-pointing local main at deployed commit"
git update-ref refs/heads/main "$COMMIT"
git reset --hard >/dev/null 2>&1
git fetch origin main --quiet 2>/dev/null || true
DEPTH=$(git rev-list --count origin/main 2>/dev/null || echo 1)
echo "✅ deployed — remote history depth: $DEPTH"
