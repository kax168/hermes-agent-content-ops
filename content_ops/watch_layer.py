"""Event-aware watch layer for the public Hermes Content Ops sample.

The private workflow still uses cron for the 07:00 and 18:00 publishing rhythm.
This module models the missing layer suggested by community feedback: wake the
agent when an important local state change appears, while keeping publishing
draft-first and auditable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable


WATCHED_FILES = [
    "topic_research.md",
    "article.md",
    "article.html",
    "article.json",
    "human_review.approved",
    "wechat_api.failed",
]


@dataclass(frozen=True)
class WatchEvent:
    kind: str
    path: str
    reason: str
    severity: str = "info"


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def scan_content_package(root: Path) -> list[WatchEvent]:
    """Scan a content package directory for wake-worthy local events."""
    events: list[WatchEvent] = []

    if not root.exists():
        return [
            WatchEvent(
                kind="missing_package",
                path=str(root),
                reason="content package directory does not exist",
                severity="warning",
            )
        ]

    for name in WATCHED_FILES:
        path = root / name
        if path.exists():
            events.append(classify_file_event(path, root))

    return events


def classify_file_event(path: Path, root: Path) -> WatchEvent:
    relative = _relative(path, root)
    if path.name == "wechat_api.failed":
        return WatchEvent(
            kind="retry_needed",
            path=relative,
            reason="WeChat draft upload failed; agent should repair or retry safely",
            severity="error",
        )
    if path.name == "human_review.approved":
        return WatchEvent(
            kind="human_review_ready",
            path=relative,
            reason="human review approved a queued item; agent may continue packaging",
        )
    if path.name == "topic_research.md":
        return WatchEvent(
            kind="source_changed",
            path=relative,
            reason="topic research changed; agent should re-evaluate freshness and angle",
        )
    if path.name in {"article.md", "article.html", "article.json"}:
        return WatchEvent(
            kind="draft_changed",
            path=relative,
            reason="draft artifact changed; agent should validate package consistency",
        )
    return WatchEvent(kind="file_changed", path=relative, reason="watched file changed")


def decide_wake(events: Iterable[WatchEvent]) -> dict[str, object]:
    event_list = list(events)
    should_wake = any(event.kind in {"retry_needed", "human_review_ready", "source_changed"} for event in event_list)
    next_action = "wake_agent" if should_wake else "keep_sleeping"
    if any(event.kind == "retry_needed" for event in event_list):
        next_action = "wake_agent_for_safe_retry"
    return {
        "wakeAgent": should_wake,
        "nextAction": next_action,
        "events": [event.__dict__ for event in event_list],
    }


def write_watch_report(decision: dict[str, object], out: Path) -> None:
    report = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        **decision,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

