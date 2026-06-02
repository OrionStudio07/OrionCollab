import unreal
import sys

def verify():
    print("--- STARTING WIDGET SERIALIZATION VERIFICATION ---")
    widget_package = "/Game/CollaborativeViewer/UMG"
    widgets_to_load = [
        "WBP_OrionRoot",
        "WBP_TopBar",
        "WBP_SidePanel",
        "WBP_EquipmentDetails",
        "WBP_BottomBar",
        "WBP_ToolRadialMenu",
        "WBP_Notification",
        "WBP_ModalOverlay"
    ]
    
    success = True
    for name in widgets_to_load:
        path = f"{widget_package}/{name}"
        try:
            asset = unreal.load_asset(path)
            if asset:
                print(f"SUCCESS: Loaded {name} successfully. Class: {asset.get_class().get_name()}")
            else:
                print(f"ERROR: Failed to load widget asset: {name} at {path}!")
                success = False
        except Exception as e:
            print(f"EXCEPTION loading {name}: {e}")
            success = False
            
    if success:
        print("--- ALL WIDGET SERIALIZATION CHECKS PASSED ---")
        return True
    else:
        print("--- WIDGET SERIALIZATION CHECKS FAILED ---")
        return False

if __name__ == "__main__":
    verify()
