import unreal

def inspect():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt"
    with open(results_path, "w") as f:
        f.write("=== INSPECTING LEVEL SETTINGS ===\n")
        try:
            world = unreal.EditorLevelLibrary.get_editor_world()
            if not world:
                f.write("ERROR: Could not get editor world!\n")
                return
                
            f.write(f"Active World Name: {world.get_name()}\n")
            
            # Query WorldSettings and GameMode override
            world_settings = world.get_world_settings()
            if world_settings:
                f.write(f"WorldSettings: {world_settings.get_name()}\n")
                gm_override = world_settings.get_editor_property("default_game_mode")
                if gm_override:
                    f.write(f"GameMode Override: {gm_override.get_name()} ({gm_override.get_path_name()})\n")
                else:
                    f.write("GameMode Override: None (using default)\n")
            else:
                f.write("ERROR: Could not get WorldSettings!\n")
                
        except Exception as e:
            f.write(f"EXCEPTION: {e}\n")

if __name__ == "__main__":
    inspect()
