# Orion Studios — Technical Requirement Document (TRD)
**Version 1.0.0** · Orion Studios · 2026-05-31

---

## AI READING INSTRUCTION

Read `[SPEC]` sections for authoritative technical specifications.
Read `[NOTE]` sections for design rationale and context.
Read `[BUG]` sections for known issues and workarounds.

---

## 1. System Overview

**[SPEC]**

- **Engine:** Unreal Engine 5.8
- **Base Template:** CollabViewer Template (CVT) — provides orbit/FPV/VR cameras, multi-user sessions, annotation, measurement, explode, laser pointer, Datasmith import
- **Language:** Blueprint primary (all gameplay logic); C++ for performance-critical subsystems (HierarchyManager search, SnapManager vertex queries)
- **Build Targets:** Windows Desktop (.exe) + PC VR (Meta Quest Link / SteamVR)
- **Reference Scale:** 6500 equipment tags, 1394 instrumentation points, ~500 process lines, ~200 unique equipment

---

## 2. Technology Stack

**[SPEC]**

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Engine | Unreal Engine | 5.8 | Runtime, editor, packaging |
| Template | CollabViewer Template | UE5.8 bundled | Multi-user, tools, pawn hierarchy |
| Rendering | Lumen (desktop) / Baked (VR) | Native | GI, reflections |
| UI | UMG (Unreal Motion Graphics) | Native | All in-game UI widgets |
| Data | UE5 Data Tables + JSON config | Native | Equipment metadata, tour waypoints, NPC definitions |
| Networking | CVT session system | Native | Multi-user collaboration |
| VR | OpenXR via SteamVR / Meta Quest Link | Native | PC tethered VR |
| Localization | FText + String Tables | Native | Localization-ready text |
| Build | UnrealBuildTool | Native | Compilation, cooking, packaging |
| CAD Pipeline | Datasmith (3ds Max exporter) | UE5.8 bundled | Geometry import |
| Metadata Pipeline | Python 3.x (Plant 3D script) | External | Tag/metadata export |

**[NOTE]**
No external package dependencies (npm, pip, NuGet) for the runtime application. The Python script is a standalone development tool used once during client onboarding.

---

## 3. Module Architecture

### 3.1 Module Classification

**[SPEC]**

Modules are classified into three types based on their lifecycle and communication pattern:

| Type | UE5 Class | Lifecycle | Examples |
|------|-----------|-----------|----------|
| **World Subsystem** | `UWorldSubsystem` | Created per-world; destroyed on level unload; accessible via `GetWorld()->GetSubsystem<>()` | ModeManager, HierarchyManager, MetadataLinker, TelemetryManager |
| **Command Component** | `BP_BaseCommandComponent` child | Created by pawn on spawn; follows CVT lifecycle `Bind_Options → Execute → Disabled`; participates in SaveGame | Enhanced Xray, Explode, CropBox, Measurement, Snapshot, RatioScale, DataSmith, Annotation, Bookmark |
| **Actor** | `AActor` | Placed in level or spawned at runtime; standard actor lifecycle | TourManager, InspectionManager, NPCManager, ZoneAnimationManager, InteractiveObjects |
| **Game Instance** | `UGameInstance` child | Persists across level loads | ConfigLoader (reads OrionConfig.json once at app start) |

### 3.2 World Subsystem Specifications

#### BP_OrionModeManager (World Subsystem)

**[SPEC]**

```text
Purpose: Global mode state management
Lifecycle: Created when main level loads; destroyed on level unload

Enum EOrionMode:
  MODE_LAUNCHER    = 0   // Role selection, settings
  MODE_SHOWCASE    = 1   // Mode A — presentation
  MODE_OPERATIONS  = 2   // Mode C — engineering
  MODE_TRAINING    = 3   // Reserved for v2

API:
  SetMode(EOrionMode NewMode) → void

    - Validates permission via CanAccessMode()
    - Updates internal state
    - Fires OnModeChanged multicast delegate
    - Broadcasts to all network clients via GameState

  GetCurrentMode() → EOrionMode

  CanAccessMode(EOrionMode Mode, EOrionRole Role) → bool

    - Admin: all modes
    - Engineer: SHOWCASE + OPERATIONS
    - Viewer: SHOWCASE only

Delegates:
  OnModeChanged(EOrionMode OldMode, EOrionMode NewMode) → multicast
```

#### BP_HierarchyManager (World Subsystem)

**[SPEC]**

```text
Purpose: Equipment hierarchy tree and search
Lifecycle: Builds tree on level load from Data Tables

Data Structure (in-memory):
  TMap<FName, FBuildingNode> BuildingMap
  Each FBuildingNode contains:
    FName BuildingID
    FText DisplayName
    TArray<FRoomNode> Rooms

  Each FRoomNode contains:
    FName RoomID
    FText DisplayName
    EZoneClassification SafetyZone  // Clean, Chemical, Electrical, Confined
    TArray<FEquipmentNode> Equipment

  Each FEquipmentNode contains:
    FName EquipmentID
    FText DisplayName
    FString PIDTag
    FString ProcessLine
    EEquipmentType Type
    TWeakObjectPtr<AActor> WorldActor  // Resolved by MetadataLinker
    TArray<FName> ComponentIDs  // Lazy-loaded on expand

API:
  BuildTree() → void  // Called on BeginPlay; runs on background thread
  GetBuildingList() → TArray<FBuildingNode>
  GetRoomsByBuilding(FName BuildingID) → TArray<FRoomNode>
  GetEquipmentByRoom(FName RoomID) → TArray<FEquipmentNode>
  GetComponentsByEquipment(FName EquipmentID) → TArray<FName>  // Lazy
  SearchAll(FString Query) → TArray<FSearchResult>  // Fuzzy match
  GetEquipmentActor(FName EquipmentID) → AActor*

Search Implementation:

  - Indexed fields: DisplayName, PIDTag, ProcessLine, RoomName, BuildingName
  - Matching: case-insensitive substring + Levenshtein distance for fuzzy
  - Cache: TMap<FString, TArray<FSearchResult>> for repeat queries
  - Performance target: <200ms for any query across 6500 entries

Delegates:
  OnEquipmentSelected(FName EquipmentID) → multicast
  OnTreeReady() → multicast  // Fired when background build completes
```

#### BP_MetadataLinker (World Subsystem)

**[SPEC]**

```text
Purpose: Auto-match Datasmith-imported actors to Data Table rows
Lifecycle: Runs once on level load after Data Tables are populated

Algorithm:

  1. Scan all actors with "Datasmith" tag or specific actor classes
  2. For each actor, extract candidate name (actor label / component name)
  3. Normalize: strip prefixes (SM_, BP_), convert to lowercase
  4. Match against DT_Equipment.EquipmentID using:

     a. Exact match (highest confidence)
     b. Contains match (medium confidence)
     c. Levenshtein distance ≤ 3 (low confidence, flagged as "ambiguous")

  5. Tag matched actors with EquipmentID as actor tag
  6. Store match results in TMap<FName, TWeakObjectPtr<AActor>>
  7. Generate report: {matched: N, unmatched: N, ambiguous: N}

API:
  GetMetadataLinkerSubsystem(const UObject* WorldContextObject) → UOrionMetadataLinker*  // Static getter for Python/BP access
  RunMatching() → FMatchReport
  GetActorForEquipment(FName EquipmentID) → AActor*
  GetUnmatchedActors() → TArray<AActor*>
  ManualLink(AActor* Actor, FName EquipmentID) → void

Delegates:
  OnMatchingComplete(FMatchReport Report) → multicast
```

#### BP_TelemetryManager (World Subsystem)

**[SPEC]**

```text
Purpose: Local analytics logging
Output: Saved/Logs/Telemetry/YYYY-MM-DD_session.json

Events Logged:

  - ModeTransition {timestamp, from_mode, to_mode}
  - EquipmentView {timestamp, equipment_id, duration_seconds}
  - ToolUsage {timestamp, tool_name, action}
  - TourCompletion {timestamp, tour_name, completion_percent}
  - SnapshotCapture {timestamp, filename}
  - SessionDuration {start_time, end_time, total_seconds}

Privacy: No PII collected — interaction events with timestamps only
Format: JSON array, one object per event — compatible with future cloud upload
```

### 3.3 Command Component Specifications

**[SPEC]**

All enhanced command components follow CVT's base lifecycle:

```text
EventExecuteAfterSpawnPawn
  → Bind_Options (subscribe to input, configure UI)
  → Execute (tool is active, processing input)
  → Disabled (tool deactivated, cleanup)

SaveGame hooks:
  → EventBindSaveState (serialize current state to BP_Data_SaveGame)
  → EventBindLoadState (deserialize state from BP_Data_SaveGame)
```

| Component | Extends | New Capabilities |
|-----------|---------|-----------------|
| BP_OrionMeasurement | BP_DimensionComponent | Multi-point polyline, angles, area, snap system, units toggle, save measurements |
| BP_OrionXray | BP_XrayComponent | Per-zone/per-equipment selective, color-coded overlays, opacity slider, layer toggle |
| BP_OrionExplode | BP_ExplodeComponent | 3-level hierarchical, building floor explode, callout labels, distance slider, assembly instruction mode |
| BP_OrionCropBox | BP_CropBoxComponent | UE5.8 gizmo, stencil-buffer section-fill, 2D section capture, plane vs cube toggle, multiple sections |
| BP_OrionSnapshot | BP_Snapshot | Dark theme restyle, output linked to telemetry directory |
| BP_OrionRatioScale | BP_Scale_Component | Dark theme restyle, spatial validation retained |
| BP_OrionDataSmith | BP_DataSmith_Component | Dark theme restyle, auto-tag runtime-loaded geometry via MetadataLinker |
| BP_OrionAnnotation | BP_AnnotationComponent | Category tags (safety/maintenance/design), category filter, export report |
| BP_OrionBookmark | BP_BookmarkComponent | Organize by category, share across sessions |

### 3.4 Actor Specifications

#### BP_SnapManager (Actor Component on Measurement Command)

**[SPEC]**

```text
Purpose: AutoCAD-style geometric snapping for measurement tool

Snap Types (priority order):

  1. Intersection (two edge crossings)
  2. Vertex (nearest mesh vertex within radius)
  3. Midpoint (midpoint of nearest edge)
  4. Center (bounding box center of component)
  5. Edge (closest point on nearest edge)
  6. Face (surface normal projection)

Algorithm per frame (cursor moved):

  1. Line trace from camera through cursor → HitResult on StaticMesh
  2. If snap enabled:

     a. Get hit actor's UStaticMeshComponent → UStaticMesh
     b. Read LOD0 vertex buffer (local space)
     c. Transform vertices to world space
     d. Find nearest vertex within snap radius (default: 5cm)
     e. If vertex found → snap to vertex
     f. Else → build edge list from index buffer
     g. Find closest point on nearest edge
     h. If within snap radius → check midpoint proximity (2.5cm inner)
     i. Apply snap with visual indicator

Visual Indicators (3D widget meshes):
  Diamond mesh → Vertex
  Circle mesh → Midpoint
  Square mesh → Center
  X mesh → Intersection
  All use emissive teal material (#00D4AA) with 1Hz pulse animation

Config:
  Snap radius: 5cm world (configurable in settings)
  Snap toggle: S key
  Performance: <16ms per frame (must not stall cursor movement)
```

#### BP_CameraSweepManager (Actor Component)

**[SPEC]**

```text
Purpose: Smooth camera interpolation between positions

Algorithm:

  1. Receive target transform (location + rotation)
  2. Calculate optimal viewing distance based on target actor bounds
  3. Plan path with collision avoidance:

     a. Sphere trace from current to target
     b. If blocked → add waypoint above obstruction

  4. Interpolate along path using cubic easing (ease-in-out)
  5. On arrival → fire OnSweepComplete delegate

Parameters:
  SweepSpeed: Fast (1s), Medium (2s), Slow (3s)
  MinViewDistance: 200 units
  MaxViewDistance: 2000 units
  CollisionAvoidanceRadius: 50 units

Delegates:
  OnSweepComplete(FName TargetID) → multicast
```

---

## 4. Data Architecture

### 4.1 Data Table Schemas

**[SPEC]**

#### DT_Equipment (Master Table — ~6500 rows for Orion Demo Client)

| Column | UE Type | Constraints | Example |
|--------|---------|-------------|---------|
| EquipmentID | FName | Primary key; matches actor tag | `Mixer_01` |
| DisplayName | FText | String Table ref | `Ribbon Mixer #1` |
| PIDTag | FString | P&ID tag format | `M-101` |
| ProcessLine | FString | FK → DT_ProcessLines | `PL-001` |
| BuildingID | FName | FK → DT_Buildings | `Building_A` |
| RoomID | FName | FK → DT_Rooms | `Room_101` |
| EquipmentType | EEquipmentType | Enum | `Mixer` |
| Manufacturer | FString | | `GEA Group` |
| Model | FString | | `tCut 200` |
| Specs | FString | JSON blob | `{"capacity_kg": 500}` |
| DrawingPaths | TArray\<FString\> | Relative content paths | `["/Game/Drawings/M101_GA.png"]` |
| AnimationClass | TSoftClassPtr | Nullable | `BP_MixerAnim` |
| HasExplode | bool | Default false | `true` |
| MaintenanceComponents | TArray\<FName\> | Component IDs | `["Motor_01", "Shaft_01"]` |
| ZoneID | FName | FK → DT_Zones | `Zone_101` |

#### DT_Buildings (~5-10 rows)

| Column | UE Type | Example |
|--------|---------|---------|
| BuildingID | FName | `Building_A` |
| DisplayName | FText | `Main Production Building` |
| Floors | int32 | `3` |
| LocationBounds | FBox | World space AABB |

#### DT_Rooms (~50-100 rows)

| Column | UE Type | Example |
|--------|---------|---------|
| RoomID | FName | `Room_101` |
| BuildingID | FName | `Building_A` |
| DisplayName | FText | `Mixing Hall` |
| Floor | int32 | `1` |
| Function | FString | `Raw material mixing` |
| SafetyZoneType | EZoneClassification | `Chemical` |
| SafetyZoneColor | FLinearColor | `(1.0, 0.8, 0.0, 0.5)` |

#### DT_ProcessLines (~500 rows)

| Column | UE Type | Example |
|--------|---------|---------|
| ProcessLineID | FString | `PL-001` |
| DisplayName | FText | `Raw Milk Reception` |
| ConnectedEquipment | TArray\<FName\> | `["Pump_01", "Tank_01", "Valve_01"]` |
| PIDDocPath | FString | `/Game/PIDs/PL001.pdf` |

#### DT_Zones (~20-50 rows)

| Column | UE Type | Example |
|--------|---------|---------|
| ZoneID | FName | `Zone_101` |
| BoundsOrigin | FVector | World space center |
| BoundsExtent | FVector | Half-extent |
| ActiveEquipment | TArray\<FName\> | Equipment activated in this zone |

#### DT_TourWaypoints (~10-30 rows per tour)

| Column | UE Type | Example |
|--------|---------|---------|
| WaypointID | FName | `Tour01_WP03` |
| TourName | FString | `Investor Tour` |
| Sequence | int32 | `3` |
| CameraTransform | FTransform | World space |
| InfoText | FText | `This is the main mixing hall...` |
| VOPath | FSoftObjectPath | `/Game/Audio/Tour01_WP03.wav` |

#### DT_NPCs (~10-30 rows)

| Column | UE Type | Example |
|--------|---------|---------|
| NPCID | FName | `Worker_01` |
| NPCType | ENPCType | `AmbientWorker` |
| ZoneID | FName | `Zone_101` |
| AnimationSet | FName | `CheckingGauges` |
| PatrolPath | FSoftObjectPath | `/Game/Splines/Patrol_01` |

#### DT_InspectionSteps (~8 rows per equipment × ~8 equipment)

| Column | UE Type | Example |
|--------|---------|---------|
| StepID | FName | `Mixer01_Step1` |
| EquipmentID | FName | `Mixer_01` |
| Sequence | int32 | `1` |
| Description | FText | `Check motor coupling alignment` |
| ExpectedCondition | FText | `No visible wear or offset` |
| CameraTransform | FTransform | Inspection viewpoint |
| PhotoRefPath | FString | `/Game/InspectionPhotos/M101_Step1.png` |

---

## 5. UI Architecture

### 5.1 Widget Hierarchy

**[SPEC]**

```text
WBP_OrionRoot (UUserWidget — viewport root, always active, Z-Order 0)
│
├── WBP_TopBar (UUserWidget — horizontal bar, top edge)
│   ├── IMG_ClientLogo (UImage — loaded from OrionConfig.json logo_path)
│   ├── TXT_PlantName (UTextBlock — from config)
│   ├── TXT_ModeIndicator (UTextBlock — "SHOWCASE" / "OPERATIONS")
│   ├── BTN_Settings (UButton → opens WBP_ModalOverlay)
│   └── TXT_UserRole (UTextBlock — current role)
│
├── WBP_SidePanel (UUserWidget — collapsible left panel, 320px width)
│   ├── WBP_SearchBar (UUserWidget)
│   │   ├── EDT_SearchInput (UEditableTextBox)
│   │   └── LST_SearchResults (UListView — virtualized)
│   ├── WBP_TreeBrowser (UUserWidget)
│   │   └── LST_TreeView (UListView — virtualized, 6500+ entries)
│   └── WBP_EquipmentDetails (UUserWidget — slides in from right)
│       ├── TAB_Overview / TAB_Components / TAB_Actions / TAB_Drawings / TAB_Data
│       └── Content panels per tab
│
├── WBP_BottomBar (UUserWidget — horizontal bar, bottom edge)
│   ├── WBP_ToolPalette (tool icons — context-sensitive per mode)
│   ├── TXT_MeasurementReadout (live measurement display)
│   ├── BTN_MinimapToggle (toggles minimap visibility)
│   └── TXT_SnapStatus (shows "SNAP: ON/OFF")
│
├── WBP_Minimap (UUserWidget — corner overlay, toggleable)
│   ├── IMG_MinimapRT (UImage — bound to render target)
│   ├── IMG_PlayerArrow (UImage — rotates with player heading)
│   ├── WBP_FloorSelector (tab buttons: F1, F2, F3...)
│   └── Click input handler → teleport pipeline
│
├── WBP_ToolRadialMenu (UUserWidget — quick-access wheel, Z-Order 5)
│
├── WBP_Notification (UUserWidget — toast stack, Z-Order 10)
│
├── WBP_DebugOverlay (UUserWidget — dev-only, Z-Order 15)
│   ├── TXT_FPS, TXT_DrawCalls, TXT_Mode, TXT_PawnType
│   └── TXT_HoverEquipmentID (visible on mouse hover in debug mode)
│
└── WBP_ModalOverlay (UUserWidget — full-screen dimmed overlay, Z-Order 20)
    ├── WBP_SettingsPanel
    ├── WBP_ConfirmDialog
    └── WBP_ErrorReport
```

### 5.2 Widget Performance Requirements

**[SPEC]**

| Widget | Technique | Target |
|--------|-----------|--------|
| WBP_TreeBrowser | UListView (virtualized) — only renders visible entries + 5 buffer | 60fps scroll at 6500 entries |
| WBP_SearchResults | UListView (virtualized) — max 50 results displayed | <200ms from keystroke to results |
| WBP_Minimap | Render target throttled to 10fps | <0.5ms GPU per frame |
| WBP_EquipmentDetails | Lazy tab loading — only active tab populates | <100ms tab switch |
| All panels | Slide-in/fade animations at 0.3s ease-out | 60fps during animation |

### 5.3 Hierarchical Tree Browser Specification

**[SPEC]**

The `WBP_TreeBrowser` is a collapsible, virtualized sidebar menu displaying the plant hierarchy: `Buildings` > `Rooms` > `Equipment` > `Components`.

1. **Virtualized List Container:**
   - Must use `UListView` (`LST_TreeView`) to support 6,500+ items at 60fps.
   - List data objects must be instances of `UOrionTreeItemData` (UObject).

2. **Row Widget: `WBP_TreeItemRow`:**
   - Inherits `IUserObjectListEntry` interface.
   - Indentation: spacer width dynamically set to `Depth * 16.0`.
   - Toggle Expand/Collapse: button visible only for nodes with children (non-components).
   - Selection: Clicking a row highlights the row (accent `#00D4AA` background) and triggers camera sweep and highlight on the target actor in the viewport.

3. **Flat-List Assembly Algorithm:**
   - **Initial Population:** Query buildings from `BP_HierarchyManager`, instantiate `UOrionTreeItemData` at depth 0, and call `ListView->SetListItems`.
   - **Node Expanded:** Click arrow -> `bIsExpanded = true`, retrieve children, insert them in the flat array directly after the parent's index, and refresh.
   - **Node Collapsed:** Click arrow -> `bIsExpanded = false`, traverse forward from parent index, remove all consecutive elements with `Depth > ParentDepth`, and refresh.

---

## 6. Inter-System Communication

### 6.1 Event Flow Diagram

**[SPEC]**

```text
OnModeChanged (BP_OrionModeManager)
├── → WBP_OrionRoot: Reconfigure panel visibility, toolbar buttons
├── → Command Components: Enable/disable per mode (Xray, Explode, etc.)
├── → BP_NPCManager: Start/stop NPC zone animations
├── → BP_ZoneAnimationManager: Activate/deactivate zone triggers
├── → BP_TelemetryManager: Log mode transition event
└── → CVT SessionManager: Broadcast mode change to all network clients

OnEquipmentSelected (BP_HierarchyManager)
├── → BP_CameraSweepManager: Sweep to equipment location
├── → WBP_EquipmentDetails: Populate tabs with DT_Equipment data
├── → WBP_TreeBrowser: Highlight selected node, expand ancestors
├── → BP_ZoneAnimationManager: Activate equipment's zone
├── → BP_TelemetryManager: Log equipment view event
└── → CVT SessionManager: Broadcast selection to peers

OnZoneEntered (BP_ZoneAnimationManager)
├── → Equipment animations: Play zone equipment animations
├── → BP_NPCManager: Activate zone NPCs
├── → WBP_Minimap: Highlight active zone
├── → Post-process: Apply zone-specific PP override
└── → BP_TelemetryManager: Log zone entry

OnConfigReloaded (BP_ConfigLoader) — dev builds only
├── → WBP_OrionRoot: Update accent colors, logos, branding
├── → BP_OrionModeManager: Update mode availability
└── → Feature systems: Enable/disable per feature flags

OnMatchingComplete (BP_MetadataLinker)
├── → BP_HierarchyManager: Populate WorldActor references
├── → WBP_TreeBrowser: Enable navigation (was disabled during matching)
└── → WBP_Notification: Show match report toast
```

### 6.2 Delegate Binding Pattern

**[SPEC]**

All inter-system communication uses UE5 multicast delegates (not direct function calls):

```cpp
// Declaration (in BP_OrionModeManager)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(
    FOnModeChanged, EOrionMode, OldMode, EOrionMode, NewMode);

UPROPERTY(BlueprintAssignable) FOnModeChanged OnModeChanged;

// Subscription (in any system's BeginPlay)
ModeManager->OnModeChanged.AddDynamic(this, &UMySystem::HandleModeChanged);

// Firing (when mode changes)
OnModeChanged.Broadcast(OldMode, NewMode);
```

---

## 7. Networking & Replication

**[SPEC]**

- All networking extends CVT's existing session infrastructure
- **No custom networking code** is written; Orion uses CVT's replication framework
- Mode state is replicated via a `UPROPERTY(Replicated)` on the Game State (CVT pattern)
- Command component state replicates automatically because they inherit from BP_BaseCommandComponent which already handles this
- Session recording is **local only** — not replicated; the host records, clients do not

**[NOTE]**
CVT uses a listen-server model. One player hosts; others join. The host's `BP_OrionModeManager` is authoritative. Mode changes are RPCed to the host, which validates and broadcasts.

---

## 8. SaveGame Integration

**[SPEC]**

| Saveable State | Storage Location | Method |
|---------------|-----------------|--------|
| Bookmarks + categories | BP_BookmarkComponent SaveGame data | Extends EventBindSaveState |
| Measurements + labels | BP_DimensionComponent SaveGame data | Extends EventBindSaveState |
| Annotations + categories | BP_AnnotationComponent SaveGame data | Extends EventBindSaveState |
| Xray state | BP_XrayComponent SaveGame data | Extends EventBindSaveState |
| CropBox positions | BP_CropBoxComponent SaveGame data | Extends EventBindSaveState |
| Inspection progress | BP_Data_SaveGame custom field | New: TMap\<FName, TArray\<bool\>\> |
| Mode + selected equipment | BP_Data_SaveGame custom field | New: EOrionMode + FName |
| Session recording data | Separate file | New: Saved/SessionRecordings/*.json |

---

## 9. Performance Budgets

### 9.1 Frame Budget (16.67ms @ 60fps)

**[SPEC]**

| System | Budget | Notes |
|--------|--------|-------|
| Rendering (GPU) | 10ms | Lumen GI, post-process, mesh rendering |
| UI (UMG) | 1ms | Virtualized lists, minimal overdraw |
| Game Logic | 2ms | Mode manager, hierarchy queries, zone checks |
| Physics/Collision | 1ms | Minimal — mostly line traces for measurement |
| Animation | 1ms | Max 3 active zones, LOD-based animation |
| Networking | 0.5ms | CVT session sync |
| Buffer | 1.17ms | Headroom for spikes |

### 9.2 Memory Budget (Desktop)

**[SPEC]**

| Category | Budget | Notes |
|----------|--------|-------|
| Scene meshes | 2-4 GB | LODs reduce distant mesh memory |
| Textures | 1-2 GB | Virtual textures where supported |
| Data Tables (all) | <50 MB | 6500 rows × ~2KB per row |
| UI widgets | <100 MB | Virtualized lists minimize widget count |
| Render targets | <32 MB | Minimap 512×512 + CropBox section 2048×2048 |
| Audio | <200 MB | Tour VO + ambient + interaction sounds |

### 9.3 Render Target Specifications

**[SPEC]**

| Target | Resolution (Desktop) | Resolution (VR) | Update Rate |
|--------|---------------------|------------------|-------------|
| Minimap | 512×512 | 256×256 | 10fps (throttled) |
| Section Capture | 2048×2048 | 1024×1024 | On-demand only |
| Snapshot | Viewport resolution | Viewport resolution | On-demand |

---

## 10. Config System

### 10.1 OrionConfig.json Schema

**[SPEC]**

```json
{
  "$schema": "OrionConfig/v1",
  "client": {
    "company_name": "string (required)",
    "plant_name": "string (required)",
    "logo_path": "string (content-relative path, validated)",
    "accent_color": "string (hex color, validated: #RRGGBB)"
  },
  "modes": {
    "showcase": "bool (default: true)",
    "training": "bool (default: false)",
    "operations": "bool (default: true)"
  },
  "features": {
    "minimap": "bool (default: true)",
    "guided_tour": "bool (default: true)",
    "npc_workers": "bool (default: true)",
    "session_recording": "bool (default: false)",
    "simulation_data": "bool (default: false)"
  },
  "optimization": {
    "lumen_enabled": "bool (default: true)",
    "vr_mode": "string (enum: pc_tethered | disabled)",
    "target_fps_desktop": "int (default: 60)",
    "target_fps_vr": "int (default: 72)"
  },
  "save_game": {
    "save_file_prefix": "string (default: Orion)",
    "auto_save_interval_seconds": "int (default: 300)"
  }
}
```

### 10.2 Validation Rules

**[SPEC]**

| Field | Validation | On Failure |
|-------|-----------|------------|
| company_name | Non-empty string | Use "Orion Studios" default |
| logo_path | File exists at path | Use embedded Orion logo |
| accent_color | Regex: `^#[0-9A-Fa-f]{6}$` | Use default `#00D4AA` |
| modes.\* | Boolean | Default to true/false per field |
| target_fps_\* | Integer 30-144 | Clamp to range |
| Entire file | Valid JSON | Use full embedded defaults; show warning banner |

### 10.3 Hot-Reload (Dev Builds Only)

**[SPEC]**

```text

1. BP_ConfigLoader registers a file watcher on OrionConfig.json path
2. On file change detected → re-parse JSON
3. Validate against schema
4. Fire OnConfigReloaded multicast delegate
5. All subscribed systems update without app restart
6. Shipping builds: hot-reload disabled (FPlatformFileManager watcher not created)

```

---

## 11. Build & Deployment

### 11.1 Build Configurations

**[SPEC]**

| Configuration | Use | Defines |
|--------------|-----|---------|
| DebugGame | Development | `WITH_ORION_DEBUG=1`, hot-reload, debug overlay |
| Development | Internal testing | `WITH_ORION_DEBUG=1`, some debug features |
| Shipping | Client delivery | No debug overlay, no hot-reload, no console commands |

### 11.2 Platform-Specific Settings

**[SPEC]**

| Setting | Desktop | VR |
|---------|---------|-----|
| Rendering | Lumen GI | Lumen simplified or fully baked |
| Post-process | Full (bloom, DOF, chromatic aberration) | Reduced (bloom only) |
| Target FPS | 60 | 72 |
| Minimap RT | 512×512 | 256×256 |
| Animation LOD | Full quality all active zones | Reduced quality, max 2 active zones |
| Input | Keyboard + Mouse | Motion controllers + head tracking |

---

## 12. Error Handling & Graceful Degradation

**[SPEC]**

| Failure | Detection | Response | User Feedback |
|---------|-----------|----------|---------------|
| Config missing | FileExists check at startup | Load embedded defaults | Persistent warning banner |
| Config malformed | JSON parse error | Load defaults for invalid fields | Toast notification listing failed fields |
| MetadataLinker <90% match | Match report count check | Allow manual linking | Editor Utility Widget report |
| Data Table import error | CreateTableFromJSONString error array | Continue with partial data | Error toast; unmatched equipment hidden |
| VR headset disconnected | OpenXR session lost event | Auto-switch to desktop pawn | Reconnection prompt dialog |
| Multi-user desync | Heartbeat timeout (5s) | Auto-resync from host state | If resync fails → rejoin prompt |
| Asset path not found | FSoftObjectPath resolve failure | Use placeholder asset | Log warning |
| Search returns empty | Result count == 0 | Show "No results" with suggestions | Alternative query hints |
| Out of memory | Platform memory warning | Reduce quality settings | Quality reduction toast |

---

## 13. Security Considerations

**[SPEC]**

- No user authentication system (roles selected at launcher, not authenticated)
- No network traffic leaves the local network (CVT session is LAN/direct IP)
- OrionConfig.json is trusted (no untrusted user input)
- Telemetry logs contain no PII (only interaction events with timestamps)
- P&ID documents launched via OS (no in-app rendering of potentially sensitive PDFs)
- Session recordings stored locally only (not uploaded)

**[NOTE]**
If cloud features are added in v2, security requirements will need a full review including auth, TLS, and data classification.

---

## 🔗 Correlation Map
- **Dashboard:** [Home](../Home.md)
- **Governing Specifications:** [PRD](prd.md) · [TRD](trd.md)
- **Implementation & Tasks:** [Plan](../.notes/decisions/implementation_plan.md) · [Tasks](../.notes/logs/task.md) · [Walkthrough](../.notes/logs/walkthrough.md) · [Session Log](../.notes/logs/session_log.md)
- **Active Agent System:** [Rules](../.agents/rules/agents.md)


---
## 🔗 Correlation Map
- **Dashboard:** [Home](../Home.md)
- **Governing Specifications:** [PRD](prd.md) · [TRD](trd.md)
- **Implementation & Tasks:** [Plan](../.notes/decisions/implementation_plan.md) · [Tasks](../.notes/logs/task.md) · [Walkthrough](../.notes/logs/walkthrough.md) · [Session Log](../.notes/logs/session_log.md)
- **Active Agent System:** [Rules](../.agents/rules/agents.md)
