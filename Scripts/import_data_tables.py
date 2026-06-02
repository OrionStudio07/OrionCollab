import unreal
import os

def import_tables():
    project_dir = "C:/Users/SHO/Documents/Unreal Projects/OrionCollab"
    destination_path = "/Game/CollaborativeViewer/Data"
    csv_dir = f"{project_dir}/Content/CollaborativeViewer/Data"
    
    # Define tables mapping: (Asset Name, Struct Name, CSV File Name)
    tables = [
        ("DT_Equipment", "EquipmentTableRow", "DT_Equipment.csv"),
        ("DT_Buildings", "BuildingTableRow", "DT_Buildings.csv"),
        ("DT_Rooms", "RoomTableRow", "DT_Rooms.csv"),
        ("DT_ProcessLines", "ProcessLineTableRow", "DT_ProcessLines.csv"),
        ("DT_Zones", "ZoneTableRow", "DT_Zones.csv"),
        ("DT_TourWaypoints", "TourWaypointTableRow", "DT_TourWaypoints.csv"),
        ("DT_NPCs", "NPCTableRow", "DT_NPCs.csv"),
        ("DT_InspectionSteps", "InspectionStepTableRow", "DT_InspectionSteps.csv")
    ]
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    for asset_name, struct_name, csv_file in tables:
        asset_path = f"{destination_path}/{asset_name}"
        csv_path = os.path.join(csv_dir, csv_file)
        
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV file not found at {csv_path}")
            continue
            
        # Load C++ Struct
        struct_path = f"/Script/OrionCollab.{struct_name}"
        row_struct = unreal.load_object(None, struct_path)
        if not row_struct:
            print(f"ERROR: Could not load row struct '{struct_path}'. Ensure the C++ project is compiled!")
            continue
            
        # Check if asset exists, if not create it
        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            dt_asset = unreal.load_asset(asset_path)
            print(f"INFO: Data Table {asset_name} already exists. Re-importing CSV data.")
        else:
            factory = unreal.DataTableFactory()
            factory.set_editor_property("struct", row_struct)
            
            dt_asset = asset_tools.create_asset(
                asset_name=asset_name,
                package_path=destination_path,
                asset_class=unreal.DataTable,
                factory=factory
            )
            
        if dt_asset:
            # Fill from CSV
            success = unreal.DataTableFunctionLibrary.fill_data_table_from_csv_file(dt_asset, csv_path)
            if success:
                unreal.EditorAssetLibrary.save_loaded_asset(dt_asset)
                print(f"SUCCESS: Imported {csv_file} into {asset_name} using struct {struct_name}.")
            else:
                print(f"FAILED: Could not fill Data Table {asset_name} from CSV {csv_file}.")
        else:
            print(f"FAILED: Could not create/load Data Table asset for {asset_name}.")

if __name__ == "__main__":
    import_tables()
