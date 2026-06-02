# Orion Studios — Performance Budgets

Used by @perf-auditor. Every system measured against trd.md Section 9.

---

## Release Gate Acceptance Criteria (Blockers)

Any implementation threatening these is a blocker — not a warning:

| Criterion | Threshold |
|-----------|----------|
| Desktop FPS | ≥60fps with Morde Foods scene (6500 actors) |
| VR FPS | ≥72fps with simplified lighting |
| Level load time | <30s for 6500 tagged actors |
| Search latency | <200ms for any query |
| Tree browser scroll | 60fps with 6500 entries |
| MetadataLinker match rate | >90% of known Datasmith actors |

---

## Frame Budget — 16.67ms @ 60fps (trd.md Section 9.1)

| System | Budget | Notes |
|--------|--------|-------|
| Rendering (GPU) | 10ms | Lumen GI, post-process, mesh rendering |
| UI (UMG) | 1ms | Virtualized lists, minimal overdraw |
| Game Logic | 2ms | Mode manager, hierarchy queries, zone checks |
| Physics/Collision | 1ms | Line traces for measurement only |
| Animation | 1ms | Max 3 active zones; LOD-based |
| Networking | 0.5ms | CVT session sync |
| Buffer | 1.17ms | Headroom for spikes |

---

## Memory Budget — Desktop (trd.md Section 9.2)

| Category | Budget |
|----------|--------|
| Scene meshes | 2–4 GB |
| Textures | 1–2 GB |
| Data Tables (all combined) | <50 MB |
| UI widgets | <100 MB |
| Render targets | <32 MB |
| Audio | <200 MB |

---

## Render Target Specifications (trd.md Section 9.3)

| Target | Desktop | VR | Update rate |
|--------|---------|-----|-------------|
| Minimap | 512×512 | 256×256 | 10fps throttled |
| Section Capture | 2048×2048 | 1024×1024 | On-demand only |
| Snapshot | Viewport res | Viewport res | On-demand |

---

## Audit Output Format

```
PERFORMANCE AUDIT
─────────────────
System: [class name — verbatim from spec]
Spec Ref: [trd.md Section 9.X]

OPERATION:
  What runs: [description]
  Thread: [game thread / background thread / render thread]
  Frequency: [every frame / throttled Xhz / on-demand / once at load]
  Dataset: [estimated entry count]
  Budget ref: [trd.md Section 9 line item]

RISK: [LOW / MEDIUM / HIGH / BLOCKER]
Reasoning: [why this level]

MITIGATIONS REQUIRED:
  □ [specific mitigation — implementation note]
  □ [specific mitigation — implementation note]

VERDICT: [PASS / PASS WITH MITIGATIONS / FAIL — BLOCKER]
```

---

## Required Background Threading

These must NOT run on the game thread:

| System | Method | Thread requirement |
|--------|--------|--------------------|
| BP_HierarchyManager | BuildTree() | Background thread |
| BP_HierarchyManager | SearchAll() | Background thread (or cache hit) |
| BP_MetadataLinker | RunMatching() | Background thread |

---

## Required Virtualized Lists

| Widget | Entries | Requirement |
|--------|---------|-------------|
| WBP_TreeBrowser | 6500+ | UListView — mandatory |
| Any list > 50 items | >50 | UListView — mandatory |

Never use ScrollBox + VerticalBox for lists with >50 items.

---

## Zone Animation Limits

| Platform | Max active zones | Animation quality |
|---------|-----------------|-------------------|
| Desktop | 3 simultaneous | Full quality |
| VR | 2 simultaneous | Reduced quality |

LOD-based animation required — no full-quality animation on distant equipment.

---

## Automatic FAIL Conditions

These are immediate FAIL — no mitigations accepted:

- Any list >50 items rendered without UListView virtualization
- BuildTree() or SearchAll() running on the game thread
- Minimap render target updating every frame (must be throttled ≤10fps)
- More than 3 active zone animations simultaneously on desktop
- More than 2 active zone animations simultaneously on VR
- Any claim that a system "should perform fine" without citing a budget
- Section Capture render target updating on Tick (on-demand only)

---

## Platform Rendering Differences

| Setting | Desktop | VR |
|---------|---------|-----|
| Rendering | Full Lumen GI | Simplified Lumen or baked |
| Post-process | Full (bloom, DOF, chromatic aberration) | Bloom only |
| Target FPS | 60 | 72 |
| Minimap RT | 512×512 | 256×256 |
| Active zones | Max 3 | Max 2 |
| Animation LOD | Full quality | Reduced quality |
