# Orion Studios — System Flow Diagrams
**Version 1.0.0** · Orion Studios · 2026-05-31

---

## 1. Application Boot Flow

```mermaid
flowchart TD
    A[App Launch] --> B[BP_OrionGameInstance::Init]
    B --> C[BP_ConfigLoader::LoadConfig]
    C --> D{OrionConfig.json exists?}
    D -- Yes --> E[Parse JSON]
    D -- No --> F[Use Embedded Defaults]
    F --> G[Show Warning Banner]
    E --> H{Valid JSON?}
    H -- Yes --> I[BP_ConfigValidator::Validate]
    H -- No --> F
    I --> J{All fields valid?}
    J -- Yes --> K[Store Config Struct]
    J -- Partial --> L[Use defaults for invalid fields]
    L --> M[Show Toast: invalid fields list]
    M --> K
    K --> N[Load Login Level]
    N --> O[Spawn BP_LoginMenuPawn]
    O --> P[Display Branded Launcher]
    P --> Q{User selects role}
    Q --> R[BP_OrionModeManager::SetMode]
    R --> S[Load Main Level]
    S --> T[BP_MetadataLinker::RunMatching]
    S --> U[BP_HierarchyManager::BuildTree]
    T --> V{Match rate > 90%?}
    V -- Yes --> W[Fire OnMatchingComplete]
    V -- No --> X[Show Unmatched Report]
    X --> W
    U --> Y[Fire OnTreeReady]
    W --> Z[Enable Navigation UI]
    Y --> Z
    Z --> AA[App Ready]
    G --> N
```

---

## 2. Mode Switching Flow

```mermaid
flowchart TD
    A[User requests mode switch] --> B[BP_OrionModeManager::SetMode]
    B --> C{CanAccessMode?}
    C -- No --> D[Show Permission Denied Toast]
    C -- Yes --> E[Store old mode]
    E --> F[Update internal mode state]
    F --> G[Fire OnModeChanged delegate]
    
    G --> H[WBP_OrionRoot::HandleModeChanged]
    H --> I[Reconfigure panel visibility]
    H --> J[Update toolbar buttons]
    H --> K[Update mode indicator text]
    
    G --> L[Command Components]
    L --> M[Enable/Disable per mode config]
    
    G --> N[BP_NPCManager]
    N --> O{Mode == SHOWCASE?}
    O -- Yes --> P[Activate NPC animations]
    O -- No --> Q[Deactivate NPCs]
    
    G --> R[BP_ZoneAnimationManager]
    R --> S{Mode == SHOWCASE?}
    S -- Yes --> T[Enable zone triggers]
    S -- No --> U[Disable zone triggers]
    
    G --> V[BP_TelemetryManager]
    V --> W[Log ModeTransition event]
    
    G --> X{Multi-user session?}
    X -- Yes --> Y[Broadcast to all clients via GameState]
    X -- No --> Z[Local only]
```

---

## 3. Equipment Selection Flow

```mermaid
flowchart TD
    A[User action] --> B{Source?}
    
    B -- Tree Browser Click --> C[WBP_TreeBrowser::OnNodeClicked]
    B -- Search Result Click --> D[WBP_SearchBar::OnResultSelected]
    B -- Minimap Click --> E[WBP_Minimap::OnMapClicked]
    B -- 3D Viewport Click --> F[Line trace → hit actor]
    B -- Carousel Click --> G[WBP_EquipmentCarousel::OnThumbnailClicked]
    
    C --> H[Get EquipmentID from node]
    D --> H
    F --> I{Actor has EquipmentID tag?}
    I -- Yes --> H
    I -- No --> J[No selection - ignore]
    G --> H
    
    E --> K[Convert UV to World XY]
    K --> L[Line trace down for floor]
    L --> M{Valid floor hit?}
    M -- Yes --> N[Teleport to floor position]
    M -- No --> O[Show error indicator on minimap]
    
    H --> P[BP_HierarchyManager::SelectEquipment]
    P --> Q[Fire OnEquipmentSelected delegate]
    
    Q --> R[BP_CameraSweepManager::SweepTo]
    R --> S[Calculate optimal view distance]
    S --> T[Plan collision-free path]
    T --> U[Interpolate camera along path]
    U --> V[Apply pulsing outline highlight]
    
    Q --> W[WBP_EquipmentDetails::Populate]
    W --> X[Load DT_Equipment row]
    X --> Y[Fill Overview tab]
    X --> Z[Prepare lazy tabs]
    
    Q --> AA[WBP_TreeBrowser::HighlightNode]
    AA --> AB[Expand ancestor nodes]
    AA --> AC[Scroll to selected node]
    
    Q --> AD[BP_ZoneAnimationManager::ActivateZone]
    AD --> AE[Start equipment zone animations]
    
    Q --> AF[BP_TelemetryManager::LogEquipmentView]
```

---

## 4. Guided Tour Flow

```mermaid
flowchart TD
    A[User starts tour] --> B[BP_GuidedTourManager::StartTour]
    B --> C[Load DT_TourWaypoints for selected tour]
    C --> D[Sort by Sequence]
    D --> E[Set CurrentWaypoint = 0]
    E --> F[Navigate to waypoint]
    
    F --> G[BP_CameraSweepManager::SweepTo waypoint transform]
    G --> H[On arrival: show info panel]
    H --> I[Play VO audio if available]
    I --> J[Update progress bar]
    
    J --> K{User input?}
    K -- Next --> L{More waypoints?}
    L -- Yes --> M[CurrentWaypoint++]
    M --> F
    L -- No --> N[Tour Complete]
    
    K -- Previous --> O{CurrentWaypoint > 0?}
    O -- Yes --> P[CurrentWaypoint--]
    P --> F
    O -- No --> Q[Stay at first waypoint]
    
    K -- Pause --> R[Pause camera movement]
    R --> S{Resume pressed?}
    S -- Yes --> F
    
    K -- Exit --> T[Exit Tour Mode]
    T --> U[Restore free camera]
    U --> V[Hide tour UI]
    
    N --> W[Show completion screen]
    W --> X[BP_TelemetryManager::LogTourCompletion]
    X --> V

    style N fill:#00D4AA,color:#000
    style T fill:#FF5252,color:#fff
```

---

## 5. Measurement Tool Flow with Snap System

```mermaid
flowchart TD
    A[User activates Measurement tool] --> B[BP_OrionMeasurement::Execute]
    B --> C[Enable cursor tracking]
    
    C --> D[Mouse move event]
    D --> E[Line trace from camera through cursor]
    E --> F{Hit static mesh?}
    F -- No --> G[Show free cursor]
    F -- Yes --> H{Snap enabled?}
    
    H -- No --> I[Use raw hit position]
    H -- Yes --> J[BP_SnapManager::FindSnap]
    
    J --> K[Get UStaticMesh vertex buffer]
    K --> L[Transform vertices to world space]
    L --> M{Nearest vertex within 5cm?}
    M -- Yes --> N[Snap to vertex - show diamond]
    M -- No --> O[Build edge list from index buffer]
    O --> P{Nearest edge within 5cm?}
    P -- Yes --> Q{Within 2.5cm of midpoint?}
    Q -- Yes --> R[Snap to midpoint - show circle]
    Q -- No --> S[Snap to edge point]
    P -- No --> T{Within 5cm of bbox center?}
    T -- Yes --> U[Snap to center - show square]
    T -- No --> I
    
    N --> V[Display snap indicator]
    R --> V
    S --> V
    U --> V
    I --> V
    
    V --> W{Left click?}
    W -- Yes --> X[Place measurement point]
    X --> Y{First point?}
    Y -- Yes --> Z[Start polyline]
    Y -- No --> AA[Add segment]
    AA --> AB[Calculate segment length]
    AA --> AC[Calculate angle at vertex]
    AA --> AD[Update total length]
    
    W -- No --> D
    
    AB --> AE[Display segment label]
    AC --> AF[Display angle label]
    AD --> AG[Update readout in bottom bar]
    
    AG --> AH{Double-click or Enter?}
    AH -- Yes --> AI{Path closed?}
    AI -- Yes --> AJ[Calculate polygon area]
    AI -- No --> AK[Finalize open polyline]
    AJ --> AL[Display area label]
    AK --> AL
    AL --> AM[Prompt: Save measurement?]
    AM -- Yes --> AN[Save to SaveGame with label]
    AM -- No --> AO[Keep as temporary]
    
    AH -- No --> D
```

---

## 6. CropBox Section-Fill Flow

```mermaid
flowchart TD
    A[User activates CropBox] --> B[BP_OrionCropBox::Execute]
    B --> C{Plane or Cube mode?}
    
    C -- Plane --> D[Spawn infinite clip plane actor]
    C -- Cube --> E[Spawn bounded clip volume actor]
    
    D --> F[Attach UE5.8 transform gizmo]
    E --> F
    
    F --> G[User manipulates gizmo]
    G --> H[Update clip plane/volume position]
    
    H --> I[Custom Depth Material Pass]
    I --> J[Assign custom stencil values to meshes]
    J --> K{Equipment type?}
    K -- Pipe --> L[Stencil value = 1]
    K -- Structure --> M[Stencil value = 2]
    K -- Electrical --> N[Stencil value = 3]
    K -- Other --> O[Stencil value = 4]
    
    L --> P[Post-Process Material reads stencil buffer]
    M --> P
    N --> P
    O --> P
    
    P --> Q[Identify pixels at stencil transition boundary]
    Q --> R{Fill mode?}
    R -- Solid --> S[Render solid color by stencil value]
    R -- 45° Hatching --> T[Render diagonal line pattern]
    R -- Cross-Hatching --> U[Render cross-hatch pattern]
    R -- Color by Type --> V[Color map: pipe=blue, struct=white, elec=yellow]
    
    S --> W[Render section view]
    T --> W
    U --> W
    V --> W
    
    W --> X{User requests 2D export?}
    X -- Yes --> Y[SceneCaptureComponent2D aligned with plane]
    Y --> Z[Set orthographic projection]
    Z --> AA[Capture to 2048x2048 render target]
    AA --> AB[Export via ImageWriteQueue]
    AB --> AC[Save PNG to disk]
    AC --> AD[Show save confirmation toast]
    X -- No --> G
```

---

## 7. Minimap Click-to-Teleport Flow

```mermaid
flowchart TD
    A[User clicks minimap widget] --> B[Capture click position in widget space]
    B --> C[Normalize to 0-1 UV space]
    C --> D[Get minimap camera orthographic bounds]
    D --> E["World_X = OrthoMin_X + U × (OrthoMax_X - OrthoMin_X)"]
    E --> F["World_Y = OrthoMin_Y + V × (OrthoMax_Y - OrthoMin_Y)"]
    F --> G["Line trace from (World_X, World_Y, MaxWorldZ) downward"]
    
    G --> H{Hit result?}
    H -- No --> I[Show red X on minimap at click point]
    I --> J[Fade X after 1 second]
    
    H -- Yes --> K{Walkable surface?}
    K -- No --> I
    K -- Yes --> L[Sphere overlap check at destination]
    L --> M{Inside solid geometry?}
    M -- Yes --> I
    M -- No --> N[Valid teleport target confirmed]
    N --> O[BP_CameraSweepManager::SweepTo target]
    O --> P[Update player arrow on minimap]
```

---

## 8. MetadataLinker Matching Flow

```mermaid
flowchart TD
    A[Level load complete] --> B[BP_MetadataLinker::RunMatching]
    B --> C[Scan all actors with Datasmith tag]
    C --> D[Load DT_Equipment into memory]
    
    D --> E[For each Datasmith actor]
    E --> F[Extract actor label / component name]
    F --> G["Normalize: strip SM_, BP_ prefixes; lowercase"]
    
    G --> H{Exact match in DT_Equipment.EquipmentID?}
    H -- Yes --> I[Tag actor with EquipmentID - HIGH confidence]
    
    H -- No --> J{Contains match?}
    J -- Yes --> K[Tag actor - MEDIUM confidence]
    
    J -- No --> L{Levenshtein distance ≤ 3?}
    L -- Yes --> M[Flag as AMBIGUOUS - needs manual review]
    
    L -- No --> N[Mark as UNMATCHED]
    
    I --> O[Store in TMap]
    K --> O
    M --> P[Add to ambiguous list]
    N --> Q[Add to unmatched list]
    
    O --> R{More actors?}
    P --> R
    Q --> R
    R -- Yes --> E
    R -- No --> S[Generate match report]
    
    S --> T["Report: {matched: N, unmatched: N, ambiguous: N}"]
    T --> U[Fire OnMatchingComplete delegate]
    U --> V{Match rate > 90%?}
    V -- Yes --> W[Proceed normally]
    V -- No --> X[Show unmatched report in Editor Utility Widget]
    X --> Y[Enable manual linking UI]
```

---

## 9. Multi-User Session Flow

```mermaid
flowchart TD
    A[Host starts session] --> B[CVT BP_LoginMenuPawn handles lobby]
    B --> C[Host selects role: Admin]
    C --> D[BP_OrionModeManager::SetMode on host]
    
    E[Client joins session] --> F[CVT session handshake]
    F --> G[Client selects role]
    G --> H{Role allowed by host?}
    H -- No --> I[Reject with reason]
    H -- Yes --> J[Client joins with role]
    
    J --> K[Sync current mode from GameState]
    K --> L[Client UI configures for mode + role]
    
    D --> M{Mode change by host?}
    M -- Yes --> N[Update GameState replicated property]
    N --> O[All clients receive OnRep_CurrentMode]
    O --> P[Each client fires local OnModeChanged]
    
    Q[Any user selects equipment] --> R{Has permission for tool?}
    R -- No --> S[Tool disabled - show lock icon]
    R -- Yes --> T[Execute tool locally]
    T --> U[CVT replicates tool state]
    
    V[Host starts session recording] --> W[BP_SessionRecorder::StartRecording]
    W --> X[Capture every 100ms: camera transform + active tool + annotations]
    X --> Y{Recording active?}
    Y -- Yes --> X
    Y -- Stop --> Z[Save to Saved/SessionRecordings/timestamp.json]
    
    AA[Heartbeat monitor] --> AB{Client response within 5s?}
    AB -- Yes --> AA
    AB -- No --> AC[Mark client as disconnected]
    AC --> AD[Attempt auto-resync from host state]
    AD --> AE{Resync successful?}
    AE -- Yes --> AF[Resume session]
    AE -- No --> AG[Show rejoin prompt to client]
```

---

## 10. SaveGame Flow

```mermaid
flowchart TD
    A[Save triggered] --> B{Trigger source?}
    B -- Auto-save timer --> C[Every 300s per config]
    B -- Manual save --> D[User presses save button]
    B -- Mode switch --> E[Save before mode change]
    B -- App exit --> F[Save on EndPlay]
    
    C --> G[BP_Data_SaveGame::SaveState]
    D --> G
    E --> G
    F --> G
    
    G --> H[For each Command Component]
    H --> I[Fire EventBindSaveState]
    I --> J[Component serializes its state]
    J --> K{More components?}
    K -- Yes --> H
    K -- No --> L[Save Orion custom fields]
    
    L --> M[Serialize current mode]
    L --> N[Serialize selected equipment]
    L --> O[Serialize inspection progress]
    L --> P[Serialize bookmark categories]
    
    M --> Q[Write to save file]
    N --> Q
    O --> Q
    P --> Q
    
    Q --> R[Save file: Saved/SaveGames/PREFIX_slot.sav]
    R --> S[Show save confirmation toast]
    
    T[Load triggered] --> U[BP_Data_SaveGame::LoadState]
    U --> V[Read save file]
    V --> W[For each Command Component]
    W --> X[Fire EventBindLoadState]
    X --> Y[Component deserializes its state]
    Y --> Z{More components?}
    Z -- Yes --> W
    Z -- No --> AA[Load Orion custom fields]
    AA --> AB[Restore mode]
    AA --> AC[Restore selected equipment]
    AA --> AD[Restore inspection progress]
    AB --> AE[Fire OnModeChanged]
    AC --> AF[Fire OnEquipmentSelected]
```

---

## 11. Config Validation & Hot-Reload Flow

```mermaid
flowchart TD
    A[BP_ConfigLoader initialized] --> B{Dev build?}
    B -- Yes --> C[Register file watcher on OrionConfig.json]
    B -- No --> D[Skip file watcher]
    
    C --> E{File change detected?}
    E -- Yes --> F[Re-parse JSON]
    F --> G[BP_ConfigValidator::Validate]
    G --> H{All fields valid?}
    H -- Yes --> I[Update config struct]
    H -- Partial --> J[Merge valid fields with defaults]
    J --> K[Show toast: list of invalid fields]
    K --> I
    H -- All invalid --> L[Keep current config]
    L --> M[Show error toast]
    
    I --> N[Fire OnConfigReloaded delegate]
    N --> O[WBP_OrionRoot: update colors/logo]
    N --> P[BP_OrionModeManager: update mode availability]
    N --> Q[Feature systems: toggle features]
    
    E -- No --> E
    D --> R[Config loaded once at startup - no reload]
```

---

## 12. Content Pipeline Flow (Client Onboarding)

```mermaid
flowchart TD
    A[New Client Project] --> B[Receive Plant 3D .dwg files]
    
    B --> C[Pipeline A: Geometry]
    C --> D[Open in 3ds Max]
    D --> E[QA cleanup: fix normals, merge meshes, assign materials]
    E --> F[Datasmith Export from 3ds Max]
    F --> G[Import .udatasmith into UE5]
    
    B --> H[Pipeline B: Metadata]
    H --> I[Run Python export script on Plant 3D]
    I --> J[Generate equipment_metadata.json]
    J --> K[Import JSON into UE5 Data Tables]
    
    G --> L[Pipeline C: Matching]
    K --> L
    L --> M[BP_MetadataLinker::RunMatching]
    M --> N{Match rate > 90%?}
    N -- Yes --> O[Auto-tagged scene ready]
    N -- No --> P[Open Equipment Tagger utility]
    P --> Q[Manual linking of unmatched actors]
    Q --> O
    
    O --> R[Content Author: Configure zones]
    R --> S[Zone Painter utility: draw trigger volumes]
    S --> T[Content Author: Build tour]
    T --> U[Tour Path Editor: click waypoints in viewport]
    U --> V[Content Author: Create OrionConfig.json]
    V --> W[Config Generator utility: fill form → export]
    
    W --> X[Validation Pass utility]
    X --> Y{All checks pass?}
    Y -- Yes --> Z[Client scene ready for delivery]
    Y -- No --> AA[Fix reported issues]
    AA --> X

    style Z fill:#00D4AA,color:#000
```
