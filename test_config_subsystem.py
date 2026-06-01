import unreal
import sys

def run_tests():
    print("--- ORION CONFIG SUBSYSTEM AUTOMATED TESTS ---")
    
    # 1. Check if class exists
    try:
        subsystem_class = unreal.OrionConfigSubsystem
    except AttributeError:
        print("ERROR: OrionConfigSubsystem class is not registered in unreal namespace!")
        sys.exit(1)
        
    print("SUCCESS: OrionConfigSubsystem class found.")
    
    # 2. Get the Class Default Object (CDO)
    cdo = unreal.get_default_object(subsystem_class)
    if not cdo:
        print("ERROR: Could not get CDO for OrionConfigSubsystem!")
        sys.exit(1)
    print("SUCCESS: Retrieved OrionConfigSubsystem CDO.")
    
    # 3. Call LoadConfig on the CDO
    print("Calling LoadConfig() on CDO...")
    success = cdo.load_config()
    if not success:
        print("ERROR: LoadConfig() returned False!")
        sys.exit(1)
    print("SUCCESS: LoadConfig() completed successfully.")
    
    # 4. Read loaded config values
    config = cdo.get_config()
    print(f"Loaded Company Name: {config.client.company_name}")
    print(f"Loaded Plant Name: {config.client.plant_name}")
    print(f"Loaded Accent Color: {config.client.accent_color}")
    print(f"Loaded Target FPS (Desktop): {config.optimization.target_fps_desktop}")
    
    # Asserts
    assert config.client.company_name == "Morde Foods", f"Assert failed: Company name should be 'Morde Foods', got '{config.client.company_name}'"
    assert config.client.plant_name == "P2 Manufacturing Plant", f"Assert failed: Plant name should be 'P2 Manufacturing Plant', got '{config.client.plant_name}'"
    assert config.optimization.target_fps_desktop == 60, f"Assert failed: Target FPS Desktop should be 60, got {config.optimization.target_fps_desktop}"
    assert cdo.is_config_valid == True, "Assert failed: is_config_valid should be True"
    
    print("SUCCESS: All asserts passed!")
    print("--- ORION CONFIG SUBSYSTEM TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
