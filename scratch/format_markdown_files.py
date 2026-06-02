import os
import re

project_root = r"c:\Users\SHO\Documents\Unreal Projects\OrionCollab"

files_to_format = [
    os.path.join(project_root, ".agents", "rules", "agents.md"),
    os.path.join(project_root, ".agents", "rules", "GEMINI.md"),
    os.path.join(project_root, ".agents", "rules", "guide.md"),
    os.path.join(project_root, "GoverningDocuments", "backend_schema.md"),
    os.path.join(project_root, "GoverningDocuments", "flow_diagrams.md"),
    os.path.join(project_root, "GoverningDocuments", "OrionCollab_Features_Reference.md"),
    os.path.join(project_root, "GoverningDocuments", "prd.md"),
    os.path.join(project_root, "GoverningDocuments", "trd.md")
]

def format_markdown(content):
    # 1. Strip trailing whitespace from every line
    lines = [line.rstrip() for line in content.splitlines()]
    
    # 2. Fix header formatting (ensure space after # and blank line before header)
    new_lines = []
    in_frontmatter = False
    frontmatter_count = 0
    in_code_block = False
    
    for i, line in enumerate(lines):
        # Track frontmatter (starts and ends with --- at line starts)
        if line == "---":
            if i == 0 or (i > 0 and frontmatter_count < 2):
                in_frontmatter = not in_frontmatter
                frontmatter_count += 1
                new_lines.append(line)
                continue
        
        if in_frontmatter:
            new_lines.append(line)
            continue
            
        # Track code blocks
        if line.startswith("```"):
            in_code_block = not in_code_block
            # Ensure code blocks have a language (default to text if missing)
            if in_code_block and line == "```":
                line = "```text"
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        # Check for headers: must start with '#' followed by space
        header_match = re.match(r"^(#+)(.*)$", line)
        if header_match:
            hashes = header_match.group(1)
            title = header_match.group(2)
            if title and not title.startswith(" "):
                line = f"{hashes} {title}"
            
            # Ensure blank line before header
            if new_lines and new_lines[-1] != "":
                new_lines.append("")
                
        # Check for horizontal rules: '---'
        if line == "---":
            if new_lines and new_lines[-1] != "":
                new_lines.append("")
                
        new_lines.append(line)
        
        # Ensure blank line after horizontal rules
        if line == "---" and i < len(lines) - 1 and lines[i+1] != "":
            new_lines.append("")
            
    # 3. Clean up list spacing
    list_item_pattern = re.compile(r"^\s*([-*+]|\d+\.)\s+")
    
    final_lines = []
    in_list = False
    
    for i, line in enumerate(new_lines):
        is_list = bool(list_item_pattern.match(line))
        
        if is_list:
            if not in_list:
                # List started! Ensure preceding line is empty
                if final_lines and final_lines[-1] != "" and not final_lines[-1].startswith("#"):
                    final_lines.append("")
                in_list = True
        else:
            if in_list:
                # List ended! Ensure next line is empty
                if line != "" and final_lines[-1] != "":
                    final_lines.append("")
                in_list = False
                
        final_lines.append(line)
        
    # 4. Remove consecutive blank lines
    collapsed_lines = []
    for line in final_lines:
        if line == "":
            if not collapsed_lines or collapsed_lines[-1] != "":
                collapsed_lines.append(line)
        else:
            collapsed_lines.append(line)
            
    # Remove leading/trailing blank lines in the file
    while collapsed_lines and collapsed_lines[0] == "":
        collapsed_lines.pop(0)
    while collapsed_lines and collapsed_lines[-1] == "":
        collapsed_lines.pop()
        
    # 5. Join and ensure trailing newline
    return "\n".join(collapsed_lines) + "\n"

# Run the formatting for all specified files
for file_path in files_to_format:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        original_content = f.read()
    
    formatted_content = format_markdown(original_content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted_content)
        
    print(f"Successfully formatted: {os.path.relpath(file_path, project_root)}")

print("\nFormatting completed successfully!")
