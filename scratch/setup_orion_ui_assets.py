import unreal
import os

def setup_widgets():
    print("--- STARTING ORION WIDGET ASSET INITIALIZATION ---")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    widget_parent = unreal.load_class(None, "/Script/UMG.UserWidget")
    if not widget_parent:
        print("ERROR: Could not load UserWidget C++ parent class!")
        return False
        
    widget_package = "/Game/CollaborativeViewer/UMG"
    
    widgets_to_create = [
        "WBP_OrionRoot",
        "WBP_TopBar",
        "WBP_SidePanel",
        "WBP_EquipmentDetails",
        "WBP_BottomBar",
        "WBP_ToolRadialMenu",
        "WBP_Notification",
        "WBP_ModalOverlay"
    ]
    
    for widget_name in widgets_to_create:
        widget_path = f"{widget_package}/{widget_name}"
        
        if unreal.EditorAssetLibrary.does_asset_exist(widget_path):
            print(f"INFO: {widget_name} already exists.")
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
                
    print("--- ORION WIDGET ASSET INITIALIZATION COMPLETE ---")
    return True

if __name__ == "__main__":
    setup_widgets()
