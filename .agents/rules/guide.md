---
trigger: always_on
glob: Workspace
description: Directory Structure

```
.agents/
├── agents.md                    ← Agent persona definitions (load this first)
├── skills/
│   ├── [orion-pre-task-checklist.md](../skills/orion/orion-pre-task-checklist/SKILL.md)     ← Mandatory pre-task protocol
│   ├── [orion-spec-validation.md](../skills/orion/orion-spec-validation/SKILL.md)        ← @spec-guardian validation rules
│   ├── [orion-blueprint-patterns.md](../skills/orion/orion-blueprint-patterns/SKILL.md)     ← @blueprint-engineer patterns
│   ├── [orion-cpp-patterns.md](../skills/orion/orion-cpp-patterns/SKILL.md)           ← @cpp-engineer (narrow scope)
│   ├── [orion-ui-system.md](../skills/orion/orion-ui-system/SKILL.md)              ← @ui-engineer design tokens + rules
│   ├── [orion-debug-protocol.md](../skills/orion/orion-debug-protocol/SKILL.md)         ← @debugger Self-Correction Analysis
│   ├── [orion-data-schema.md](../skills/orion/orion-data-schema/SKILL.md)            ← @data-engineer schema rules
│   ├── [orion-performance-budgets.md](../skills/orion/orion-performance-budgets/SKILL.md)    ← @perf-auditor budget table
│   └── [orion-session-log-template.md](../skills/orion/orion-session-log-template/SKILL.md)  ← @session-logger log format
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
```text
/newmodule BP_OrionModeManager
```

**Debug a bug:**
```text
/debug BP_HierarchyManager BuildTree() crashes — null pointer on Data Table lookup at level load
```

**Phase gate check:**
```text
/phasegate 0
```

**General task (enter through @lead directly):**
```text
@lead I want to implement the config loader today. Phase 0, Task 0.4.
```

---

## The Three Rules

1. **@lead is always the entry point** — never call a sub-agent directly for new tasks
2. **@spec-guardian must APPROVE before any code is written** — never skip it
3. **@session-logger runs at the end of every session** — no exceptions

Without the session log, the next AI session starts blind.

---

---

## 🔗 Correlation Map
- **Dashboard:** [Home](../../Home.md)
- **Governing Specifications:** [PRD](../../GoverningDocuments/prd.md) · [TRD](../../GoverningDocuments/trd.md)
- **Implementation & Tasks:** [Plan](../../.notes/decisions/implementation_plan.md) · [Tasks](../../.notes/logs/task.md) · [Walkthrough](../../.notes/logs/walkthrough.md) · [Session Log](../../.notes/logs/session_log.md)
- **Active Agent System:** [Rules](agents.md)


---
## 🔗 Correlation Map
- **Dashboard:** [Home](../../Home.md)
- **Governing Specifications:** [PRD](../../GoverningDocuments/prd.md) · [TRD](../../GoverningDocuments/trd.md)
- **Implementation & Tasks:** [Plan](../../.notes/decisions/implementation_plan.md) · [Tasks](../../.notes/logs/task.md) · [Walkthrough](../../.notes/logs/walkthrough.md) · [Session Log](../../.notes/logs/session_log.md)
- **Active Agent System:** [Rules](agents.md)
