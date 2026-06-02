# Orion Studios — UI System & Design Tokens

Used by @ui-engineer. Governs all UMG widget implementation.

---

## Fixed Widget Hierarchy (Locked — No New Root Widgets)

```
WBP_OrionRoot  (root — always active)
├── WBP_TopBar           logo, mode indicator, settings, user info
├── WBP_SidePanel        collapsible — context-sensitive per mode
│   ├── WBP_TreeBrowser      hierarchy navigation
│   ├── WBP_EquipmentDetails tabbed details panel
│   └── WBP_SearchPanel      search bar + results
├── WBP_BottomBar        tool palette, measurement readout, minimap toggle
├── WBP_Minimap          2D render target minimap widget
├── WBP_ToolRadialMenu   quick-access tool wheel
├── WBP_Notification     toast notifications
└── WBP_ModalOverlay     confirmation dialogs, settings
```

New UI must be a child of the appropriate existing container.
Requesting a new root-level widget requires explicit user approval.

---

## Design System Tokens (Never Hardcode — Reference These)

| Token | Value | Use case |
|-------|-------|----------|
| Background Primary | `#0A1628` | Main panels, root bg |
| Background Secondary | `#1A2332` | Sub-panels, cards |
| Accent | `#00D4AA` | Active, selected, interactive |
| Warning | `#FFB74D` | Due maintenance, caution |
| Alert | `#FF5252` | Errors, alarms, overdue |
| Text Primary | White @ 90% opacity | Body text |
| Text Secondary | White @ 60% opacity | Labels, metadata |
| Panel Style | Glassmorphism | Semi-transparent, blur backdrop, border glow |
| Transition Panels | 0.3s ease-out | Slide in/fade |
| Transition Hover | 0.15s | Hover states |

---

## Mandatory Rules

1. **All display text**: `FText` bound to `ST_Orion_UI.csv` — no hardcoded strings
2. **Lists >50 entries**: `UListView` (virtualized) — never ScrollBox + VerticalBox
3. **Colors**: Reference design tokens — never hardcode hex
4. **Transitions**: 0.3s ease-out (panels) / 0.15s (hover)
5. **WBP_TreeBrowser**: UListView mandatory — 6500 entries, must hold 60fps scroll

---

## Widget Implementation Format

```
WIDGET: [WBP_WidgetName]
PARENT: [parent widget in hierarchy]
SPEC REF: [trd.md Section / implementation_plan.md section]
PERF BUDGET: [from trd.md Section 9]

LAYOUT:
  Root → [container type] → [leaf widgets]

BINDINGS:
  Data:  [property] ← [source class/function]
  Event: [user action] → [handler function]
  Delegate: [system event] → [handler function]

STATES:
  [state name]: [condition] → [visual change]

FTEXT KEYS (ST_Orion_UI.csv):
  [key] → "[displayed text]"

ANIMATIONS:
  [name]: [trigger] → [effect] — [duration]

PERFORMANCE:
  Virtualized list: [yes (UListView) / no — reason]
  Render target: [if applicable — resolution + update rate]
  Update frequency: [always / on-demand / throttled at Xhz]
```

---

## WBP_EquipmentDetails — Fixed Tab Structure

Tab order and content are locked (trd.md Section 5):

| Tab | Contents | Data source |
|-----|----------|-------------|
| Overview | Name, P&ID tag, process line, manufacturer, model, key specs | FEquipmentTableRow |
| Components | Parts tree, replacement intervals, materials | Lazy-loaded on expand |
| Actions | Explode, Isolate, Xray, Animate, Inspect buttons | Calls Command Components |
| Drawings | 2D CAD viewer — pan/zoom/fullscreen | DrawingPaths field (Q2 affects impl) |
| Data | Simulation placeholder — "Live data unavailable (v2)" | Out of scope v1 |

---

## Mode-Responsive SidePanel Behavior

WBP_SidePanel subscribes to BP_OrionModeManager::OnModeChanged:

```
MODE_LAUNCHER:   Hide SidePanel entirely
MODE_SHOWCASE:   Show TreeBrowser + SearchPanel
                 Show EquipmentDetails only when equipment is selected
MODE_OPERATIONS: Show TreeBrowser + EquipmentDetails
                 Full tool access enabled
```

---

## Minimap Specifications (trd.md Section 9.3)

| Setting | Desktop | VR |
|---------|---------|-----|
| Render target | 512×512 | 256×256 |
| Update rate | 10fps (throttled) | 10fps (throttled) |
| Player indicator | Rotating arrow at current pos | Same |
| Floor selector | Tabs: F1, F2, F3... | Same |

The minimap render target must NEVER update every frame.
Throttle to 10fps maximum. Flag any Tick-based update as a performance risk.
