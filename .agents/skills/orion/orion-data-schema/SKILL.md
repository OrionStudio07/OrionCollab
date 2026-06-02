# Orion Studios — Data Schema Reference

Used by @data-engineer. Governs all Data Table structs, config validation,
and import/export formats.

---

## Struct Output Format

```
STRUCT: [FStructName]
FILE: [StructName.h]
SPEC REF: [backend_schema.md Section 2.X]
EXTENDS: FTableRowBase

[Complete .h file — verbatim field names from spec]

VALIDATION:
  □ All fields from spec present
  □ No extra fields added
  □ Enum fields use OrionTypes.h types
  □ FText for all display names
  □ FName for all IDs and foreign keys
  □ Default values match spec exactly
  □ UE5 CSV column names match Data Table column names in spec
```

---

## Field Type Rules

| Data | Type | Never use |
|------|------|-----------|
| IDs, foreign keys | `FName` | FString for IDs |
| User-visible text | `FText` | FString for display names |
| File paths, tags | `FString` | — |
| Enum fields | Enum from OrionTypes.h | Raw int or string |
| Booleans | `bool` with default | — |
| Arrays | `TArray<FName>` or typed | — |

---

## Schema Gap Protocol

Any feature requiring a field not in backend_schema.md Section 2 must be
raised and approved before implementation:

```
⚠️ SCHEMA GAP
  Feature needing field: [feature name]
  Field needed: [field name, proposed type]
  Proposed struct: [FStructName]
  Impact: [what cannot be built without this field]
  Action: STOP — user must approve schema addition
  Do NOT add silently
```

---

## OrionConfig.json Validation Rules (trd.md Section 10.2)

| Field | Validation | On failure |
|-------|-----------|------------|
| client.company_name | Non-empty string | Default: "Orion Studios" |
| client.logo_path | File exists at path | Default: embedded Orion logo |
| client.accent_color | Regex `^#[0-9A-Fa-f]{6}$` | Default: `#00D4AA` |
| modes.* | Boolean | showcase=true, training=false, operations=true |
| target_fps_desktop | Integer 30–144 | Clamp to range |
| target_fps_vr | Integer 30–144 | Clamp to range |
| Entire file | Valid JSON | Full embedded defaults + warning banner |

For each validation failure, specify:
- Detection method
- Fallback value
- User notification: banner (file missing) / toast (fields invalid) / silent

---

## Hot-Reload Logic (Dev Builds Only — trd.md Section 10.3)

```
1. Register FPlatformFileManager watcher on OrionConfig.json path
2. On file change → re-parse JSON
3. Run validation (same rules as initial load)
4. Fire OnConfigReloaded multicast delegate
5. Subscribed systems update without app restart

Shipping builds: skip watcher entirely
Guard with: #if WITH_ORION_DEBUG ... #endif
```

---

## Pipeline B Output Verification (backend_schema.md Section 8.1)

When validating Python export from Plant 3D:
- equipment_id values must match actor naming patterns in the scene
- equipment_type values must match EEquipmentType enum values exactly
- Flag any JSON fields present but missing from FEquipmentTableRow
- Flag any FEquipmentTableRow fields missing from JSON (imports as defaults)

---

## Data Table Initialization Order

From flow_diagrams.md Flow 1 (Application Boot Flow):
```
App launch → BP_ConfigLoader → Load Login Level → Load Main Level
           → BP_MetadataLinker::RunMatching (reads DT_Equipment)
           → BP_HierarchyManager::BuildTree (reads DT_Buildings, DT_Rooms, DT_Equipment)

Data Tables must be populated BEFORE RunMatching() and BuildTree() are called.
Both fire delegates when complete. UI unlocks only after BOTH delegates fire.
```

---

## All Data Tables (CLAUDE.md Section 13)

- `DT_Equipment` — struct: `FEquipmentTableRow`
- `DT_Buildings` — struct: `FBuildingTableRow`
- `DT_Rooms` — struct: `FRoomTableRow`
- `DT_ProcessLines` — struct: `FProcessLineTableRow`
- `DT_Zones` — struct: `FZoneTableRow`
- `DT_NPCs` — struct: `FNPCTableRow`
- `DT_TourWaypoints` — struct: `FTourWaypointTableRow`
- `DT_InspectionSteps` — struct: `FInspectionStepTableRow`
