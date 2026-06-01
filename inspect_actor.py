import unreal

subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

# Spawn BP_BasePawn
pawn_class = unreal.load_class(None, "/Game/CollaborativeViewer/Blueprints/Pawn/BP_BasePawn.BP_BasePawn_C")
pawn_loc = unreal.Vector(0.0, 0.0, 100.0)
pawn_rot = unreal.Rotator(0.0, 0.0, 0.0)
pawn = unreal.EditorLevelLibrary.spawn_actor_from_class(pawn_class, pawn_loc, pawn_rot)

with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/inspect_results.txt", "w") as f:
    f.write(f"Spawned pawn instance: {pawn}\n")
    if pawn:
        # Gather subobject handles for the spawned instance
        handles = subsystem.k2_gather_subobject_data_for_instance(pawn)
        f.write(f"Number of subobject handles: {len(handles)}\n")
        
        # Load sweep class
        sweep_class_path = "/Game/CollaborativeViewer/Blueprints/Pawn/BP_CameraSweepManager.BP_CameraSweepManager_C"
        sweep_class = unreal.load_class(None, sweep_class_path)
        f.write(f"Loaded component class: {sweep_class}\n")
        
        if sweep_class and len(handles) > 0:
            params = unreal.AddNewSubobjectParams()
            params.new_class = sweep_class
            params.parent_handle = handles[0]
            # Since this is an instance, we do not provide blueprint_context (or do we?)
            # Let's try without blueprint_context first
            try:
                res = subsystem.add_new_subobject(params)
                if isinstance(res, tuple):
                    new_handle = res[0]
                    fail_reason = res[1]
                else:
                    new_handle = res
                    fail_reason = "No tuple"
                
                is_valid = unreal.SubobjectDataBlueprintFunctionLibrary.is_handle_valid(new_handle)
                f.write(f"Add subobject valid: {is_valid}\n")
                f.write(f"Fail reason: {fail_reason}\n")
                
                if is_valid:
                    # Check if component is in the actor's components list
                    components = pawn.get_components_by_class(unreal.OrionCameraSweepManager)
                    f.write(f"Found components of type OrionCameraSweepManager on instance: {len(components)}\n")
            except Exception as e:
                f.write(f"Failed to add component to instance: {e}\n")
        
        # Clean up
        unreal.EditorLevelLibrary.destroy_actor(pawn)
