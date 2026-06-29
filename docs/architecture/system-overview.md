# System Architecture Overview

> Derived from the [Technical Reference Document](../../GoverningDocuments/trd.md)

---

## Engine & Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Engine | Unreal Engine | 5.8 | Runtime, editor, packaging |
| Template | CollabViewer Template (CVT) | UE5.8 bundled | Multi-user, tools, pawn hierarchy |
| Rendering | Lumen (desktop) / Baked (VR) | Native | GI, reflections |
| UI | UMG (Unreal Motion Graphics) | Native | All in-game UI widgets |
| Data | UE5 Data Tables + JSON config | Native | Equipment metadata, tour waypoints, NPC defs |
| Networking | CVT session system | Native | Multi-user collaboration |
| VR | OpenXR via SteamVR / Meta Quest Link | Native | PC tethered VR |
| CAD Pipeline | Datasmith (3ds Max exporter) | UE5.8 bundled | Geometry import |
| Metadata | Python 3.x (Plant 3D script) | External | Tag/metadata export |

---

## Module Architecture

Modules are classified into four types based on lifecycle and communication pattern:

```mermaid
graph TB
    subgraph "Game Instance (Persists Across Levels)"
        CL["BP_ConfigLoader<br/>OrionConfig.json parsing"]
    end

    subgraph "World Subsystems (Per-Level Lifecycle)"
        MM["BP_OrionModeManager<br/>Mode state machine"]
        HM["BP_HierarchyManager<br/>Equipment tree + search"]
        ML["BP_MetadataLinker<br/>Actor ↔ DataTable matching"]
        TM["BP_TelemetryManager<br/>Analytics logging"]
    end

    subgraph "Command Components (CVT Tool Lifecycle)"
        XR["Enhanced Xray"]
        EX["Enhanced Explode"]
        CB["Enhanced CropBox"]
        MS["Enhanced Measurement"]
        SS["Snapshot Tool"]
        RS["RatioScale Tool"]
    end

    subgraph "Level Actors (Placed/Spawned)"
        TR["TourManager"]
        IM["InspectionManager"]
        NM["NPCManager"]
        ZA["ZoneAnimationManager"]
    end

    CL -->|Provides Config| MM
    CL -->|Feature Flags| HM
    MM -->|OnModeChanged| HM
    MM -->|OnModeChanged| TR
    HM -->|OnEquipmentSelected| ML
    ML -->|Actor References| XR
    ML -->|Actor References| EX
```

### Module Classification

| Type | UE5 Class | Lifecycle | Examples |
|------|-----------|-----------|----------|
| **World Subsystem** | `UWorldSubsystem` | Created per-world; destroyed on level unload | ModeManager, HierarchyManager, MetadataLinker, TelemetryManager |
| **Command Component** | `BP_BaseCommandComponent` child | Follows CVT lifecycle: `Bind_Options → Execute → Disabled` | Xray, Explode, CropBox, Measurement, Snapshot, RatioScale |
| **Actor** | `AActor` | Placed in level or spawned at runtime | TourManager, InspectionManager, NPCManager |
| **Game Instance** | `UGameInstance` child | Persists across level loads | ConfigLoader |

---

## Mode System

The application operates in distinct modes, each targeting a different user persona:

```mermaid
stateDiagram-v2
    [*] --> MODE_LAUNCHER
    MODE_LAUNCHER --> MODE_SHOWCASE: Select Showcase
    MODE_LAUNCHER --> MODE_OPERATIONS: Select Operations
    MODE_SHOWCASE --> MODE_OPERATIONS: Mode Switch
    MODE_OPERATIONS --> MODE_SHOWCASE: Mode Switch
    MODE_SHOWCASE --> MODE_LAUNCHER: Exit to Lobby
    MODE_OPERATIONS --> MODE_LAUNCHER: Exit to Lobby

    state MODE_LAUNCHER {
        [*] --> RoleSelection
        RoleSelection --> SettingsPanel
    }
    state MODE_SHOWCASE {
        [*] --> GuidedTour
        GuidedTour --> FreeExploration
        FreeExploration --> ToolUsage
    }
    state MODE_OPERATIONS {
        [*] --> EquipmentBrowsing
        EquipmentBrowsing --> DetailInspection
        DetailInspection --> MaintenanceOverlay
    }
```

| Mode | Enum Value | Default Pawn | Target Persona |
|------|-----------|--------------|----------------|
| `MODE_LAUNCHER` | 0 | BP_LoginMenuPawn | All users |
| `MODE_SHOWCASE` | 1 | OrbitMode (switchable) | Visitors / Investors |
| `MODE_OPERATIONS` | 2 | WalkMode (switchable) | Plant Engineers |
| `MODE_TRAINING` | 3 | Reserved for v2 | Trainees |

---

## Data Flow

```mermaid
flowchart LR
    subgraph "Content Pipeline"
        P3D["AutoCAD Plant 3D"] -->|Python Script| JSON["Metadata JSON"]
        P3D -->|3ds Max Export| DS["Datasmith Scene"]
    end

    subgraph "UE5 Import"
        JSON -->|CSV Conversion| DT["Data Tables<br/>DT_Equipment<br/>DT_Buildings<br/>DT_Rooms<br/>DT_ProcessLines"]
        DS -->|Datasmith Import| ACT["Scene Actors"]
    end

    subgraph "Runtime Linking"
        DT --> ML2["MetadataLinker"]
        ACT --> ML2
        ML2 -->|"Matched Pairs<br/>(>90% rate)"| HM2["HierarchyManager"]
        HM2 --> UI["UI Widgets"]
    end
```

---

## C++ Subsystem Layer

The following modules are implemented in C++ for performance-critical operations:

| Module | Header | Purpose | Key API |
|--------|--------|---------|---------|
| `UOrionHierarchyManager` | `OrionHierarchyManager.h` | Equipment tree building + fuzzy search | `BuildTree()`, `SearchAll()`, `GetEquipmentByRoom()` |
| `UOrionMetadataLinker` | `OrionMetadataLinker.h` | Datasmith actor ↔ DataTable matching | `RunMatching()`, `GetActorForEquipment()` |
| `UOrionModeManager` | `OrionModeManager.h` | Mode state machine + role permissions | `SetMode()`, `CanAccessMode()` |
| `UOrionConfigSubsystem` | `OrionConfigSubsystem.h` | JSON config loading + validation | `LoadConfig()`, `GetConfig()` |
| `UOrionCameraSweepManager` | `OrionCameraSweepManager.h` | Smooth camera transitions | `SweepToLocation()`, `SweepToActor()` |

---

## Performance Budgets

| Metric | Budget | Source |
|--------|--------|--------|
| Desktop FPS | ≥60 fps | Release gate |
| VR FPS | ≥72 fps | Release gate |
| Level load time | <30 seconds (6500 actors) | Release gate |
| Search latency | <200ms any query | HierarchyManager spec |
| Tree browser scroll | 60fps with 6500 entries | Virtualized ListView |
| MetadataLinker match rate | >90% of Datasmith actors | Release gate |
