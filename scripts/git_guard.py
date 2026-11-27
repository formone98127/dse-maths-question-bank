#!/usr/bin/env python3
"""Git sync guard — 阻止「本地一路 commit，遠端一路有人 push」嘅分叉。

用法：
  python scripts/git_guard.py --check-commit   # pre-commit：落後遠端就拒絕 commit
  python scripts/git_guard.py --check-push     # pre-push：落後遠端就拒絕 push
  python scripts/git_guard.py --status         # 人手查：ahead / behind

設計理由（2026-11-27 事故）：
  本機有兩個同一 repo 嘅 clone，加上長時間冇 fetch，結果本地累積 6 個 commit、
  遠端同時有 14 個 commit，2952 個生成頁兩邊各寫一次，一合併就 2094 個衝突。
  唯一可靠嘅防法係：每次 commit / push 之前都 fetch，落後就即刻停手處理。
"""

from __future__ import annotations

import subprocess
import sys


def run(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, check=False).stdout.strip()


def ahead_behind() -> tuple[int, int]:
    """Return (ahead, behind) relative to the upstream branch."""
    upstream = run("git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if not upstream:
        return (0, 0)  # 冇 upstream 就跟唔到，交由 branch 保護處理
    out = run("git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}")
    if not out:
        return (0, 0)
    left, right = out.split()
    return int(left), int(right)


def fetch() -> bool:
    res = subprocess.run(["git", "fetch", "--quiet", "origin"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[git-guard] fetch 失敗，無法確認遠端狀態：\n{res.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "--status"

    if not fetch():
        # 離線時唔阻死工作，但要講清楚
        print("[git-guard] 警告：離線／fetch 失敗，未能核對遠端，請手動確認。", file=sys.stderr)
        return 0 if mode == "--status" else 0

    ahead, behind = ahead_behind()

    if mode == "--status":
        print(f"ahead={ahead} behind={behind}")
        return 0

    if mode in ("--check-commit", "--check-push") and behind > 0:
        action = "commit" if mode == "--check-commit" else "push"
        print(
            f"\n[git-guard] 拒絕 {action}：本地落後 origin 共 {behind} 個 commit。\n"
            f"  先執行：git pull --rebase origin main   （或 git merge origin/main）\n"
            f"  處理好衝突（生成頁一律重跑生成器，唔好逐行手改）才再 {action}。\n",
            file=sys.stderr,
        )
        return 1

    if mode == "--check-commit" and ahead >= 5:
        print(f"[git-guard] 提示：本地已累積 {ahead} 個未 push commit，請盡快 push。", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
