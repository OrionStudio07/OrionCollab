# Changelog

All notable changes to OrionCollab are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.3.0] — 2026-06-29

### Added
- Professional GitHub portfolio structure with comprehensive documentation
- `docs/` directory with architecture, design, setup, and API reference documentation
- `README.md` with project overview, architecture diagrams, and feature showcase
- `LICENSE` (MIT), `CONTRIBUTING.md`, and `CHANGELOG.md`
- Organized `Scripts/` into `automation/`, `setup/`, `tests/`, and `config/` subdirectories
- HTML UI/UX demos preserved in `docs/demos/`

### Changed
- Expanded `.gitignore` to comprehensive UE5 industry standard
- Removed generated files from tracking (`.sln`, `.log`, `__pycache__/`, `scratch/`, `.obsidian/`)

---

## [0.2.0] — 2026-06-28

### Added
- Phase 2 Task 2.1 — UI widget system implementation
- `WBP_OrionRoot` root widget with mode-based layout transitions
- `WBP_TreeBrowser` with virtualized ListView for 6,500+ entries
- Glassmorphism material system (`M_Orion_GlassPanel`)
- Design pattern documentation (OrionRoot, TreeBrowser, ConfigLoader, UI Material Spec)
- Organized documentation vault with Obsidian hub

---

## [0.1.0] — 2026-06-27

### Added
- Initial project setup with Unreal Engine 5.8 + CollabViewer Template
- C++ World Subsystems:
  - `UOrionHierarchyManager` — Equipment hierarchy tree with fuzzy search
  - `UOrionMetadataLinker` — Datasmith actor ↔ DataTable auto-matching
  - `UOrionModeManager` — Mode state machine with role-based access
  - `UOrionConfigSubsystem` — JSON configuration loading and validation
  - `UOrionCameraSweepManager` — Smooth spline-based camera transitions
- Python automation scripts for metadata conversion and Data Table import
- Python test suite for all C++ subsystems
- Governing documents: PRD, TRD, Backend Schema, Flow Diagrams
- `OrionConfig.json` per-client configuration system
- MCP bridge for AI-assisted development workflow
