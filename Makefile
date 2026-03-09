SHELL := /bin/bash
PY := /root/policy/venv/bin/python
RUN_ID ?= run-unknown

.PHONY: help doctor evidence awareness slice verify ship clean_reports orchestrator

help:
	@echo "Targets:"
	@echo "  make doctor"
	@echo "  make evidence RUN_ID=..."
	@echo "  make awareness RUN_ID=..."
	@echo "  make slice RUN_ID=... DAY=YYYY-MM-DD SYMBOLS=A,B START=HH:MM END=HH:MM"
	@echo "  make verify"
	@echo "  make ship MSG='...'"
	@echo "  make orchestrator ARGS='run --steps default'"
	@echo "  make clean_reports RUN_ID=..."

doctor:
	@bash tools/doctor.sh

# Creates/updates evidence skeleton (no trading integration yet)
evidence:
	@$(PY) tools/evidence.py --run-id "$(RUN_ID)"

awareness:
	@bash tools/observe.sh "$(RUN_ID)"

# Market slice stub (later you will implement OSS/MySQL fetch here)
slice:
	@$(PY) tools/slice.py --run-id "$(RUN_ID)" --day "$(DAY)" --symbols "$(SYMBOLS)" --start "$(START)" --end "$(END)"

verify:
	@if ls tests/task_*.py >/dev/null 2>&1; then \
		$(PY) -m pytest -q tests/task_*.py; \
	else \
		echo "VERIFY: no tests/task_*.py files present; skipping pytest"; \
	fi

# Convenience wrapper around tools/ship.sh
ship:
	@if [ -z "$(MSG)" ]; then echo "MSG is required. Example: make ship MSG='$(RUN_ID): fix smoke'"; exit 2; fi
	@bash tools/ship.sh "$(MSG)"

orchestrator:
	@$(PY) tools/run_main.py $(ARGS)

clean_reports:
	@if [ "$(RUN_ID)" = "run-unknown" ]; then echo "RUN_ID required"; exit 2; fi
	@rm -rf "reports/$(RUN_ID)" || true
