#!/usr/bin/env python3
import argparse, json, os, platform, subprocess, sys
from datetime import datetime

MAX_FILE_BYTES = 5 * 1024 * 1024  # 5MB

def sh(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8", errors="replace").strip()
        return out
    except Exception:
        return ""

def ensure_file(path: str, default: str) -> None:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(default)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    run_id = args.run_id
    base = os.path.join("reports", run_id)
    samples = os.path.join(base, "samples")
    os.makedirs(samples, exist_ok=True)

    meta_path = os.path.join(base, "meta.json")
    summary_path = os.path.join(base, "summary.md")
    decision_path = os.path.join(base, "decision.md")

    meta = {
        "run_id": run_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "git_commit": sh(["git", "rev-parse", "HEAD"]),
        "git_branch": sh(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "dirty": sh(["git", "status", "--porcelain"]) != "",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "limits": {
            "max_file_bytes": MAX_FILE_BYTES,
            "max_table_rows_default": 500,
        },
        "notes": "Evidence skeleton generated. Populate summary/decision as you work.",
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    ensure_file(summary_path, f"""# Summary ({run_id})

## Status
- Created evidence skeleton.

## Symptoms / Context
- TODO

## What changed
- TODO

## Verification
- Command: `make verify`
- Result: TODO

## Notes
- File size limit: 5MB
- Table row limit: 500 unless task overrides
""")

    ensure_file(decision_path, f"""# Decision Log ({run_id})

## Hypotheses
- TODO

## Experiments / Checks
- TODO

## Conclusion
- TODO

## Follow-ups
- TODO
""")

    print(f"[evidence] created/updated: {base}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())