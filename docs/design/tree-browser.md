# Tree Browser — Virtualized Hierarchy Rendering

> Derived from [WBP_TreeBrowser_Logic](../../.notes/patterns/WBP_TreeBrowser_Logic.md)

---

## Overview

The Tree Browser (`WBP_TreeBrowser`) renders the plant's full equipment hierarchy (6,500+ items across Buildings → Rooms → Equipment → Components) using a **virtualized `UListView`** — not nested scroll boxes — to maintain 60fps during scrolling.

---

## Architecture

### Data Model: `UOrionTreeItemData`

A lightweight `UObject` that separates data from visual representation, enabling widget row recycling:

| Property | Type | Description |
|----------|------|-------------|
| `NodeID` | `FName` | Primary identifier matching equipment tags |
| `DisplayName` | `FText` | Localized display name |
| `Category` | Enum | `Building`, `Room`, `Equipment`, `Component` |
| `EquipmentType` | `EEquipmentType` | Determines outliner icon |
| `Depth` | `int32` | Indentation level (0–3) |
| `IsExpanded` | `bool` | Expansion state tracking |
| `ParentID` | `FName` | Reference to parent node |

### Row Widget: `WBP_TreeItemRow`

Implements `IUserObjectListEntry` for ListView recycling:

```
Horizontal Box
├── Spacer (Width = Depth × 16px)
├── Button: Expand/Collapse Arrow (visible if has children)
├── Image: Category Icon
├── TextBlock: DisplayName
└── TextBlock: P&ID Tag (Equipment only)
```

---

## Flat-List Algorithm

Trees are rendered as flat lists with dynamic insertion/removal:

### Expand Node
1. Set `ParentNode.IsExpanded = true`
2. Fetch children from `BP_HierarchyManager`
3. Create child data objects with `Depth = Parent.Depth + 1`
4. Insert immediately after parent index in the flat array
5. Call `ListView.RequestRefresh()`

### Collapse Node
1. Set `ParentNode.IsExpanded = false`
2. Remove all consecutive items with `Depth > Parent.Depth`
3. Call `ListView.RequestRefresh()`

---

## Performance Budgets

| Metric | Budget |
|--------|--------|
| Flat list insertion | <1ms per operation |
| Memory (6,500 data objects) | <100KB |
| Active row widget instances | ~20 (viewport visible) |
| Scroll frame rate | 60fps sustained |
