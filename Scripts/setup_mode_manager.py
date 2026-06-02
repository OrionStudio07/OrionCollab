import unreal

def create_mode_manager_assets():
    destination_path = "/Game/CollaborativeViewer/Blueprints/GameInstance"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    manager_name = "BP_OrionModeManager"
    manager_path = f"{destination_path}/{manager_name}"
    
    parent_class = unreal.load_class(None, "/Script/OrionCollab.OrionModeManager")
    if not parent_class:
        print("ERROR: Could not load OrionModeManager C++ class!")
        return

    # Delete if it exists so we recreate it with the correct parent
    if unreal.EditorAssetLibrary.does_asset_exist(manager_path):
        print(f"INFO: {manager_name} exists. Deleting to recreate with C++ parent.")
        unreal.EditorAssetLibrary.delete_asset(manager_path)
        
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    manager_asset = asset_tools.create_asset(
        asset_name=manager_name,
        package_path=destination_path,
        asset_class=unreal.Blueprint,
        factory=factory
    )
    if manager_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(manager_asset)
        print(f"SUCCESS: Created {manager_name} asset subclassing OrionModeManager.")
    else:
        print(f"FAILED: Could not create {manager_name}.")

if __name__ == "__main__":
    create_mode_manager_assets()
