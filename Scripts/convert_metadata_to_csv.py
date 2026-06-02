import os
import sys
import json
import csv

def escape_specs_json(specs_dict):
    """Serialize dynamic specs dictionary to JSON and double up double-quotes for UE5 CSV compliance"""
    if not specs_dict:
        return '"{}"'
    json_str = json.dumps(specs_dict, ensure_ascii=False)
    # Double up double-quotes for CSV cell wrapping
    escaped_json = json_str.replace('"', '""')
    return f'"{escaped_json}"'

def format_ue_vector(x=0.0, y=0.0, z=0.0):
    """Format FVector to UE5 CSV style: \"(X=0.000,Y=0.000,Z=0.000)\""""
    return f'"(X={x:.3f},Y={y:.3f},Z={z:.3f})"'

def format_ue_color(r=0.5, g=0.5, b=0.5, a=0.3):
    """Format FLinearColor to UE5 CSV style: \"(R=0.500,G=0.500,B=0.500,A=0.300)\""""
    return f'"(R={r:.3f},G={g:.3f},B={b:.3f},A={a:.3f})"'

def format_ue_array(items):
    """Format TArray<FName> to UE5 CSV style: \"(Item1,Item2)\""""
    if not items:
        return '"()"'
    joined_items = ",".join(items)
    return f'"({joined_items})"'

def convert_metadata(json_path, output_dir):
    print(f"INFO: Converting metadata from {json_path} to CSV files in: {output_dir}")
    
    if not os.path.exists(json_path):
        print(f"ERROR: Metadata JSON not found at: {json_path}")
        return False
        
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        print(f"INFO: Loaded {len(metadata)} equipment entries.")
        
        # 1. Output DT_Equipment.csv
        eq_csv_path = os.path.join(output_dir, "DT_Equipment.csv")
        
        unique_buildings = set()
        unique_rooms = set()
        process_lines_map = {} # Maps ProcessLineID to unique list of EquipmentIDs
        
        with open(eq_csv_path, 'w', encoding='utf-8', newline='') as f:
            # Note: UE5 expects the first column to be named '---' for the RowName
            f.write("---,EquipmentID,DisplayName,PIDTag,EquipmentType,ProcessLine,BuildingID,RoomID,ZoneID,Manufacturer,Model,SpecsJSON,bHasExplode\n")
            
            for idx, eq in enumerate(metadata):
                row_name = f"Row_{idx+1:03d}"
                eq_id = eq.get("equipment_id", "Unknown")
                display_name = eq.get("display_name", "")
                pid_tag = eq.get("pid_tag", "")
                eq_type = eq.get("equipment_type", "Other")
                process_line = eq.get("process_line", "PL-001")
                building_id = eq.get("building_id", "Building_A")
                room_id = eq.get("room_id", "Room_101")
                manufacturer = eq.get("manufacturer", "Unknown")
                model = eq.get("model", "Unknown")
                specs = eq.get("specs", {})
                
                # Format custom SpecsJSON with doubled double-quotes
                specs_json = escape_specs_json(specs)
                
                # Deduce features
                b_has_explode = "true" if eq_type in ["Mixer", "Vessel", "Pump", "Compressor", "HeatExchanger"] else "false"
                zone_id = f"Zone_{room_id.split('_')[-1]}" if "_" in room_id else "Zone_101"
                
                # Collect entities for relational tables
                unique_buildings.add(building_id)
                unique_rooms.add((room_id, building_id))
                
                if process_line not in process_lines_map:
                    process_lines_map[process_line] = []
                process_lines_map[process_line].append(eq_id)
                
                # Write row verbatim to CSV to preserve custom double-quoted strings
                line = f'{row_name},{eq_id},"{display_name}",{pid_tag},{eq_type},{process_line},{building_id},{room_id},{zone_id},"{manufacturer}","{model}",{specs_json},{b_has_explode}\n'
                f.write(line)
                
        print(f"SUCCESS: Generated {eq_csv_path}")

        # 2. Output DT_Buildings.csv
        bld_csv_path = os.path.join(output_dir, "DT_Buildings.csv")
        with open(bld_csv_path, 'w', encoding='utf-8', newline='') as f:
            f.write("---,BuildingID,DisplayName,Floors,LocationOrigin,LocationExtent\n")
            for idx, bld in enumerate(sorted(unique_buildings)):
                row_name = f"Row_{idx+1:03d}"
                display_name = f"{bld.replace('_', ' ')}"
                origin = format_ue_vector(0.0, 0.0, 0.0)
                extent = format_ue_vector(1000.0, 1000.0, 1000.0)
                f.write(f'{row_name},{bld},"{display_name}",3,{origin},{extent}\n')
        print(f"SUCCESS: Generated {bld_csv_path}")

        # 3. Output DT_Rooms.csv
        rm_csv_path = os.path.join(output_dir, "DT_Rooms.csv")
        with open(rm_csv_path, 'w', encoding='utf-8', newline='') as f:
            f.write("---,RoomID,BuildingID,DisplayName,Floor,Function,SafetyZoneType,SafetyZoneColor\n")
            for idx, (rm, bld) in enumerate(sorted(unique_rooms)):
                row_name = f"Row_{idx+1:03d}"
                display_name = f"Hall {rm.split('_')[-1]}" if "_" in rm else rm
                color = format_ue_color(0.5, 0.5, 0.5, 0.3)
                f.write(f'{row_name},{rm},{bld},"{display_name}",1,"Mixing and Processing",General,{color}\n')
        print(f"SUCCESS: Generated {rm_csv_path}")

        # 4. Output DT_ProcessLines.csv
        pl_csv_path = os.path.join(output_dir, "DT_ProcessLines.csv")
        with open(pl_csv_path, 'w', encoding='utf-8', newline='') as f:
            f.write("---,ProcessLineID,DisplayName,ConnectedEquipment,PIDDocPath\n")
            for idx, (pl_id, equips) in enumerate(sorted(process_lines_map.items())):
                row_name = f"Row_{idx+1:03d}"
                display_name = f"Process Line {pl_id}"
                connected_array = format_ue_array(equips)
                doc_path = f"/Game/PIDs/{pl_id.replace('-', '')}.pdf"
                f.write(f'{row_name},{pl_id},"{display_name}",{connected_array},"{doc_path}"\n')
        print(f"SUCCESS: Generated {pl_csv_path}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Exception occurred while converting metadata to CSV: {e}")
        return False

if __name__ == "__main__":
    json_file = "equipment_metadata.json"
    content_dir = "Content/CollaborativeViewer/Data"
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    if len(sys.argv) > 2:
        content_dir = sys.argv[2]
        
    success = convert_metadata(json_file, content_dir)
    sys.exit(0 if success else 1)
