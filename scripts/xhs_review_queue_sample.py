#!/usr/bin/env python3
"""Sanitized sample of the Xiaohongshu pet-supplies review queue."""

from __future__ import annotations

import json
import urllib.parse
from datetime import datetime
from pathlib import Path


BASE = Path.home() / ".hermes" / "xhs-pet-supplies-videos"
QUERIES = [
    "宠物用品 带货",
    "宠物好物 带货",
    "猫咪用品 好物",
    "狗狗用品 好物",
    "pet supplies",
]
CRITERIA = [
    "Pet-supplies product or affiliate-style video.",
    "No Chinese narration.",
    "No Chinese on-screen text, or at most 10 Chinese characters.",
    "Do not download or repost videos; save public links only.",
]


def search_url(query: str) -> str:
    return "https://www.xiaohongshu.com/search_result?" + urllib.parse.urlencode({"keyword": query})


def main() -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {today} Xiaohongshu pet-supplies review queue",
        "",
        "## Criteria",
        *[f"- {item}" for item in CRITERIA],
        "",
        "## Search URLs",
        *[f"- {query}: {search_url(query)}" for query in QUERIES],
    ]
    review_file = out_dir / "review_queue.txt"
    review_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": "review_queue_ready", "review_file": str(review_file)}, ensure_ascii=False))
    print(json.dumps({"wakeAgent": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

