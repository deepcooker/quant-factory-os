from __future__ import annotations

import sys


def main() -> None:
    print("INTENTIONAL_FAILURE_SAMPLE_START")
    raise AssertionError("intentional failure sample for gate readability")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"INTENTIONAL_FAILURE_SAMPLE_ERROR: {exc}", file=sys.stderr)
        raise
