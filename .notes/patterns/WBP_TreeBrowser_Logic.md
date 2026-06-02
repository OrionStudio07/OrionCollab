# Widget Logic Specification — WBP_TreeBrowser

To support high-performance rendering of the plant's 6,500+ tags, the Tree Browser widget `WBP_TreeBrowser` must utilize a virtualized `UListView` container, avoiding traditional nested scroll boxes.

---

## 1. Data Model: `UOrionTreeItemData` (UObject)
Because `UListView` recycles widget rows, it requires data representation separated from the visual widget row class. We define a lightweight data object:

* **Base Class:** `UObject`
* **Properties:**
  - `NodeID` (FName): Primary identifier matching building, room, or equipment tags.
  - `DisplayName` (FText): Localized name for display.
  - `Category` (Enum): `Building`, `Room`, `Equipment`, `Component`.
  - `EquipmentType` (EEquipmentType): Decides which Outliner icon to display.
  - `Depth` (int32): Indentation level (0 = Building, 1 = Room, 2 = Equipment, 3 = Component).
  - `IsExpanded` (bool): Tracking flag for list assembly.
  - `ParentID` (FName): Reference to the parent node.

---

## 2. Row Widget: `WBP_TreeItemRow` (List Entry)

* **Interface Inherited:** `IUserObjectListEntry`
* **Layout Structure:**
  - Horizontal Box
    - Spacer (Width bound to `Data->Depth * 16.0` to handle indent spacing)
    - Button: Expand/Collapse Arrow (Visible only if node has children)
    - Image: Category Icon (Pumps, vessels, indicators, etc.)
    - TextBlock: DisplayName
    - TextBlock: P&ID tag (if Category == Equipment)
* **Binding logic (`OnListItemObjectSet`):**
  - Read `Data` properties.
  - Update indentation spacer width.
  - Assign corresponding icons and text fields.
  - If selected, apply accent highlight `#00D4AA` background.

---

## 3. Flat-List Assembly Algorithm (Expansion & Collapse)
To display a tree in a flat virtualized list view, the widget manages the list contents dynamically:

### 3.1 Initial Population
1. On `OnTreeReady` event:
2. Retrieve top-level buildings list from `BP_HierarchyManager`.
3. Create `UOrionTreeItemData` instances for each building (Depth = 0).
4. Add instances to the ListView's data array via `ListView->SetListItems(ItemArray)`.

### 3.2 Expand Node
When the expand arrow is clicked on a row representing node `ParentNode`:
1. `ParentNode->IsExpanded = true`.
2. Retrieve child nodes from `BP_HierarchyManager` (e.g. if Building, get Rooms; if Room, get Equipment).
3. Create data objects for children with `Depth = ParentNode->Depth + 1` and `ParentID = ParentNode->NodeID`.
4. Find the index of `ParentNode` in the flat `ItemArray`.
5. Insert the array of child data objects immediately after that index.
6. Call `ListView->RequestRefresh()` or update items.

### 3.3 Collapse Node
When the collapse arrow is clicked on `ParentNode`:
1. `ParentNode->IsExpanded = false`.
2. Traverse forward in `ItemArray` starting from the index of `ParentNode`.
3. Remove all consecutive items that have a `Depth` greater than `ParentNode->Depth`.
4. Call `ListView->RequestRefresh()`.

---

## 4. Performance Requirements
* **Budgets:**
  - Flat list generation / array insertion < 1ms (within the 16.6ms frame budget).
  - Memory footprints: <100KB for all data objects (6,500 rows).
  - Maximum active row widget instances: ~20 (covering visible viewport bounds), yielding negligible GPU draw overhead.


---
## 🔗 Correlation Map
- **Dashboard:** [Home](../../Home.md)
- **Governing Specifications:** [PRD](../../GoverningDocuments/prd.md) · [TRD](../../GoverningDocuments/trd.md)
- **Implementation & Tasks:** [Plan](../decisions/implementation_plan.md) · [Tasks](../logs/task.md) · [Walkthrough](../logs/walkthrough.md) · [Session Log](../logs/session_log.md)
- **Active Agent System:** [Rules](../../.agents/rules/agents.md)
