# Contributing to OrionCollab

Thank you for your interest in contributing to OrionCollab! This document outlines the guidelines and processes for contributing.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Set up** the development environment (see [Getting Started](docs/setup/getting-started.md))
4. **Create a branch** for your work

---

## Branch Naming

Use descriptive branch names with the following prefixes:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/annotation-filters` |
| `fix/` | Bug fixes | `fix/search-fuzzy-matching` |
| `docs/` | Documentation only | `docs/update-pipeline-guide` |
| `refactor/` | Code restructuring | `refactor/hierarchy-manager` |
| `test/` | Test additions | `test/metadata-linker-coverage` |

---

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Build process, tooling, or auxiliary changes |
| `perf` | Performance improvement |

### Examples
```
feat(hierarchy): add fuzzy search with Levenshtein distance
fix(config): handle missing accent_color field gracefully
docs(readme): add architecture diagram
test(metadata): add matching accuracy test for 6500 entries
```

---

## Pull Request Process

1. **Update documentation** if your change affects public APIs or behavior
2. **Run tests** to verify no regressions:
   ```bash
   python Scripts/tests/test_hierarchy_manager.py
   python Scripts/tests/test_metadata_linker.py
   ```
3. **Fill out the PR template** describing:
   - What changed and why
   - How it was tested
   - Screenshots (for UI changes)
4. **Request review** from a maintainer
5. **Address feedback** before merge

---

## Code Style

### C++ (Source/)
- Follow [Unreal Engine Coding Standard](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine)
- Use `UPROPERTY()` / `UFUNCTION()` macros for all exposed members
- All display strings use `FText` with String Table references
- Prefix classes: `U` for UObjects, `A` for Actors, `F` for structs, `E` for enums

### Blueprint
- Name Blueprints with `BP_` prefix, Widgets with `WBP_` prefix
- Use the CVT `BP_BaseCommandComponent` lifecycle for tools
- Document complex graphs with comment boxes

### Python (Scripts/)
- Python 3.10+ compatible
- Use descriptive function and variable names
- Add docstrings to all public functions

---

## Architecture Guidelines

- **World Subsystems** for always-active infrastructure (ModeManager, HierarchyManager)
- **Command Components** for tools that follow the CVT lifecycle
- **Level Actors** for spawnable/placed gameplay elements
- **Data Tables** for all structured data (no hardcoded values)
- **String Tables** for all display text (`ST_Orion_UI.csv`)
- **OrionConfig.json** for per-client configuration

---

## Reporting Issues

Open a GitHub Issue with:
- **Title**: Clear, descriptive summary
- **Description**: Steps to reproduce, expected behavior, actual behavior
- **Environment**: UE version, OS, hardware (especially for performance issues)
- **Screenshots/Logs**: Include relevant visuals or log output

---

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
