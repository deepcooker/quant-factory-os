# SESSION_COACH_PROTOCOL

## Purpose
This protocol is a lightweight personal operator aid for running multiple Codex windows against the same project.

It is not part of the formal runtime mainline.
It does not replace:
- `appserverclient`
- `taskclient`
- `gitclient`

It only standardizes how one "coach" window should guide and validate:
- one `baseline` window
- one `fork-run` window

## Role Split

### 1. Coach
The coach window does not execute the main work itself.
It is responsible for:
- identity confirmation prompts
- next-question generation
- answer validation
- next-step routing

### 2. Baseline
The baseline window is the project learning anchor.
It is responsible for:
- confirming `session_registry.learn_session_baseline`
- answering high-quality `PROJECT_GUIDE` questions
- judging mainline direction from current evidence

The baseline window should not be used for normal day-to-day implementation work once learning is complete.

### 3. Fork-Run
The fork-run window is the current working session.
It is responsible for:
- confirming `session_registry.fork_current_session`
- executing formal next-hop commands
- handling concrete implementation or verification work

The fork-run window should not restart baseline learning unless explicitly told to do so.

## Minimal Interaction Rules

### A. Identity Confirmation
Before asking for reasoning or execution, the coach must first force identity confirmation.

For baseline, require confirmation of:
- `session_registry.learn_session_baseline.thread_id`
- `status`
- `effort`

For fork-run, require confirmation of:
- `session_registry.fork_current_session.thread_id`
- `forked_from_thread_id`
- `status`

If identity is not confirmed first, the reply fails.

### B. What The Coach May Ask

For `baseline`:
- answer one `PROJECT_GUIDE` question
- explain whether a step belongs to the formal mainline
- classify a failure as logic vs environment boundary

For `fork-run`:
- execute the next formal command
- report execution result
- re-read `tools/project_config.json`
- confirm whether runtime truth was written back

### C. Pass / Retry Rule
Each coach step should end in one of only two outcomes:
- `pass`
- `retry`

`pass` means:
- the identity was confirmed
- the answer or command result is specific and evidence-based
- the next hop can be issued

`retry` means:
- identity was not confirmed
- answer stayed generic
- command result was not tied back to `tools/project_config.json`

### D. Next-Step Routing
- If the baseline answer is good enough, the coach should either:
  - ask the next high-value `PROJECT_GUIDE` question
  - or route to `fork-current`
- If the fork-run command succeeds, the coach should move to the next formal execution step.
- If the fork-run command fails, the coach should first force failure classification:
  - mainline logic failure
  - runtime/environment boundary failure

## Standard Prompt Shapes

### 1. Baseline Identity Prompt
Use this pattern:

```text
You are not a normal discussion thread. You are the current baseline session.

1. Read tools/project_config.json.
2. Confirm session_registry.learn_session_baseline.
3. Report thread_id / status / effort.
4. Do not expand to other topics.
```

### 2. Fork-Run Identity Prompt
Use this pattern:

```text
You are not the baseline. You are the current forked working session.

1. Read tools/project_config.json.
2. Confirm session_registry.fork_current_session.
3. Report thread_id / forked_from_thread_id / status.
4. Do not expand to other topics.
```

### 3. Fork-Run Execution Prompt
Use this pattern:

```text
You are the current forked working session.

1. Read tools/project_config.json first.
2. Confirm the current fork session is ready.
3. Execute the next formal command.
4. Read tools/project_config.json again.
5. Report only:
   - what you saw before execution
   - what you executed
   - what runtime truth was written back
```

### 4. Failure Classification Prompt
Use this pattern:

```text
Do not re-explain the project.

Please classify the last failure:
1. Was the formal next hop correct?
2. Did the failure come from repo logic, or from runtime/environment boundaries?
3. What is the correct next action now?
Only answer these three points.
```

## Scope Boundary
This protocol is intentionally small.

It does not define:
- role-thread orchestration policy
- task decomposition policy
- automatic multi-window control
- app-server transport behavior

Those remain owned by:
- `AGENTS.md`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`

## Relationship To Skills
This file is the repo-owned protocol.

A skill may wrap this protocol for easier reuse, but the protocol remains the source text to audit and evolve.
