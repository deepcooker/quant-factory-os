#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path


def build_log_header(run_id: str, a9_root: str, cmd: list[str]) -> str:
    lines = [
        "a9 dry-run",
        f"run_id: {run_id}",
        f"cwd: {os.getcwd()}",
        f"python: {sys.executable}",
        f"a9_root: {a9_root}",
        f"command: {' '.join(cmd)}",
        "",
    ]
    return "\n".join(lines)


def write_log(run_id: str, content: str) -> Path:
    reports_dir = Path("reports") / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    log_path = reports_dir / "a9_stdout.log"
    log_path.write_text(content, encoding="utf-8")
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a9quant dry-run check.")
    parser.add_argument("--run-id", default=os.getenv("RUN_ID", "run-unknown"))
    parser.add_argument("--a9-root", default="/root/a9quant-strategy")
    args = parser.parse_args()

    a9_root = args.a9_root
    if not os.path.isdir(a9_root):
        msg = f"ERROR: a9 root not found or not a directory: {a9_root}"
        log = build_log_header(args.run_id, a9_root, [])
        log += msg + "\n"
        write_log(args.run_id, log)
        print(msg, file=sys.stderr)
        return 1

    code = (
        "import os,sys\n"
        "root=sys.argv[1]\n"
        "print('a9-root', root)\n"
        "print('exists', os.path.isdir(root))\n"
        "print('entries', len(os.listdir(root)))\n"
    )
    cmd = [sys.executable, "-c", code, a9_root]
    header = build_log_header(args.run_id, a9_root, cmd)

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    log = header
    log += "stdout:\n" + proc.stdout
    log += "stderr:\n" + proc.stderr
    log += f"exit_code: {proc.returncode}\n"
    write_log(args.run_id, log)

    if proc.returncode != 0:
        print("ERROR: a9 dry-run failed. See reports/{}/a9_stdout.log".format(args.run_id), file=sys.stderr)
        return proc.returncode

    print("OK: a9 dry-run complete. See reports/{}/a9_stdout.log".format(args.run_id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
