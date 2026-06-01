---
description:
---

## Workflow Steps

### Step 1 — @lead loads the gate checklist

@lead reads AI_EXECUTION_PLAN.md for the completed phase and lists
every gate check item explicitly.

### Step 2 — @spec-guardian verifies spec compliance

Confirms no class names were invented, no CVT files modified, no
out-of-scope items implemented.

### Step 3 — @perf-auditor checks performance gates

For Phase 0: compile clean, no warnings
For Phase 1: subsystems initialize in correct order
For Phase 2: search <200ms, tree scroll 60fps  
For Phase 3: FPS targets met, animation limits respected
For Phase 4: all acceptance criteria met

### Step 4 — Gate result reported

```
PHASE [N] GATE CHECK RESULT
────────────────────────────
□ [gate check] — PASS / FAIL / NOT TESTED
□ [gate check] — PASS / FAIL / NOT TESTED
[all gates listed]

OVERALL: [PHASE COMPLETE — proceed to Phase N+1 / BLOCKED — items to fix]

Blocking items (if any):
- [item]: [what needs to be done before advancing]

Open questions to resolve before Phase [N+1]:
- [Q number]: [description]
```

### Step 5 — @session-logger produces phase completion report

Appends the Phase Completion Report section to the session log.

