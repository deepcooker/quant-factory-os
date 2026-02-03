SHELL := /bin/bash
PY := python3
RUN_ID ?= run-unknown

.PHONY: help doctor evidence slice verify ship clean_reports

help:
	@echo "Targets:"
	@echo "  make doctor"
	@echo "  make evidence RUN_ID=..."
	@echo "  make slice RUN_ID=... DAY=YYYY-MM-DD SYMBOLS=A,B START=HH:MM END=HH:MM"
	@echo "  make verify"
	@echo "  make ship MSG='...'"
	@echo "  make clean_reports RUN_ID=..."

doctor:
	@bash tools/doctor.sh

# Creates/updates evidence skeleton (no trading integration yet)
evidence:
	@$(PY) tools/evidence.py --run-id "$(RUN_ID)"

# Market slice stub (later you will implement OSS/MySQL fetch here)
slice:
	@$(PY) tools/slice.py --run-id "$(RUN_ID)" --day "$(DAY)" --symbols "$(SYMBOLS)" --start "$(START)" --end "$(END)"

verify:
	@$(PY) -m pytest -q

# Convenience wrapper around tools/ship.sh
ship:
	@if [ -z "$(MSG)" ]; then echo "MSG is required. Example: make ship MSG='$(RUN_ID): fix smoke'"; exit 2; fi
	@bash tools/ship.sh "$(MSG)"

clean_reports:
	@if [ "$(RUN_ID)" = "run-unknown" ]; then echo "RUN_ID required"; exit 2; fi
	@rm -rf "reports/$(RUN_ID)" || true