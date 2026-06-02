import os

project_root = r"c:\Users\SHO\Documents\Unreal Projects\OrionCollab"

# Define document list with their relative paths from project root
docs = {
    "Home": "Home.md",
    "PRD": "GoverningDocuments/prd.md",
    "TRD": "GoverningDocuments/trd.md",
    "Schema": "GoverningDocuments/backend_schema.md",
    "Flows": "GoverningDocuments/flow_diagrams.md",
    "Features": "GoverningDocuments/OrionCollab_Features_Reference.md",
    
    "ImplPlan": ".notes/decisions/implementation_plan.md",
    
    "ConfigLogic": ".notes/patterns/BP_ConfigLoader_Logic.md",
    "RootLogic": ".notes/patterns/WBP_OrionRoot_Logic.md",
    "TreeLogic": ".notes/patterns/WBP_TreeBrowser_Logic.md",
    "MaterialSpec": ".notes/patterns/UI_Material_Spec.md",
    
    "Task": ".notes/logs/task.md",
    "Walkthrough": ".notes/logs/walkthrough.md",
    "SessionLog": ".notes/logs/session_log.md",
    "UIWalkthrough": ".notes/logs/ui_implementation_walkthrough.md",
    
    "AgentRules": ".agents/rules/agents.md",
    "AgentGuide": ".agents/rules/guide.md"
}

# 1. Generate Home.md at project root
home_content = """# Orion Studios — Project Knowledge Graph Hub
Welcome to the Orion Collab visualization platform documentation dashboard.

---

## 📂 Vault Documentation Map

### 1. Specification & Requirements (Context)
*   [Product Requirement Document (PRD)]({PRD})
*   [Technical Reference Document (TRD)]({TRD})
*   [Backend Schema Specifications]({Schema})
*   [System Integration Flow Diagrams]({Flows})
*   [Comprehensive Features Reference]({Features})

### 2. Implementation & Design Decisions
*   [Core UI/UX Implementation Plan]({ImplPlan})
*   [Active Task Tracker (Todo)]({Task})

### 3. Logic & Design Patterns
*   [BP_ConfigLoader Subsystem Logic]({ConfigLogic})
*   [WBP_OrionRoot Layout Logic]({RootLogic})
*   [WBP_TreeBrowser Virtualization Logic]({TreeLogic})
*   [UI Glassmorphism Material Spec]({MaterialSpec})

### 4. Walkthroughs & Session History
*   [Implementation Walkthrough]({Walkthrough})
*   [High-fidelity UI Walkthrough]({UIWalkthrough})
*   [Session Log (Continuity)]({SessionLog})

### 5. AI Agent Rules & Workflows
*   [Antigravity Agents Persona Rules]({AgentRules})
*   [Workflows and Commands Guide]({AgentGuide})
"""

# Format Home.md links (since Home.md is in project root, relative path is exactly its path in docs)
home_links = {k: v.replace("\\", "/") for k, v in docs.items()}
with open(os.path.join(project_root, "Home.md"), "w", encoding="utf-8") as f:
    f.write(home_content.format(**home_links))
print("Created Home.md dashboard.")


# Helper to calculate relative path from one file to another
def get_relative_path(from_file, to_file):
    from_dir = os.path.dirname(from_file)
    # Calculate common prefix path
    rel_path = os.path.relpath(to_file, from_dir)
    return rel_path.replace("\\", "/")


# 2. Inject Correlation maps to all other files
for name, rel_path in docs.items():
    if name == "Home":
        continue
    
    file_path = os.path.join(project_root, rel_path)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    # Read file content
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Remove old correlation block if it exists
    # To prevent duplicate appends
    correlation_marker = "\n\n---\n## 🔗 Correlation Map"
    if correlation_marker in content:
        content = content.split(correlation_marker)[0]
    
    # Generate correlation map for this file
    correlation_links = {
        "Home": get_relative_path(rel_path, docs["Home"]),
        "PRD": get_relative_path(rel_path, docs["PRD"]),
        "TRD": get_relative_path(rel_path, docs["TRD"]),
        "ImplPlan": get_relative_path(rel_path, docs["ImplPlan"]),
        "Task": get_relative_path(rel_path, docs["Task"]),
        "Walkthrough": get_relative_path(rel_path, docs["Walkthrough"]),
        "SessionLog": get_relative_path(rel_path, docs["SessionLog"]),
        "Rules": get_relative_path(rel_path, docs["AgentRules"])
    }
    
    correlation_map = correlation_marker + """
- **Dashboard:** [Home]({Home})
- **Governing Specifications:** [PRD]({PRD}) · [TRD]({TRD})
- **Implementation & Tasks:** [Plan]({ImplPlan}) · [Tasks]({Task}) · [Walkthrough]({Walkthrough}) · [Session Log]({SessionLog})
- **Active Agent System:** [Rules]({Rules})
""".format(**correlation_links)
    
    # Save file with correlation map
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content + correlation_map)
    print(f"Injected correlation map into: {rel_path}")

print("\nSuccessfully established full vault correlation maps!")
