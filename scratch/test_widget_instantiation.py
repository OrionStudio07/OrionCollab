import unreal
import sys
import traceback

def test_instantiation():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/widget_test_results.txt"
    
    with open(results_path, "w") as f:
        f.write("==================================================\n")
        f.write("       WBP_ORIONROOT INSTANTIATION DIAGNOSTICS      \n")
        f.write("==================================================\n")
        
        try:
            # 1. Load class
            widget_class_path = "/Game/CollaborativeViewer/UMG/WBP_OrionRoot.WBP_OrionRoot_C"
            widget_class = unreal.load_class(None, widget_class_path)
            if not widget_class:
                f.write(f"ERROR: Could not load WBP_OrionRoot class from {widget_class_path}!\n")
                return False
            f.write("SUCCESS: Loaded WBP_OrionRoot class.\n")
            
            # 2. Get editor world using multiple fallback methods
            world = None
            try:
                world = unreal.EditorLevelLibrary.get_editor_world()
                f.write(f"Tried EditorLevelLibrary.get_editor_world(): {world}\n")
            except Exception as e_ell:
                f.write(f"EditorLevelLibrary.get_editor_world() failed: {e_ell}\n")
                
            if not world:
                try:
                    world = unreal.UnrealEditorSubsystem().get_editor_world()
                    f.write(f"Tried UnrealEditorSubsystem.get_editor_world(): {world}\n")
                except Exception as e_ues:
                    f.write(f"UnrealEditorSubsystem.get_editor_world() failed: {e_ues}\n")
                    
            if not world:
                f.write("ERROR: Could not retrieve editor world via any method!\n")
                return False
                
            f.write(f"SUCCESS: Got editor world context: {world.get_name()}\n")
            
            # 3. Create widget instance
            f.write("Attempting to create widget...\n")
            widget_instance = unreal.WidgetBlueprintLibrary.create(world, widget_class, None)
            if not widget_instance:
                f.write("ERROR: Failed to instantiate WBP_OrionRoot!\n")
                return False
            f.write("SUCCESS: Programmatically instantiated WBP_OrionRoot.\n")
            
            # 4. Verify class and cast
            f.write(f"Widget instance name: {widget_instance.get_name()}\n")
            f.write(f"Widget instance class: {widget_instance.get_class().get_name()}\n")
            cast_widget = unreal.UserWidget.cast(widget_instance)
            if not cast_widget:
                f.write("ERROR: Could not cast instance to UserWidget!\n")
                return False
            f.write("SUCCESS: Cast verification passed.\n")
            f.write("--- ALL WBP_ORIONROOT INSTANTIATION TESTS PASSED ---\n")
            return True
            
        except Exception as e:
            f.write(f"EXCEPTION OCCURRED: {e}\n")
            f.write("Traceback:\n")
            f.write(traceback.format_exc() + "\n")
            return False

if __name__ == "__main__":
    test_instantiation()
