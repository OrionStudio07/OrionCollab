---
description:
---
## Workflow Steps

### Step 1 — @debugger takes the report

@lead delegates to @debugger with:
- Exact description of what is happening vs what should happen
- Which class/function/Blueprint graph is affected
- Last implementation change before this broke
- Any error messages

### Step 2 — @debugger runs full analysis

@debugger loads `.agents/skills/orion-debug-protocol.md` and produces
the complete Self-Correction Analysis. Does NOT suggest a fix yet.

### Step 3 — @spec-guardian verifies what correct behavior looks like

@spec-guardian loads `.agents/skills/orion-spec-validation.md` and
quotes the exact spec text that defines the correct behavior for this
feature. Confirms whether the bug is a spec divergence or a runtime error.

### Step 4 — @perf-auditor checks if performance is involved

If the bug involves timing, frame drops, or load times, @perf-auditor
runs in parallel with Step 3.

### Step 5 — Fix options presented to user

@debugger presents Option A (surgical) and Option B (broader) with
scopes and risks clearly stated. Waits for user to choose.

### Step 6 — Implementation of approved fix

@lead delegates the approved fix to the appropriate implementer.
Scope is strictly limited to what was approved in Step 5.

### Step 7 — @session-logger logs the fix

Documents: what broke, root cause, fix applied, spec ref, CVT integrity.
