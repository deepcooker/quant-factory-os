# AGENTS.md (Hard Rules for Codex / Agents)

This repo is an OS for quant engineering. Agents MUST obey these rules.

## 0) Scope
- You work ONLY inside this repository.
- Never invent data. Never assume prod access.
- Prefer deterministic scripts + evidence, not long chat.

## 1) Entry: Tasks are syscall
- All work MUST start from a task file under /TASKS.
- If no task is provided, pick the next unchecked item in QUEUE.md and create a TASK file first.
- Never change code without an active task ID and RUN_ID.

## 2) Output: Evidence is memory
For each task you MUST create/update:
- reports/<RUN_ID>/meta.json
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md

Optional:
- reports/<RUN_ID>/samples/*.csv.gz
- MISTAKES/<RUN_ID>.md (only if failure)

## 3) Constraints (Data / Size / Secrets)
- Never write or commit secrets. Never print secrets.
- Never commit production data. Use synthetic or reduced samples only.
- Hard limits:
  - Any single generated file <= 5MB
  - Any table-like output <= 500 rows unless explicitly requested by task

## 4) Allowed Commands (Default)
Use ONLY these unless task explicitly authorizes more:
- tools/qf
- tools/doctor.sh
- tools/enter.sh
- tools/task.sh
- tools/ship.sh
- tools/view.sh
- make evidence RUN_ID=...
- make verify
- make slice RUN_ID=... DAY=... SYMBOLS=... START=... END=...
- pytest -q

Notes:
- Primary agent entrypoint is `tools/qf` (`init/plan/do/resume`).
- `tools/enter.sh` and `tools/onboard.sh` are compatibility wrappers.

## Reading policy
- 长文件阅读必须使用 tools/view.sh 分段查看，不得直接使用 sed/cat/rg/grep/awk。

## 5) Workflow (Must follow)
1) Read TASKS/<task>.md and confirm acceptance criteria.
2) Run `make evidence RUN_ID=<RUN_ID>` (creates evidence skeleton).
3) Implement change in smallest diff possible.
4) Run `make verify` until green.
5) Write decision + update summary (what changed / why / risks / verify commands).
6) Ship via `tools/ship.sh` or `make ship` (if defined).

## 6) Failure protocol
If stuck or tests fail:
- Capture the failing command + minimal logs in reports/<RUN_ID>/summary.md
- Write MISTAKES/<RUN_ID>.md with:
  - symptom, root cause hypothesis, fix, guardrail test suggestion
  - process category: thinking_error / decision_error / execution_error / verification_error / recovery_error / business_error
- Add/strengthen a test to prevent regression.
- Treat mistakes as end-to-end process memory, not only business/domain errors.

## 7) PR discipline (Single-user but strict)
- One task -> one branch -> one PR
- PR title MUST include RUN_ID
- PR body MUST include:
  - Why / What / Verify
  - Evidence paths

## 8) Session init gate (Mandatory, once per session)
Before any implementation, you MUST complete init and pass readiness checks:
1) Run `tools/qf init`
2) Read, in order:
   - `AGENTS.md`
   - `chatlogs/PROJECT_GUIDE.md`
   - `TASKS/STATE.md`
   - `TASKS/QUEUE.md`
   - `docs/WORKFLOW.md`
   - `docs/ENTITIES.md`
   - latest `reports/<RUN_ID>/decision.md`
3) Restate and get confirmation before coding:
   - Goal (1 sentence)
   - Scope (exact paths)
   - Acceptance (verify/evidence/scope)
   - Execution steps (evidence -> implement -> verify -> reports -> ship)
   - Stop condition (finish and wait)
4) Record readiness gate:
   - Run `tools/qf ready RUN_ID=<run-id>` (interactive or via `QF_READY_*` envs).
   - `tools/qf do` MUST fail if no valid `reports/<RUN_ID>/ready.json`.
5) If restatement is missing or unclear, STOP and do not modify code.

## 9) Governance policy (Default)
- This repo is PR-driven and local-verify-first.
- Required before ship: local `make verify` is green and recorded in reports.
- Do not rely on GitHub Actions queues as required path.
- `.github/workflows/*.yml|*.yaml` is blocked by default in `tools/ship.sh`.
  To allow intentionally for one run:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`
