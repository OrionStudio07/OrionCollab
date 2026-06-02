# UI Material Specification — Glassmorphism Theme

This document defines the technical setup for achieving high-fidelity glassmorphic panels inside Unreal Engine 5.8 UMG, adhering to the Modern Industrial Dashboard tokens.

---

## 1. Widget Layout Pattern (Backbuffer Blur Stack)
In Unreal Engine screen-space UMG, materials cannot directly sample the scene backbuffer for screen-space blur. The most performant and stable approach is to stack a native `Background Blur` widget directly under a `Border` widget using a custom styling material:

```
[UMG Hierarchy Panel]
└── Overlay (Panel Widget)
    ├── Background Blur Widget (Z-Order: 0)
    │   ├── Properties:
    │   │   - Blur Strength: 15.0
    │   │   - Horizontal/Vertical Alignment: Fill
    └── Border Widget (Z-Order: 1)
        ├── Properties:
        │   - Brush: Material'M_Orion_GlassPanel'
        └── [Child Content Widgets] (Z-Order: 2)
```

---

## 2. Material Definition: `M_Orion_GlassPanel`

* **Material Domain:** User Interface
* **Blend Mode:** Translucent
* **Target Output:** Emissive Color, Opacity

### 2.1 Material Parameters (Constants/Vectors)
| Name | Type | Value | Hex / Token | Purpose |
|------|------|-------|-------------|---------|
| `BaseColor` | Vector4 | `(0.04, 0.08, 0.15, 0.65)` | `#0A1628` at 65% | Core deep navy background |
| `BorderColor` | Vector4 | `(0.0, 0.83, 0.67, 1.0)` | `#00D4AA` at 100% | Primary accent teal for active highlight |
| `EdgeHighlight` | Scalar | `0.15` | N/A | Ambient specular shine strength at edges |
| `NoiseScale` | Scalar | `4.0` | N/A | Frequency of micro-imperfection noise |

### 2.2 Material Node Graph Logic

#### Step 1: Base Translucency
1. Connect `BaseColor` (Constant3Vector `#0A1628`) to the multiply node.
2. Multiply by a soft vertical gradient using `TextureCoordinate.Y` to make the bottom of panels slightly darker than the top (simulating overhead industrial lighting).
3. Connect the output to the **Emissive Color** pin of the UI material node.

#### Step 2: Custom Specular Edge Highlight (Outer Glow)
To create a premium glass thickness effect at the borders:
1. Use `Generate1DLineMask` or a custom texture mask of a rounded box frame.
2. Apply a `Fresnel` node (or simple UV border math: `Step` and `SmoothStep` on the margins of `TextureCoordinate`).
3. Lerp between the base opacity and the `BorderColor` based on the mask to create a 1px inner border outline of `#00D4AA` or a soft white shine `#FFFFFF`.

#### Step 3: Glass Texture Noise (Micro-specularity)
1. Add a low-intensity `TextureSample` using a tiled grayscale micro-noise normal map (`T_MicroScratch_N` or engine default noise).
2. Panner the noise subtly or tie it to the camera rotation/view angle so the reflections shift dynamically as the player walks or moves in VR.
3. Multiply the noise by `EdgeHighlight` and add it to the final Emissive Color.

---

## 3. UMG Brush Setup
When implementing the panels, assign the material to the border brush. Ensure the **Draw As** property is set to **Image** and the margins are configured to prevent stretching of the edge highlights.


---
## 🔗 Correlation Map
- **Dashboard:** [Home](../../Home.md)
- **Governing Specifications:** [PRD](../../GoverningDocuments/prd.md) · [TRD](../../GoverningDocuments/trd.md)
- **Implementation & Tasks:** [Plan](../decisions/implementation_plan.md) · [Tasks](../logs/task.md) · [Walkthrough](../logs/walkthrough.md) · [Session Log](../logs/session_log.md)
- **Active Agent System:** [Rules](../../.agents/rules/agents.md)
