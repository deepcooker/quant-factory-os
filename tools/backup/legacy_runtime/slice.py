#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path


def _seed(s: str) -> int:
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--day", required=True)      # YYYY-MM-DD
    ap.add_argument("--symbols", required=True)  # A,B,C
    ap.add_argument("--start", required=True)    # HH:MM
    ap.add_argument("--end", required=True)      # HH:MM
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    out_dir = repo / "reports" / args.run_id / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)

    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    if not syms:
        raise SystemExit("symbols is empty")

    start_dt = datetime.fromisoformat(f"{args.day}T{args.start}:00")
    end_dt = datetime.fromisoformat(f"{args.day}T{args.end}:00")
    if end_dt < start_dt:
        raise SystemExit("end < start")

    # hard limit: <=500 rows (AGENTS)
    max_rows = 500
    per_sym = max(1, max_rows // len(syms))
    total_seconds = int((end_dt - start_dt).total_seconds())
    step = max(1, total_seconds // max(1, per_sym - 1))

    rng = random.Random(_seed(f"{args.run_id}|{args.day}|{args.symbols}|{args.start}|{args.end}"))

    fname = f"slice_{args.day}_{args.start.replace(':','')}-{args.end.replace(':','')}_{len(syms)}sym.csv.gz"
    out_path = out_dir / fname

    rows = 0
    with gzip.open(out_path, "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ts", "symbol", "price", "qty"])
        for sym in syms:
            price = rng.uniform(100, 30000)
            t = start_dt
            n = 0
            while t <= end_dt and n < per_sym:
                price = max(0.01, price * (1.0 + rng.uniform(-0.0008, 0.0008)))
                qty = rng.uniform(0.001, 1.0)
                w.writerow([t.isoformat(), sym, f"{price:.4f}", f"{qty:.6f}"])
                rows += 1
                n += 1
                t = t + timedelta(seconds=step)

    print(f"OK: wrote {out_path} rows={rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
