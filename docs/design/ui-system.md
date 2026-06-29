# UI Design System

> Derived from [WBP_OrionRoot_Logic](.notes/patterns/WBP_OrionRoot_Logic.md) and [UI_Material_Spec](.notes/patterns/UI_Material_Spec.md)

---

## Design Philosophy

OrionCollab uses a **Modern Industrial Dashboard** aesthetic — glassmorphic panels over a photorealistic 3D viewport, with a teal accent (`#00D4AA`) on deep navy (`#0A1628`) backgrounds. The UI adapts its layout and visible elements based on the active operating mode.

---

## Root Widget: WBP_OrionRoot

The root widget coordinates all in-game UI through mode-driven visibility and animated transitions.

### Widget Hierarchy

```
WBP_OrionRoot
├── TopBar          — Horizontal header (branding, mode indicator, user)
├── SidePanel       — Collapsible sidebar (tree browser, search, details)
├── BottomBar       — Horizontal footer (tool palette, tour controls)
├── Minimap         — Overlay radar map with floor selector
└── ModalOverlay    — High-priority popups (lobby UI, settings)
```

### Mode-Based Visibility Matrix

| Widget | MODE_LAUNCHER | MODE_SHOWCASE | MODE_OPERATIONS |
|--------|:------------:|:------------:|:--------------:|
| TopBar | Collapsed | Visible | Visible |
| SidePanel | Collapsed | Collapsible | Visible (Details) |
| BottomBar | Collapsed | Visible (Tour) | Visible (Tools) |
| Minimap | Collapsed | Collapsed | Visible |
| ModalOverlay | Visible (Lobby) | Hidden | Hidden |

### Transition Animations

All visibility transitions use UMG Timelines:
- **Duration**: 0.3 seconds
- **Easing**: Cubic Ease-Out
- **Slide-In**: Translation from `-320px` → `0px`, opacity `0.0` → `1.0`
- **Slide-Out**: Translation from `0px` → `-320px`, opacity `1.0` → `0.0`

---

## Glassmorphism Material: M_Orion_GlassPanel

A custom UMG material that creates premium glass-like panel surfaces.

### Material Properties

| Parameter | Type | Value | Purpose |
|-----------|------|-------|---------|
| `BaseColor` | Vector4 | `(0.04, 0.08, 0.15, 0.65)` | Deep navy at 65% opacity |
| `BorderColor` | Vector4 | `(0.0, 0.83, 0.67, 1.0)` | Teal accent highlight |
| `EdgeHighlight` | Scalar | `0.15` | Edge specular shine strength |
| `NoiseScale` | Scalar | `4.0` | Micro-imperfection frequency |

### Implementation Stack (UMG)

```
Overlay (Panel Widget)
├── Background Blur Widget (Z-Order: 0)
│   └── Blur Strength: 15.0
└── Border Widget (Z-Order: 1)
    └── Brush: M_Orion_GlassPanel
        └── [Child Content Widgets]
```

### Material Node Graph

1. **Base Translucency**: Vertical gradient darkening (simulating overhead industrial lighting)
2. **Edge Highlight**: Fresnel-based 1px inner border with `#00D4AA` accent
3. **Glass Noise**: Animated micro-scratch texture for dynamic reflections

---

## Design Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | `#0A1628` | Panel backgrounds |
| `--color-accent` | `#00D4AA` | Active highlights, borders |
| `--color-text-primary` | `#FFFFFF` | Primary text |
| `--color-text-secondary` | `#8B9DC3` | Secondary/muted text |
| `--blur-strength` | `15.0` | Background blur |
| `--panel-opacity` | `65%` | Panel translucency |
| `--transition-duration` | `0.3s` | All UI transitions |
| `--transition-easing` | Cubic Ease-Out | Transition curve |
| `--indent-unit` | `16px` | Tree indentation per depth level |
