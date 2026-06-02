# Implementation Plan — UI/UX Implementation from HTML Dashboard

This implementation plan details the strategy for translating the fully interactive HTML dashboard mockup (`Orion_UI_UX_Preview.html`) into the actual Unreal Engine 5.8 project `OrionCollab`. 

It outlines the creation of the complete widget tree, styling variables matching the SCADA-inspired glassmorphism tokens, localization-ready string tables, and dynamic Blueprint logic to bind the interface directly to C++ world subsystems (e.g. `BP_OrionModeManager` and `BP_HierarchyManager`).

---

## User Review Required

> [!IMPORTANT]
> - **CVT Base Protection:** All new UI/UX components are built as separate custom widgets stacked on top of or delegating to the base CollabViewer Template. No base CVT widgets will be destructively modified.
> - **Data-Driven Panels:** The equipment details drawings tab is designed to dynamically load exported AutoCAD Plant 3D 2D drawings exclusively in **PNG format** using `UTexture2D` runtime loading, as resolved in the spec.
> - **High-Performance ListView:** The sidebar tree browser will utilize a virtualized `UListView` rather than a scroll box to prevent game-thread render stalls with 6,500+ items.

---

## Open Questions

None. All architectural and feature ambiguities (e.g., Drone splines vs FlyMode camera, 2D drawings format) have been resolved in the governing documents.

---

## Proposed Changes

### UMG UI Foundation & Token Setup
We will populate the localization string table with all text keys from the mockup, establish the glassmorphism materials/colors in-editor, and write an automation script to programmatically create the missing UMG widget assets with correct class hierarchy.

#### [NEW] [ST_Orion_UI.csv](file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/Content/CollaborativeViewer/UMG/ST_Orion_UI.csv)
- Populate String Table CSV with all UI strings (English only) for top bar, role selection, quality buttons, sidebar tabs, and tooltips.

#### [NEW] [setup_orion_ui_assets.py](file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/scratch/setup_orion_ui_assets.py)
- A python script to programmatically instantiate all required UMG Widget Blueprints in the Unreal Editor under `/Game/CollaborativeViewer/UMG`:
  - `WBP_OrionRoot` (Root layout & coordination)
  - `WBP_TopBar` (Header bar with branding & pills)
  - `WBP_SidePanel` (Sidebar parent panel)
  - `WBP_EquipmentDetails` (Tabbed 3D inspection viewer)
  - `WBP_BottomBar` (Footer bar holding bottom tools)
  - `WBP_ToolRadialMenu` (Q-menu tool selector wheel)
  - `WBP_Notification` (Stack of toast alerts)
  - `WBP_ModalOverlay` (Full screen menu & settings overlay)

---

### Root Widget Coordination & Easing Transitions
We will define the event logic in `WBP_OrionRoot` to manage layout updates during mode switches and handle collapsible side panels using smooth timelines.

#### [NEW] [WBP_OrionRoot_Logic.md](file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/Content/CollaborativeViewer/UMG/WBP_OrionRoot_Logic.md)
- Specification file outlining member variables, timeline curves (0.3s cubic ease-out), initialization steps, and the mode-to-visibility state transitions matrix.

---

### Side Panel List Virtualization
We will enforce performance bounds on lists that render up to 6,500 entries by establishing data-object list rows.

#### [NEW] [WBP_TreeBrowser_Logic.md](file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/Content/CollaborativeViewer/UMG/WBP_TreeBrowser_Logic.md)
- Logic specification file details for `WBP_TreeBrowser` virtualized `UListView` row reuse, depth indentation spacers, selection delegate bindings, and dynamic flat-list expansion/collapse algorithms.

---

## Verification Plan

### Automated Tests
1. **Asset Presence Verification:** Execute test script in editor to check that all programmatically generated widgets exist in the asset registry.
2. **String Table Key Validity:** Parse `ST_Orion_UI.csv` and ensure zero empty entries or key collisions.
3. **Mode Transition Integration:** Run `test_mode_manager.py` to confirm that state changes propagate correctly through delegate listeners.

### Manual Verification
1. **Interactive Review:** Launch the project level in the Unreal Editor, open the newly instantiated `WBP_OrionRoot` widget, and verify layout anchors.
2. **Visual Checklist:** Confirm spacing, SCADA glassmorphism borders, active color states (`#00D4AA` teal accent, `#0A1628` background) align 1:1 with the `Orion_UI_UX_Preview.html` design standard.


---
## 🔗 Correlation Map
- **Dashboard:** [Home](../../Home.md)
- **Governing Specifications:** [PRD](../../GoverningDocuments/prd.md) · [TRD](../../GoverningDocuments/trd.md)
- **Implementation & Tasks:** [Plan](implementation_plan.md) · [Tasks](../logs/task.md) · [Walkthrough](../logs/walkthrough.md) · [Session Log](../logs/session_log.md)
- **Active Agent System:** [Rules](../../.agents/rules/agents.md)
