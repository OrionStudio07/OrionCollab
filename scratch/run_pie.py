import unreal
import time

def run_pie_test():
    print("--- STARTING PIE TEST RUN ON SAMPLE LEVEL ---")
    
    # Get current editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world context!")
        return False
        
    print(f"Active Editor World: {world.get_name()}")
    
    # 1. Start PIE simulation
    print("Starting Play-in-Editor simulation...")
    unreal.EditorLevelLibrary.editor_play_simulate()
    
    # Yield and wait 2 seconds for level tick and initialization to run
    time.sleep(2.0)
    
    # 2. End PIE simulation
    print("Stopping Play-in-Editor simulation...")
    unreal.EditorLevelLibrary.editor_end_play()
    
    print("SUCCESS: PIE test run executed and completed successfully.")
    return True

if __name__ == "__main__":
    run_pie_test()
