# Widget Logic Specification — WBP_OrionRoot

The root widget `WBP_OrionRoot` coordinates the layout, transitions, and mode bindings for all in-game interface components.

---

## 1. Member Variables & References
| Variable Name | Type | Access | Description |
|---------------|------|--------|-------------|
| `TopBar` | `WBP_TopBar` Widget Ref | Read-Only | Horizontal header control |
| `SidePanel` | `WBP_SidePanel` Widget Ref | Read-Only | Collapsible vertical sidebar |
| `BottomBar` | `WBP_BottomBar` Widget Ref | Read-Only | Horizontal footer/tool palette |
| `Minimap` | `WBP_Minimap` Widget Ref | Read-Only | Overlay radar map |
| `ModalOverlay` | `WBP_ModalOverlay` Widget Ref | Read-Only | High-priority settings/popups |
| `ActiveMode` | `EOrionMode` (Enum) | Read-Write | Local cache of active mode state |
| `IsSidePanelCollapsed` | Boolean | Read-Write | Tracks sidebar visibility |

---

## 2. Event Graph Flow (Blueprint Logic)

### 2.1 Event Construct (Initialization)
1. Call `GetWorld()` -> `GetSubsystem<UP_OrionModeManager>()` to cache the ModeManager subsystem reference.
2. Bind the custom function `HandleModeChanged` to the ModeManager's `OnModeChanged` multicast delegate.
3. Cache local child references (`TopBar`, `SidePanel`, `BottomBar`, `Minimap`).
4. Read the initial mode: `ActiveMode = ModeManager->GetCurrentMode()`.
5. Call `ConfigureUIForMode(ActiveMode, InitialStartup = true)`.

### 2.2 HandleModeChanged (Multicast Callback)
* **Inputs:** `EOrionMode OldMode`, `EOrionMode NewMode`
* **Sequence:**
  1. `ActiveMode = NewMode`.
  2. Call `ConfigureUIForMode(NewMode, InitialStartup = false)`.
  3. Log event using `BP_TelemetryManager` (e.g. Mode transition completed).

---

## 3. UI State Transitions Matrix

```
┌─────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Widget Element  │ MODE_LAUNCHER        │ MODE_SHOWCASE        │ MODE_OPERATIONS      │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ TopBar          │ Collapsed            │ Visible              │ Visible              │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ SidePanel       │ Collapsed            │ Collapsible (Default)│ Visible (Details)    │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ BottomBar       │ Collapsed            │ Visible (Showcase)   │ Visible (Operations) │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ Minimap         │ Collapsed            │ Collapsed            │ Visible              │
├─────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ ModalOverlay    │ Visible (Lobby UI)   │ Hidden               │ Hidden               │
└─────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

### 3.1 Transition Animations (Timeline Specs)
All state changes between `Visible` and `Collapsed` must utilize a UMG Timeline:
* **Duration:** 0.3 seconds.
* **Easing Curve:** Cubic Ease-Out.
* **Execution:**
  - On Slide-In: Animate translation offset from `-320px` to `0px` and opacity from `0.0` to `1.0`.
  - On Slide-Out: Animate translation from `0px` to `-320px` and opacity from `1.0` to `0.0`.
