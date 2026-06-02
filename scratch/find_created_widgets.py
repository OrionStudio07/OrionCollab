import unreal
import time

def find_widgets():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt"
    with open(results_path, "w") as f:
        f.write("=== FINDING RUNTIME VIEWPORT WIDGETS ===\n")
        try:
            # 1. Start PIE simulation
            f.write("Starting simulation...\n")
            unreal.EditorLevelLibrary.editor_play_simulate()
            
            # Wait 2.0 seconds for all systems to construct and draw UI
            time.sleep(2.0)
            
            # 2. Query PIE world
            pie_worlds = unreal.EditorLevelLibrary.get_pie_worlds(True)
            if not pie_worlds:
                f.write("ERROR: No active PIE worlds found!\n")
                unreal.EditorLevelLibrary.editor_end_play()
                return
                
            pie_world = pie_worlds[0]
            f.write(f"Active PIE World: {pie_world.get_name()}\n")
            
            # 3. Find all UserWidget instances using WidgetLibrary
            f.write("Querying active UserWidgets...\n")
            all_widgets = unreal.WidgetLibrary.get_all_widgets_of_class(pie_world, unreal.UserWidget, True)
            f.write(f"Total active UserWidgets found: {len(all_widgets)}\n")
            for w in all_widgets:
                f.write(f"  - Name: {w.get_name()} | Class: {w.get_class().get_name()}\n")
                
            # 4. Stop simulation
            unreal.EditorLevelLibrary.editor_end_play()
            f.write("Simulation stopped.\n")
            
        except Exception as e:
            f.write(f"EXCEPTION: {e}\n")

if __name__ == "__main__":
    find_widgets()
