import unreal

def inspect():
    out_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt"
    with open(out_path, "w") as f:
        f.write("=== INSPECTING GAMEMODE AND HUD ===\n")
        try:
            gm_path = "/Game/CollaborativeViewer/Blueprints/GameMode/BP_CollaborativeViewer_GameMode"
            gm_bp = unreal.load_asset(gm_path)
            if not gm_bp:
                f.write("ERROR: Could not load BP_CollaborativeViewer_GameMode asset!\n")
                return False
                
            f.write(f"Loaded GameMode asset: {gm_bp.get_name()}\n")
            
            # Get generated class and CDO
            bp_class = gm_bp.generated_class()
            cdo = unreal.get_default_object(bp_class)
            
            # Print classes
            f.write(f"Default Pawn Class: {cdo.get_editor_property('default_pawn_class').get_name()}\n")
            f.write(f"Player Controller Class: {cdo.get_editor_property('player_controller_class').get_name()}\n")
            f.write(f"HUD Class: {cdo.get_editor_property('hud_class').get_name()}\n")
            
        except Exception as e:
            f.write(f"EXCEPTION OCCURRED: {e}\n")

if __name__ == "__main__":
    inspect()
