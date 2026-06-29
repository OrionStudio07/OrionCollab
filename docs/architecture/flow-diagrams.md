# Flow Diagrams

> Canonical event sequences for all major features. See the full specification in [flow_diagrams.md](../../GoverningDocuments/flow_diagrams.md).

---

## Application Boot Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant GI as GameInstance
    participant CL as BP_ConfigLoader
    participant MM as ModeManager
    participant HM as HierarchyManager
    participant ML as MetadataLinker
    participant UI as WBP_OrionRoot

    App->>GI: Init()
    GI->>CL: Initialize()
    CL->>CL: LoadConfig()
    CL-->>GI: Config Ready

    App->>MM: BeginPlay()
    MM->>MM: SetMode(MODE_LAUNCHER)

    App->>HM: BeginPlay()
    HM->>HM: BuildTree() [Background Thread]

    App->>ML: BeginPlay()
    Note over ML: Waits for HM.OnTreeReady

    HM-->>ML: OnTreeReady
    ML->>ML: RunMatching()
    ML-->>HM: Actor References Populated

    GI-->>UI: CreateWidget(WBP_OrionRoot)
    UI->>MM: GetCurrentMode()
    UI->>UI: ConfigureUIForMode(MODE_LAUNCHER)
```

---

## Mode Transition Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as WBP_OrionRoot
    participant MM as ModeManager
    participant Net as GameState (Network)

    User->>UI: Select Mode (e.g., Showcase)
    UI->>MM: SetMode(MODE_SHOWCASE)
    MM->>MM: CanAccessMode(MODE_SHOWCASE, UserRole)
    
    alt Access Denied
        MM-->>UI: Permission Denied
    else Access Granted
        MM->>MM: Update Internal State
        MM->>Net: Broadcast to Clients
        MM-->>UI: OnModeChanged(LAUNCHER → SHOWCASE)
        UI->>UI: ConfigureUIForMode(MODE_SHOWCASE)
        UI->>UI: Animate Panel Transitions (0.3s)
    end
```

---

## Equipment Selection Flow

```mermaid
sequenceDiagram
    participant User
    participant TB as WBP_TreeBrowser
    participant HM as HierarchyManager
    participant ML as MetadataLinker
    participant CS as CameraSweepManager
    participant DP as Details Panel

    User->>TB: Click Equipment Node
    TB->>HM: OnEquipmentSelected(EquipmentID)
    HM->>ML: GetActorForEquipment(EquipmentID)
    ML-->>HM: Actor Reference
    HM-->>CS: SweepToActor(Actor)
    CS->>CS: Calculate Spline Path
    CS->>CS: Animate Camera (smooth transition)
    HM-->>DP: Display Equipment Metadata
    DP->>DP: Show Overview/Components/Actions/Drawings tabs
```

---

## Search Flow

```mermaid
sequenceDiagram
    participant User
    participant SB as Search Bar
    participant HM as HierarchyManager
    participant UI as Results Panel

    User->>SB: Type Query "P-101"
    SB->>SB: Debounce (200ms)
    SB->>HM: SearchAll("P-101")
    
    Note over HM: Indexed fields: DisplayName,<br/>PIDTag, ProcessLine,<br/>RoomName, BuildingName
    
    HM->>HM: Case-insensitive substring match
    HM->>HM: Levenshtein fuzzy matching
    HM->>HM: Check cache for repeat queries
    HM-->>UI: TArray<FSearchResult>
    
    UI->>UI: Group by Category<br/>(Building/Room/Equipment/ProcessLine)
    UI->>UI: Display with category icons
```

---

## MetadataLinker Matching Flow

```mermaid
sequenceDiagram
    participant ML as MetadataLinker
    participant Scene as Level Actors
    participant DT as Data Tables

    ML->>Scene: Scan actors with "Datasmith" tag
    
    loop For Each Actor
        ML->>ML: Extract candidate name
        ML->>ML: Normalize (strip SM_, BP_, lowercase)
        ML->>DT: Match against DT_Equipment.EquipmentID
        
        alt Exact Match
            ML->>ML: Confidence: HIGH
        else Contains Match
            ML->>ML: Confidence: MEDIUM
        else Levenshtein ≤ 3
            ML->>ML: Confidence: LOW (flagged)
        else No Match
            ML->>ML: Add to unmatched list
        end
        
        ML->>Scene: Tag actor with EquipmentID
    end
    
    ML-->>ML: Generate Report<br/>{matched: N, unmatched: N, ambiguous: N}
```
