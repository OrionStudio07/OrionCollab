import unreal
import sys
import math

def run_tests():
    print("--- ORION CAMERA SWEEP SYSTEM AUTOMATED TESTS ---")
    
    # 1. Verify C++ Class exists
    try:
        sweep_class = unreal.OrionCameraSweepManager
    except AttributeError:
        print("ERROR: OrionCameraSweepManager class is not registered!")
        sys.exit(1)
    print("SUCCESS: OrionCameraSweepManager C++ class found.")

    # 2. Get editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        sys.exit(1)
    print(f"SUCCESS: Got editor world: {world.get_name()}")

    # 3. Spawn Mock Pawn
    pawn_class = unreal.Pawn
    pawn_loc = unreal.Vector(0.0, 0.0, 100.0)
    pawn_rot = unreal.Rotator(0.0, 0.0, 0.0)
    pawn = unreal.EditorLevelLibrary.spawn_actor_from_class(pawn_class, pawn_loc, pawn_rot)
    if not pawn:
        print("ERROR: Could not spawn mock pawn!")
        sys.exit(1)
    print("SUCCESS: Spawned mock Pawn.")

    # Add component using SubobjectDataSubsystem on spawned instance
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_instance(pawn)
    if len(handles) == 0:
        print("ERROR: No subobject handles gathered for pawn!")
        unreal.EditorLevelLibrary.destroy_actor(pawn)
        sys.exit(1)
        
    params = unreal.AddNewSubobjectParams()
    params.new_class = unreal.load_class(None, "/Game/CollaborativeViewer/Blueprints/Pawn/BP_CameraSweepManager.BP_CameraSweepManager_C")
    if not params.new_class:
        params.new_class = unreal.OrionCameraSweepManager
        
    params.parent_handle = handles[0]
    
    new_handle_res = subsystem.add_new_subobject(params)
    new_handle = new_handle_res[0] if isinstance(new_handle_res, tuple) else new_handle_res
    
    if not unreal.SubobjectDataBlueprintFunctionLibrary.is_handle_valid(new_handle):
        print("ERROR: Could not instantiate and register component via SubobjectDataSubsystem!")
        unreal.EditorLevelLibrary.destroy_actor(pawn)
        sys.exit(1)
        
    components = pawn.get_components_by_class(unreal.OrionCameraSweepManager)
    if len(components) == 0:
        print("ERROR: Component not found in actor's component list after addition!")
        unreal.EditorLevelLibrary.destroy_actor(pawn)
        sys.exit(1)
        
    comp = components[0]
    print("SUCCESS: Instantiated and registered OrionCameraSweepManager component.")

    # 5. Verify default properties
    assert comp.sweep_speed == unreal.OrionSweepSpeed.MEDIUM, f"Expected MEDIUM (1), got {comp.sweep_speed}"
    assert comp.min_view_distance == 200.0, f"Expected 200.0, got {comp.min_view_distance}"
    assert comp.max_view_distance == 2000.0, f"Expected 2000.0, got {comp.max_view_distance}"
    assert comp.collision_avoidance_radius == 50.0, f"Expected 50.0, got {comp.collision_avoidance_radius}"
    assert comp.is_sweeping() == False, "Expected IsSweeping to be False initially"
    print("SUCCESS: Default component property values verified.")

    # 6. Verify setting properties
    comp.set_editor_property("sweep_speed", unreal.OrionSweepSpeed.FAST)
    comp.set_editor_property("min_view_distance", 300.0)
    comp.set_editor_property("max_view_distance", 1500.0)
    comp.set_editor_property("collision_avoidance_radius", 40.0)
    
    assert comp.sweep_speed == unreal.OrionSweepSpeed.FAST, "Failed to set sweep_speed to FAST"
    assert comp.min_view_distance == 300.0, "Failed to set min_view_distance"
    assert comp.max_view_distance == 1500.0, "Failed to set max_view_distance"
    assert comp.collision_avoidance_radius == 40.0, "Failed to set collision_avoidance_radius"
    print("SUCCESS: Property modification verified.")

    # 7. Test CalculateOptimalCameraLocation math
    target_class = unreal.StaticMeshActor
    target_loc = unreal.Vector(1000.0, 1000.0, 100.0)
    target = unreal.EditorLevelLibrary.spawn_actor_from_class(target_class, target_loc, pawn_rot)
    if not target:
        print("ERROR: Could not spawn target actor!")
        unreal.EditorLevelLibrary.destroy_actor(pawn)
        sys.exit(1)

    print(f"Testing optimal framing math looking at actor at {target_loc}...")
    optimal_loc, optimal_rot = comp.calculate_optimal_camera_location(target)
    print(f"Calculated optimal location: {optimal_loc}, rotation: {optimal_rot}")
    
    # Target is at 1000, 1000, 100. Pawn is at 0, 0, 100.
    # The direction from target to camera (0,0,100 - 1000,1000,100) is (-1000, -1000, 0).
    # Since Z is < 0.2, the Z component is overridden to 0.3 to maintain elevation.
    # Therefore, the Z coordinate of optimal_loc should be greater than the target's Z (100.0).
    assert optimal_loc.z > 100.0, f"Expected camera to be elevated above 100.0, got Z={optimal_loc.z}"
    
    # The distance from optimal_loc to target should be within [min_view_distance, max_view_distance]
    dist_vec = optimal_loc - target_loc
    distance = math.sqrt(dist_vec.x**2 + dist_vec.y**2 + dist_vec.z**2)
    print(f"Calculated distance: {distance} units (Min: {comp.min_view_distance}, Max: {comp.max_view_distance})")
    assert (comp.min_view_distance - 0.1) <= distance <= (comp.max_view_distance + 0.1), "Optimal location distance is out of bounds!"
    print("SUCCESS: Optimal camera location framing math validated.")

    # 8. Test SweepToActor initiation
    print("Triggering SweepToActor...")
    comp.sweep_to_actor(target, "MockEquipmentID")
    assert comp.is_sweeping() == True, "Expected component is_sweeping to be True after sweep trigger"
    print("SUCCESS: Camera sweep correctly initiated.")

    # Clean up spawned test actors
    unreal.EditorLevelLibrary.destroy_actor(pawn)
    unreal.EditorLevelLibrary.destroy_actor(target)
    print("SUCCESS: Cleaned up spawned mock actors.")
    
    print("--- ALL ORION CAMERA SWEEP SYSTEM TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
