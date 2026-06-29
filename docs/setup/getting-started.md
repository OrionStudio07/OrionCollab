# Getting Started

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Unreal Engine** | 5.8 | Install via Epic Games Launcher |
| **Visual Studio** | 2022+ | With "Game development with C++" workload |
| **Python** | 3.10+ | For automation/metadata scripts |
| **.NET SDK** | 6.0+ | Required by UE5 build tools |
| **Git** | 2.30+ | With LFS support for binary assets |

### Optional
| Requirement | Purpose |
|-------------|---------|
| **AutoCAD Plant 3D** | Source CAD data (only for new plant onboarding) |
| **Autodesk 3ds Max** | Geometry QA cleanup before Datasmith export |
| **Meta Quest Link** or **SteamVR** | VR headset support |

---

## Clone & Setup

```bash
# Clone the repository
git clone https://github.com/OrionStudio07/OrionCollab.git
cd OrionCollab

# Generate project files (Windows)
# Right-click OrionCollab.uproject → "Generate Visual Studio project files"
# Or from command line:
"C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat" ^
  OrionCollabEditor Win64 Development OrionCollab.uproject
```

## First Run

1. **Open the project** in Unreal Engine 5.8 by double-clicking `OrionCollab.uproject`
2. **Wait for shaders** to compile (first launch may take 10–15 minutes)
3. **Verify plugins** are enabled: Open Edit → Plugins and confirm:
   - Datasmith Importer ✅
   - DatasmithCAD Importer ✅
   - Python Script Plugin ✅
   - JSON Blueprint Utilities ✅
   - Remote Control ✅
   - OpenXR ✅
4. **Check configuration**: Verify `Scripts/config/OrionConfig.json` exists. If missing, the app falls back to embedded defaults with a warning banner.
5. **Play in Editor**: Press `Alt+P` to launch the application in-editor.

---

## Project Structure

```
OrionCollab/
├── Config/                     # UE5 engine & project settings
├── Content/                    # All UE5 assets (blueprints, maps, UMG, meshes)
│   ├── ArchVis/               # Architecture visualization sample content
│   └── CollaborativeViewer/   # CVT base template + Orion extensions
│       ├── Blueprints/        # Game logic, subsystems, tools
│       ├── Data/              # Data Tables (equipment, buildings, etc.)
│       ├── Maps/              # Level maps
│       ├── UMG/               # UI widgets and textures
│       └── ...
├── Source/                     # C++ source code
│   └── OrionCollab/           # Main module
│       ├── OrionHierarchyManager.*    # Equipment tree + search
│       ├── OrionMetadataLinker.*      # Actor ↔ DataTable matching
│       ├── OrionModeManager.*         # Mode state machine
│       ├── OrionConfigSubsystem.*     # JSON config loading
│       └── OrionCameraSweepManager.*  # Smooth camera transitions
├── Scripts/                    # Python tooling
│   ├── automation/            # Pipeline scripts (metadata conversion, import)
│   ├── setup/                 # Editor setup scripts
│   ├── tests/                 # Automated test scripts
│   └── config/                # OrionConfig.json
├── GoverningDocuments/         # Specifications (PRD, TRD, schemas, flows)
├── docs/                       # Portfolio documentation
├── UnrealMCP/                  # MCP bridge for AI-assisted development
└── .notes/                     # Design patterns & session logs
```

---

## Running Tests

```bash
# Run all Python tests from the project root
python Scripts/tests/test_config_subsystem.py
python Scripts/tests/test_hierarchy_manager.py
python Scripts/tests/test_metadata_linker.py
python Scripts/tests/test_mode_manager.py
python Scripts/tests/test_camera_sweep.py
python Scripts/tests/test_minimap_logic.py
python Scripts/tests/test_search_ui.py
```

> **Note**: Most tests require the Unreal Editor to be running with the project open, as they communicate via the MCP bridge or Remote Control API.
