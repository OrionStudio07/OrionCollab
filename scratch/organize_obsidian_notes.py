import os
import shutil
import re

# Paths definition
project_root = r"c:\Users\SHO\Documents\Unreal Projects\OrionCollab"
app_data_brain = r"C:\Users\SHO\.gemini\antigravity-ide\brain\7fa1c8a9-3efa-4341-ba25-b0dc2a9f4e12"
vault_root = os.path.join(project_root, ".notes")

# Folder structure
folders = ["context", "decisions", "patterns", "logs", "assets"]

# Ensure directories exist
for folder in folders:
    os.makedirs(os.path.join(vault_root, folder), exist_ok=True)
print("Created Obsidian folder structure under .notes/")

# List of files to copy: (source, destination_folder, destination_filename)
files_to_copy = [
    # Governing specs (Context)
    (os.path.join(project_root, "GoverningDocuments", "prd.md"), "context", "prd.md"),
    (os.path.join(project_root, "GoverningDocuments", "trd.md"), "context", "trd.md"),
    (os.path.join(project_root, "GoverningDocuments", "backend_schema.md"), "context", "backend_schema.md"),
    (os.path.join(project_root, "GoverningDocuments", "flow_diagrams.md"), "context", "flow_diagrams.md"),
    (os.path.join(project_root, "GoverningDocuments", "OrionCollab_Features_Reference.md"), "context", "OrionCollab_Features_Reference.md"),
    
    # Coding/Subsystem Patterns
    (os.path.join(project_root, "Content", "CollaborativeViewer", "Blueprints", "GameInstance", "BP_ConfigLoader_Logic.md"), "patterns", "BP_ConfigLoader_Logic.md"),
    (os.path.join(project_root, "Content", "CollaborativeViewer", "UMG", "WBP_OrionRoot_Logic.md"), "patterns", "WBP_OrionRoot_Logic.md"),
    (os.path.join(project_root, "Content", "CollaborativeViewer", "UMG", "WBP_TreeBrowser_Logic.md"), "patterns", "WBP_TreeBrowser_Logic.md"),
    (os.path.join(project_root, "Content", "CollaborativeViewer", "UMG", "Materials", "UI_Material_Spec.md"), "patterns", "UI_Material_Spec.md"),
    
    # Decisions (Implementation plan)
    (os.path.join(app_data_brain, "implementation_plan.md"), "decisions", "implementation_plan.md"),
    
    # Logs & Trackers
    (os.path.join(app_data_brain, "task.md"), "logs", "task.md"),
    (os.path.join(app_data_brain, "walkthrough.md"), "logs", "walkthrough.md"),
    (os.path.join(app_data_brain, "session_log.md"), "logs", "session_log.md"),
    (os.path.join(app_data_brain, "ui_implementation_walkthrough.md"), "logs", "ui_implementation_walkthrough.md"),
]

# Media assets
media_assets = [
    "media__1780393738160.png",
    "media__1780398497313.jpg",
    "media__1780399236007.png",
    "orion_ui_mockup_1780394141047.png"
]

# Copy media assets to .notes/assets/
for asset in media_assets:
    src_path = os.path.join(app_data_brain, asset)
    dest_path = os.path.join(vault_root, "assets", asset)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied asset: {asset} -> .notes/assets/")
    else:
        print(f"Asset not found: {src_path}")

# Regex patterns for links to rewrite
# 1. file:///C:/Users/SHO/.gemini/antigravity-ide/brain/7fa1c8a9-3efa-4341-ba25-b0dc2a9f4e12/ -> ../assets/
brain_uri_pat = r"file:///C:/Users/SHO/\.gemini/antigravity-ide/brain/[0-9a-f\-]+/"
# 2. file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/ -> relative project links
project_uri_pat = r"file:///c:/Users/SHO/Documents/Unreal%20Projects/OrionCollab/"

# Copy and rewrite markdown links
for src, dest_fol, dest_name in files_to_copy:
    if not os.path.exists(src):
        print(f"Source file not found: {src}")
        continue
    
    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Calculate relative prefix based on folder
    # context/, decisions/, patterns/, logs/ are all 1 level deep from vault root
    # So relative prefix to assets is "../assets/"
    # Relative prefix to context is "../context/"
    # Relative prefix to logs is "../logs/"
    
    # Perform link rewrites
    # Rewrite brain image paths to relative assets path
    content = re.sub(brain_uri_pat, "../assets/", content, flags=re.IGNORECASE)
    
    # Rewrite specific local links to relative folder layout
    # e.g. ui_implementation_walkthrough.md was referenced from root
    content = content.replace("ui_implementation_walkthrough.md", "ui_implementation_walkthrough.md")
    
    # If the file is implementation_plan.md or walkthrough.md, let's fix other file links
    if dest_name in ["walkthrough.md", "session_log.md", "task.md", "ui_implementation_walkthrough.md"]:
        # Fix link to ui_implementation_walkthrough.md
        # If in logs/, it's in the same directory, so it should be "ui_implementation_walkthrough.md"
        content = re.sub(project_uri_pat + r"ui_implementation_walkthrough\.md", "ui_implementation_walkthrough.md", content, flags=re.IGNORECASE)
        # Fix link to ST_Orion_UI.csv
        content = re.sub(project_uri_pat + r"Content/CollaborativeViewer/UMG/ST_Orion_UI\.csv", "../../Content/CollaborativeViewer/UMG/ST_Orion_UI.csv", content, flags=re.IGNORECASE)
    
    dest_path = os.path.join(vault_root, dest_fol, dest_name)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Processed: {dest_name} -> .notes/{dest_fol}/{dest_name}")

print("\nAll files successfully organized and updated for Obsidian!")
