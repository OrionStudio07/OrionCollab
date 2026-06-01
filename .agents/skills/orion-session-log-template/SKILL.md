# Orion Studios — Session Log Template

Used by @session-logger. Called by @lead at the end of every session.
This log is the only continuity between AI sessions.

---

## Session Log

```
ORION STUDIOS SESSION LOG
─────────────────────────
Date: [YYYY-MM-DD]
Phase: [Phase N — description]
Session type: [New module / Continue / Debug / UI / Data / Phase transition]

## IMPLEMENTED THIS SESSION

| Class/File | Methods or Events | Spec Reference | Status |
|------------|------------------|----------------|--------|
| [name] | [method list] | [section] | Complete / Partial |

## GATE CHECKS COMPLETED

□ [gate check description] — PASS / FAIL / NOT TESTED
□ [gate check description] — PASS / FAIL / NOT TESTED

## NOT DONE (and why)

- [item]: [blocked by / deferred / requires Q answer / out of time]

## GRAY AREAS FLAGGED

- [gray area]: [what decision is needed, from whom]
- (or: "None this session")

## OPEN QUESTIONS STATUS

| Q | Description | Status | Blocks |
|---|-------------|--------|--------|
| Q1 | Plant 3D Python access | Unresolved / Resolved: [answer] | Pipeline B |
| Q2 | CAD drawing format | Unresolved / Resolved: [answer] | Drawings tab |
| Q3 | Animation type | Unresolved / Resolved: [answer] | ZoneAnimationManager |
| Q4 | NPC model type | Unresolved / Resolved: [answer] | NPCManager |
| Q5 | Recording scope | Unresolved / Resolved: [answer] | BP_SessionRecorder |

## CVT INTEGRITY CHECK

□ No CVT base files modified this session
□ All Orion classes extend CVT by subclassing or delegate binding only
□ CommonFunctions_CV not modified this session

## NEXT SESSION SETUP

First task: [exact task name and description]
Phase: [Phase N]
Spec sections to load: [list — be specific, e.g. "trd.md Section 3.2"]

---
CONTEXT PACKAGE (paste this at start of next session):
───────────────────────────────────────────────────────
ORION STUDIOS SESSION CONTEXT
Project: Orion Studios — Industrial Plant Visualization Platform
Engine: Unreal Engine 5.8
Base: CollabViewer Template (CVT) — extend only, never modify CVT directly
Language: Blueprint primary; C++ for performance-critical systems only

ACTIVE TASK: [next task]
PHASE: [Phase N]
SPEC REFERENCES: [list]

PREVIOUS SESSION SUMMARY:
[paste this full log here]
───────────────────────────────────────────────────────
```

---

## Phase Completion Report (append when a full phase is done)

```
## PHASE [N] COMPLETION REPORT

Gate checks from AI_EXECUTION_PLAN.md:
  □ [gate check] — PASS / FAIL
  □ [gate check] — PASS / FAIL
  [all gate checks for this phase]

Phase [N+1] readiness:
  □ All Phase [N] gates: PASS
  □ No blocking gray areas open
  □ No out-of-scope items accidentally implemented
  □ No CVT files modified across any session this phase

Phase [N+1] first tasks (from AI_EXECUTION_PLAN.md):
  1. [task name] — [brief description]
  2. [task name] — [brief description]

ACTION REQUIRED BEFORE PHASE [N+1]:
  [Open questions that must be answered, approvals needed,
   external inputs required — or "None, ready to proceed"]
```

---

## Quality Check Before Finalizing

Before outputting the log, verify:

- Every class name appears verbatim in the spec or CLAUDE.md Section 13
- Every spec reference is a real section number that exists in the document
- The context package has everything needed for a cold-start AI to resume
  correctly without access to this conversation
- No CVT integrity violations went unlogged
- Open questions table is accurate — nothing resolved without noting it
