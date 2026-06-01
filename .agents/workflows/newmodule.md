---
description:
---

## Workflow Steps

### Step 1 — @lead runs pre-task checklist

@lead loads `.agents/skills/orion-pre-task-checklist.md` and answers
every item before proceeding. If any item cannot be answered from the
spec documents, stop and report the gray area to the user.

### Step 2 — @lead produces implementation plan

Format:
```
TASK: Implement [ClassName]
SPEC REFERENCE: [trd.md Section X.Y]

1. [Step] → verify: [exact check]
2. [Step] → verify: [exact check]
3. [Step] → verify: [exact check]

GRAY AREAS: [or "none"]
AWAITING APPROVAL: yes
```

@lead pauses here. Do not continue until the user approves the plan.

### Step 3 — @spec-guardian validates

@lead delegates to @spec-guardian with the plan and spec section.
@spec-guardian loads `.agents/skills/orion-spec-validation.md` and
produces a SPEC VALIDATION REPORT.

If BLOCKED: stop, report findings to user, do not proceed.
If APPROVED WITH FLAGS: proceed, but surface all flags to user.
If APPROVED: proceed to Step 4.

### Step 4 — Implementation

@lead delegates to the correct implementer:

| What is being built | Agent |
|---------------------|-------|
| Blueprint logic, delegates, Event Graphs | @blueprint-engineer |
| C++ (OrionTypes.h, HierarchyManager search, SnapManager) | @cpp-engineer |
| UMG widget | @ui-engineer |
| Data Table struct or config validation | @data-engineer |

If the task has performance implications → also call @perf-auditor in parallel.

### Step 5 — @session-logger produces log

@lead calls @session-logger at the end of the session.
@session-logger loads `.agents/skills/orion-session-log-template.md`
and produces the complete session log + next session context package.