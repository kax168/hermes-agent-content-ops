#!/usr/bin/env python3
"""Sanitized sample of the Hermes-scheduled WeChat draft pipeline.

This file is intentionally safe to publish. It shows the architecture without
including real account IDs, access tokens, draft IDs, or private prompts.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


OUT_BASE = Path.home() / ".hermes" / "wechat-mp"


def collect_topics(slot: str) -> list[dict[str, str]]:
    """In production this queries Google News, HN, product updates, etc."""
    return [
        {
            "source": "Google News",
            "title": "Example AI agent tool trend",
            "url": "https://example.com/ai-agent-trend",
            "fit": slot,
        },
        {
            "source": "Hacker News",
            "title": "Example discussion about AI workflows",
            "url": "https://news.ycombinator.com/",
            "fit": slot,
        },
    ]


def render_wechat_html(title: str, digest: str) -> str:
    """Render WeChat-safe HTML with inline styles only."""
    return f"""
<section style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;line-height:1.8;color:#172033;">
  <section style="padding:22px 20px;border-radius:22px;background:linear-gradient(135deg,#071a2f,#0f766e);color:#fff;">
    <p style="margin:0 0 8px;font-size:13px;color:#9ff7e5;">AI / Global Growth / Content Ops</p>
    <h1 style="margin:0;font-size:24px;line-height:1.35;">{title}</h1>
  </section>
  <section style="padding:16px 18px;border-radius:18px;background:#f0fdfa;border:1px solid #99f6e4;margin:16px 0;">
    <strong>Takeaway:</strong><br>{digest}
  </section>
  <h2 style="font-size:20px;color:#0f172a;">1. Why this matters today</h2>
  <p>Hermes selected this topic from current sources before generating the article.</p>
  <h2 style="font-size:20px;color:#0f172a;">2. Practical workflow</h2>
  <p>The article package includes research, Markdown, HTML, JSON, image plan, and a local cover.</p>
  <section style="margin:22px 0;padding:16px;border-radius:18px;background:#0f172a;color:#e2e8f0;">
    <p style="margin:0 0 10px;color:#67e8f9;font-weight:700;">Action Card</p>
    <p>• Validate source freshness</p>
    <p>• Create WeChat-safe HTML</p>
    <p>• Upload as draft, not auto-publish by default</p>
  </section>
</section>
""".strip()


def build_article(slot: str) -> dict[str, str]:
    topics = collect_topics(slot)
    title = "How Hermes Turns AI Trend Research Into a WeChat Draft"
    digest = "A small but real content operations workflow powered by scheduled agent work."
    return {
        "title": title,
        "digest": digest,
        "content": render_wechat_html(title, digest),
        "topics": json.dumps(topics, ensure_ascii=False),
    }


def main() -> int:
    slot = "morning"
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = OUT_BASE / today / slot
    out_dir.mkdir(parents=True, exist_ok=True)

    article = build_article(slot)
    (out_dir / "topic_research.md").write_text(article["topics"] + "\n", encoding="utf-8")
    (out_dir / "article.html").write_text(article["content"] + "\n", encoding="utf-8")
    (out_dir / "article.json").write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"status": "ready_for_wechat_draft", "out_dir": str(out_dir)}, ensure_ascii=False))
    print(json.dumps({"wakeAgent": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

