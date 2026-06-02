import unreal
import os

def setup():
    print("--- STARTING MINIMAP ASSET INITIALIZATION ---")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # 1. Create RT_Minimap (TextureRenderTarget2D)
    rt_name = "RT_Minimap"
    rt_package = "/Game/CollaborativeViewer/UMG/Textures"
    rt_path = f"{rt_package}/{rt_name}"
    
    if unreal.EditorAssetLibrary.does_asset_exist(rt_path):
        print(f"INFO: {rt_name} already exists. Loading asset.")
        rt_asset = unreal.load_asset(rt_path)
    else:
        factory = unreal.TextureRenderTargetFactoryNew()
        rt_asset = asset_tools.create_asset(
            asset_name=rt_name,
            package_path=rt_package,
            asset_class=unreal.TextureRenderTarget2D,
            factory=factory
        )
        
    if rt_asset:
        rt_asset.set_editor_property("size_x", 512)
        rt_asset.set_editor_property("size_y", 512)
        rt_asset.set_editor_property("render_target_format", unreal.TextureRenderTargetFormat.RTF_RGBA8)
        unreal.EditorAssetLibrary.save_loaded_asset(rt_asset)
        print(f"SUCCESS: Created/Configured {rt_name} TextureRenderTarget2D (512x512, RGBA8).")
    else:
        print(f"ERROR: Could not create {rt_name}!")
        return False
        
    # 2. Create BP_MinimapCamera (SceneCapture2D Blueprint Actor)
    camera_name = "BP_MinimapCamera"
    camera_package = "/Game/CollaborativeViewer/Blueprints"
    camera_path = f"{camera_package}/{camera_name}"
    
    parent_class = unreal.load_class(None, "/Script/Engine.SceneCapture2D")
    if not parent_class:
        print("ERROR: Could not load SceneCapture2D C++ parent class!")
        return False
        
    if unreal.EditorAssetLibrary.does_asset_exist(camera_path):
        print(f"INFO: {camera_name} already exists.")
        camera_asset = unreal.load_asset(camera_path)
    else:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", parent_class)
        camera_asset = asset_tools.create_asset(
            asset_name=camera_name,
            package_path=camera_package,
            asset_class=unreal.Blueprint,
            factory=factory
        )
        
    if camera_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(camera_asset)
        print(f"SUCCESS: Created {camera_name} Blueprint subclassing SceneCapture2D.")
    else:
        print(f"ERROR: Could not create {camera_name}!")
        return False
        
    # 3. Create WBP_Minimap (UserWidget Blueprint)
    widget_name = "WBP_Minimap"
    widget_package = "/Game/CollaborativeViewer/UMG"
    widget_path = f"{widget_package}/{widget_name}"
    
    widget_parent = unreal.load_class(None, "/Script/UMG.UserWidget")
    if not widget_parent:
        print("ERROR: Could not load UserWidget C++ parent class!")
        return False
        
    if unreal.EditorAssetLibrary.does_asset_exist(widget_path):
        print(f"INFO: {widget_name} already exists.")
        widget_asset = unreal.load_asset(widget_path)
    else:
        factory = unreal.WidgetBlueprintFactory()
        factory.set_editor_property("parent_class", widget_parent)
        widget_asset = asset_tools.create_asset(
            asset_name=widget_name,
            package_path=widget_package,
            asset_class=unreal.WidgetBlueprint,
            factory=factory
        )
        
    if widget_asset:
        unreal.EditorAssetLibrary.save_loaded_asset(widget_asset)
        print(f"SUCCESS: Created {widget_name} WidgetBlueprint.")
    else:
        print(f"ERROR: Could not create {widget_name}!")
        return False
        
    print("--- MINIMAP ASSET INITIALIZATION COMPLETE ---")
    return True

if __name__ == "__main__":
    setup()
