#!/usr/bin/env bash
# Commit + push the site repo, surviving the data.js conflicts that the other
# machine causes (data.js is one long JSON line, so git cannot merge it).
# Rule: on conflict take upstream, then replay our imports with the idempotent
# resync script, then continue the rebase.
#   bash scripts/sync_push.sh "commit message"
set -u
MSG=${1:-"content: 上線卷一內容"}
ROOT=/c/Users/Administrator/dsehub
cd "$ROOT" || exit 1
export PYTHONPATH=
PY=python
LOG=$ROOT/.sync_push.log
: > "$LOG"

git add -A >> "$LOG" 2>&1
git commit -q -m "$MSG" >> "$LOG" 2>&1

if git pull --rebase -q origin main >> "$LOG" 2>&1; then
  git push -q origin main >> "$LOG" 2>&1 && echo "PUSHED (clean)"
  exit 0
fi

echo "conflict — resolving" >> "$LOG"
for f in $(git diff --name-only --diff-filter=U); do
  git checkout --ours "$f" 2>/dev/null || git checkout --theirs "$f"
  git add "$f"
done
[ -f docs/data.js ] && $PY scripts/resync_from_bank.py --write >> "$LOG" 2>&1
git add -A >> "$LOG" 2>&1
git -c core.editor=true rebase --continue >> "$LOG" 2>&1
git push -q origin main >> "$LOG" 2>&1 && echo "PUSHED (resolved via resync)"
git log --oneline -1
