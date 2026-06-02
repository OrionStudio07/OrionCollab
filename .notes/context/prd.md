# Orion Studios — Product Requirement Document (PRD)
**Version 1.0.0** · Orion Studios · 2026-05-31

---

## Problem Statement

Industrial plants (food processing, chemical, manufacturing) need a way to showcase their facilities to investors, onboard employees, and support engineering inspections — without requiring physical access. Current solutions are either:

1. **Static renders/videos:** Non-interactive; can't answer investor questions on-the-fly
2. **Generic VR walkthroughs:** Lack engineering data integration (P&ID, specs, process lines)
3. **CAD viewers (Navisworks, BIM360):** Powerful but ugly, slow, and intimidating for non-technical stakeholders

Plant operators need a **single application** that serves three distinct audiences (investors, trainees, engineers) with a premium visual experience, real equipment data, and multi-user collaboration — all powered by their existing AutoCAD Plant 3D models.

---

## Solution

**Orion Studios** is a reusable Unreal Engine 5.8 application built on the CollabViewer Template (CVT) that transforms AutoCAD Plant 3D exports into an interactive, photorealistic industrial visualization platform.

**Key differentiators:**

- **Dual-import pipeline:** Geometry from 3ds Max + metadata from Plant 3D Python script, auto-matched by tag
- **Mode-based access:** Role-based launcher routes users to Showcase (investors), Operations (engineers), or Training (v2)
- **Client-swappable:** Per-client JSON config changes branding, features, and plant data without touching platform code
- **Multi-user collaboration:** Built-in collaborative sessions with role-based permissions and session recording
- **Desktop + PC VR:** Single codebase targets both desktop and tethered VR experiences

---

## Actors & Personas

| Actor | Description | Primary Mode | Technical Level |
|-------|-------------|-------------|-----------------|
| **Visitor / Investor** | Non-technical stakeholders touring the plant for due diligence or sales | Mode A — Showcase | None |
| **Plant Engineer** | Operations/maintenance engineers inspecting equipment and accessing P&ID docs | Mode C — Operations | High |
| **Trainee / Employee** | New hires completing onboarding and safety training | Mode B — Training (v2) | Low-Medium |
| **Session Admin** | IT/management controlling multi-user sessions and roles | Launcher + All Modes | Medium |
| **Content Author (Sho/Rohit)** | Developers setting up new client plant scenes in UE5 Editor | Editor Only | Expert |

---

## User Stories

### Launcher & Configuration

1. As a **Visitor**, I want to see the client's branded logo and plant name on launch, so that I know I'm in the right application.
2. As a **Session Admin**, I want to select my role from a picker, so that I get the correct mode and permissions.
3. As a **Session Admin**, I want to configure graphics quality and VR toggle from the settings panel, so that performance matches my hardware.
4. As an **Engineer**, I want to switch between Showcase and Operations mode in-app, so that I can give a tour then dive into specs without restarting.
5. As a **Content Author**, I want to edit `OrionConfig.json` and see changes hot-reload in-editor, so that I can iterate on client branding without rebuilding.
6. As a **Content Author**, I want the app to show a warning banner if the config file is missing, so that I know to fix it before a demo.

### Navigation (All Modes)

7. As a **Visitor**, I want to browse a collapsible tree of Buildings > Rooms > Equipment, so that I can understand the plant's spatial organization.
8. As a **Visitor**, I want to click any tree node and have the camera sweep smoothly to that location, so that navigation feels premium.
9. As an **Engineer**, I want to type a P&ID tag (e.g., `P-101`) into a search bar and teleport directly to that equipment, so that I save time finding specific units.
10. As a **Visitor**, I want search results grouped by category (Building, Room, Equipment, Process Line) with icons, so that I can distinguish between result types.
11. As an **Engineer**, I want to click any point on a 2D minimap and teleport there, so that I can navigate large plants efficiently.
12. As a **Visitor**, I want the minimap to show my current position and heading as a rotating arrow, so that I stay oriented.
13. As a **Visitor**, I want floor selector tabs (F1, F2, F3) on the minimap, so that I can switch between floors in multi-story buildings.
14. As a **Visitor**, I want to use FlyMode (free aerial camera) to get overhead perspectives, so that I can see the plant layout from above.
15. As a **Visitor**, I want a bottom carousel of key equipment thumbnails that I can click to teleport sequentially, so that I can follow the process flow.
16. As an **Engineer**, I want search to match fuzzy queries across equipment names, tags, and process line codes, so that typos don't block me.
17. As a **Visitor**, I want recent searches saved for quick re-access, so that I don't retype commonly-visited equipment.

### Mode A — Showcase

18. As a **Visitor**, I want a guided tour that automatically moves the camera along a scripted path with info panels at each stop, so that I get a hands-free overview.
19. As a **Visitor**, I want Play/Pause/Next/Previous controls during the guided tour, so that I can control the pace.
20. As a **Visitor**, I want a progress bar showing my position in the tour, so that I know how much is left.
21. As a **Visitor**, I want to see NPC workers performing tasks in each zone, so that the plant feels alive and realistic.
22. As a **Visitor**, I want doors to open automatically as I approach, so that the experience feels immersive.
23. As a **Visitor**, I want to see conveyor belts and mixers running with animations, so that I understand the production flow.
24. As a **Visitor**, I want zone-based animation activation (only the current zone's equipment animates), so that performance stays smooth.
25. As a **Visitor**, I want premium Lumen lighting with HDRI sky and post-process effects, so that the plant looks photorealistic.
26. As an **Engineer**, I want to toggle Global Xray to see all pipes, ducts, and structural elements through walls, so that I can understand hidden routing.
27. As an **Engineer**, I want per-equipment Xray that only affects the selected unit, so that context is preserved.
28. As an **Engineer**, I want Xray materials color-coded by system type (pipes=blue, structure=white, electrical=yellow), so that I can distinguish systems at a glance.
29. As an **Engineer**, I want to place a section cut plane through any point in the plant, so that I can see cross-sections of equipment and rooms.
30. As an **Engineer**, I want section-fill hatching on cut faces (engineering-style diagonal lines), so that sections look professional.
31. As an **Engineer**, I want to export a 2D section capture as PNG, so that I can include it in reports.
32. As an **Engineer**, I want hierarchical explode (Level 1: assemblies, Level 2: sub-components, Level 3: individual parts), so that I can understand equipment construction.
33. As an **Engineer**, I want building floor explode (floors separate vertically), so that I can see multi-story layouts.
34. As an **Engineer**, I want floating callout labels on each exploded component, so that I can identify parts.
35. As an **Engineer**, I want a distance slider to continuously control explosion distance, so that I can find the right separation.
36. As an **Engineer**, I want to measure multi-point polyline distances with segment lengths, total length, and angles, so that I can do field verification.
37. As an **Engineer**, I want AutoCAD-style snapping (vertex, edge, midpoint, center), so that measurements are precise.
38. As an **Engineer**, I want to toggle measurement units between Meters, Feet, and Millimeters, so that I work in familiar units.
39. As an **Engineer**, I want to save labeled measurements for later reference, so that I can compare over time.
40. As a **Visitor**, I want to take a Snapshot of the current view and save it with a timestamp, so that I can document the tour.

### Mode C — Operations

41. As an **Engineer**, I want to click any equipment and see a tabbed details panel (Overview, Components, Actions, Drawings, Data), so that all information is in one place.
42. As an **Engineer**, I want the Overview tab to show name, P&ID tag, process line, manufacturer, model, and key specs, so that I have quick identification.
43. As an **Engineer**, I want the Components tab to show a hierarchical parts tree with replacement intervals and materials, so that I can plan maintenance.
44. As an **Engineer**, I want the Actions tab to have buttons for Explode, Isolate, Xray, Animate, and Inspect, so that I can interact with the equipment in context.
45. As an **Engineer**, I want a 2D CAD drawing viewer (pan/zoom/fullscreen) in the Drawings tab, so that I can reference technical drawings without leaving the app.
46. As an **Engineer**, I want to launch a step-by-step inspection walkthrough (up to 8 steps per equipment) from the Actions tab, so that I can follow a checklist.
47. As an **Engineer**, I want each inspection step to show a description, expected condition, and photo reference while highlighting the target component, so that I know exactly what to check.
48. As an **Engineer**, I want maintenance overlay callouts showing part name, last maintenance date, interval, and status (OK/Due/Overdue), so that I can prioritize work.
49. As an **Engineer**, I want to click a P&ID hotspot in 3D space and have it open the P&ID PDF document in my OS viewer, so that I can cross-reference.
50. As an **Engineer**, I want to select a process line tag and see the entire pipe path highlighted with pulsing flow animation, so that I can trace the process.
51. As an **Engineer**, I want annotations with category tags (safety, maintenance, design review), so that notes are organized.
52. As an **Engineer**, I want to filter annotations by category, so that I only see relevant notes.

### Multi-User & Session

53. As a **Session Admin**, I want role-based permissions (Admin, Engineer, Viewer) so that visitors can't modify annotations.
54. As a **Session Admin**, I want synchronized mode state, so that all participants see the same mode when I switch.
55. As a **Session Admin**, I want to record camera paths and interactions for playback, so that I can review sessions offline.
56. As a **Session Admin**, I want to replay recorded sessions with a timeline scrubber, so that I can jump to key moments.
57. As a **Session Admin**, I want to export/import session recordings as files, so that I can share them.

### VR

58. As a **Visitor in VR**, I want the same tour, navigation, and visualization features at 72fps minimum, so that the experience is comfortable.
59. As an **Engineer in VR**, I want to interact with equipment, open details panels, and use tools, so that VR is a full-featured experience.

### Content Authoring (Editor-Only)

60. As a **Content Author**, I want an Equipment Tagger widget to batch-assign IDs and zones to selected actors, so that scene setup is fast.
61. As a **Content Author**, I want a Zone Painter widget to draw trigger volumes with visual feedback, so that zones are easy to configure.
62. As a **Content Author**, I want a Tour Path Editor to click waypoints in the viewport and auto-generate DT_TourWaypoints rows, so that tour creation is visual.
63. As a **Content Author**, I want a Validation Pass that checks for unmatched actors, missing textures, and broken references, so that I catch errors before shipping.
64. As a **Content Author**, I want a Config Generator widget to fill in client details and export a validated OrionConfig.json, so that config creation is error-free.

### Analytics & Telemetry

65. As a **Session Admin**, I want local JSON logs of mode transitions, equipment views, tool usage, and tour completions, so that I can demonstrate engagement to clients.
66. As a **Session Admin**, I want telemetry output in a format compatible with future cloud upload, so that we can add cloud analytics later.

### Accessibility

67. As a **Visitor**, I want three text size presets (Standard, Medium, Large), so that I can read UI text comfortably.
68. As a **Visitor**, I want a high-contrast mode toggle, so that panel borders and text are easier to read in bright rooms.
69. As an **Engineer**, I want status indicators to use shapes and pulse animations (not just color), so that colorblind users can distinguish states.
70. As a **Visitor**, I want full keyboard navigation across all UI panels, so that I can navigate without a mouse.

---

## Implementation Decisions

### Architecture

- **Engine:** Unreal Engine 5.8 with CollabViewer Template (CVT) as base
- **Mode System:** `BP_OrionModeManager` as a World Subsystem (not Game Instance) — resets on level load, replicates via Game State
- **Tool Architecture:** All enhanced tools extend CVT's `BP_BaseCommandComponent` to inherit the `EventExecuteAfterSpawnPawn → Bind_Options → Execute → Disabled` lifecycle, SaveGame serialization, and multi-user replication
- **Standalone Systems:** ModeManager, HierarchyManager, MetadataLinker, TelemetryManager are World Subsystems (not command components) because they're always-active infrastructure
- **Data Layer:** UE5 Data Tables (DT_Equipment, DT_Buildings, DT_Rooms, DT_ProcessLines, DT_Zones, DT_NPCs, DT_TourWaypoints, DT_InspectionSteps) populated from JSON/CSV import
- **Config:** Per-client `OrionConfig.json` with schema validation, graceful fallback to embedded defaults, and hot-reload in dev builds
- **Utilities:** `CommonFunctions_Orion` as a new Blueprint Function Library (does not modify CVT's `CommonFunctions_CV`)
- **SaveGame:** All Orion features hook into CVT's existing SaveGame system via `EventBindSaveState` / `EventBindLoadState` delegates
- **Localization:** All display text uses `FText` with `ST_Orion_UI.csv` String Table from day one (Hindi/English deferred)

### Pawn Architecture

- No new Drone pawn — FlyMode pawn extended with spline movement overlay
- MODE_LAUNCHER maps to BP_LoginMenuPawn
- MODE_SHOWCASE defaults to OrbitMode, switchable to WalkMode/FlyMode
- MODE_OPERATIONS defaults to WalkMode, switchable to OrbitMode/FlyMode
- VR toggle → BP_VRPawn (any mode)

### Content Pipeline

- **Pipeline A (Geometry):** AutoCAD Plant 3D → 3ds Max (QA cleanup) → Datasmith → UE5
- **Pipeline B (Metadata):** AutoCAD Plant 3D → Python export script → JSON → Data Tables
- **Pipeline C (Matching):** `BP_MetadataLinker` auto-matches imported actors to Data Table rows by name/ID pattern

### Multi-User

- Extends CVT's existing session management (not a replacement)
- Adds role-based permissions, synchronized mode state, and session recording on top
- Session recording stores camera positions + interactions + annotations (medium scope, ~MB/min)

---

## Testing Decisions

### What Makes a Good Test
- Tests verify **external behavior** visible to users, not internal implementation details
- Tests use **known reference data** (10 pre-configured test equipment items with expected results)
- Performance tests measure against **concrete thresholds** (60fps, <200ms, <30s)

### Modules Under Test

| Module | Test Type | Key Assertions |
|--------|-----------|---------------|
| Config Loader | Unit | Valid JSON → correct struct; malformed JSON → fallback defaults with warning; missing file → embedded defaults |
| Data Table Loading | Unit | CSV/JSON import → correct row count; FindRow returns correct data |
| Hierarchy Manager | Unit | GetBuildingList returns all buildings; GetEquipmentByRoom returns correct filtered set; search returns fuzzy matches |
| MetadataLinker | Integration | Known scene + known metadata → >90% match rate; unmatched report generated |
| Mode Manager | Integration | SetMode changes UI visibility; CanAccessMode enforces role restrictions |
| Camera Sweep | Integration | Sweep to known location arrives within timeout; no clipping through geometry |
| Search System | Performance | Any query returns in <200ms for 6500 entries |
| Tree Browser | Performance | Scrolling 6500 entries maintains 60fps |
| Snap System | Unit | Known geometry → correct snap point positions (vertex, edge, midpoint, center) |
| SaveGame | Integration | Save state → load state → all tool states match |
| Minimap Teleport | Integration | Click UV coordinate → lands on valid floor position |

### Prior Art
- CVT's existing SaveGame tests provide the pattern for save/load round-trip testing
- Blueprint unit test framework used throughout

---

## Out of Scope (v1)

| Feature | Reason | Architecture Prep |
|---------|--------|-------------------|
| Mode B — Training | Deferred to v2; scope too large for v1 | MODE_TRAINING enum reserved; DT_SOPSteps, DT_QuizQuestions schemas defined |
| Live Simulation Data | Requires external software integration | Data tab placeholder in Equipment Details; BP_SimDataManager interface defined |
| Thermal/Safety Heatmap | Requires simulation data | Zone system supports overlay materials |
| Construction Timeline | Requires per-equipment phase data | DT_Equipment has construction_phase placeholder |
| Hindi/English Localization | FText prep in place; translation effort deferred | ST_Orion_UI.csv String Table with English entries |
| Cloud Session Logging | Local JSON sufficient for v1 | Telemetry format compatible with future cloud API |
| Standalone Quest APK | Requires separate optimization pass | VR quality tier supported in optimization foundation |
| Client Plugin System | No client yet needs custom extensions | IOrionFeaturePlugin interface defined; Content/ClientPlugins/ folder reserved |

---

## Acceptance Criteria (Release Gate)

| Criterion | Threshold |
|-----------|-----------|
| Desktop FPS | ≥60fps with Morde Foods scene loaded |
| VR FPS | ≥72fps with simplified lighting |
| Level load time | <30 seconds for 6500 tagged actors |
| Search latency | <200ms for any query |
| Tree browser scroll | 60fps with 6500 entries |
| Guided tour | Plays start-to-finish with all waypoints |
| Config swap | Change OrionConfig.json → app reflects changes |
| MetadataLinker match rate | >90% of known Datasmith actors |
| Multi-user session | 2+ users with role-based permissions functional |
| All enhanced tools | Xray, Explode, CropBox, Measurement, Snapshot, RatioScale, DataSmith working |

---

## Further Notes

- **Reference client data:** Morde Foods P2 Manufacturing Plant — 6500 tags, 1394 instrumentation points, ~500 process lines, ~200 unique equipment
- **Team:** Sho (lead developer), Rohit (content author/co-developer)
- **Open questions on Q1-Q5** (Plant 3D Python access, CAD drawing format, animation authoring, NPC character models, session recording scope) require client input before Phase 1 begins

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
