#!/usr/bin/env python3
"""Scan a local content package and decide whether Hermes should wake."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content_ops.watch_layer import decide_wake, scan_content_package, write_watch_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the sample Content Ops watch layer")
    parser.add_argument("package", type=Path, help="Content package directory to scan")
    parser.add_argument("--out", type=Path, default=Path("watch-report.json"))
    args = parser.parse_args()

    decision = decide_wake(scan_content_package(args.package))
    write_watch_report(decision, args.out)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

