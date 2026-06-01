import unreal

output_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/inspect_api_output.txt"
with open(output_path, "w") as f:
    f.write("--- SEARCHING UNREAL NAMESPACE ---\n")
    
    # Search unreal functions/classes
    all_unreal = dir(unreal)
    component_related = [x for x in all_unreal if "component" in x.lower()]
    f.write("Component-related classes/functions:\n")
    f.write(str(component_related) + "\n\n")
    
    # Search EditorActorSubsystem
    try:
        subsystem = unreal.EditorActorSubsystem
        f.write("EditorActorSubsystem methods:\n")
        f.write(str([m for m in dir(subsystem) if not m.startswith("_")]) + "\n")
    except Exception as e:
        f.write("EditorActorSubsystem not found: " + str(e) + "\n")
