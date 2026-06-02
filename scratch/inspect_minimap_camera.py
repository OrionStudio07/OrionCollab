import unreal

def inspect_and_configure():
    out_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/camera_properties.txt"
    with open(out_path, "w") as f:
        f.write("--- INSPECTING AND CONFIGURING BP_MINIMAPCAMERA ---\n")
        try:
            # Load blueprint class
            camera_bp_path = "/Game/CollaborativeViewer/Blueprints/BP_MinimapCamera"
            camera_bp = unreal.load_asset(camera_bp_path)
            if not camera_bp:
                f.write("ERROR: Could not load BP_MinimapCamera asset!\n")
                return False
                
            f.write(f"Loaded blueprint asset: {camera_bp.get_name()}\n")
            
            # Get the generated class of the blueprint
            bp_class = camera_bp.generated_class()
            cdo = unreal.get_default_object(bp_class)
            
            # Use correct capture component name
            capture_component = cdo.get_editor_property("capture_component2d")
            if not capture_component:
                f.write("ERROR: Could not get capture_component2d from CDO!\n")
                return False
                
            f.write(f"Capture Component: {capture_component.get_name()}\n")
            
            # Configure defaults (no "b_" prefix)
            capture_component.set_editor_property("capture_every_frame", False)
            capture_component.set_editor_property("capture_on_movement", False)
            capture_component.set_editor_property("projection_type", unreal.CameraProjectionMode.ORTHOGRAPHIC)
            
            # Load RT_Minimap and set as texture target
            rt_path = "/Game/CollaborativeViewer/UMG/Textures/RT_Minimap"
            rt_asset = unreal.load_asset(rt_path)
            if rt_asset:
                capture_component.set_editor_property("texture_target", rt_asset)
                f.write("SUCCESS: Assigned texture_target to RT_Minimap.\n")
            else:
                f.write("ERROR: Could not load RT_Minimap!\n")
                
            # Save blueprint asset
            unreal.EditorAssetLibrary.save_loaded_asset(camera_bp)
            f.write("SUCCESS: Configured and saved BP_MinimapCamera CDO defaults!\n")
            
            # Re-verify
            f.write("Re-verifying CDO settings:\n")
            f.write(f" - capture_every_frame: {capture_component.get_editor_property('capture_every_frame')}\n")
            f.write(f" - capture_on_movement: {capture_component.get_editor_property('capture_on_movement')}\n")
            f.write(f" - projection_type: {capture_component.get_editor_property('projection_type')}\n")
            f.write(f" - texture_target: {capture_component.get_editor_property('texture_target').get_name()}\n")
            
        except Exception as e:
            f.write(f"EXCEPTION: {e}\n")
            return False
            
    return True

if __name__ == "__main__":
    inspect_and_configure()
