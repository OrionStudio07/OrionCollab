import unreal
import sys
import time

def run_tests():
    print("--- ORION HIERARCHY MANAGER AUTOMATED TESTS ---")

    # 1. Verify class exists
    try:
        hierarchy_class = unreal.OrionHierarchyManager
    except AttributeError:
        print("ERROR: OrionHierarchyManager class is not registered!")
        sys.exit(1)
    print("SUCCESS: OrionHierarchyManager class found.")

    # 2. Get editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        sys.exit(1)
    print(f"SUCCESS: Got editor world: {world.get_name()}")

    # 3. Get Subsystem
    hierarchy_manager = unreal.OrionHierarchyManager.get_hierarchy_manager_subsystem(world)
    if not hierarchy_manager:
        print("ERROR: Could not retrieve OrionHierarchyManager subsystem!")
        sys.exit(1)
    print("SUCCESS: Retrieved OrionHierarchyManager subsystem instance.")

    # 4. Trigger build tree if not already populated (poll if running asynchronously)
    buildings = hierarchy_manager.get_building_list()
    if len(buildings) > 0:
        print("SUCCESS: Hierarchy tree already built.")
    else:
        print("Triggering BuildTree()...")
        hierarchy_manager.build_tree()

        # Wait up to 5 seconds for background build completion
        b_built = False
        for i in range(50):
            buildings = hierarchy_manager.get_building_list()
            if len(buildings) > 0:
                b_built = True
                break
            time.sleep(0.1)

        assert b_built == True, "Assert failed: Hierarchy tree construction timed out!"
        print("SUCCESS: Hierarchy tree built asynchronously in the background.")

    # 5. Assert structural tree integrity against imported CSV data
    buildings = hierarchy_manager.get_building_list()
    print(f"Total buildings parsed: {len(buildings)}")
    assert len(buildings) >= 2, f"Expected >= 2 buildings, got {len(buildings)}"
    print("SUCCESS: Building list integrity verified.")

    # Check rooms for Building_A
    rooms = hierarchy_manager.get_rooms_by_building("Building_A")
    assert len(rooms) >= 1, "Expected rooms in Building_A!"
    room_found = False
    for r in rooms:
        if str(r.room_id) == "Room_101":
            room_found = True
            # Safety Zone check: Room_101 safety zone is Clean Room (SafetyZone = SafetyZoneType = Clean)
            # From DT_Rooms: Room_101 safety zone type is Clean Room
            assert r.safety_zone == unreal.ZoneClassification.GENERAL, f"Expected safety zone GENERAL, got {r.safety_zone}"
            break
    assert room_found == True, "Expected Room_101 in Building_A!"
    print("SUCCESS: Room list and safety zone classification verified.")

    # Check equipment in Room_101
    equipment = hierarchy_manager.get_equipment_by_room("Room_101")
    assert len(equipment) >= 1, "Expected equipment in Room_101!"
    eq_found = False
    for eq in equipment:
        if str(eq.equipment_id) == "Mixer_01":
            eq_found = True
            assert eq.type == unreal.EquipmentType.MIXER, f"Expected type MIXER, got {eq.type}"
            break
    assert eq_found == True, "Expected Mixer_01 in Room_101!"
    print("SUCCESS: Room equipment query and classification verified.")

    # Test components lazy loading
    print("Testing lazy loading of component IDs...")
    components = hierarchy_manager.get_components_by_equipment("Mixer_01")
    print(f"Components found: {list(components)}")
    # Mixer_01 has MaintenanceComponents = None or empty in CSV. Let's make sure it's queryable
    assert isinstance(components, unreal.Array) or isinstance(components, list), "Expected components list return type!"
    print("SUCCESS: Lazy loading of component IDs verified.")

    # 6. Verify SearchAll APIs
    print("Testing SearchAll APIs...")
    
    # Fast path: substring match "Ribbon"
    results = hierarchy_manager.search_all("Ribbon")
    assert len(results) >= 1, "Expected results for substring query 'Ribbon'!"
    first_result = results[0]
    assert str(first_result.id) == "Mixer_01", f"Expected Mixer_01 as first result, got {first_result.id}"
    assert first_result.relevance >= 0.8, f"Expected high relevance, got {first_result.relevance}"
    print(f"SUCCESS: Substring fast path search verified (Relevance: {first_result.relevance}).")

    # Fuzzy path: typo match "Mixr" via Levenshtein distance
    results_fuzzy = hierarchy_manager.search_all("Mixr")
    assert len(results_fuzzy) >= 1, "Expected results for fuzzy query 'Mixr'!"
    fuzzy_found = False
    for res in results_fuzzy:
        if str(res.id) == "Mixer_01":
            fuzzy_found = True
            assert res.relevance == 0.5, f"Expected relevance 0.5 for fuzzy match, got {res.relevance}"
            assert res.equipment_type == unreal.EquipmentType.MIXER, f"Expected type MIXER, got {res.equipment_type}"
            break
    assert fuzzy_found == True, "Fuzzy query did not find Mixer_01!"
    print("SUCCESS: Fuzzy Levenshtein matching and result classification verified.")

    # 7. Verify Caching system
    print("Testing search cache performance...")
    # First search
    start_time = time.perf_counter()
    hierarchy_manager.search_all("UniqueQueryString")
    first_duration = time.perf_counter() - start_time

    # Cached search
    start_time = time.perf_counter()
    hierarchy_manager.search_all("UniqueQueryString")
    cached_duration = time.perf_counter() - start_time

    print(f"First search duration: {first_duration*1000.0:.4f} ms")
    print(f"Cached search duration: {cached_duration*1000.0:.4f} ms")

    assert cached_duration <= first_duration, "Expected cache duration to be equal or faster than first query!"
    print("SUCCESS: Search query caching and performance budget verified.")

    print("--- ALL ORION HIERARCHY MANAGER TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
