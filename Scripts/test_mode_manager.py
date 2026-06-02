import unreal
import sys

def run_tests():
    print("--- ORION MODE MANAGER AUTOMATED TESTS ---")
    
    # 1. Verify class exists
    try:
        manager_class = unreal.OrionModeManager
    except AttributeError:
        print("ERROR: OrionModeManager class is not registered!")
        sys.exit(1)
    print("SUCCESS: OrionModeManager class found.")
    
    # 2. Get editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        sys.exit(1)
    print(f"SUCCESS: Got editor world: {world.get_name()}")
    
    # 3. Get Subsystem
    manager = unreal.OrionModeManager.get_mode_manager_subsystem(world)
    if not manager:
        print("ERROR: Could not retrieve OrionModeManager subsystem!")
        sys.exit(1)
    print("SUCCESS: Retrieved OrionModeManager subsystem instance.")
    
    # 4. Test CanAccessMode rules
    print("Testing CanAccessMode permissions...")
    # Admin
    assert manager.can_access_mode(unreal.OrionMode.MODE_LAUNCHER, unreal.OrionRole.ROLE_ADMIN) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_SHOWCASE, unreal.OrionRole.ROLE_ADMIN) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_OPERATIONS, unreal.OrionRole.ROLE_ADMIN) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_TRAINING, unreal.OrionRole.ROLE_ADMIN) == True
    print("SUCCESS: Admin accesses all modes verified.")
    
    # Engineer
    assert manager.can_access_mode(unreal.OrionMode.MODE_LAUNCHER, unreal.OrionRole.ROLE_ENGINEER) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_SHOWCASE, unreal.OrionRole.ROLE_ENGINEER) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_OPERATIONS, unreal.OrionRole.ROLE_ENGINEER) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_TRAINING, unreal.OrionRole.ROLE_ENGINEER) == False
    print("SUCCESS: Engineer accesses correct modes verified.")
    
    # Viewer
    assert manager.can_access_mode(unreal.OrionMode.MODE_LAUNCHER, unreal.OrionRole.ROLE_VIEWER) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_SHOWCASE, unreal.OrionRole.ROLE_VIEWER) == True
    assert manager.can_access_mode(unreal.OrionMode.MODE_OPERATIONS, unreal.OrionRole.ROLE_VIEWER) == False
    assert manager.can_access_mode(unreal.OrionMode.MODE_TRAINING, unreal.OrionRole.ROLE_VIEWER) == False
    print("SUCCESS: Viewer accesses correct modes verified.")
    
    # 5. Test state transitions
    print("Testing SetMode/GetMode transitions...")
    
    # Set to Viewer and attempt invalid transition to Operations
    manager.set_current_role(unreal.OrionRole.ROLE_VIEWER)
    manager.set_mode(unreal.OrionMode.MODE_LAUNCHER) # reset
    
    # Try to enter Operations
    manager.set_mode(unreal.OrionMode.MODE_OPERATIONS)
    current_mode = manager.get_current_mode()
    assert current_mode == unreal.OrionMode.MODE_LAUNCHER, f"Assert failed: Viewer entered Operations! Current mode: {current_mode}"
    print("SUCCESS: Viewer rejected from Operations.")
    
    # Try to enter Showcase
    manager.set_mode(unreal.OrionMode.MODE_SHOWCASE)
    current_mode = manager.get_current_mode()
    assert current_mode == unreal.OrionMode.MODE_SHOWCASE, f"Assert failed: Viewer could not enter Showcase! Current mode: {current_mode}"
    print("SUCCESS: Viewer entered Showcase successfully.")
    
    # Set to Engineer and enter Operations
    manager.set_current_role(unreal.OrionRole.ROLE_ENGINEER)
    manager.set_mode(unreal.OrionMode.MODE_OPERATIONS)
    current_mode = manager.get_current_mode()
    assert current_mode == unreal.OrionMode.MODE_OPERATIONS, f"Assert failed: Engineer could not enter Operations! Current mode: {current_mode}"
    print("SUCCESS: Engineer entered Operations successfully.")
    
    print("--- ALL ORION MODE MANAGER TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
