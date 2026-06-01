import sys
sys.path.append("C:/Users/SHO/Documents/Unreal Projects/OrionCollab")

print("--- AUTOMATED ASSET SETUP STARTING ---")

try:
    import setup_config_loader
    setup_config_loader.create_config_assets()
except Exception as e:
    print("ERROR running setup_config_loader:", e)

try:
    import import_data_tables
    import_data_tables.import_tables()
except Exception as e:
    print("ERROR running import_data_tables:", e)

try:
    import setup_camera_sweep
    setup_camera_sweep.create_sweep_assets()
except Exception as e:
    print("ERROR running setup_camera_sweep:", e)

print("--- AUTOMATED ASSET SETUP COMPLETED ---")
