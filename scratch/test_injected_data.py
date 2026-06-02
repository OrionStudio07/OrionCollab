import urllib.request
import json
import time
import sys

def make_rc_call(payload):
    url = "http://127.0.0.1:30010/remote/object/call"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_injected_data_tests():
    print("=== STARTING INJECTED TEST DATA VERIFICATION ===")
    
    # 1. Trigger BuildTree() asynchronously
    build_command = (
        "import unreal; "
        "world = unreal.EditorLevelLibrary.get_editor_world(); "
        "hierarchy_manager = unreal.OrionHierarchyManager.get_hierarchy_manager_subsystem(world); "
        "hierarchy_manager.build_tree(); "
        "print('BuildTree triggered successfully')"
    )
    
    build_payload = {
        "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        "functionName": "ExecutePythonCommand",
        "parameters": {
            "PythonCommand": build_command
        }
    }
    
    print("Triggering BuildTree() inside Unreal Editor...")
    build_res = make_rc_call(build_payload)
    print(f"Response: {build_res}")
    
    # 2. Sleep for 1.0 second on the host side
    # This yields the Unreal Engine Game Thread completely, allowing it to process Slate events, ticks,
    # and ENamedThreads::GameThread background completion dispatches!
    print("Waiting 1.0 second for async background tree construction to complete...")
    time.sleep(1.0)
    
    # 3. Query and verify Mixer_02 via SearchAll and Hierarchy Subsystem
    verify_command = """import unreal
import sys
world = unreal.EditorLevelLibrary.get_editor_world()
hierarchy_manager = unreal.OrionHierarchyManager.get_hierarchy_manager_subsystem(world)
buildings = hierarchy_manager.get_building_list()
if len(buildings) == 0:
    print('ERROR: Tree was not built properly!')
    sys.exit(1)
results = hierarchy_manager.search_all('Fluidized')
if len(results) == 0:
    print('ERROR: Search for Fluidized returned 0 results!')
    sys.exit(1)
res = results[0]
assert str(res.id) == 'Mixer_02', f'Expected Mixer_02, got {res.id}'
assert str(res.display_name) == 'Fluidized Mixer #2', f'Expected Fluidized Mixer #2, got {res.display_name}'
assert res.equipment_type == unreal.EquipmentType.MIXER, f'Expected MIXER type, got {res.equipment_type}'
print('SUCCESS: Verified injected Mixer_02 properties and search capability.')
"""
    
    verify_payload = {
        "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        "functionName": "ExecutePythonCommand",
        "parameters": {
            "PythonCommand": verify_command
        }
    }
    
    print("Querying and verifying search and properties for injected 'Mixer_02'...")
    try:
        verify_res = make_rc_call(verify_payload)
        print(f"Verification call completed. ReturnValue: {verify_res.get('ReturnValue')}")
        print("SUCCESS: Injected data verification tests PASSED!")
        print("=== INJECTED TEST DATA VERIFICATION COMPLETE ===")
    except Exception as e:
        print(f"FAILED: verification failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_injected_data_tests()
