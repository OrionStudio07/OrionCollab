import unreal

def create_empty_string_table():
    destination_path = "/Game/CollaborativeViewer/UMG"
    asset_name = "ST_Orion_UI"
    
    # 1. Get Asset Tools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 2. Programmatically create the blank String Table asset using StringTableFactory
    string_table = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=destination_path,
        asset_class=unreal.StringTable,
        factory=unreal.StringTableFactory()
    )
    
    if string_table:
        # 3. Save the created asset
        unreal.EditorAssetLibrary.save_loaded_asset(string_table)
        print("SUCCESS: Programmatically created empty String Table asset ST_Orion_UI.")
    else:
        print("FAILED: Could not create String Table asset.")

if __name__ == "__main__":
    create_empty_string_table()
