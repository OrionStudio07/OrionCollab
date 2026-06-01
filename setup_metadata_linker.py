import unreal

def create_linker_assets():
    destination_path = "/Game/CollaborativeViewer/Blueprints/GameInstance"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    linker_name = "BP_MetadataLinker"
    linker_path = f"{destination_path}/{linker_name}"
    
    parent_class = unreal.load_class(None, "/Script/OrionCollab.OrionMetadataLinker")
    if not parent_class:
        print("ERROR: Could not load OrionMetadataLinker C++ class!")
        return

    # Delete if it exists so we recreate it with the correct parent
    if unreal.EditorAssetLibrary.does_asset_exist(linker_path):
        print(f"INFO: {linker_name} exists. Deleting to recreate with C++ parent.")
        unreal.EditorAssetLibrary.delete_asset(linker_path)
        
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    linker_asset = asset_tools.create_asset(
        asset_name=linker_name,
        package_path=destination_path,
        asset_class=unreal.Blueprint,
        factory=factory
    )
    if linker_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(linker_asset)
        print(f"SUCCESS: Created {linker_name} asset subclassing OrionMetadataLinker.")
    else:
        print(f"FAILED: Could not create {linker_name}.")

if __name__ == "__main__":
    create_linker_assets()
