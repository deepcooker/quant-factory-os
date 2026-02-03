#!/usr/bin/env python3
import argparse, json, os
from datetime import datetime

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--day", required=True)
    ap.add_argument("--symbols", required=True)  # comma-separated
    ap.add_argument("--start", required=True)    # HH:MM
    ap.add_argument("--end", required=True)      # HH:MM
    args = ap.parse_args()

    base = os.path.join("reports", args.run_id)
    os.makedirs(base, exist_ok=True)
    req_path = os.path.join(base, "market_slice_request.json")

    req = {
        "run_id": args.run_id,
        "requested_at": datetime.utcnow().isoformat() + "Z",
        "day": args.day,
        "symbols": [s.strip() for s in args.symbols.split(",") if s.strip()],
        "window": {"start": args.start, "end": args.end},
        "status": "stub",
        "next_step": "Implement data extraction from your market data source into reports/<run_id>/samples/market_slice_1m.csv.gz",
        "limits": {"max_rows": 500, "max_file_bytes": 5_000_000},
    }

    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(req, f, indent=2, ensure_ascii=False)

    print(f"[slice] wrote request: {req_path}")
    print("[slice] (stub) no actual data extracted yet.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())