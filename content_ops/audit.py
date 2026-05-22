"""Finish-up audit helpers for the public Hermes Content Ops package."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


REQUIRED_FILES = [
    "README.md",
    "dev-post.md",
    "submission-checklist.md",
    "scripts/wechat_pipeline_sample.py",
    "scripts/xhs_review_queue_sample.py",
    "assets/hero.png",
    "assets/architecture.png",
]

FINISHED_FILES = [
    "BEFORE_AFTER.md",
    "FINISH_UP_A_THON.md",
    ".github/workflows/ci.yml",
    ".github/copilot-instructions.md",
    "tests/test_audit.py",
]


@dataclass(frozen=True)
class AuditResult:
    name: str
    ok: bool
    detail: str


def check_required_files(root: Path) -> list[AuditResult]:
    results: list[AuditResult] = []
    for relative in REQUIRED_FILES + FINISHED_FILES:
        path = root / relative
        results.append(
            AuditResult(
                name=f"file:{relative}",
                ok=path.exists(),
                detail="present" if path.exists() else "missing",
            )
        )
    return results


def check_secret_hygiene(root: Path) -> list[AuditResult]:
    risky_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"access[_-]?token\s*[:=]\s*['\"]?[A-Za-z0-9._-]{20,}", re.IGNORECASE),
        re.compile(r"app[_-]?secret\s*[:=]\s*['\"]?[A-Za-z0-9._-]{20,}", re.IGNORECASE),
        re.compile(r"wx[a-f0-9]{12,}", re.IGNORECASE),
    ]
    public_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".py", ".yml", ".yaml", ".json", ".txt", ".example"}
    ]
    findings: list[str] = []
    for path in public_files:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if path.name == ".env.example":
            continue
        for pattern in risky_patterns:
            if pattern.search(text):
                findings.append(f"{path.relative_to(root)} matches {pattern.pattern}")
    return [
        AuditResult(
            name="secret_hygiene",
            ok=not findings,
            detail="no obvious credential tokens found" if not findings else "; ".join(findings),
        )
    ]


def check_docs_quality(root: Path) -> list[AuditResult]:
    before_after = root / "BEFORE_AFTER.md"
    finish = root / "FINISH_UP_A_THON.md"
    checks = [
        (
            "before_after_mentions_before",
            before_after.exists() and "Before" in before_after.read_text(encoding="utf-8"),
            "before/after narrative is documented",
        ),
        (
            "finish_notes_mentions_copilot",
            finish.exists() and "Copilot" in finish.read_text(encoding="utf-8"),
            "Copilot workflow notes are documented",
        ),
    ]
    return [AuditResult(name=name, ok=ok, detail=detail if ok else "missing evidence") for name, ok, detail in checks]


def run_audit(root: Path) -> list[AuditResult]:
    return [
        *check_required_files(root),
        *check_secret_hygiene(root),
        *check_docs_quality(root),
    ]


def audit_summary(results: list[AuditResult]) -> dict[str, object]:
    failed = [result for result in results if not result.ok]
    return {
        "status": "pass" if not failed else "fail",
        "checks": len(results),
        "failed": [result.name for result in failed],
    }
