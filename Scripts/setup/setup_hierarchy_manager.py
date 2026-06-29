import unreal

def create_hierarchy_assets():
    destination_path = "/Game/CollaborativeViewer/Blueprints/GameInstance"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    hierarchy_name = "BP_HierarchyManager"
    hierarchy_path = f"{destination_path}/{hierarchy_name}"
    
    parent_class = unreal.load_class(None, "/Script/OrionCollab.OrionHierarchyManager")
    if not parent_class:
        print("ERROR: Could not load OrionHierarchyManager C++ class!")
        return

    # If the asset already exists, we skip recreation to avoid locked package conflicts.
    # Its C++ parent class (OrionHierarchyManager) is already verified and correctly mapped.
    if unreal.EditorAssetLibrary.does_asset_exist(hierarchy_path):
        print(f"SUCCESS: {hierarchy_name} already exists. Skipping recreation.")
        return

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    hierarchy_asset = asset_tools.create_asset(
        asset_name=hierarchy_name,
        package_path=destination_path,
        asset_class=unreal.Blueprint,
        factory=factory
    )
    if hierarchy_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(hierarchy_asset)
        print(f"SUCCESS: Created {hierarchy_name} asset subclassing OrionHierarchyManager.")
    else:
        print(f"FAILED: Could not create {hierarchy_name}.")

if __name__ == "__main__":
    create_hierarchy_assets()
