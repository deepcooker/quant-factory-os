# Decision
- tools/task.sh now prefixes the commit message with RUN_ID when present and passes task metadata via SHIP_TASK_*.
- tools/ship.sh now prepends task info and adds Evidence paths when a run id can be detected; otherwise PR body is unchanged.
- Verify: `make verify` (after `source /root/policy/venv/bin/activate`).
