import os
import sys
import sqlite3
import json
import re

def clean_id(tag_name):
    """Normalize tag names to generate valid equipment IDs (e.g. Mixer_01)"""
    if not tag_name:
        return "Unknown_Equipment"
    # Replace spaces, dashes, hyphens, and slashes with underscores
    cleaned = re.sub(r'[\s\-\\\/]+', '_', tag_name)
    # Remove any other non-alphanumeric characters except underscores
    cleaned = re.sub(r'[^\w]', '', cleaned)
    return cleaned

def extract_metadata(db_path, output_json_path):
    print(f"INFO: Connecting to AutoCAD Plant 3D database at: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found at: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Resilient SQL query with fallback
        query = """
        SELECT 
            e.PnPID, 
            e.Tag, 
            e.LongDescription, 
            e.Class, 
            e.Manufacturer, 
            e.Model,
            i.Area, 
            i.LineNumberTag
        FROM Equipment e
        LEFT JOIN EngineeringItems i ON e.PnPID = i.PnPID
        """
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            print("INFO: Executed Equipment join query successfully.")
        except sqlite3.OperationalError as join_err:
            print(f"WARNING: Joint query failed ({join_err}). Falling back to simple query on Equipment table...")
            # Fallback: query Equipment table directly in case EngineeringItems is missing
            fallback_query = "SELECT PnPID, Tag, LongDescription, Class, Manufacturer, Model, PnPID, PnPID FROM Equipment"
            try:
                cursor.execute(fallback_query)
                rows = cursor.fetchall()
                print("INFO: Executed fallback Equipment query successfully.")
            except sqlite3.OperationalError as fallback_err:
                print(f"ERROR: Fallback query failed ({fallback_err}). Database schema does not contain an Equipment table.")
                conn.close()
                return False

        # Get column names to capture extra specs dynamically
        column_names = [description[0].lower() for description in cursor.description]
        
        equipment_list = []
        
        for row in rows:
            # Map standard columns
            pnpid = row[0]
            tag = row[1] if row[1] else f"EQ_{pnpid}"
            long_desc = row[2] if row[2] else f"Equipment {tag}"
            eq_type = row[3] if row[3] else "Other"
            manufacturer = row[4] if row[4] else "Unknown Manufacturer"
            model = row[5] if row[5] else "Unknown Model"
            area = row[6] if row[6] else "Building_A"
            process_line = row[7] if row[7] else "PL-001"
            
            # Map to standard Orion JSON format
            eq_id = clean_id(tag)
            
            # Collect extra attributes as specs
            specs = {
                "pnpid": pnpid,
                "class_type": eq_type,
            }
            
            # If there are additional custom columns in the DB, append them to specs
            for idx, col in enumerate(column_names):
                if col not in ["pnpid", "tag", "longdescription", "class", "manufacturer", "model", "area", "linenumbertag"]:
                    specs[col] = row[idx] if row[idx] is not None else ""

            # Ensure default building/room references
            building_id = clean_id(area) if area else "Building_A"
            room_id = "Room_101" # Default room reference, overridden during CSV conversion if needed
            
            eq_data = {
                "equipment_id": eq_id,
                "display_name": long_desc,
                "pid_tag": tag,
                "equipment_type": eq_type,
                "process_line": process_line,
                "building_id": building_id,
                "room_id": room_id,
                "manufacturer": manufacturer,
                "model": model,
                "specs": specs
            }
            
            equipment_list.append(eq_data)

        # Write to JSON
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(equipment_list, f, indent=2, ensure_ascii=False)
            
        print(f"SUCCESS: Exported {len(equipment_list)} equipment entries to {output_json_path}")
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: Exception occurred while extracting metadata: {e}")
        return False

if __name__ == "__main__":
    db_file = "Piping.db"
    out_file = "equipment_metadata.json"
    
    if len(sys.argv) > 1:
        db_file = sys.argv[1]
    if len(sys.argv) > 2:
        out_file = sys.argv[2]
        
    success = extract_metadata(db_file, out_file)
    sys.exit(0 if success else 1)
