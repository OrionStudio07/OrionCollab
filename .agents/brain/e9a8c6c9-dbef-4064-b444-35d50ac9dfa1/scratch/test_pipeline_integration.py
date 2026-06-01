import sqlite3
import os
import sys
import json

def create_mock_database(db_path):
    print(f"INFO: Creating mock database at: {db_path}")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create EngineeringItems table
    cursor.execute("""
    CREATE TABLE EngineeringItems (
        PnPID INTEGER PRIMARY KEY,
        Tag TEXT,
        Area TEXT,
        LineNumberTag TEXT
    )
    """)
    
    # 2. Create Equipment table
    cursor.execute("""
    CREATE TABLE Equipment (
        PnPID INTEGER PRIMARY KEY,
        Tag TEXT,
        LongDescription TEXT,
        Class TEXT,
        Manufacturer TEXT,
        Model TEXT
    )
    """)
    
    # 3. Populate mock data
    mock_items = [
        (101, "Mixer_01", "Building_A", "PL-001"),
        (102, "Pump_01", "Building_A", "PL-001"),
        (103, "Vessel_01", "Building_B", "PL-002")
    ]
    
    mock_equipment = [
        (101, "Mixer_01", "Ribbon Mixer #1", "Mixer", "GEA Group", "tCut 200"),
        (102, "Pump_01", "Feed Pump #1", "Pump", "Grundfos", "CR 32-2"),
        (103, "Vessel_01", "Storage Tank #1", "Vessel", "Feldmeier", "FT-500")
    ]
    
    cursor.executemany("INSERT INTO EngineeringItems VALUES (?, ?, ?, ?)", mock_items)
    cursor.executemany("INSERT INTO Equipment VALUES (?, ?, ?, ?, ?, ?)", mock_equipment)
    
    conn.commit()
    conn.close()
    print("SUCCESS: Mock database populated.")

def run_integration_test():
    print("--- PIPELINE B INTEGRATION TEST RUNNER ---")
    sys.path.append("C:/Users/SHO/Documents/Unreal Projects/OrionCollab")
    
    db_path = "mock_Piping.db"
    json_path = "mock_metadata.json"
    csv_dir = "Content/CollaborativeViewer/Data"
    
    # Step 1: Create mock db
    create_mock_database(db_path)
    
    # Step 2: Run extract script
    print("Running export_plant3d_metadata.py...")
    import export_plant3d_metadata
    success = export_plant3d_metadata.extract_metadata(db_path, json_path)
    assert success == True, "Extraction script reported failure!"
    
    # Verify JSON file
    assert os.path.exists(json_path) == True, "JSON output not created!"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert len(data) == 3, f"Expected 3 entries, got {len(data)}"
    print("SUCCESS: JSON output matches mock data count.")
    
    # Verify schema fields
    first_item = data[0]
    expected_keys = ["equipment_id", "display_name", "pid_tag", "equipment_type", "process_line", "building_id", "room_id", "manufacturer", "model", "specs"]
    for key in expected_keys:
        assert key in first_item, f"Expected key '{key}' in JSON entry, not found!"
    print("SUCCESS: JSON schema fields validated.")
    
    # Step 3: Run convert script
    print("Running convert_metadata_to_csv.py...")
    import convert_metadata_to_csv
    success = convert_metadata_to_csv.convert_metadata(json_path, csv_dir)
    assert success == True, "Conversion script reported failure!"
    
    # Step 4: Verify generated CSV files
    csv_files = ["DT_Equipment.csv", "DT_Buildings.csv", "DT_Rooms.csv", "DT_ProcessLines.csv"]
    for f in csv_files:
        path = os.path.join(csv_dir, f)
        assert os.path.exists(path) == True, f"Expected CSV file not found: {path}"
        print(f"SUCCESS: Validated existence of {f}")
        
    # Verify DT_Equipment.csv columns and escaping
    eq_path = os.path.join(csv_dir, "DT_Equipment.csv")
    with open(eq_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check headers
    assert "---,EquipmentID,DisplayName,PIDTag,EquipmentType,ProcessLine,BuildingID,RoomID,ZoneID,Manufacturer,Model,SpecsJSON,bHasExplode" in content, "DT_Equipment.csv headers mismatch!"
    
    # Check escaping of SpecsJSON double-quotes
    assert '"{""pnpid"": 101, ""class_type"": ""Mixer""}"' in content or '"{""pnpid"": 101, ""class_type"": ""Mixer""}' in content or '""pnpid"": 101' in content, "SpecsJSON double quotes escaping failed!"
    print("SUCCESS: Checked SpecsJSON double-quote escaping successfully.")
    
    # Clean up mock files
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists(json_path):
        os.remove(json_path)
    print("SUCCESS: Cleaned up temporary integration test files.")
    
    print("--- ALL PIPELINE INTEGRATION TESTS PASSED ---")

if __name__ == "__main__":
    run_integration_test()
