import unreal

def inspect():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt"
    with open(results_path, "w") as f:
        f.write("=== INSPECTING WIDGET LIBRARIES AND CLASSES ===\n")
        
        # Check WidgetLibrary
        try:
            f.write(f"\nWidgetLibrary methods:\n")
            for m in dir(unreal.WidgetLibrary):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")
            
        # Check UserWidgetFunctionLibrary
        try:
            f.write(f"\nUserWidgetFunctionLibrary methods:\n")
            for m in dir(unreal.UserWidgetFunctionLibrary):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")
            
        # Check WidgetLayoutLibrary
        try:
            f.write(f"\nWidgetLayoutLibrary methods:\n")
            for m in dir(unreal.WidgetLayoutLibrary):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")
            
        # Check UserWidget
        try:
            f.write(f"\nUserWidget methods:\n")
            for m in dir(unreal.UserWidget):
                f.write(f"  - {m}\n")
        except Exception as e:
            f.write(f"ERROR: {e}\n")

if __name__ == "__main__":
    inspect()
