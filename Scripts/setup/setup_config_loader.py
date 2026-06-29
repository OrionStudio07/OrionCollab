import unreal

def create_config_assets():
    destination_path = "/Game/CollaborativeViewer/Blueprints/GameInstance"
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 1. Create BP_ConfigLoader (subclass of OrionConfigSubsystem)
    loader_name = "BP_ConfigLoader"
    loader_path = f"{destination_path}/{loader_name}"
    
    parent_class = unreal.load_class(None, "/Script/OrionCollab.OrionConfigSubsystem")
    if not parent_class:
        print("ERROR: Could not load OrionConfigSubsystem C++ class!")
        return

    # Delete if it exists so we recreate it with the correct parent
    if unreal.EditorAssetLibrary.does_asset_exist(loader_path):
        print(f"INFO: {loader_name} exists. Deleting to recreate with C++ parent.")
        unreal.EditorAssetLibrary.delete_asset(loader_path)
        
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    loader_asset = asset_tools.create_asset(
        asset_name=loader_name,
        package_path=destination_path,
        asset_class=unreal.Blueprint,
        factory=factory
    )
    if loader_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(loader_asset)
        print(f"SUCCESS: Created {loader_name} asset subclassing OrionConfigSubsystem.")
    else:
        print(f"FAILED: Could not create {loader_name}.")

    # 2. Create BP_OrionGameInstance (subclass of BP_CollaborativeViewer_GameInstance)
    instance_name = "BP_OrionGameInstance"
    instance_path = f"{destination_path}/{instance_name}"
    parent_class_path = "/Game/CollaborativeViewer/Blueprints/GameInstance/BP_CollaborativeViewer_GameInstance.BP_CollaborativeViewer_GameInstance_C"
    
    if unreal.EditorAssetLibrary.does_asset_exist(instance_path):
        print(f"INFO: {instance_name} already exists.")
    else:
        # Load the generated class of the parent Blueprint
        parent_class = unreal.load_class(None, parent_class_path)
        if parent_class:
            factory = unreal.BlueprintFactory()
            factory.set_editor_property("parent_class", parent_class)
            
            instance_asset = asset_tools.create_asset(
                asset_name=instance_name,
                package_path=destination_path,
                asset_class=unreal.Blueprint,
                factory=factory
            )
            if instance_asset:
                unreal.EditorAssetLibrary.save_loaded_asset(instance_asset)
                print(f"SUCCESS: Created {instance_name} subclassing BP_CollaborativeViewer_GameInstance.")
            else:
                print(f"FAILED: Could not create {instance_name}.")
        else:
            print(f"FAILED: Could not load parent class {parent_class_path}.")

if __name__ == "__main__":
    create_config_assets()
