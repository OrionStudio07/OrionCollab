# Orion Studios — Spec Validation Protocol

Used by @spec-guardian. Validates every proposed implementation against the
five governing documents before any code is written.

---

## Validation Output Format

```
SPEC VALIDATION REPORT
──────────────────────
Task: [what was submitted for validation]
Spec Reference: [trd.md / prd.md / backend_schema.md section]

FINDINGS:
  ✓ [passed check — cite spec text]
  ⛔ [blocked item — cite spec text]
  ⚠️  [flagged item — cite spec text]

VERDICT: [APPROVED / BLOCKED / APPROVED WITH FLAGS]
Required changes before proceeding: [list, or "none"]
```

---

## Check 1 — Class Name Registry

Every class name must appear verbatim in trd.md Section 3 or CLAUDE.md
Section 13. Reject anything that does not:

```
⛔ NAME MISMATCH
  Proposed: [name]
  Spec says: [exact name from trd.md Section X]
  Action: Use spec name verbatim — do not rename
```

**Known-good class names (from CLAUDE.md Section 13):**

World Subsystems:
- `BP_OrionModeManager`
- `BP_HierarchyManager`
- `BP_MetadataLinker`
- `BP_TelemetryManager`

Game Instance:
- `BP_OrionGameInstance`
- `BP_ConfigLoader`

Command Components (all extend BP_BaseCommandComponent):
- `BP_OrionMeasurement` extends `BP_DimensionComponent`
- `BP_OrionXray` extends `BP_XrayComponent`
- `BP_OrionExplode` extends `BP_ExplodeComponent`
- `BP_OrionCropBox` extends `BP_CropBoxComponent`
- `BP_OrionSnapshot` extends `BP_SnapshotComponent`
- `BP_OrionRatioScale` extends `BP_RatioScaleComponent`
- `BP_OrionDataSmith` extends `BP_DataSmithComponent`

Actors:
- `BP_GuidedTourManager`
- `BP_InspectionManager`
- `BP_NPCManager`
- `BP_ZoneAnimationManager`
- `BP_CameraSweepManager` (Actor Component)
- `BP_SnapManager` (Actor Component)
- `BP_SessionRecorder`

Widgets:
- `WBP_OrionRoot`, `WBP_TopBar`, `WBP_SidePanel`, `WBP_TreeBrowser`
- `WBP_EquipmentDetails`, `WBP_SearchPanel`, `WBP_BottomBar`
- `WBP_Minimap`, `WBP_ToolRadialMenu`, `WBP_Notification`, `WBP_ModalOverlay`

---

## Check 2 — Lifecycle Verification

| Type | Base Class | Lifecycle |
|------|-----------|-----------|
| World Subsystem | UWorldSubsystem | Created per-world; destroyed on level unload |
| Command Component | BP_BaseCommandComponent | Bind_Options → Execute → Disabled |
| Actor | AActor | Placed or spawned; standard actor lifecycle |
| Game Instance | UGameInstance | Persists across level loads |
| UMG Widget | UUserWidget | Created by owning widget; destroyed with it |

---

## Check 3 — API Signature Verification

Compare proposed methods against trd.md Section 3.x.
Flag any renamed methods, missing parameters, or wrong return types:

```
⛔ API MISMATCH
  Proposed: [method signature]
  Spec says (trd.md Section X.Y): [exact method signature]
  Action: Match spec verbatim
```

---

## Check 4 — CVT Extension Check

SAFE — extend by:
- Subclassing (e.g., extends BP_BaseCommandComponent)
- Binding to delegates (EventBindSaveState, EventBindLoadState, OnModeChanged)
- Adding new Blueprint Function Library (CommonFunctions_Orion only)

BLOCKED — never:
- Modify any CVT Blueprint directly
- Replace CVT session management
- Modify CommonFunctions_CV
- Delete, rename, or reorder CVT classes

```
⛔ CVT VIOLATION
  Proposed action: [description]
  Why blocked: CVT base modification per CLAUDE.md Section 7
  Alternative: [extension path — subclass / delegate binding]
```

---

## Check 5 — Open Question Guard

If implementation touches any of these areas, flag before proceeding:

| Question | Area affected |
|----------|--------------|
| Q1 | Plant 3D Python access → Pipeline B, MetadataLinker |
| Q2 | CAD drawing format → WBP_EquipmentDetails Drawings tab |
| Q3 | Animation type → BP_ZoneAnimationManager, all equipment animations |
| Q4 | NPC model type → BP_NPCWorker, BP_NPCManager |
| Q5 | Recording scope → BP_SessionRecorder |

```
⚠️ OPEN QUESTION DEPENDENCY
  Question: Q[N] — [description]
  Blocks: [what cannot be decided without this answer]
  Action: Implement placeholder only; do not guess
```

---

## Check 6 — Out-of-Scope Guard

Block any work on these v1 exclusions:
Mode B Training | Live Simulation Data | Thermal Heatmaps | Construction Timeline
| Localization content | Cloud Logging | Standalone Quest APK | Client Plugins

```
⛔ OUT OF SCOPE (v1)
  Requested: [description]
  Reason: PRD Section "Out of Scope (v1)"
  Prep architecture exists: [yes/no — describe placeholder]
  Action: Implement placeholder/interface only
```

---

## Check 7 — Schema Verification

All Data Table field names must match backend_schema.md Section 2 exactly:

```
⚠️ SCHEMA GAP
  Field needed: [field name, proposed type]
  Location: [struct name]
  Status: EXISTS in backend_schema.md Section 2.X / DOES NOT EXIST
  Action if missing: Flag for user approval before proceeding
```

---

## Check 8 — Performance Flag

For any system running on Tick, processing datasets, or allocating memory:

```
⚠️ PERFORMANCE CHECK
  Operation: [what is running]
  Frequency: [per-frame / throttled / on-demand / once at load]
  Dataset size: [estimate]
  Budget reference: [trd.md Section 9 line item]
  Risk: [low / medium / high]
  Mitigation: [background thread / cache / UListView / throttle]
```
