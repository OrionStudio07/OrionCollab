import os

project_root = r"c:\Users\SHO\Documents\Unreal Projects\OrionCollab"
agents_file = os.path.join(project_root, ".agents", "rules", "agents.md")
guide_file = os.path.join(project_root, ".agents", "rules", "guide.md")

# 1. Update agents.md
if os.path.exists(agents_file):
    with open(agents_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    replacements = {
        "Load skill: .agents/skills/orion-spec-validation.md": "Load skill: [Orion Spec Validation](../skills/orion/orion-spec-validation/SKILL.md)",
        "Load skill: .agents/skills/orion-blueprint-patterns.md": "Load skill: [Orion Blueprint Patterns](../skills/orion/orion-blueprint-patterns/SKILL.md)",
        "Load skill: .agents/skills/orion-cpp-patterns.md": "Load skill: [Orion C++ Patterns](../skills/orion/orion-cpp-patterns/SKILL.md)",
        "Load skill: .agents/skills/orion-ui-system.md": "Load skill: [Orion UI System](../skills/orion/orion-ui-system/SKILL.md)",
        "Load skill: .agents/skills/orion-debug-protocol.md": "Load skill: [Orion Debug Protocol](../skills/orion/orion-debug-protocol/SKILL.md)",
        "Load skill: .agents/skills/orion-data-schema.md": "Load skill: [Orion Data Schema](../skills/orion/orion-data-schema/SKILL.md)",
        "Load skill: .agents/skills/orion-performance-budgets.md": "Load skill: [Orion Performance Budgets](../skills/orion/orion-performance-budgets/SKILL.md)",
        "Load skill: .agents/skills/orion-session-log-template.md": "Load skill: [Orion Session Log Template](../skills/orion/orion-session-log-template/SKILL.md)"
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(agents_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated agents.md with skill links.")

# 2. Update guide.md
if os.path.exists(guide_file):
    with open(guide_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    guide_replacements = {
        "├── orion-pre-task-checklist.md": "├── [orion-pre-task-checklist.md](../skills/orion/orion-pre-task-checklist/SKILL.md)",
        "├── orion-spec-validation.md": "├── [orion-spec-validation.md](../skills/orion/orion-spec-validation/SKILL.md)",
        "├── orion-blueprint-patterns.md": "├── [orion-blueprint-patterns.md](../skills/orion/orion-blueprint-patterns/SKILL.md)",
        "├── orion-cpp-patterns.md": "├── [orion-cpp-patterns.md](../skills/orion/orion-cpp-patterns/SKILL.md)",
        "├── orion-ui-system.md": "├── [orion-ui-system.md](../skills/orion/orion-ui-system/SKILL.md)",
        "├── orion-debug-protocol.md": "├── [orion-debug-protocol.md](../skills/orion/orion-debug-protocol/SKILL.md)",
        "├── orion-data-schema.md": "├── [orion-data-schema.md](../skills/orion/orion-data-schema/SKILL.md)",
        "├── orion-performance-budgets.md": "├── [orion-performance-budgets.md](../skills/orion/orion-performance-budgets/SKILL.md)",
        "└── orion-session-log-template.md": "└── [orion-session-log-template.md](../skills/orion/orion-session-log-template/SKILL.md)"
    }
    
    for old, new in guide_replacements.items():
        content = content.replace(old, new)
        
    with open(guide_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated guide.md with skill links.")
