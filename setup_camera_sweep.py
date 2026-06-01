import unreal

def create_sweep_assets():
    destination_path = "/Game/CollaborativeViewer/Blueprints/Pawn"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    sweep_name = "BP_CameraSweepManager"
    sweep_path = f"{destination_path}/{sweep_name}"
    
    parent_class = unreal.load_class(None, "/Script/OrionCollab.OrionCameraSweepManager")
    if not parent_class:
        print("ERROR: Could not load OrionCameraSweepManager C++ class!")
        return

    # Delete if it exists so we recreate it with the correct parent
    if unreal.EditorAssetLibrary.does_asset_exist(sweep_path):
        print(f"INFO: {sweep_name} exists. Deleting to recreate with C++ parent.")
        unreal.EditorAssetLibrary.delete_asset(sweep_path)
        
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    sweep_asset = asset_tools.create_asset(
        asset_name=sweep_name,
        package_path=destination_path,
        asset_class=unreal.Blueprint,
        factory=factory
    )
    if sweep_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(sweep_asset)
        print(f"SUCCESS: Created {sweep_name} asset subclassing OrionCameraSweepManager.")
    else:
        print(f"FAILED: Could not create {sweep_name}.")

if __name__ == "__main__":
    create_sweep_assets()
