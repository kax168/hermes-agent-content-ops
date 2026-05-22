#!/usr/bin/env python3
"""Run the Finish-Up-A-Thon completion audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content_ops.audit import audit_summary, run_audit


def main() -> int:
    root = ROOT
    results = run_audit(root)
    summary = audit_summary(results)
    report_lines = [
        "# Finish-Up-A-Thon Completion Audit",
        "",
        f"Status: **{summary['status']}**",
        f"Checks: **{summary['checks']}**",
        "",
        "## Results",
        "",
    ]
    for result in results:
        mark = "PASS" if result.ok else "FAIL"
        report_lines.append(f"- {mark}: {result.name} - {result.detail}")

    out = root / "finish-audit-report.md"
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"report={out.relative_to(root)}")
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
