# Orion Studios — Self-Correction Analysis Protocol

Used by @debugger. From CLAUDE.md Section 12.
Never suggest a fix before the full analysis is complete.

---

## Analysis Template

```
SELF-CORRECTION ANALYSIS
─────────────────────────
ERROR/ISSUE: [exact — what is happening vs what should happen]
WHERE: [class, function, Blueprint graph, C++ line]

ROOT CAUSE HYPOTHESIS:
  1. [most likely — cite reasoning]
  2. [second possibility — cite reasoning]
  3. [third if relevant]

SPEC CHECK:
  Flow diagram governing this feature: [flow_diagrams.md Flow N]
  Step where bug occurs: [step N in that flow]
  What spec says should happen: "[exact quote from trd.md / flow_diagrams.md]"
  Does current implementation match? [yes / no]
  If no: what specifically diverged?

LAST CHANGE ANALYSIS:
  Last implementation change before this broke: [description]
  Touches CVT code? [yes = higher risk / no]
  Could that change have caused this? [yes / no / possibly — explain]

FIX OPTIONS:
  Option A (surgical — touches only the broken thing):
    Scope: [exactly what changes]
    Risk: [what else could be affected]
  Option B (broader — addresses root cause):
    Scope: [exactly what changes]
    Risk: [what else could be affected]

RECOMMENDATION: [Option A / B — with reasoning]
```

---

## Escalation Rules

**CVT code involved**: Always recommend Option A (surgical). Never modify CVT
to fix an Orion bug — find the extension path instead.

**Spec divergence found**: The fix must bring the implementation INTO compliance
with the spec. Do not rationalize the current broken behavior.

**Timing issue suspected** (null pointer at init, delegate not firing): Always
check flow_diagrams.md Flow 1 (Application Boot Flow) for correct init order.

**Performance degradation**: Call @perf-auditor in parallel with this analysis.

---

## Common Orion Bug Patterns

### Null pointer at level load
Check Application Boot Flow (flow_diagrams.md Flow 1).
`BuildTree()` and `RunMatching()` run in parallel after level load.
Neither should depend on the other being complete first.
Systems that need both must wait for BOTH `OnTreeReady` AND `OnMatchingComplete`.

### Wrong enum value
Cross-reference backend_schema.md Section 1.
Enums are uint8 — verify no implicit cast.

### Delegate not firing
Check that binding happened in BeginPlay AFTER the source is initialized.
World Subsystems initialize before Actors.
Delegate subscriptions from Actors: BeginPlay only, never Constructor.

### CVT SaveGame not restoring
Both `EventBindSaveState` AND `EventBindLoadState` must be implemented.
Missing either one breaks the round-trip silently.

### Search latency >200ms
Check: (1) background thread actually used?, (2) cache checked before scan?,
(3) Data Tables fully loaded before search runs?

### Xray colors wrong
Stencil values per flow_diagrams.md Flow 6:
  Pipe = 1, Structure = 2, Electrical = 3, Other = 4
Post-process reads stencil buffer. Color map:
  pipes = blue, structure = white, electrical = yellow

### Mode change not propagating to clients
Mode state replicates via `UPROPERTY(Replicated)` on Game State.
Check that `OnRep_CurrentMode` is implemented and fires local `OnModeChanged`.

---

## Fix Constraints

A fix is INVALID if it:
- Modifies any CVT base file
- Deviates from the spec without explicitly flagging the deviation
- Touches more code than necessary to fix the root cause hypothesis
- Cannot be traced to a spec requirement
