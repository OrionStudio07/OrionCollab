# Test Scripts

Automated test suite for validating C++ subsystems and Blueprint logic via the MCP bridge and Remote Control API.

## Scripts

| Script | Module Under Test | Key Assertions |
|--------|------------------|----------------|
| `test_config_subsystem.py` | `UOrionConfigSubsystem` | Valid JSON → correct struct; malformed → fallback defaults |
| `test_hierarchy_manager.py` | `UOrionHierarchyManager` | Building/room/equipment queries; fuzzy search accuracy |
| `test_metadata_linker.py` | `UOrionMetadataLinker` | >90% match rate; unmatched report generation |
| `test_mode_manager.py` | `UOrionModeManager` | Mode transitions; role-based access enforcement |
| `test_camera_sweep.py` | `UOrionCameraSweepManager` | Sweep arrival within timeout; no geometry clipping |
| `test_minimap_logic.py` | Minimap System | UV coordinate → valid floor position teleport |
| `test_search_ui.py` | Search UI | <200ms query latency; result grouping by category |

## Prerequisites

- Unreal Editor must be running with the OrionCollab project open
- MCP bridge must be active (see `UnrealMCP/`)
- Python 3.10+

## Usage

```bash
# Run individual tests
python Scripts/tests/test_hierarchy_manager.py
python Scripts/tests/test_metadata_linker.py

# Run all tests
python Scripts/tests/test_config_subsystem.py
python Scripts/tests/test_hierarchy_manager.py
python Scripts/tests/test_metadata_linker.py
python Scripts/tests/test_mode_manager.py
python Scripts/tests/test_camera_sweep.py
python Scripts/tests/test_minimap_logic.py
python Scripts/tests/test_search_ui.py
```
