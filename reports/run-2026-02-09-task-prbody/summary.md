# Summary
- Why: tools/task.sh generated an unused PR body and tools/ship.sh lacked evidence links required by AGENTS.
- What: removed unused PR body generation, passed task info to ship, and added task/evidence sections to PR body when available.
- Verify: `make verify` (after `source /root/policy/venv/bin/activate`).
