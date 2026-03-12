#!/usr/bin/env python3

from pathlib import Path
import runpy
import sys


def main() -> int:
    target = Path(__file__).with_name("run_a9.py")
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
