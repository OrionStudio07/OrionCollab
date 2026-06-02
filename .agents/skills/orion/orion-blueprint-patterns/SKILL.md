# Orion Studios — Blueprint Implementation Patterns

Used by @blueprint-engineer. Governs all Blueprint logic implementation.

---

## Implementation Output Format

```
FUNCTION: [FunctionName]
LOCATION: [Class name — must be verbatim from spec]
SPEC REF: [trd.md Section X.Y]

INPUTS:
  [ParamName]: [Type]

OUTPUTS:
  [ReturnName]: [Type]

GRAPH:
  1. [Node type: description] → [output pin] → [next node]
  2. [Branch: condition]
       → True:  [action]
       → False: [action]
  3. [Event/Delegate fire: name, params]

SPEC COMPLIANCE:
  ✓ [what spec requirement this satisfies]
  ✓ [what spec requirement this satisfies]

UNVERIFIED ITEMS:
  [Anything marked [UNVERIFIED — check before using]]
```

---

## CVT Command Component Lifecycle (Required Pattern)

Every BP_Orion* Command Component must implement this exact lifecycle:

```
EventExecuteAfterSpawnPawn
  └─→ Bind_Options
        Subscribe to input actions
        Configure UI bindings
        Set initial state

  └─→ Execute (tool active)
        Process input events
        Update visual state
        Fire telemetry

  └─→ Disabled (tool deactivated)
        Cleanup
        Unbind inputs
        Reset visual state

SAVEGAME HOOKS (both required — missing either breaks round-trip):
  EventBindSaveState
    └─→ Serialize current tool state → BP_Data_SaveGame

  EventBindLoadState
    └─→ Deserialize state from BP_Data_SaveGame
        └─→ Restore tool to saved state
```

---

## Delegate Wiring Pattern

For every delegate subscription, document completely:

```
DELEGATE BINDING
  Delegate: [OwnerClass]::[DelegateName]
  Subscriber: [This class]
  Handler: [function name in this class]
  Bound in: [BeginPlay / OnConstruction / specific event]
  Unbound in: [EndPlay / OnDestroyed / specific event]
```

---

## World Subsystem Access Pattern

```
Get subsystem in Blueprint:
  GetGameInstance → GetSubsystem (BP_OrionGameInstance)
  GetWorld → GetSubsystem (World Subsystems)

Order of availability at level load (Application Boot Flow):
  1. BP_OrionGameInstance::Init → BP_ConfigLoader runs
  2. Level loads → World Subsystems initialize
  3. Level loads → Actors begin play
  4. BP_MetadataLinker::RunMatching → fires OnMatchingComplete
  5. BP_HierarchyManager::BuildTree → fires OnTreeReady (background thread)
  6. Both delegates fired → Navigation UI enabled

Never access a World Subsystem from an Actor's Constructor.
Use BeginPlay with delegate binding instead.
```

---

## Known Safe CVT APIs (from spec and CLAUDE.md)

Use these freely — they are confirmed in spec documents:

```
Base classes:
  BP_BaseCommandComponent     — base for all command components
  BP_BasePawn                 — base pawn
  BP_LoginMenuPawn            — launcher/login pawn
  BP_VRPawn                   — VR pawn

SaveGame hooks (confirmed in spec):
  EventBindSaveState          — serialize to BP_Data_SaveGame
  EventBindLoadState          — deserialize from BP_Data_SaveGame

Utilities:
  CommonFunctions_Orion       — safe to use and modify (Orion-owned)
  CommonFunctions_CV          — READ ONLY; never modify
```

**For any CVT API NOT in the above list:**
Mark as `[UNVERIFIED — confirm in CVT source before connecting]`

---

## Telemetry Logging (Required Call Points)

Call BP_TelemetryManager for these events (trd.md Section 3.2):

```
Mode transition:        LogModeTransition(OldMode, NewMode)
Equipment viewed:       LogEquipmentView(EquipmentID, DurationSeconds)
Tool used:              LogToolUsage(ToolName, Action)
Tour completed:         LogTourCompletion(TourName, CompletionPercent)
Snapshot taken:         LogSnapshotCapture(Filename)
```

---

## Anti-Hallucination Discipline

Before referencing ANY class, node, or API not in this skill file or the spec:

1. Do NOT assume it exists in CVT
2. Mark it: `[UNVERIFIED — confirm in CVT source before use]`
3. List it in the UNVERIFIED ITEMS section of your output
4. Sho must verify in actual CVT project files before the node is connected

Wrong pattern:
> "I'll call `MatchActorsToTable()` on the linker..."

Correct pattern:
> "Per trd.md Section 3.2, the method is `RunMatching()`. Calling that now."

---

## Mode-Responsive Behavior Pattern

Subscribe to BP_OrionModeManager::OnModeChanged in BeginPlay.
Handle each mode state explicitly — never use an implicit "else":

```
OnModeChanged(OldMode, NewMode):
  Switch on NewMode:
    MODE_LAUNCHER:   [specific actions]
    MODE_SHOWCASE:   [specific actions]
    MODE_OPERATIONS: [specific actions]
    MODE_TRAINING:   Log warning "Training reserved for v2" — do nothing else
```
