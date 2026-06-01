import unreal
import sys

def run_tests():
    print("--- ORION METADATA LINKER AUTOMATED TESTS ---")
    
    # 1. Verify class exists
    try:
        linker_class = unreal.OrionMetadataLinker
    except AttributeError:
        print("ERROR: OrionMetadataLinker class is not registered!")
        sys.exit(1)
    print("SUCCESS: OrionMetadataLinker class found.")
    
    # 2. Get editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        sys.exit(1)
    print(f"SUCCESS: Got editor world: {world.get_name()}")
    
    # 3. Get Subsystem
    linker = unreal.OrionMetadataLinker.get_metadata_linker_subsystem(world)
    if not linker:
        print("ERROR: Could not retrieve OrionMetadataLinker subsystem!")
        sys.exit(1)
    print("SUCCESS: Retrieved OrionMetadataLinker subsystem instance.")
    
    # 4. Spawn a mock Datasmith actor
    print("Spawning mock Datasmith actor...")
    actor_class = unreal.StaticMeshActor
    actor_location = unreal.Vector(0.0, 0.0, 0.0)
    actor_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    
    # Spawn actor using EditorLevelLibrary
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, actor_location, actor_rotation)
    if not actor:
        print("ERROR: Could not spawn mock actor!")
        sys.exit(1)
        
    actor.set_actor_label("SM_Mixer_01_uaid_123")
    actor.tags.append("Datasmith")
    print(f"SUCCESS: Spawned mock actor: {actor.get_actor_label()}")
    
    # 5. Run matching
    print("Running RunMatching()...")
    report = linker.run_matching()
    print(f"Total Scanned: {report.total_actors}")
    print(f"Matched count: {report.matched}")
    print(f"Unmatched count: {report.unmatched}")
    
    # Asserts
    # Since we spawned "SM_Mixer_01_uaid_123" with "Datasmith" tag,
    # the matching algorithm should normalize it to "mixer_01".
    # In DT_Equipment (which we verified has "Mixer_01"), this should be an Exact Match.
    # So Matched should be at least 1!
    assert report.matched >= 1, f"Assert failed: Expected matched count >= 1, got {report.matched}"
    
    # Check if the actor now has the tag "Mixer_01"
    has_tag = False
    for tag in actor.tags:
        if str(tag) == "Mixer_01":
            has_tag = True
            break
    assert has_tag == True, "Assert failed: Actor did not receive EquipmentID tag!"
    print("SUCCESS: Mock actor was correctly tagged with EquipmentID.")
    
    # Check GetActorForEquipment
    matched_actor = linker.get_actor_for_equipment("Mixer_01")
    assert matched_actor == actor, "Assert failed: GetActorForEquipment did not return the correct actor!"
    print("SUCCESS: GetActorForEquipment returned the correct matched actor.")
    
    # Test manual link
    print("Testing ManualLink...")
    # Spawn another actor
    unlinked_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, actor_location, actor_rotation)
    unlinked_actor.set_actor_label("UnrelatedMesh")
    
    # Manually link to Mixer_01
    linker.manual_link(unlinked_actor, "Mixer_01")
    
    # Verify manual link was successful
    matched_actor = linker.get_actor_for_equipment("Mixer_01")
    assert matched_actor == unlinked_actor, "Assert failed: ManualLink did not override the match!"
    
    # Clean up spawned test actors so we don't pollute the level
    unreal.EditorLevelLibrary.destroy_actor(actor)
    unreal.EditorLevelLibrary.destroy_actor(unlinked_actor)
    print("SUCCESS: Cleaned up spawned mock actors.")
    
    print("--- ALL METADATA LINKER TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
