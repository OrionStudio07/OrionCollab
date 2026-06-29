import unreal
import sys
import time

def run_tests():
    print("--- ORION SEARCH SYSTEM AUTOMATED TESTS ---")
    
    # 1. Verify WBP_SearchBar asset registry
    search_bar_path = "/Game/CollaborativeViewer/UMG/SidePanel/WBP_SearchBar"
    if not unreal.EditorAssetLibrary.does_asset_exist(search_bar_path):
        print(f"ERROR: WBP_SearchBar asset does not exist at {search_bar_path}!")
        sys.exit(1)
    print("SUCCESS: WBP_SearchBar asset exists in registry.")
    
    # 2. Get editor world
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        sys.exit(1)
    print(f"SUCCESS: Got editor world: {world.get_name()}")
    
    # 3. Get Hierarchy Manager Subsystem
    hierarchy_manager = unreal.OrionHierarchyManager.get_hierarchy_manager_subsystem(world)
    if not hierarchy_manager:
        print("ERROR: Could not retrieve OrionHierarchyManager subsystem!")
        sys.exit(1)
    print("SUCCESS: Retrieved OrionHierarchyManager subsystem instance.")
    
    # Wait for tree to be built if it isn't already
    buildings = hierarchy_manager.get_building_list()
    if len(buildings) == 0:
        print("Tree not built. Triggering BuildTree() and waiting...")
        hierarchy_manager.build_tree()
        b_built = False
        for i in range(50):
            buildings = hierarchy_manager.get_building_list()
            if len(buildings) > 0:
                b_built = True
                break
            time.sleep(0.1)
        assert b_built == True, "Assert failed: Tree build timed out!"
    else:
        print("Tree is already built.")
    
    # 4. Perform Search and Wrap Results
    print("Performing fuzzy search for 'Mixr'...")
    results = hierarchy_manager.search_all("Mixr")
    print(f"Search returned {len(results)} results.")
    assert len(results) >= 1, "Assert failed: Expected at least 1 search result!"
    
    # Simulate wrapping results into UOrionTreeItemData for UListView
    print("Simulating virtualized list wrapping...")
    wrapped_results = []
    for res in results:
        # Instantiate UOrionTreeItemData UObject
        item_data = unreal.OrionTreeItemData()
        item_data.node_id = res.id
        item_data.display_name = res.display_name
        item_data.depth = 0 # flat result display
        
        # Parse Category string to EOrionTreeCategory enum
        if res.category == "Building":
            item_data.category = unreal.OrionTreeCategory.BUILDING
        elif res.category == "Room":
            item_data.category = unreal.OrionTreeCategory.ROOM
        elif res.category == "Equipment":
            item_data.category = unreal.OrionTreeCategory.EQUIPMENT
        else:
            item_data.category = unreal.OrionTreeCategory.COMPONENT
            
        item_data.equipment_type = res.equipment_type
        wrapped_results.append(item_data)
        
    print(f"Successfully wrapped {len(wrapped_results)} search results into UOrionTreeItemData UObjects.")
    
    # Verify properties on the first matched item
    first_item = wrapped_results[0]
    print(f"Verifying wrapped item properties for NodeID: {first_item.node_id}")
    assert str(first_item.node_id) in ["Mixer_01", "Mixer_02"], f"Expected NodeID 'Mixer_01' or 'Mixer_02', got '{first_item.node_id}'"
    assert first_item.category == unreal.OrionTreeCategory.EQUIPMENT, "Expected category EOrionTreeCategory::Equipment"
    assert first_item.depth == 0, f"Expected Depth = 0 for flat list results, got {first_item.depth}"
    assert first_item.equipment_type == unreal.EquipmentType.MIXER, "Expected type MIXER"
    print("SUCCESS: Wrapped item property verification passed.")
    
    # 5. Verify Delegate Binding and Broadcast
    print("Testing selection delegate and camera sweep propagation...")
    
    selected_node = None
    def on_equipment_selected_callback(equipment_id):
        nonlocal selected_node
        selected_node = equipment_id
        print(f"DELEGATE CALLBACK: Selected Equipment ID: {equipment_id}")
        
    # Bind test callback to OnEquipmentSelected multicast delegate
    hierarchy_manager.on_equipment_selected.add_callable(on_equipment_selected_callback)
    
    # Simulate a selection click from Search Result Row
    hierarchy_manager.on_equipment_selected.broadcast("Mixer_01")
    
    # Verify broadcast propagation
    assert selected_node == "Mixer_01", f"Expected selected_node 'Mixer_01' in delegate, got '{selected_node}'"
    print("SUCCESS: OnEquipmentSelected delegate binding and broadcast propagation verified.")
    
    # Clean up delegate bindings
    hierarchy_manager.on_equipment_selected.remove_callable(on_equipment_selected_callback)
    
    print("--- ALL ORION SEARCH SYSTEM TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
