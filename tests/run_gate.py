from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_REPORT_DIR = REPO_ROOT / "state" / "test_reports"
GATE_SUMMARY_PATH = STATE_REPORT_DIR / "gate_summary.json"
GATE_SUMMARY_MD_PATH = STATE_REPORT_DIR / "gate_summary.md"


def run_cmd(name: str, cmd: list[str], env: dict[str, str] | None = None) -> dict:
    started = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env or os.environ.copy(),
    )
    ended = time.time()
    return {
        "name": name,
        "command": cmd,
        "returncode": proc.returncode,
        "pass": proc.returncode == 0,
        "duration_sec": round(ended - started, 3),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "timestamp": ended,
    }


def get_git_commit() -> str | None:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def main() -> None:
    STATE_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    py_compile = run_cmd(
        "py_compile",
        [
            sys.executable,
            "-m",
            "py_compile",
            "tools/main.py",
            "tools/app.py",
            "tools/project_config.py",
            "core/schema_utils.py",
            "tests/fakes/fake_app.py",
            "tests/run_smoke_suite.py",
            "tests/integration_real_app_smoke.py",
            "tests/smoke_happy_path.py",
            "tests/smoke_major_defect_replan.py",
            "tests/smoke_resume_after_merged.py",
            "tests/smoke_send_back_to_dev_repair.py",
            "tests/smoke_critical_discussion_block.py",
            "tests/smoke_cycle_limit_block.py",
            "tests/test_app_contract.py",
        ],
    )

    smoke_suite = run_cmd(
        "smoke_suite",
        [sys.executable, "tests/run_smoke_suite.py"],
    )

    if os.environ.get("RUN_REAL_APP_SERVER") == "1":
        integration = run_cmd(
            "integration_real_app",
            [sys.executable, "tests/integration_real_app_smoke.py"],
            env={**os.environ, "RUN_REAL_APP_SERVER": "1"},
        )
        integration_status = "passed" if integration["pass"] else "failed"
    else:
        integration = {
            "name": "integration_real_app",
            "command": [sys.executable, "tests/integration_real_app_smoke.py"],
            "returncode": 0,
            "pass": True,
            "duration_sec": 0.0,
            "stdout": "SKIPPED: set RUN_REAL_APP_SERVER=1 to run real app-server smoke\n",
            "stderr": "",
            "timestamp": time.time(),
        }
        integration_status = "skipped"

    gate_passed = py_compile["pass"] and smoke_suite["pass"] and integration_status in {"skipped", "passed"}
    summary_text = (
        f"py_compile: {'PASS' if py_compile['pass'] else 'FAIL'}\n"
        f"smoke_suite: {'PASS' if smoke_suite['pass'] else 'FAIL'}\n"
        f"integration_real_app: {integration_status.upper()}\n"
        f"overall: {'PASS' if gate_passed else 'FAIL'}"
    )

    summary = {
        "gate": "experiment_line_gate",
        "generated_at": time.time(),
        "cwd": str(REPO_ROOT),
        "python_version": sys.version,
        "platform": platform.platform(),
        "git_commit": get_git_commit(),
        "run_real_app_server": os.environ.get("RUN_REAL_APP_SERVER") == "1",
        "py_compile_passed": py_compile["pass"],
        "smoke_suite_passed": smoke_suite["pass"],
        "integration_real_app_status": integration_status,
        "all_passed": gate_passed,
        "summary_text": summary_text,
        "steps": {
            "py_compile": py_compile,
            "smoke_suite": smoke_suite,
            "integration_real_app": integration,
        },
    }
    GATE_SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    GATE_SUMMARY_MD_PATH.write_text(
        "\n".join(
            [
                "# Gate Summary",
                "",
                f"- generated_at: {summary['generated_at']}",
                f"- git_commit: {summary['git_commit']}",
                f"- py_compile: {'PASS' if py_compile['pass'] else 'FAIL'}",
                f"- smoke_suite: {'PASS' if smoke_suite['pass'] else 'FAIL'}",
                f"- integration_real_app: {integration_status.upper()}",
                f"- overall: {'PASS' if gate_passed else 'FAIL'}",
                f"- json_report: {GATE_SUMMARY_PATH}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"{'py_compile':<24} {'PASS' if py_compile['pass'] else 'FAIL'}")
    print(f"{'smoke_suite':<24} {'PASS' if smoke_suite['pass'] else 'FAIL'}")
    print(f"{'integration_real_app':<24} {integration_status.upper()}")

    for step in [py_compile, smoke_suite, integration]:
        if not step["pass"]:
            stderr_lines = [line for line in step["stderr"].splitlines() if line.strip()]
            tail = "\n".join(stderr_lines[-5:]) if stderr_lines else "(no stderr)"
            print("")
            print(f"[FAILURE] step={step['name']} returncode={step['returncode']}")
            print(tail)
            print(f"report_json={GATE_SUMMARY_PATH}")
            print(f"report_md={GATE_SUMMARY_MD_PATH}")

    sys.exit(0 if gate_passed else 1)


if __name__ == "__main__":
    main()
