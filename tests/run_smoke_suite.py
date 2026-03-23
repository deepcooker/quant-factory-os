from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_REPORT_DIR = REPO_ROOT / "state" / "test_reports"
SUMMARY_PATH = STATE_REPORT_DIR / "smoke_summary.json"

CASES = [
    ("smoke_happy_path", "tests/smoke_happy_path.py"),
    ("smoke_major_defect_replan", "tests/smoke_major_defect_replan.py"),
    ("smoke_resume_after_merged", "tests/smoke_resume_after_merged.py"),
    ("smoke_send_back_to_dev_repair", "tests/smoke_send_back_to_dev_repair.py"),
    ("smoke_critical_discussion_block", "tests/smoke_critical_discussion_block.py"),
    ("smoke_cycle_limit_block", "tests/smoke_cycle_limit_block.py"),
    ("test_app_contract", "tests/test_app_contract.py"),
]


def run_case(name: str, script: str) -> dict:
    started = time.time()
    proc = subprocess.run(
        [sys.executable, script],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    ended = time.time()
    return {
        "name": name,
        "script": script,
        "pass": proc.returncode == 0,
        "returncode": proc.returncode,
        "duration_sec": round(ended - started, 3),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "error": proc.stderr.strip() if proc.returncode != 0 else "",
        "timestamp": ended,
    }


def main() -> None:
    STATE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = [run_case(name, script) for name, script in CASES]
    summary = {
        "suite": "smoke_suite",
        "generated_at": time.time(),
        "all_passed": all(item["pass"] for item in results),
        "results": results,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    for item in results:
        label = "PASS" if item["pass"] else "FAIL"
        print(f"{item['name']:<34} {label}")

    sys.exit(0 if summary["all_passed"] else 1)


if __name__ == "__main__":
    main()
