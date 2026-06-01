---
trigger: always_on
glob: Workspace
description: Directory Structure

```
.agents/
├── agents.md                    ← Agent persona definitions (load this first)
├── skills/
│   ├── orion-pre-task-checklist.md     ← Mandatory pre-task protocol
│   ├── orion-spec-validation.md        ← @spec-guardian validation rules
│   ├── orion-blueprint-patterns.md     ← @blueprint-engineer patterns
│   ├── orion-cpp-patterns.md           ← @cpp-engineer (narrow scope)
│   ├── orion-ui-system.md              ← @ui-engineer design tokens + rules
│   ├── orion-debug-protocol.md         ← @debugger Self-Correction Analysis
│   ├── orion-data-schema.md            ← @data-engineer schema rules
│   ├── orion-performance-budgets.md    ← @perf-auditor budget table
│   └── orion-session-log-template.md  ← @session-logger log format
└── workflows/
    ├── newmodule.md     ← /newmodule [ClassName] — start new implementation
    ├── debug.md         ← /debug [description] — debug broken feature
    └── phasegate.md     ← /phasegate [N] — run phase gate check
```

## Agent Team

| Handle | Role | When called |
|--------|------|-------------|
| @lead | Lead Engineer — orchestrator | Entry point for every task |
| @spec-guardian | Validates against spec docs | Before any code is written |
| @blueprint-engineer | Blueprint logic | After @spec-guardian approves |
| @cpp-engineer | C++ (narrow scope only) | OrionTypes.h, search, snap |
| @ui-engineer | UMG widgets | After @spec-guardian approves |
| @debugger | Self-Correction Analysis | When features fail |
| @data-engineer | Data Tables, config, schema | Data layer tasks |
| @perf-auditor | Performance budgets | Any system touching Tick/memory |
| @session-logger | Session logs | End of every session |

---

## How to Start a Session

**New module:**
```
/newmodule BP_OrionModeManager
```

**Debug a bug:**
```
/debug BP_HierarchyManager BuildTree() crashes — null pointer on Data Table lookup at level load
```

**Phase gate check:**
```
/phasegate 0
```

**General task (enter through @lead directly):**
```
@lead I want to implement the config loader today. Phase 0, Task 0.4.
```

---

## The Three Rules

1. **@lead is always the entry point** — never call a sub-agent directly for new tasks
2. **@spec-guardian must APPROVE before any code is written** — never skip it
3. **@session-logger runs at the end of every session** — no exceptions

Without the session log, the next AI session starts blind.
---

