import unreal

def print_paths():
    out_lines = []
    out_lines.append("--- PRINTING OBJECT PATHS ---")
    
    try:
        subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        if subsystem:
            out_lines.append(f"EditorActorSubsystem path: {subsystem.get_path_name()}")
        else:
            out_lines.append("EditorActorSubsystem not found!")
    except Exception as e:
        out_lines.append(f"Error getting EditorActorSubsystem: {e}")

    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        if world:
            out_lines.append(f"World: {world.get_name()}")
            hierarchy_manager = unreal.OrionHierarchyManager.get_hierarchy_manager_subsystem(world)
            if hierarchy_manager:
                out_lines.append(f"OrionHierarchyManager path: {hierarchy_manager.get_path_name()}")
            else:
                out_lines.append("OrionHierarchyManager not found!")
        else:
            out_lines.append("World not found!")
    except Exception as e:
        out_lines.append(f"Error getting HierarchyManager: {e}")

    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/paths_output.txt", "w") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    print_paths()
