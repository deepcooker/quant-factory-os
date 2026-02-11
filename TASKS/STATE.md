# STATE

## Current baseline
- Core tooling available: `tools/start.sh`, `tools/enter.sh`, `tools/doctor.sh`,
  `tools/view.sh`, `tools/find.sh`.
- Documentation baseline in place: `docs/WORKFLOW.md`, `docs/ENTITIES.md`,
  `docs/README.md` (if present).

## Current conventions
- Task = requirement definition (source of truth for scope).
- PR = delivery artifact for one task.
- RUN_ID = evidence namespace under `reports/<RUN_ID>/`.
- Handoff rule: `docs/WORKFLOW.md` Memory & Context.
- Boundary v0: `docs/BOUNDARY_A9.md`.

## Next steps
- Finish baseline hardening, then begin main project integration.
- Define external data ingestion strategy and constraints (sources, format,
  retention).
- Define database/storage strategy and interfaces.
- Confirm OSS dependency policy and allowlist.
- Add minimal regression tests for core tooling and workflow enforcement.

## Current blockers / risks
- External data and database/OSS integration policies are not yet defined.
