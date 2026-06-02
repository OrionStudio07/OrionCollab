# Orion Studios — Comprehensive Features Reference
**Source:** `prd.md v1.0.0`, `trd.md v1.0.0`, `backend_schema.md v1.0.0`, `flow_diagrams.md v1.0.0`, `implementation_plan.md`
**Compiled:** 2026-06-02

> [!IMPORTANT]
> Every item in this document is cited directly from a governing specification. No content has been inferred or invented. Section references appear after each claim.

---

## Table of Contents

1. [Problem Statement & Solution](#1-problem-statement--solution)
2. [Actors & Personas](#2-actors--personas)
3. [User Stories (All 70)](#3-user-stories-all-70)
4. [System Architecture](#4-system-architecture)
5. [Module Specifications](#5-module-specifications)
6. [Data Architecture](#6-data-architecture)
7. [UI Architecture](#7-ui-architecture)
8. [Canonical System Flows](#8-canonical-system-flows)
9. [Config System](#9-config-system)
10. [Performance Budgets](#10-performance-budgets)
11. [Error Handling Matrix](#11-error-handling-matrix)
12. [Build & Deployment](#12-build--deployment)
13. [Acceptance Criteria (Release Gate)](#13-acceptance-criteria-release-gate)
14. [Out of Scope (v1)](#14-out-of-scope-v1)
15. [Resolved Questions](#15-resolved-questions)

---

## 1. Problem Statement & Solution

**Problem** `[prd.md §Problem Statement]`

Industrial plants (food processing, chemical, manufacturing) need a way to showcase their facilities to investors, onboard employees, and support engineering inspections — without requiring physical access. Current solutions are:

- **Static renders/videos:** Non-interactive; can't answer investor questions on-the-fly.
- **Generic VR walkthroughs:** Lack engineering data integration (P&ID, specs, process lines).
- **CAD viewers (Navisworks, BIM360):** Powerful but ugly, slow, and intimidating for non-technical stakeholders.

**Solution** `[prd.md §Solution]`

**Orion Studios** is a reusable Unreal Engine 5.8 application built on the CollabViewer Template (CVT) that transforms AutoCAD Plant 3D exports into an interactive, photorealistic industrial visualization platform.

Key differentiators `[prd.md §Solution]`:

- **Dual-import pipeline:** Geometry from 3ds Max + metadata from Plant 3D Python script, auto-matched by tag.
- **Mode-based access:** Role-based launcher routes users to Showcase (investors), Operations (engineers), or Training (v2).
- **Client-swappable:** Per-client JSON config changes branding, features, and plant data without touching platform code.
- **Multi-user collaboration:** Built-in collaborative sessions with role-based permissions and session recording.
- **Desktop + PC VR:** Single codebase targets both desktop and tethered VR experiences.

**Reference client:** Morde Foods P2 Manufacturing Plant — 6500 tags, 1394 instrumentation points, ~500 process lines, ~200 unique equipment. `[trd.md §1]`

---

## 2. Actors & Personas

`[prd.md §Actors & Personas]`

| Actor | Description | Primary Mode | Technical Level |
|-------|-------------|-------------|-----------------|
| **Visitor / Investor** | Non-technical stakeholders touring the plant for due diligence or sales | Mode A — Showcase | None |
| **Plant Engineer** | Operations/maintenance engineers inspecting equipment and accessing P&ID docs | Mode C — Operations | High |
| **Trainee / Employee** | New hires completing onboarding and safety training | Mode B — Training (v2) | Low-Medium |
| **Session Admin** | IT/management controlling multi-user sessions and roles | Launcher + All Modes | Medium |
| **Content Author** | Developers setting up new client plant scenes in UE5 Editor | Editor Only | Expert |

---

## 3. User Stories (All 70)

### 3.1 Launcher & Configuration `[prd.md §Launcher & Configuration]`

| # | Actor | Story |
|---|-------|-------|
| US-01 | Visitor | See the client's branded logo and plant name on launch, so I know I'm in the right application. |
| US-02 | Session Admin | Select my role from a picker, so I get the correct mode and permissions. |
| US-03 | Session Admin | Configure graphics quality and VR toggle from the settings panel, so performance matches my hardware. |
| US-04 | Engineer | Switch between Showcase and Operations mode in-app, so I can give a tour then dive into specs without restarting. |
| US-05 | Content Author | Edit `OrionConfig.json` and see changes hot-reload in-editor, so I can iterate on client branding without rebuilding. |
| US-06 | Content Author | App shows a warning banner if the config file is missing, so I know to fix it before a demo. |

### 3.2 Navigation — All Modes `[prd.md §Navigation (All Modes)]`

| # | Actor | Story |
|---|-------|-------|
| US-07 | Visitor | Browse a collapsible tree of Buildings > Rooms > Equipment, so I can understand the plant's spatial organization. |
| US-08 | Visitor | Click any tree node and have the camera sweep smoothly to that location, so navigation feels premium. |
| US-09 | Engineer | Type a P&ID tag (e.g., `P-101`) into a search bar and teleport directly to that equipment, so I save time finding specific units. |
| US-10 | Visitor | Search results grouped by category (Building, Room, Equipment, Process Line) with icons, so I can distinguish between result types. |
| US-11 | Engineer | Click any point on a 2D minimap and teleport there, so I can navigate large plants efficiently. |
| US-12 | Visitor | Minimap shows my current position and heading as a rotating arrow, so I stay oriented. |
| US-13 | Visitor | Floor selector tabs (F1, F2, F3) on the minimap, so I can switch between floors in multi-story buildings. |
| US-14 | Visitor | Use FlyMode (free aerial camera) to get overhead perspectives, so I can see the plant layout from above. |
| US-15 | Visitor | A bottom carousel of key equipment thumbnails that I can click to teleport sequentially, so I can follow the process flow. |
| US-16 | Engineer | Search matches fuzzy queries across equipment names, tags, and process line codes, so typos don't block me. |
| US-17 | Visitor | Recent searches saved for quick re-access, so I don't retype commonly-visited equipment. |

### 3.3 Mode A — Showcase `[prd.md §Mode A — Showcase]`

| # | Actor | Story |
|---|-------|-------|
| US-18 | Visitor | A guided tour that automatically moves the camera along a scripted path with info panels at each stop, so I get a hands-free overview. |
| US-19 | Visitor | Play/Pause/Next/Previous controls during the guided tour, so I can control the pace. |
| US-20 | Visitor | A progress bar showing my position in the tour, so I know how much is left. |
| US-21 | Visitor | See NPC workers performing tasks in each zone, so the plant feels alive and realistic. |
| US-22 | Visitor | Doors open automatically as I approach, so the experience feels immersive. |
| US-23 | Visitor | See conveyor belts and mixers running with animations, so I understand the production flow. |
| US-24 | Visitor | Zone-based animation activation (only the current zone's equipment animates), so performance stays smooth. |
| US-25 | Visitor | Premium Lumen lighting with HDRI sky and post-process effects, so the plant looks photorealistic. |
| US-26 | Engineer | Toggle Global Xray to see all pipes, ducts, and structural elements through walls, so I understand hidden routing. |
| US-27 | Engineer | Per-equipment Xray that only affects the selected unit, so context is preserved. |
| US-28 | Engineer | Xray materials color-coded by system type (pipes=blue, structure=white, electrical=yellow), so I can distinguish systems at a glance. |
| US-29 | Engineer | Place a section cut plane through any point in the plant, so I can see cross-sections of equipment and rooms. |
| US-30 | Engineer | Section-fill hatching on cut faces (engineering-style diagonal lines), so sections look professional. |
| US-31 | Engineer | Export a 2D section capture as PNG, so I can include it in reports. |
| US-32 | Engineer | Hierarchical explode (Level 1: assemblies, Level 2: sub-components, Level 3: individual parts), so I can understand equipment construction. |
| US-33 | Engineer | Building floor explode (floors separate vertically), so I can see multi-story layouts. |
| US-34 | Engineer | Floating callout labels on each exploded component, so I can identify parts. |
| US-35 | Engineer | A distance slider to continuously control explosion distance, so I can find the right separation. |
| US-36 | Engineer | Measure multi-point polyline distances with segment lengths, total length, and angles, so I can do field verification. |
| US-37 | Engineer | AutoCAD-style snapping (vertex, edge, midpoint, center), so measurements are precise. |
| US-38 | Engineer | Toggle measurement units between Meters, Feet, and Millimeters, so I work in familiar units. |
| US-39 | Engineer | Save labeled measurements for later reference, so I can compare over time. |
| US-40 | Visitor | Take a Snapshot of the current view and save it with a timestamp, so I can document the tour. |

### 3.4 Mode C — Operations `[prd.md §Mode C — Operations]`

| # | Actor | Story |
|---|-------|-------|
| US-41 | Engineer | Click any equipment and see a tabbed details panel (Overview, Components, Actions, Drawings, Data), so all information is in one place. |
| US-42 | Engineer | Overview tab shows name, P&ID tag, process line, manufacturer, model, and key specs, so I have quick identification. |
| US-43 | Engineer | Components tab shows hierarchical parts tree with replacement intervals and materials, so I can plan maintenance. |
| US-44 | Engineer | Actions tab has buttons for Explode, Isolate, Xray, Animate, and Inspect, so I can interact with the equipment in context. |
| US-45 | Engineer | 2D CAD drawing viewer (pan/zoom/fullscreen) in the Drawings tab, so I can reference technical drawings without leaving the app. |
| US-46 | Engineer | Launch a step-by-step inspection walkthrough (up to 8 steps per equipment) from the Actions tab, so I can follow a checklist. |
| US-47 | Engineer | Each inspection step shows a description, expected condition, and photo reference while highlighting the target component, so I know exactly what to check. |
| US-48 | Engineer | Maintenance overlay callouts showing part name, last maintenance date, interval, and status (OK/Due/Overdue), so I can prioritize work. |
| US-49 | Engineer | Click a P&ID hotspot in 3D space and have it open the P&ID PDF document in my OS viewer, so I can cross-reference. |
| US-50 | Engineer | Select a process line tag and see the entire pipe path highlighted with pulsing flow animation, so I can trace the process. |
| US-51 | Engineer | Annotations with category tags (safety, maintenance, design review), so notes are organized. |
| US-52 | Engineer | Filter annotations by category, so I only see relevant notes. |

### 3.5 Multi-User & Session `[prd.md §Multi-User & Session]`

| # | Actor | Story |
|---|-------|-------|
| US-53 | Session Admin | Role-based permissions (Admin, Engineer, Viewer) so visitors can't modify annotations. |
| US-54 | Session Admin | Synchronized mode state, so all participants see the same mode when I switch. |
| US-55 | Session Admin | Record camera paths and interactions for playback, so I can review sessions offline. |
| US-56 | Session Admin | Replay recorded sessions with a timeline scrubber, so I can jump to key moments. |
| US-57 | Session Admin | Export/import session recordings as files, so I can share them. |

### 3.6 VR `[prd.md §VR]`

| # | Actor | Story |
|---|-------|-------|
| US-58 | Visitor in VR | Same tour, navigation, and visualization features at 72fps minimum, so the experience is comfortable. |
| US-59 | Engineer in VR | Interact with equipment, open details panels, and use tools, so VR is a full-featured experience. |

### 3.7 Content Authoring — Editor Only `[prd.md §Content Authoring]`

| # | Actor | Story |
|---|-------|-------|
| US-60 | Content Author | Equipment Tagger widget to batch-assign IDs and zones to selected actors, so scene setup is fast. |
| US-61 | Content Author | Zone Painter widget to draw trigger volumes with visual feedback, so zones are easy to configure. |
| US-62 | Content Author | Tour Path Editor to click waypoints in the viewport and auto-generate DT_TourWaypoints rows, so tour creation is visual. |
| US-63 | Content Author | A Validation Pass that checks for unmatched actors, missing textures, and broken references, so I catch errors before shipping. |
| US-64 | Content Author | A Config Generator widget to fill in client details and export a validated OrionConfig.json, so config creation is error-free. |

### 3.8 Analytics & Telemetry `[prd.md §Analytics & Telemetry]`

| # | Actor | Story |
|---|-------|-------|
| US-65 | Session Admin | Local JSON logs of mode transitions, equipment views, tool usage, and tour completions, so I can demonstrate engagement to clients. |
| US-66 | Session Admin | Telemetry output in a format compatible with future cloud upload, so we can add cloud analytics later. |

### 3.9 Accessibility `[prd.md §Accessibility]`

| # | Actor | Story |
|---|-------|-------|
| US-67 | Visitor | Three text size presets (Standard, Medium, Large), so I can read UI text comfortably. |
| US-68 | Visitor | A high-contrast mode toggle, so panel borders and text are easier to read in bright rooms. |
| US-69 | Engineer | Status indicators use shapes and pulse animations (not just color), so colorblind users can distinguish states. |
| US-70 | Visitor | Full keyboard navigation across all UI panels, so I can navigate without a mouse. |

---

## 4. System Architecture

`[prd.md §Architecture]`, `[trd.md §1]`, `[trd.md §2]`

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Engine | Unreal Engine | 5.8 | Runtime, editor, packaging |
| Template | CollabViewer Template (CVT) | UE5.8 bundled | Multi-user, tools, pawn hierarchy |
| Rendering | Lumen (desktop) / Baked (VR) | Native | GI, reflections |
| UI | UMG (Unreal Motion Graphics) | Native | All in-game UI widgets |
| Data | UE5 Data Tables + JSON config | Native | Equipment metadata, tour waypoints, NPC definitions |
| Networking | CVT session system | Native | Multi-user collaboration |
| VR | OpenXR via SteamVR / Meta Quest Link | Native | PC tethered VR |
| Localization | FText + String Tables | Native | Localization-ready text |
| Build | UnrealBuildTool | Native | Compilation, cooking, packaging |
| CAD Pipeline | Datasmith (3ds Max exporter) | UE5.8 bundled | Geometry import |
| Metadata Pipeline | Python 3.x (Plant 3D script) | External | Tag/metadata export |

**Language:** Blueprint primary (all gameplay logic); C++ for performance-critical subsystems (HierarchyManager search, SnapManager vertex queries). `[trd.md §1]`

**Build Targets:** Windows Desktop (.exe) + PC VR (Meta Quest Link / SteamVR). `[trd.md §1]`

### 4.1 Module Classification `[trd.md §3.1]`

| Type | UE5 Class | Lifecycle | Examples |
|------|-----------|-----------|---------|
| **World Subsystem** | `UWorldSubsystem` | Created per-world; destroyed on level unload | ModeManager, HierarchyManager, MetadataLinker, TelemetryManager |
| **Command Component** | `BP_BaseCommandComponent` child | Created by pawn on spawn; follows CVT lifecycle; participates in SaveGame | Enhanced Xray, Explode, CropBox, Measurement, Snapshot, RatioScale, DataSmith, Annotation, Bookmark |
| **Actor** | `AActor` | Placed in level or spawned at runtime | TourManager, InspectionManager, NPCManager, ZoneAnimationManager, InteractiveObjects |
| **Game Instance** | `UGameInstance` child | Persists across level loads | ConfigLoader |

### 4.2 Pawn Architecture `[prd.md §Pawn Architecture]`

| Mode | Pawn |
|------|------|
| `MODE_LAUNCHER` | `BP_LoginMenuPawn` |
| `MODE_SHOWCASE` | OrbitMode (default), switchable to WalkMode/FlyMode |
| `MODE_OPERATIONS` | WalkMode (default), switchable to OrbitMode/FlyMode |
| VR toggle | `BP_VRPawn` (any mode) |

> **Note:** No new Drone pawn. FlyMode pawn extended with spline movement overlay. `[prd.md §Pawn Architecture]`

### 4.3 Content Pipeline `[prd.md §Content Pipeline]`, `[implementation_plan.md §1.3]`

| Pipeline | Steps |
|----------|-------|
| **A — Geometry** | AutoCAD Plant 3D → 3ds Max (QA cleanup) → Datasmith → UE5 |
| **B — Metadata** | AutoCAD Plant 3D → Python export script → JSON → Data Tables |
| **C — Matching** | `BP_MetadataLinker` auto-matches imported actors to Data Table rows by name/ID pattern |

---

## 5. Module Specifications

### 5.1 BP_OrionModeManager (World Subsystem) `[trd.md §3.2]`

**Purpose:** Global mode state management. Created when main level loads; destroyed on level unload.

**Enum `EOrionMode`** `[backend_schema.md §1]`:
| Value | Int | Display Name |
|-------|-----|-------------|
| `MODE_LAUNCHER` | 0 | Launcher |
| `MODE_SHOWCASE` | 1 | Showcase |
| `MODE_OPERATIONS` | 2 | Operations |
| `MODE_TRAINING` | 3 | Training (v2) — Reserved |

**API:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `SetMode` | `SetMode(EOrionMode NewMode) → void` | Validates permission, updates state, fires `OnModeChanged`, broadcasts to all network clients via GameState |
| `GetCurrentMode` | `GetCurrentMode() → EOrionMode` | Returns active mode |
| `CanAccessMode` | `CanAccessMode(EOrionMode Mode, EOrionRole Role) → bool` | Admin: all modes; Engineer: SHOWCASE + OPERATIONS; Viewer: SHOWCASE only |

**Delegates:**

- `OnModeChanged(EOrionMode OldMode, EOrionMode NewMode)` — multicast

---

### 5.2 BP_HierarchyManager (World Subsystem) `[trd.md §3.2]`

**Purpose:** Equipment hierarchy tree and search. Builds tree on level load from Data Tables.

**Data Structures:**

- `TMap<FName, FBuildingNode> BuildingMap`
- `FBuildingNode` → `FName BuildingID`, `FText DisplayName`, `TArray<FRoomNode> Rooms`
- `FRoomNode` → `FName RoomID`, `FText DisplayName`, `EZoneClassification SafetyZone`, `TArray<FEquipmentNode> Equipment`
- `FEquipmentNode` → `FName EquipmentID`, `FText DisplayName`, `FString PIDTag`, `FString ProcessLine`, `EEquipmentType Type`, `TWeakObjectPtr<AActor> WorldActor`, `TArray<FName> ComponentIDs`

**API:**
| Method | Returns | Notes |
|--------|---------|-------|
| `BuildTree()` | void | Called on BeginPlay; runs on background thread |
| `GetBuildingList()` | `TArray<FBuildingNode>` | |
| `GetRoomsByBuilding(FName BuildingID)` | `TArray<FRoomNode>` | |
| `GetEquipmentByRoom(FName RoomID)` | `TArray<FEquipmentNode>` | |
| `GetComponentsByEquipment(FName EquipmentID)` | `TArray<FName>` | Lazy-loaded on expand |
| `SearchAll(FString Query)` | `TArray<FSearchResult>` | Fuzzy match |
| `GetEquipmentActor(FName EquipmentID)` | `AActor*` | |

**Search Implementation:**

- Indexed fields: `DisplayName`, `PIDTag`, `ProcessLine`, `RoomName`, `BuildingName`
- Matching: case-insensitive substring + Levenshtein distance for fuzzy
- Cache: `TMap<FString, TArray<FSearchResult>>` for repeat queries
- **Performance target: <200ms for any query across 6500 entries**

**Delegates:**

- `OnEquipmentSelected(FName EquipmentID)` — multicast
- `OnTreeReady()` — multicast (fired when background build completes)

---

### 5.3 BP_MetadataLinker (World Subsystem) `[trd.md §3.2]`

**Purpose:** Auto-match Datasmith-imported actors to Data Table rows. Runs once on level load after Data Tables are populated.

**Matching Algorithm:**

1. Scan all actors with "Datasmith" tag
2. Extract candidate name (actor label / component name)
3. Normalize: strip prefixes (`SM_`, `BP_`), convert to lowercase
4. Match against `DT_Equipment.EquipmentID`:
   - Exact match → HIGH confidence
   - Contains match → MEDIUM confidence
   - Levenshtein distance ≤ 3 → LOW confidence (flagged as "ambiguous")
5. Tag matched actors with EquipmentID as actor tag
6. Store results in `TMap<FName, TWeakObjectPtr<AActor>>`
7. Generate report: `{matched: N, unmatched: N, ambiguous: N}`

**API:**
| Method | Returns |
|--------|---------|
| `GetMetadataLinkerSubsystem(const UObject* WorldContextObject)` | `UOrionMetadataLinker*` |
| `RunMatching()` | `FMatchReport` |
| `GetActorForEquipment(FName EquipmentID)` | `AActor*` |
| `GetUnmatchedActors()` | `TArray<AActor*>` |
| `ManualLink(AActor* Actor, FName EquipmentID)` | void |

**Delegates:**

- `OnMatchingComplete(FMatchReport Report)` — multicast

---

### 5.4 BP_TelemetryManager (World Subsystem) `[trd.md §3.2]`

**Purpose:** Local analytics logging.
**Output file:** `Saved/Logs/Telemetry/YYYY-MM-DD_session.json`

**Events Logged:**
| Event | Fields |
|-------|--------|
| `ModeTransition` | `{timestamp, from_mode, to_mode}` |
| `EquipmentView` | `{timestamp, equipment_id, duration_seconds}` |
| `ToolUsage` | `{timestamp, tool_name, action}` |
| `TourCompletion` | `{timestamp, tour_name, completion_percent}` |
| `SnapshotCapture` | `{timestamp, filename}` |
| `SessionDuration` | `{start_time, end_time, total_seconds}` |

Privacy: No PII collected. Format: JSON array, compatible with future cloud upload.

---

### 5.5 Command Components `[trd.md §3.3]`

All enhanced command components follow CVT's base lifecycle:
```text
EventExecuteAfterSpawnPawn
  → Bind_Options (subscribe to input, configure UI)
  → Execute (tool is active, processing input)
  → Disabled (tool deactivated, cleanup)

SaveGame hooks:
  → EventBindSaveState (serialize current state)
  → EventBindLoadState (deserialize state)
```

| Component | Extends | New Capabilities |
|-----------|---------|-----------------|
| `BP_OrionMeasurement` | `BP_DimensionComponent` | Multi-point polyline, angles, area, snap system, units toggle, save measurements |
| `BP_OrionXray` | `BP_XrayComponent` | Per-zone/per-equipment selective, color-coded overlays, opacity slider, layer toggle |
| `BP_OrionExplode` | `BP_ExplodeComponent` | 3-level hierarchical, building floor explode, callout labels, distance slider, assembly instruction mode |
| `BP_OrionCropBox` | `BP_CropBoxComponent` | UE5.8 gizmo, stencil-buffer section-fill, 2D section capture, plane vs cube toggle, multiple sections |
| `BP_OrionSnapshot` | `BP_Snapshot` | Dark theme restyle, output linked to telemetry directory |
| `BP_OrionRatioScale` | `BP_Scale_Component` | Dark theme restyle, spatial validation retained |
| `BP_OrionDataSmith` | `BP_DataSmith_Component` | Dark theme restyle, auto-tag runtime-loaded geometry via MetadataLinker |
| `BP_OrionAnnotation` | `BP_AnnotationComponent` | Category tags (safety/maintenance/design), category filter, export report |
| `BP_OrionBookmark` | `BP_BookmarkComponent` | Organize by category, share across sessions |

---

### 5.6 BP_SnapManager (Actor Component) `[trd.md §3.4]`

**Purpose:** AutoCAD-style geometric snapping for measurement tool.

**Snap Types (priority order):**

1. Intersection (two edge crossings)
2. Vertex (nearest mesh vertex within radius)
3. Midpoint (midpoint of nearest edge)
4. Center (bounding box center of component)
5. Edge (closest point on nearest edge)
6. Face (surface normal projection)

**Visual Indicators (3D widget meshes):**

- Diamond mesh → Vertex
- Circle mesh → Midpoint
- Square mesh → Center
- X mesh → Intersection
- All use emissive teal material (`#00D4AA`) with 1Hz pulse animation

**Config:**

- Snap radius: 5cm world (configurable)
- Snap toggle: S key
- **Performance: <16ms per frame**

---

### 5.7 BP_CameraSweepManager (Actor Component) `[trd.md §3.4]`

**Purpose:** Smooth camera interpolation between positions.

**Parameters:**
| Param | Values |
|-------|--------|
| `SweepSpeed` | Fast (1s), Medium (2s), Slow (3s) |
| `MinViewDistance` | 200 units |
| `MaxViewDistance` | 2000 units |
| `CollisionAvoidanceRadius` | 50 units |

**Delegates:**

- `OnSweepComplete(FName TargetID)` — multicast

---

## 6. Data Architecture

### 6.1 Enum Definitions `[backend_schema.md §1]`

| Enum | Values |
|------|--------|
| `EOrionMode` | `MODE_LAUNCHER`, `MODE_SHOWCASE`, `MODE_OPERATIONS`, `MODE_TRAINING` |
| `EOrionRole` | `ROLE_VIEWER`, `ROLE_ENGINEER`, `ROLE_ADMIN` |
| `EEquipmentType` | `Pump`, `Vessel`, `Conveyor`, `Mixer`, `Valve`, `Instrument`, `HeatExchanger`, `Tank`, `Motor`, `Compressor`, `Filter`, `Pipe`, `Structure`, `Electrical`, `Other` |
| `EZoneClassification` | `General`, `Clean`, `Chemical`, `Electrical`, `Confined`, `Hazardous` |
| `ENPCType` | `AmbientWorker`, `TourGuide`, `SecurityGuard` |
| `EMaintenanceStatus` | `OK`, `Due`, `Overdue`, `Unknown` |
| `EMatchConfidence` | `Exact`, `Contains`, `Fuzzy`, `Unmatched` |
| `ESectionFillMode` | `Solid`, `Hatching45`, `CrossHatching`, `ColorByType` |
| `EMeasurementUnit` | `Meters`, `Feet`, `Millimeters` |
| `ESnapType` | `None`, `Vertex`, `Edge`, `Midpoint`, `Center`, `Face`, `Intersection` |
| `EAnnotationCategory` | `General`, `Safety`, `Maintenance`, `DesignReview` |
| `EOrionTreeCategory` | `Building`, `Room`, `Equipment`, `Component` |
| `EOrionSweepSpeed` | `Fast`, `Medium`, `Slow` |

---

### 6.2 Data Tables `[trd.md §4.1]`, `[backend_schema.md §2]`

#### DT_Equipment (Master Table — ~6500 rows)

| Column | UE Type | Constraints |
|--------|---------|-------------|
| `EquipmentID` | `FName` | Primary key; matches actor tag |
| `DisplayName` | `FText` | String Table ref |
| `PIDTag` | `FString` | P&ID tag format |
| `ProcessLine` | `FString` | FK → DT_ProcessLines |
| `BuildingID` | `FName` | FK → DT_Buildings |
| `RoomID` | `FName` | FK → DT_Rooms |
| `ZoneID` | `FName` | FK → DT_Zones |
| `EquipmentType` | `EEquipmentType` | Enum |
| `Manufacturer` | `FString` | |
| `Model` | `FString` | |
| `SpecsJSON` | `FString` | JSON blob |
| `DrawingPaths` | `TArray<FString>` | Relative content paths to PNGs |
| `AnimationClass` | `TSoftClassPtr<AActor>` | Nullable |
| `bHasExplode` | `bool` | Default false |
| `MaintenanceComponents` | `TArray<FName>` | Component IDs |

#### DT_Buildings (~5-10 rows)

| Column | UE Type |
|--------|---------|
| `BuildingID` | `FName` |
| `DisplayName` | `FText` |
| `Floors` | `int32` |
| `LocationOrigin` | `FVector` |
| `LocationExtent` | `FVector` |

#### DT_Rooms (~50-100 rows)

| Column | UE Type |
|--------|---------|
| `RoomID` | `FName` |
| `BuildingID` | `FName` |
| `DisplayName` | `FText` |
| `Floor` | `int32` |
| `Function` | `FString` |
| `SafetyZoneType` | `EZoneClassification` |
| `SafetyZoneColor` | `FLinearColor` |

#### DT_ProcessLines (~500 rows)

| Column | UE Type |
|--------|---------|
| `ProcessLineID` | `FString` |
| `DisplayName` | `FText` |
| `ConnectedEquipment` | `TArray<FName>` |
| `PIDDocPath` | `FString` |

#### DT_Zones (~20-50 rows)

| Column | UE Type |
|--------|---------|
| `ZoneID` | `FName` |
| `BoundsOrigin` | `FVector` |
| `BoundsExtent` | `FVector` |
| `ActiveEquipment` | `TArray<FName>` |

#### DT_TourWaypoints (~10-30 rows per tour)

| Column | UE Type |
|--------|---------|
| `WaypointID` | `FName` |
| `TourName` | `FString` |
| `Sequence` | `int32` |
| `CameraTransform` | `FTransform` |
| `InfoText` | `FText` |
| `VOPath` | `FSoftObjectPath` |

#### DT_NPCs (~10-30 rows)

| Column | UE Type |
|--------|---------|
| `NPCID` | `FName` |
| `NPCType` | `ENPCType` |
| `ZoneID` | `FName` |
| `AnimationSet` | `FName` |
| `PatrolPath` | `FSoftObjectPath` |

#### DT_InspectionSteps (~8 rows per equipment × ~8 equipment)

| Column | UE Type |
|--------|---------|
| `StepID` | `FName` |
| `EquipmentID` | `FName` |
| `Sequence` | `int32` |
| `Description` | `FText` |
| `ExpectedCondition` | `FText` |
| `CameraTransform` | `FTransform` |
| `PhotoRefPath` | `FString` |

#### Reserved v2 Tables `[backend_schema.md §2.9]`

| Table | Purpose |
|-------|---------|
| `FSOPStepTableRow` | Mode B Training — SOP steps |
| `FQuizQuestionTableRow` | Mode B Training — quiz questions |

---

### 6.3 Runtime Data Structures `[backend_schema.md §3]`

Key runtime types (not Data Tables):

- `FBuildingNode`, `FRoomNode`, `FEquipmentNode` — in-memory hierarchy tree
- `FSearchResult` — search result with `ID`, `DisplayName`, `Category`, `Relevance`, `EquipmentType`
- `UOrionTreeItemData` (UObject) — list item data for virtualized `UListView`
- `FMatchResult`, `FMatchReport` — MetadataLinker output
- `FOrionConfig` → `FOrionClientConfig`, `FOrionModeConfig`, `FOrionFeatureConfig`, `FOrionOptimizationConfig`, `FOrionSaveConfig`
- `FMeasurementPoint`, `FMeasurementSegment`, `FMeasurementSet` — measurement tool data

---

### 6.4 SaveGame Schema `[backend_schema.md §4]`, `[trd.md §8]`

Extension fields added to CVT's `BP_Data_SaveGame`:

| Field | Type | Description |
|-------|------|-------------|
| `LastMode` | `EOrionMode` | Last active mode |
| `LastSelectedEquipment` | `FName` | Last selected equipment ID |
| `InspectionProgress` | `TMap<FName, FOrionInspectionProgress>` | Step completion per equipment |
| `BookmarkCategories` | `TMap<FName, FString>` | BookmarkID → category |
| `AnnotationCategories` | `TMap<FName, EAnnotationCategory>` | |
| `SavedMeasurements` | `TArray<FMeasurementSet>` | Labeled measurement sets |

**Save triggers:** Auto-save (every 300s per config), manual save, mode switch, app exit. `[flow_diagrams.md §10]`

---

## 7. UI Architecture

### 7.1 Widget Hierarchy `[trd.md §5.1]`

```text
WBP_OrionRoot (viewport root, always active, Z-Order 0)
│
├── WBP_TopBar (horizontal bar, top edge)
│   ├── IMG_ClientLogo (loaded from OrionConfig.json logo_path)
│   ├── TXT_PlantName (from config)
│   ├── TXT_ModeIndicator ("SHOWCASE" / "OPERATIONS")
│   ├── BTN_Settings (opens WBP_ModalOverlay)
│   └── TXT_UserRole (current role)
│
├── WBP_SidePanel (collapsible left panel, 320px width)
│   ├── WBP_SearchBar
│   │   ├── EDT_SearchInput (UEditableTextBox)
│   │   └── LST_SearchResults (UListView — virtualized)
│   ├── WBP_TreeBrowser
│   │   └── LST_TreeView (UListView — virtualized, 6500+ entries)
│   └── WBP_EquipmentDetails (slides in from right)
│       ├── TAB_Overview / TAB_Components / TAB_Actions / TAB_Drawings / TAB_Data
│       └── Content panels per tab
│
├── WBP_BottomBar (horizontal bar, bottom edge)
│   ├── WBP_ToolPalette (context-sensitive per mode)
│   ├── TXT_MeasurementReadout (live measurement display)
│   ├── BTN_MinimapToggle
│   └── TXT_SnapStatus ("SNAP: ON/OFF")
│
├── WBP_Minimap (corner overlay, toggleable)
│   ├── IMG_MinimapRT (bound to render target)
│   ├── IMG_PlayerArrow (rotates with player heading)
│   ├── WBP_FloorSelector (tab buttons: F1, F2, F3...)
│   └── Click input handler → teleport pipeline
│
├── WBP_ToolRadialMenu (quick-access wheel, Z-Order 5)
│
├── WBP_Notification (toast stack, Z-Order 10)
│
├── WBP_DebugOverlay (dev-only, Z-Order 15)
│   ├── TXT_FPS, TXT_DrawCalls, TXT_Mode, TXT_PawnType
│   └── TXT_HoverEquipmentID
│
└── WBP_ModalOverlay (full-screen dimmed overlay, Z-Order 20)
    ├── WBP_SettingsPanel
    ├── WBP_ConfirmDialog
    └── WBP_ErrorReport
```

### 7.2 Widget Performance Requirements `[trd.md §5.2]`

| Widget | Technique | Target |
|--------|-----------|--------|
| `WBP_TreeBrowser` | `UListView` (virtualized) — only renders visible entries + 5 buffer | 60fps scroll at 6500 entries |
| `WBP_SearchResults` | `UListView` (virtualized) — max 50 results displayed | <200ms from keystroke to results |
| `WBP_Minimap` | Render target throttled to 10fps | <0.5ms GPU per frame |
| `WBP_EquipmentDetails` | Lazy tab loading — only active tab populates | <100ms tab switch |
| All panels | Slide-in/fade at **0.3s ease-out** | 60fps during animation |

### 7.3 Hierarchical Tree Browser `[trd.md §5.3]`

**`WBP_TreeBrowser`** — virtualized sidebar showing: `Buildings > Rooms > Equipment > Components`.

Key specifications:

- Must use `UListView` (`LST_TreeView`) — not ScrollBox.
- List data objects: instances of `UOrionTreeItemData` (UObject).
- **Row widget `WBP_TreeItemRow`** inherits `IUserObjectListEntry`.
- Indentation: spacer width = `Depth * 16.0`.
- Selection: row highlights with accent `#00D4AA` background; triggers camera sweep + actor highlight.

**Flat-List Assembly Algorithm:**

1. **Initial Population:** Query buildings from `BP_HierarchyManager`, instantiate `UOrionTreeItemData` at depth 0, call `ListView->SetListItems`.
2. **Node Expanded:** `bIsExpanded = true`, retrieve children, insert after parent's index, refresh.
3. **Node Collapsed:** `bIsExpanded = false`, traverse forward, remove consecutive elements with `Depth > ParentDepth`, refresh.

### 7.4 Design System Tokens `[implementation_plan.md §0.3]`

| Element | Specification |
|---------|--------------|
| Background | Deep navy `#0A1628` / charcoal `#1A2332` |
| Primary accent | Teal `#00D4AA` (active/selected states) |
| Warning | Amber `#FFB74D` (caution states) |
| Alert | Red `#FF5252` (alarm/error states) |
| Text primary | White `#FFFFFF` at 90% opacity |
| Text secondary | White at 60% opacity |
| Panel style | Glassmorphism — semi-transparent with blur backdrop, subtle border glow |
| Transitions | Smooth slide-in/fade **0.3s ease-out** for panels; **0.15s** for hover states |
| Typography | Clean sans-serif (Roboto/Inter equivalent in UMG) |
| Icons | Outlined industrial icon set; consistent stroke width |

---

## 8. Canonical System Flows

`[flow_diagrams.md]`

### Flow 1: Application Boot
1. App Launch → `BP_OrionGameInstance::Init` → `BP_ConfigLoader::LoadConfig`
2. Config exists? → Parse JSON → Validate → Store config struct
3. Config missing → Use embedded defaults → Show Warning Banner
4. Load Login Level → Spawn `BP_LoginMenuPawn` → Display Branded Launcher
5. User selects role → `BP_OrionModeManager::SetMode` → Load Main Level
6. `BP_MetadataLinker::RunMatching` + `BP_HierarchyManager::BuildTree` (parallel)
7. `OnMatchingComplete` + `OnTreeReady` → Enable Navigation UI → App Ready

### Flow 2: Mode Switching
1. User requests mode switch → `BP_OrionModeManager::SetMode`
2. `CanAccessMode`? No → Show Permission Denied Toast
3. Yes → Update state → Fire `OnModeChanged` delegate
4. Subscribers react: `WBP_OrionRoot` (panel visibility), Command Components (enable/disable), `BP_NPCManager`, `BP_ZoneAnimationManager`, `BP_TelemetryManager` (log), CVT SessionManager (broadcast to clients)

### Flow 3: Equipment Selection
**Sources:** Tree Browser click, Search Result click, Minimap click, 3D Viewport click, Carousel click.

1. Any source → Get EquipmentID → `BP_HierarchyManager::SelectEquipment`
2. Fire `OnEquipmentSelected` delegate
3. → `BP_CameraSweepManager::SweepTo` (collision-free path, pulsing outline)
4. → `WBP_EquipmentDetails::Populate` (load DT_Equipment row, lazy tabs)
5. → `WBP_TreeBrowser::HighlightNode` (expand ancestors, scroll to node)
6. → `BP_ZoneAnimationManager::ActivateZone`
7. → `BP_TelemetryManager::LogEquipmentView`

**Minimap click path:** Click UV → Convert to World XY → Line trace down → Walkable? → Sphere overlap (not inside geometry) → `BP_CameraSweepManager::SweepTo`

### Flow 4: Guided Tour
1. `BP_GuidedTourManager::StartTour` → Load `DT_TourWaypoints`, sort by Sequence
2. Per waypoint: `BP_CameraSweepManager::SweepTo` → Arrival: show info panel + play VO + update progress bar
3. Controls: Next/Previous (advance waypoint index), Pause (hold camera), Exit (restore free camera, hide tour UI)
4. On complete: Show completion screen → `BP_TelemetryManager::LogTourCompletion`

### Flow 5: Measurement Tool with Snap
1. Activate `BP_OrionMeasurement::Execute` → Enable cursor tracking
2. Per mouse move: Line trace → Hit static mesh? → Snap enabled? → `BP_SnapManager::FindSnap`
3. Snap priority: vertex (5cm) → midpoint (2.5cm) → edge → center → raw hit
4. Left click → Place measurement point → Calculate segment length, angle, total length
5. Double-click/Enter → Finalize → Calculate area if closed → Save option

### Flow 6: CropBox Section-Fill
1. Activate `BP_OrionCropBox::Execute` → Spawn clip plane/volume → Attach UE5.8 transform gizmo
2. User manipulates gizmo → Custom depth material pass → Stencil by equipment type (Pipe=1, Structure=2, Electrical=3, Other=4)
3. Post-process reads stencil → Apply fill mode (Solid, Hatching45, CrossHatching, ColorByType)
4. 2D Export: `SceneCaptureComponent2D` orthographic → `2048×2048` render target → PNG via `ImageWriteQueue`

### Flow 7: Minimap Click-to-Teleport
1. Click widget → Normalize to UV → Convert to world XY using ortho bounds
2. Line trace downward from max Z
3. Valid walkable surface → Sphere overlap check (not inside geometry) → `BP_CameraSweepManager::SweepTo` → Update player arrow
4. Invalid → Show red X on minimap (fades after 1s)

### Flow 8: MetadataLinker Matching
1. Level load → `BP_MetadataLinker::RunMatching`
2. Scan Datasmith actors → Normalize labels → Match against `DT_Equipment.EquipmentID`
3. Exact → HIGH confidence; Contains → MEDIUM; Levenshtein ≤ 3 → AMBIGUOUS; else UNMATCHED
4. Generate `FMatchReport` → Fire `OnMatchingComplete` → If match rate < 90% → Show unmatched report + enable manual linking UI

### Flow 9: Multi-User Session
1. Host starts session (CVT lobby) → selects Admin role → `BP_OrionModeManager::SetMode`
2. Client joins → CVT handshake → select role → Role allowed? → Sync current mode from GameState
3. Mode change by host → Update `GameState` replicated property → All clients receive `OnRep_CurrentMode` → Fire local `OnModeChanged`
4. Session recording: `BP_SessionRecorder::StartRecording` → Capture every 100ms (camera transform + active tool + annotations) → Save `Saved/SessionRecordings/timestamp.json`
5. Heartbeat monitor: Client no response in 5s → Auto-resync → If fails → Rejoin prompt

### Flow 10: SaveGame
Save triggers: Auto-save (300s), manual, mode switch, app exit.

1. `BP_Data_SaveGame::SaveState` → For each Command Component → Fire `EventBindSaveState`
2. Serialize Orion custom fields (mode, equipment, inspection progress, bookmark categories)
3. Write to `Saved/SaveGames/PREFIX_slot.sav` → Show save confirmation toast
4. Load: `BP_Data_SaveGame::LoadState` → Fire `EventBindLoadState` → Restore Orion fields → Fire `OnModeChanged` + `OnEquipmentSelected`

### Flow 11: Config Validation & Hot-Reload
1. Dev build only: Register file watcher on `OrionConfig.json`
2. File change detected → Re-parse → Validate → Update config struct → Fire `OnConfigReloaded`
3. Subscribers: `WBP_OrionRoot` (update colors/logo), `BP_OrionModeManager` (update mode availability), feature systems (toggle features)
4. Shipping builds: No hot-reload

### Flow 12: Content Pipeline (Client Onboarding)
1. Receive Plant 3D `.dwg` files
2. **Pipeline A:** 3ds Max QA → Datasmith Export → UE5 Import
3. **Pipeline B:** Python export script → `equipment_metadata.json` → Data Tables
4. **Pipeline C:** `BP_MetadataLinker::RunMatching` → If <90% → Equipment Tagger manual linking
5. Configure zones (Zone Painter) → Build tour (Tour Path Editor) → Create `OrionConfig.json` (Config Generator)
6. Validation Pass → All checks pass → Client scene ready

---

## 9. Config System

### 9.1 OrionConfig.json Schema `[trd.md §10.1]`

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

### 9.2 Validation Rules `[trd.md §10.2]`

| Field | Validation | On Failure |
|-------|-----------|------------|
| `company_name` | Non-empty string | Use "Orion Studios" default |
| `logo_path` | File exists at path | Use embedded Orion logo |
| `accent_color` | Regex: `^#[0-9A-Fa-f]{6}$` | Use default `#00D4AA` |
| `modes.*` | Boolean | Default to true/false per field |
| `target_fps_*` | Integer 30-144 | Clamp to range |
| Entire file | Valid JSON | Use full embedded defaults; show warning banner |

---

## 10. Performance Budgets

### 10.1 Frame Budget (16.67ms @ 60fps) `[trd.md §9.1]`

| System | Budget |
|--------|--------|
| Rendering (GPU) | 10ms |
| UI (UMG) | 1ms |
| Game Logic | 2ms |
| Physics/Collision | 1ms |
| Animation | 1ms |
| Networking | 0.5ms |
| Buffer | 1.17ms |

### 10.2 Memory Budget (Desktop) `[trd.md §9.2]`

| Category | Budget |
|----------|--------|
| Scene meshes | 2-4 GB |
| Textures | 1-2 GB |
| Data Tables (all) | <50 MB |
| UI widgets | <100 MB |
| Render targets | <32 MB |
| Audio | <200 MB |

### 10.3 Render Target Specifications `[trd.md §9.3]`

| Target | Resolution (Desktop) | Resolution (VR) | Update Rate |
|--------|---------------------|-----------------|-------------|
| Minimap | 512×512 | 256×256 | 10fps (throttled) |
| Section Capture | 2048×2048 | 1024×1024 | On-demand only |
| Snapshot | Viewport resolution | Viewport resolution | On-demand |

### 10.4 Module Performance Targets

| Module | Target | Source |
|--------|--------|--------|
| Search (any query, 6500 entries) | <200ms | `[trd.md §3.2]`, `[prd.md §Testing]` |
| Tree browser scroll (6500 entries) | 60fps | `[trd.md §5.2]` |
| Camera sweep (arrival) | Within configured SweepSpeed (1-3s) | `[trd.md §3.4]` |
| Tab switch (Equipment Details) | <100ms | `[trd.md §5.2]` |
| SnapManager per-frame | <16ms | `[trd.md §3.4]` |
| Level load (6500 actors) | <30 seconds | `[prd.md §Acceptance Criteria]` |
| MetadataLinker match rate | >90% | `[prd.md §Acceptance Criteria]` |

---

## 11. Error Handling Matrix

`[trd.md §12]`

| Failure | Detection | Response | User Feedback |
|---------|-----------|----------|---------------|
| Config missing | FileExists check at startup | Load embedded defaults | Persistent warning banner |
| Config malformed | JSON parse error | Load defaults for invalid fields | Toast listing failed fields |
| MetadataLinker <90% match | Match report count check | Allow manual linking | Editor Utility Widget report |
| Data Table import error | `CreateTableFromJSONString` error array | Continue with partial data | Error toast; unmatched equipment hidden |
| VR headset disconnected | OpenXR session lost event | Auto-switch to desktop pawn | Reconnection prompt dialog |
| Multi-user desync | Heartbeat timeout (5s) | Auto-resync from host state | If resync fails → rejoin prompt |
| Asset path not found | `FSoftObjectPath` resolve failure | Use placeholder asset | Log warning |
| Search returns empty | Result count == 0 | Show "No results" with suggestions | Alternative query hints |
| Out of memory | Platform memory warning | Reduce quality settings | Quality reduction toast |

---

## 12. Build & Deployment

`[trd.md §11]`

### Build Configurations

| Configuration | Use | Defines |
|--------------|-----|---------|
| DebugGame | Development | `WITH_ORION_DEBUG=1`, hot-reload, debug overlay |
| Development | Internal testing | `WITH_ORION_DEBUG=1`, some debug features |
| Shipping | Client delivery | No debug overlay, no hot-reload, no console commands |

### Platform Matrix

| Build | Target | Min Spec | Rendering | Target FPS |
|-------|--------|---------|-----------|-----------|
| Desktop | Windows .exe | GTX 1080 / RX 5700 | Lumen GI, full post-process | 60 |
| PC VR | Meta Quest Link / SteamVR | RTX 3080 recommended | Simplified Lumen or baked | 72 |
| Quest APK | Meta Quest 2/3 | Standalone | Fully baked, simplified meshes | Future scope |

---

## 13. Acceptance Criteria (Release Gate)

`[prd.md §Acceptance Criteria]`

| Criterion | Threshold |
|-----------|-----------|
| Desktop FPS | ≥60fps with Morde Foods scene loaded |
| VR FPS | ≥72fps with simplified lighting |
| Level load time | <30 seconds for 6500 tagged actors |
| Search latency | <200ms for any query |
| Tree browser scroll | 60fps with 6500 entries |
| Guided tour | Plays start-to-finish with all waypoints |
| Config swap | Change `OrionConfig.json` → app reflects changes |
| MetadataLinker match rate | >90% of known Datasmith actors |
| Multi-user session | 2+ users with role-based permissions functional |
| All enhanced tools | Xray, Explode, CropBox, Measurement, Snapshot, RatioScale, DataSmith working |

---

## 14. Out of Scope (v1)

`[prd.md §Out of Scope]`

| Feature | Reason | Architecture Prep |
|---------|--------|-------------------|
| Mode B — Training | Deferred to v2; scope too large for v1 | `MODE_TRAINING` enum reserved; `DT_SOPSteps`, `DT_QuizQuestions` schemas defined |
| Live Simulation Data | Requires external software integration | Data tab placeholder; `BP_SimDataManager` interface defined |
| Thermal/Safety Heatmap | Requires simulation data | Zone system supports overlay materials |
| Construction Timeline | Requires per-equipment phase data | `DT_Equipment` has `construction_phase` placeholder |
| Hindi/English Localization | FText prep in place; translation deferred | `ST_Orion_UI.csv` String Table with English entries |
| Cloud Session Logging | Local JSON sufficient for v1 | Telemetry format compatible with future cloud API |
| Standalone Quest APK | Requires separate optimization pass | VR quality tier supported in optimization foundation |
| Client Plugin System | No client yet needs custom extensions | `IOrionFeaturePlugin` interface defined; `Content/ClientPlugins/` folder reserved |

---

## 15. Resolved Questions

`[implementation_plan.md §Resolved Questions]`

| Question | Resolution |
|----------|------------|
| **Q1: Plant 3D Python Script** | `export_plant3d_metadata.py` connects directly to Plant 3D SQLite databases (e.g. `Piping.db`), queries `Equipment` and `EngineeringItems` tables, exports clean JSON. |
| **Q2: 2D CAD Drawings Format** | **PNG format** locked in for runtime loading via native `UTexture2D` APIs. No third-party PDF plugins required. |
| **Q3: Equipment Animations** | **Skeletal animations** authored in Blender/3ds Max, imported as skeletal meshes. |
| **Q4: NPC Character Models** | **Mannequin-based characters** styled with safety vest and helmet assets. |
| **Q5: Session Recording Scope** | Captures camera paths, interaction states, and annotations (~MB/min). |

---

## 16. Module Dependency Map

`[backend_schema.md §9]`

```text
BP_ConfigLoader (Game Instance)
  └── BP_OrionModeManager (World Subsystem)
        └── WBP_OrionRoot + Command Components + BP_NPCManager + BP_ZoneAnimationManager

Data Tables (DT_Equipment, DT_Buildings, etc.)
  ├── BP_MetadataLinker (World Subsystem)
  │     └── BP_HierarchyManager (World Subsystem)
  │           ├── WBP_TreeBrowser
  │           ├── WBP_SearchBar
  │           ├── WBP_EquipmentDetails
  │           └── BP_CameraSweepManager
  │                 ├── BP_GuidedTourManager
  │                 └── BP_InspectionManager
  └── BP_TelemetryManager (World Subsystem)

Command Components (Xray, Explode, CropBox, etc.)
  ├── BP_SnapManager
  ├── CVT SaveGame System
  └── BP_TelemetryManager
```

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
