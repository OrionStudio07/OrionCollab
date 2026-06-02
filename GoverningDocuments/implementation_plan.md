# Orion Studios — Industrial Visualization Platform
## Comprehensive Implementation Plan

> [!IMPORTANT]
> **Base:** Unreal Engine 5.8 CollabViewer Template (CVT)
> **Reference Client:** Morde Foods P2 Manufacturing Plant (6500 tags, 1394 instrumentation points, ~500 process lines, ~200 unique equipment)
> **Product Type:** Reusable platform — client content swapped per deployment via config file
> **Platform Targets:** Desktop (Windows .exe) + PC VR (Meta Quest Link / SteamVR)

---

## Design Decisions (Locked In)

These decisions were resolved during the grill-me session and drive the entire architecture:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data Architecture | Data Tables + JSON Config | Native UE5, Blueprint-friendly, no external deps, importable from CSV/JSON |
| Mode System | Shared Core + ModeManager subsystem | All modes share same level/pawn; UI layer and toolsets change per mode |
| Metadata Import | Dual Import Strategy | Geometry via 3ds Max (QA cleanup); metadata via parallel Plant 3D export; matched in UE5 by name/ID |
| UI Theme | Modern Industrial Dashboard | Dark navy/charcoal, teal/amber/red status colors, glassmorphism, SCADA-inspired |
| Navigation | Hierarchical Tree Browser + Search Bar | Building > Room > Equipment tree; auto-complete search; camera sweep + pulsing highlight |
| Equipment Selection | Tabbed Equipment Details Panel | Overview / Components / Actions / Drawings / Data tabs; slides in from side |
| Animation System | Zone Trigger Volumes | Per-zone activation via trigger volumes; only active zone plays animations |
| Minimap | 2D Render Target Minimap | Top-down ortho camera to texture; clickable teleport; floor selector |
| Measurement Tool | Multi-Point Polyline + AutoCAD Snapping | Unlimited points, segment lengths, total length, angles, polygon area, vertex snapping |
| CropBox | Full Overhaul | Fix lighting, UE5.8 gizmo, section-fill hatching, 2D section capture/export, plane vs cube toggle |
| Xray | Global + Selective + Color-Coded | Global toggle, per-zone/per-equipment selective, color by type (pipes=blue, structure=white, electrical=yellow) |
| Explode | Hierarchical + Assembly Instruction + Building Floor Explode | Multi-level explode, step-by-step assembly/disassembly, building floor separation |
| Guided Tour | Scripted Path + Hotspot + Sequencer Cinematic | Data-driven waypoint tour + premium Sequencer cinematics per client |
| NPCs | Ambient NPC System | Data Table driven; workers play zone-assigned animations; guide follows tour path |
| Client Branding | Per-Client JSON/INI Config | Logo, colors, company name, plant name, mode toggles, feature flags |
| Multi-User | Enhanced CVT Sessions | Role-based permissions, synchronized mode states, session recording/playback |
| VR | PC VR only (tethered) | Meta Quest Link / SteamVR; standalone Quest APK is future scope |
| Simulation Data | File-Based Polling + Manual Import | Architecture extensible but implementation deferred to future scope |

---

## Phase 0 — CVT Audit + UI/UX Foundation

**Goal:** Audit CVT baseline, optimize scene performance, and establish the new design system before any feature work.

### 0.1 CVT Codebase Audit

| Task | Details |
|------|---------|
| Blueprint inventory | Document all CVT Blueprints (Pawn, Commands, GameMode, GameInstance, UMG widgets) — understand what exists |
| Command component mapping | Map BP_BaseCommandComponent and all command children (Xray, Explode, CropBox, Annotation, Bookmark, Dimension, Snapshot, Transform) |
| Pawn hierarchy | Map BP_BasePawn → Default, VR, AR, Touch, LoginMenu pawns and their input bindings |
| Multi-user system | Understand CVT's session management (BP_LoginMenuPawn, LoginLevel, GameInstance networking) |
| ShareLibrary/CommonFunctions | Audit CommonFunctions_CV for reusable utilities |
| Input system | Map CVT's Input Action bindings and Enhanced Input setup |

### 0.2 Scene Optimization Foundation

> [!NOTE]
> Applied during client scene import. Targets: **60fps desktop / 72fps VR minimum.**

| Optimization | Approach |
|-------------|----------|
| Level instancing | Convert repeated geometry to ISM/HISM; reduces draw calls |
| Mesh optimization | LOD setup per mesh category; proxy LODs for distant equipment clusters |
| Light optimization | Baked (static environment) vs dynamic (interactive/animated); Lumen for desktop, baked for VR |
| Distance culling | Cull distance volumes per equipment tier; small props aggressively culled |
| Post-process volumes | Single global PP volume; per-zone overrides where needed |
| Group actors | Organize outliner by zone/system; enables visibility toggles per area |

### 0.3 UI/UX Design System

**Visual Identity: Modern Industrial Dashboard**

| Element | Specification |
|---------|--------------|
| Background | Deep navy `#0A1628` / charcoal `#1A2332` |
| Primary accent | Teal `#00D4AA` (active/selected states) |
| Warning | Amber `#FFB74D` (caution states) |
| Alert | Red `#FF5252` (alarm/error states) |
| Text primary | White `#FFFFFF` at 90% opacity |
| Text secondary | White at 60% opacity |
| Panel style | Glassmorphism — semi-transparent panels with blur backdrop, subtle border glow |
| Transitions | Smooth slide-in/fade (0.3s ease-out) for panels; 0.15s for hover states |
| Typography | Clean sans-serif (Roboto/Inter equivalent in UMG) |
| Icons | Outlined industrial icon set; consistent stroke width |

**Widget Architecture:**

```
WBP_OrionRoot (Root widget — always active)
├── WBP_TopBar (Logo, mode indicator, settings, user info)
├── WBP_SidePanel (Collapsible — context-sensitive per mode)
│   ├── WBP_TreeBrowser (Hierarchy navigation)
│   ├── WBP_EquipmentDetails (Tabbed details panel)
│   └── WBP_SearchPanel (Search bar + results)
├── WBP_BottomBar (Tool palette, measurement readout, minimap toggle)
├── WBP_Minimap (2D render target minimap widget)
├── WBP_ToolRadialMenu (Quick-access tool wheel)
├── WBP_Notification (Toast notifications)
└── WBP_ModalOverlay (Confirmation dialogs, settings)
```

**Key UI Changes from CVT:**

| CVT Default | Orion Enhancement |
|------------|-------------------|
| Simple game menu | Full branded launcher with role selection, settings, mode picker |
| Basic toolbar | Radial tool menu + bottom bar with contextual tools per mode |
| No sidebar | Collapsible sidebar with tree browser + search + equipment details |
| Simple HUD | Dashboard-style HUD with status indicators, breadcrumb navigation |
| No minimap | 2D render target minimap with click-to-teleport |

### 0.4 Per-Client Config System

**Config File: `OrionConfig.json`** (read at startup)

```json
{
  "client": {
    "company_name": "Morde Foods",
    "plant_name": "P2 Manufacturing Plant",
    "logo_path": "Content/ClientAssets/Logo.png",
    "accent_color": "#00D4AA"
  },
  "modes": {
    "showcase": true,
    "training": false,
    "operations": true
  },
  "features": {
    "minimap": true,
    "guided_tour": true,
    "npc_workers": true,
    "session_recording": false,
    "simulation_data": false
  },
  "optimization": {
    "lumen_enabled": true,
    "vr_mode": "pc_tethered",
    "target_fps_desktop": 60,
    "target_fps_vr": 72
  }
}
```

---

## Phase 1 — Core Architecture

**Goal:** Build the data backbone, mode management, and metadata import pipeline that all features depend on.

### 1.1 Data Table Architecture

**Master Equipment Data Table: `DT_Equipment`**

| Column | Type | Description |
|--------|------|-------------|
| EquipmentID | FName | Unique identifier matching actor name/tag |
| DisplayName | FText | Human-readable name |
| PIDTag | FString | P&ID tag (e.g., `P-101`, `V-201`) |
| ProcessLine | FString | Process line code (e.g., `PL-001`) |
| BuildingID | FName | Parent building reference |
| RoomID | FName | Parent room reference |
| EquipmentType | Enum | Pump, Vessel, Conveyor, Mixer, Valve, Instrument, etc. |
| Manufacturer | FString | OEM name |
| Model | FString | Model number |
| Specs | FString (JSON) | Key-value specs (capacity, pressure, temp rating) |
| DrawingPaths | TArray\<FString\> | Paths to 2D CAD drawing images |
| AnimationClass | TSoftClassPtr | Optional animation Blueprint reference |
| HasExplode | Bool | Whether hierarchical explode is available |
| MaintenanceComponents | TArray\<FName\> | Component IDs for maintenance tree |
| ZoneID | FName | Animation trigger zone assignment |

**Additional Data Tables:**

| Table | Purpose |
|-------|---------|
| DT_Buildings | Building hierarchy (ID, name, floors, rooms, location bounds) |
| DT_Rooms | Room definitions (ID, building, name, floor, function, safety zone color) |
| DT_ProcessLines | Process line definitions (ID, name, connected equipment, P&ID doc path) |
| DT_Zones | Animation/interaction zones (ID, bounds, active equipment list) |
| DT_NPCs | NPC definitions (ID, type, zone, animation set, patrol path) |
| DT_TourWaypoints | Guided tour waypoints (ID, tour name, sequence, camera transform, info text, VO path) |
| DT_InspectionSteps | Inspection walkthrough steps per equipment |

### 1.2 Mode Manager Subsystem

**`BP_OrionModeManager`** (Game Instance Subsystem)

```
Modes:
  - MODE_LAUNCHER (Role selection, settings)
  - MODE_SHOWCASE (Mode A — presentation/walkthrough)
  - MODE_OPERATIONS (Mode C — inspection/engineering)
  - MODE_TRAINING (Future — Mode B)

Responsibilities:
  - SetMode(NewMode) → Updates UI visibility, tool availability, pawn permissions
  - GetCurrentMode() → Returns active mode
  - CanAccessMode(Mode, Role) → Permission check
  - OnModeChanged delegate → All systems subscribe to mode changes
```

### 1.3 Dual Import Strategy — Metadata Pipeline

**Pipeline A: Geometry (existing)**
```
AutoCAD Plant 3D → 3ds Max (QA cleanup) → Datasmith Export → UE5 Import
```

**Pipeline B: Metadata (new)**
```
AutoCAD Plant 3D → Python Export Script → JSON/CSV → UE5 Data Table Import
```

**Pipeline C: Matching Tool (new)**
```
BP_MetadataLinker subsystem:
  1. On level load, scan all Datasmith-imported actors
  2. Read metadata JSON/CSV into Data Tables
  3. Match actors to Data Table rows by name/ID pattern
  4. Auto-tag matched actors with EquipmentID
  5. Report unmatched actors for manual review
  6. Generate matching report (X matched, Y unmatched, Z ambiguous)
```

> [!IMPORTANT]
> The Python export script for Plant 3D tag extraction is a critical deliverable. It must export: equipment tags, P&ID numbers, process line assignments, equipment types, and any available specs.

### 1.4 Equipment Hierarchy System

**Actor Structure:**
```
Level
├── BP_Building_A (tagged: Building_A)
│   ├── BP_Room_101 (tagged: Building_A/Room_101)
│   │   ├── SM_Mixer_01 (tagged: Building_A/Room_101/Mixer_01) → linked to DT_Equipment row
│   │   ├── SM_Pump_01 (tagged: ...)
│   │   └── BP_AnimationZone_101 (trigger volume for this room)
│   └── BP_Room_102
│       └── ...
├── BP_Building_B
│   └── ...
└── BP_ProcessLine_PL001 (spline actor connecting equipment)
```

**Hierarchy Manager: `BP_HierarchyManager`**
- Builds in-memory tree from Data Tables at level load
- Provides API: `GetBuildingList()`, `GetRoomsByBuilding(BuildingID)`, `GetEquipmentByRoom(RoomID)`, `GetComponentsByEquipment(EquipmentID)`
- Drives the Tree Browser widget
- Handles search queries with fuzzy matching across names, tags, process lines

---

## Phase 2 — Navigation & Search

**Goal:** Build the primary navigation systems that let users find and reach any point in the plant.

### 2.1 Hierarchical Tree Browser

**Widget: `WBP_TreeBrowser`**

- Collapsible sidebar showing: Buildings > Rooms > Equipment > Components
- Each node shows: icon (by type), name, P&ID tag
- Click node → camera sweeps to target with smooth interpolation
- Selected node gets pulsing outline highlight on the 3D actor
- Expand/collapse with smooth animation
- Filter dropdown: All / By Type / By Process Line / By Zone
- Badge indicators: equipment count per room, active alerts

### 2.2 Search System

**Widget: `WBP_SearchBar`**

- Top-of-sidebar search bar with auto-complete dropdown
- Searches across: equipment names, P&ID tags, process line codes, room names, building names
- Results grouped by category with icons
- Select result → camera sweep + highlight
- Recent searches history
- Keyboard shortcut: `Ctrl+F` or `/` to focus search

**Camera Sweep System: `BP_CameraSweepManager`**
- Smooth camera interpolation from current position to target
- Configurable sweep speed (fast for teleport, slow for guided feel)
- Avoids clipping through geometry (path planning with collision check)
- Arrives at optimal viewing distance/angle for target size
- Pulsing outline highlight on arrival (custom post-process material)

### 2.3 Minimap

**Widget: `WBP_Minimap`**

- Render target from top-down orthographic `BP_MinimapCamera`
- Player position indicator (rotating arrow icon)
- Equipment dots color-coded by type
- Click-to-teleport: click any point on minimap to move player there
- Zoom in/out with scroll wheel (when hovering minimap)
- Floor selector for multi-story buildings (tab buttons: F1, F2, F3...)
- Toggle button on bottom bar to show/hide
- Drag to pan the minimap view
- Highlight active zone with subtle glow

### 2.4 Drone Mode

**Camera Mode: `BP_DronePawn`**

- Aerial free-fly camera with no collision
- WASD + mouse look (or gamepad sticks)
- Altitude control: Q (up) / E (down)
- Speed control: Shift (fast) / Ctrl (slow)
- Smooth acceleration/deceleration
- Toggle from main camera mode switcher
- Can still interact with equipment (click to select, open details panel)

### 2.5 Equipment Teleport Sweep

**Widget: `WBP_EquipmentCarousel`**

- Bottom-of-screen carousel showing key equipment thumbnails
- Arrow buttons to cycle forward/backward
- Click thumbnail → camera sweeps to that equipment
- Equipment ordered by process line sequence or custom sort
- Current location indicator on carousel
- Auto-populated from Data Table (flagged equipment only, or all)

---

## Phase 3 — Mode A: Showcase

**Goal:** Photorealistic, navigable experience for investor/client presentations.

### 3.1 Guided Tour System

**Scripted Path Tour:**
- `BP_GuidedTourManager` reads `DT_TourWaypoints`
- Camera follows spline path between waypoints
- At each waypoint: camera pauses, info panel appears with text/images
- VO placeholder audio track per waypoint (can be silent)
- Player controls: Play/Pause, Next/Previous, Exit Tour
- Multiple tours per client (defined in Data Table)
- Progress bar showing tour position

**Sequencer Cinematic Tour:**
- Premium per-client Level Sequences with camera cuts
- Subtitle track for narration
- NPC guide integration (walks path, gestures)
- Triggered from tour selection menu
- Can blend back to gameplay camera at end

### 3.2 NPC System

**Ambient Workers: `BP_NPCWorker`**
- Placed in zones, assigned animations from Data Table
- Animation sets: checking gauges, walking patrol, carrying clipboard, operating controls
- Activated by zone trigger volumes (same as equipment animations)
- Simple scripted patrol paths (spline-based)
- No AI navigation — purely cosmetic

**Guide NPC: `BP_NPCGuide`**
- Follows guided tour path
- Gestures at equipment at each waypoint
- Subtitles for narration text
- Can be toggled on/off

### 3.3 Enhanced Visualization Tools

#### Xray System (Enhanced)

| Feature | Implementation |
|---------|---------------|
| Global Xray | Toggle all meshes to wireframe/transparent material (CVT base enhanced) |
| Per-equipment Xray | Select equipment → apply transparency only to selected actors |
| Per-zone Xray | Select zone → make all equipment in zone transparent |
| Color-coded | Pipes = blue wireframe, Structure = white, Electrical = yellow, Instrumentation = green |
| Opacity slider | Adjustable transparency level (0-100%) |
| Layer toggle | Show/hide specific equipment types while in Xray |

#### CropBox System (Full Overhaul)

| Feature | Implementation |
|---------|---------------|
| Fix lighting | Ensure light passes correctly through cut volume; fix current light leak |
| UE5.8 Gizmo | Replace legacy gizmo with new UE5.8 transform gizmo for manipulation |
| Plane vs Cube toggle | Switch between infinite plane slice and bounded cube volume |
| Section-fill material | Cross-section faces get engineering hatching material (configurable: solid, hatched, colored) |
| 2D section capture | Render section view to texture, export as PNG/PDF |
| Multiple sections | Support up to 3 simultaneous cut planes/volumes |

#### Explode System (Hierarchical)

| Feature | Implementation |
|---------|---------------|
| Level 1 | Main assemblies separate from equipment body |
| Level 2 | Sub-components separate from assemblies |
| Level 3 | Individual parts separate from sub-components |
| Building floor explode | Building floors separate vertically to show layout |
| Callout labels | Each exploded component gets a floating label line |
| Distance slider | Control explosion distance continuously |
| Assembly instruction mode | Step-by-step animation showing assembly/disassembly order |
| Per-equipment | Explode only selected equipment, rest stays in place |

#### Measurement Tool (Multi-Point Polyline)

| Feature | Implementation |
|---------|---------------|
| Multi-point | Click to place unlimited measurement points |
| Segment lengths | Display length between each consecutive pair |
| Total length | Running total of all segments |
| Angles | Angle display at each vertex |
| Polygon area | If path is closed, calculate and display enclosed area |
| AutoCAD snapping | Snap to vertices, edges, midpoints, centers of equipment geometry |
| Snap indicators | Visual snap point indicators (diamond at vertices, circle at midpoints) |
| Units toggle | Meters / Feet / Millimeters |
| Save measurements | Store measurement sets with labels for later reference |

### 3.4 Interactive Environment

| Feature | Implementation |
|---------|---------------|
| Interactive doors | Open/close on player approach via trigger volume; animated with sound |
| Interactive gates | Security gates with open/close interaction |
| Interactive wash stations | Activate animation on interaction (water flow, hand wash sequence) |
| Equipment animations | Conveyors, mixers, tanks filling — idle/running states per Data Table config |
| Zone-based activation | Only current zone's animations play (Zone Trigger Volumes) |
| Interactive grass | PBR wind shader reacting to player proximity and wind direction |

### 3.5 Presentation Lighting

| Feature | Implementation |
|---------|---------------|
| Lumen GI | Global Illumination for desktop builds (real-time reflections, natural light bounce) |
| HDRI Sky | High-quality sky dome with time-of-day control |
| Baked lighting variant | Pre-baked lighting for VR builds (performance) |
| Post-process volumes | Global: bloom, depth of field, color grading, chromatic aberration |
| Per-zone PP overrides | Special zones can have unique lighting moods (warm for offices, cool for cleanrooms) |

---

## Phase 4 — Mode C: Operations

**Goal:** Inspection walkthroughs, maintenance overlays, and P&ID integration for plant engineers.

### 4.1 Equipment Details Panel

**Widget: `WBP_EquipmentDetails`** (slides in from right side)

| Tab | Content |
|-----|---------|
| **Overview** | Name, P&ID tag, process line, manufacturer, model, specs, status indicator |
| **Components** | Hierarchical parts list with maintenance-relevant info; expandable tree; part count, material, replacement interval |
| **Actions** | Buttons: Explode, Isolate (hide everything else), Xray, Animate, Inspect (start walkthrough) |
| **Drawings** | 2D CAD drawing viewer with pan/zoom; multiple drawings per equipment; fullscreen toggle |
| **Data** | Simulation data readings placeholder (future scope); live values will appear here when simulation integration is built |

### 4.2 Inspection Walkthrough

**Per-Equipment Inspection: `BP_InspectionManager`**

- Step-by-step visual inspection sequence (up to 8 steps per equipment)
- Each step: camera moves to inspection point, callout highlights target area
- Instruction panel shows: step number, description, expected condition, photo reference
- Checklist-style progression (mark each step complete)
- Animated highlight ring on target component per step
- Can be launched from Equipment Details Panel → Actions → Inspect

### 4.3 Maintenance Overlay Callouts

- Floating callouts labelling components with:
  - Part name, part number
  - Last maintenance date (if data available)
  - Maintenance interval
  - Status indicator (OK / Due / Overdue)
- Toggled per equipment from Actions tab
- Animated step indicators pointing to each component
- 2D/3D annotated diagrams for each equipment unit

### 4.4 P&ID Integration

| Feature | Implementation |
|---------|---------------|
| P&ID hotspots | Clickable 3D hotspot actors placed at P&ID reference points (up to 20 per client) |
| Visual indicator | Floating P&ID tag labels in world space; toggle visibility |
| Document launch | Click hotspot → opens P&ID document via OS PDF viewer / browser |
| Process line tracing | Highlight entire process line in-scene when P&ID tag selected |
| Linked navigation | Click P&ID tag in tree browser → camera sweeps to physical location |

### 4.5 Enhanced CVT Tools

| CVT Tool | Enhancement |
|----------|-------------|
| Annotation | Add category tags (safety, maintenance, design review); filter annotations by category; export annotation report |
| Measurement | Multi-point polyline (see Phase 3) |
| Laser pointer | Add distance readout; snap to surfaces |
| Multi-user | Role-based permissions; synchronized mode states; session recording |
| Bookmark | Organize bookmarks by category; share bookmarks across sessions |

### 4.6 Multi-User Session Enhancements

| Feature | Implementation |
|---------|---------------|
| Role-based permissions | Admin (full access), Engineer (Mode C + A), Viewer (Mode A only) |
| Synchronized mode | Session host controls mode; all participants see same mode state |
| Session recording | Record camera paths, interactions, annotations for playback |
| Playback mode | Replay recorded sessions with timeline scrubber |
| Session sharing | Export/import session recordings as files |

---

## Future Scope (Phase 5+)

> [!NOTE]
> These features are architecturally accounted for (interfaces exist, data tables have placeholder columns) but implementation is deferred.

| Feature | Notes | Architecture Preparation |
|---------|-------|--------------------------|
| Mode B — Training | SOP walkthroughs, safety simulations, quiz system, assessment logging | ModeManager has MODE_TRAINING enum; DT_SOPSteps table schema reserved |
| Simulation Data Visualization | File-based polling from external software; live data rendering on equipment | DT_Equipment has Data tab placeholder; `BP_SimDataManager` interface defined |
| Thermal/Safety Heatmap Overlay | Color-coded zones by risk/temperature | Zone system supports overlay materials; Data Table has zone risk fields |
| Construction Timeline Animation | Scrubber showing build sequence | DT_Equipment has construction_phase field placeholder |
| Multi-Language (Hindi/English) | String table localization | All UI text uses FText with string table references |
| Cloud Session Logging / LMS | Cloud sync of session data | Local JSON logging outputs in format compatible with future cloud API |
| Standalone Meta Quest APK | Untethered VR build | Optimization foundation supports separate VR quality tier |
| Snapshot Comparison Mode | Before/after plant states | Bookmark system stores full scene state; comparison requires UI only |

---

## Content Pipeline (Client Handoff)

| Asset | Required By | Format | Used In |
|-------|------------|--------|---------|
| Plant 3D project | Project kick-off | .dwg (Plant 3D) | Pipeline B (metadata export) |
| 3D scene via 3ds Max | Week 1 | .udatasmith via 3ds Max Datasmith export | Pipeline A (geometry) |
| Equipment metadata JSON | Week 1 (auto-generated) | JSON from Plant 3D Python export script | DT_Equipment, DT_ProcessLines |
| 2D CAD drawings | Week 2 | PNG/PDF per equipment | Drawings tab |
| P&ID documents | Week 2 (Mode C) | PDF | P&ID hotspot launch |
| SOP documentation | Deferred (Mode B) | PDF/Word | Future: training steps |
| Client branding | Week 1 | Logo PNG + accent color hex | OrionConfig.json |
| VR hardware profile | Week 1 | Headset model + PC GPU spec | Optimization targets |

---

## Platform Matrix

| Build | Target | Minimum Spec | Rendering | Notes |
|-------|--------|-------------|-----------|-------|
| Desktop | Windows .exe | GTX 1080 / RX 5700 | Lumen GI, full post-process | Primary development target |
| PC VR | Meta Quest Link / SteamVR | RTX 3080 recommended | Simplified Lumen or baked lighting | 72fps floor; some PP effects reduced |
| Quest APK | Meta Quest 2/3 | Standalone | Fully baked, simplified meshes | **Future scope** — separate optimization pass |

---

## Technical Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     OrionConfig.json                            │
│              (Per-client branding & feature flags)              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                 BP_OrionGameInstance                             │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────────────┐ │
│  │ ModeManager  │ │ ConfigLoader │ │ SessionManager (CVT+)   │ │
│  │              │ │              │ │ - Role permissions       │ │
│  │ - Showcase   │ │ - Client cfg │ │ - Mode sync              │ │
│  │ - Operations │ │ - Feature    │ │ - Session recording      │ │
│  │ - Training*  │ │   flags      │ │                          │ │
│  └──────┬───────┘ └──────┬───────┘ └──────────┬──────────────┘ │
└─────────┼────────────────┼────────────────────┼────────────────┘
          │                │                    │
┌─────────▼────────────────▼────────────────────▼────────────────┐
│                    Core Data Layer                               │
│  ┌───────────────┐ ┌────────────────┐ ┌──────────────────────┐ │
│  │ DT_Equipment  │ │ DT_Buildings   │ │ BP_MetadataLinker    │ │
│  │ DT_Rooms      │ │ DT_ProcessLines│ │ (auto-match actors   │ │
│  │ DT_Zones      │ │ DT_NPCs        │ │  to data table rows) │ │
│  │ DT_Waypoints  │ │ DT_Inspections │ │                      │ │
│  └───────┬───────┘ └────────┬───────┘ └──────────┬───────────┘ │
└──────────┼─────────────────┼─────────────────────┼─────────────┘
           │                 │                     │
┌──────────▼─────────────────▼─────────────────────▼─────────────┐
│                    Feature Systems                              │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────────┐ │
│  │ Hierarchy    │ │ Camera Sweep  │ │ Enhanced CVT Commands  │ │
│  │ Manager      │ │ Manager       │ │ - Multi-Point Measure  │ │
│  │ - Tree API   │ │ - Sweep to    │ │ - Hierarchical Explode │ │
│  │ - Search     │ │ - Highlight   │ │ - CropBox Overhaul     │ │
│  │ - Filter     │ │ - Drone mode  │ │ - Xray Enhanced        │ │
│  └──────────────┘ └───────────────┘ └────────────────────────┘ │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────────┐ │
│  │ Tour Manager │ │ NPC Manager   │ │ Zone Animation Manager │ │
│  │ - Waypoint   │ │ - Workers     │ │ - Trigger volumes      │ │
│  │ - Sequencer  │ │ - Guide       │ │ - Per-zone activation  │ │
│  └──────────────┘ └───────────────┘ └────────────────────────┘ │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────────┐ │
│  │ Interactive  │ │ Inspection    │ │ P&ID Manager           │ │
│  │ Objects      │ │ Manager       │ │ - Hotspots             │ │
│  │ - Doors      │ │ - Step walk   │ │ - Doc launch           │ │
│  │ - Gates      │ │ - Checklists  │ │ - Process line trace   │ │
│  │ - Wash stn   │ │ - Callouts    │ │                        │ │
│  └──────────────┘ └───────────────┘ └────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────────┐
│                    UI Layer (UMG)                                │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────────┐ │
│  │ WBP_OrionRoot│ │ WBP_TopBar    │ │ WBP_SidePanel          │ │
│  │ (Root)       │ │ WBP_BottomBar │ │ - TreeBrowser           │ │
│  │              │ │ WBP_Minimap   │ │ - EquipmentDetails      │ │
│  │              │ │ WBP_ToolMenu  │ │ - SearchPanel           │ │
│  └──────────────┘ └───────────────┘ └────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## Resolved Questions

> [!NOTE]
> **Q1: Plant 3D Python Script.** Resolved. The SQLite extractor `export_plant3d_metadata.py` is fully implemented and tested. It connects directly to AutoCAD Plant 3D SQLite databases (e.g. `Piping.db`), queries the `Equipment` and `EngineeringItems` tables, and exports clean metadata JSON schemas seamlessly.
> 
> **Q2: 2D CAD Drawings Format.** Resolved. Lock in **PNG format** for error-free dynamic runtime loading in Unreal Engine via native `UTexture2D` APIs. AutoCAD drawings will be exported as high-resolution PNG images, preventing runtime crashes or license issues associated with third-party PDF plugins.
> 
> **Q3: Equipment Animations.** Resolved. Lock in **Skeletal animations** authored in Blender/3ds Max and imported as skeletal meshes, ensuring optimal runtime play rates and lifelike motion without game-thread ticking overhead.
> 
> **Q4: NPC Character Models.** Resolved. Lock in **Mannequin-based characters** styled with safety vest and helmet assets, maintaining a high frame rate and fitting the clean industrial visual theme.
> 
> **Q5: Session Recording Scope.** Resolved. Captures camera paths, interaction states, and annotations (medium scope, ~MB/min) for optimal balance of playback fidelity and storage efficiency.

---

## Verification Plan

### Automated Tests
- Blueprint unit tests for Data Table loading and hierarchy queries
- Automated camera sweep tests (target reached within timeout)
- Search system tests (query → correct results for known data)
- Mode switching tests (permissions enforced correctly)
- Config loader tests (valid/invalid JSON handling)

### Manual Verification
- 60fps desktop / 72fps VR with Morde Foods scene loaded
- Full tree browser navigation with 6500+ equipment entries
- Search across P&ID tags, equipment names, process lines
- All CVT enhanced tools (Xray, Explode, CropBox, Measurement) working correctly
- Guided tour plays from start to finish
- Multi-user session with role-based permissions
- Client config swap test (change OrionConfig.json → app reflects changes)

### Performance Benchmarks
- Level load time with 6500 tagged actors < 30 seconds
- Search response time < 200ms for any query
- Camera sweep animation smooth (no hitches during interpolation)
- Zone animation activation/deactivation < 1 frame
- UI panel open/close transitions at 60fps
