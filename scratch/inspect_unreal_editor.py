import unreal

def inspect():
    out_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/inspect_api_output.txt"
    with open(out_path, "w") as f:
        f.write("=== INSPECTING UNREAL EDITOR PYTHON API ===\n")
        
        # Check UnrealEditorSubsystem
        try:
            editor_subsystem = unreal.UnrealEditorSubsystem()
            f.write(f"\nUnrealEditorSubsystem methods:\n")
            for m in dir(editor_subsystem):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR loading UnrealEditorSubsystem: {e}\n")
            
        # Check EditorLevelLibrary
        try:
            f.write(f"\nEditorLevelLibrary methods:\n")
            for m in dir(unreal.EditorLevelLibrary):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR loading EditorLevelLibrary: {e}\n")

if __name__ == "__main__":
    inspect()
