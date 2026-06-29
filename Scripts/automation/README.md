# Automation Scripts

Pipeline and data import scripts for converting AutoCAD Plant 3D data into UE5 Data Tables.

## Scripts

| Script | Purpose |
|--------|---------|
| `automate_all.py` | Master script — runs the full automation pipeline sequentially |
| `export_plant3d_metadata.py` | Extracts equipment metadata from AutoCAD Plant 3D via Python API |
| `convert_metadata_to_csv.py` | Converts exported JSON metadata to CSV format for UE5 Data Table import |
| `import_data_tables.py` | Imports CSV data into UE5 Data Tables via editor scripting API |
| `import_string_table.py` | Imports `ST_Orion_UI.csv` string table for localization-ready text |

## Usage

```bash
# Run the full pipeline
python Scripts/automation/automate_all.py

# Or run individual steps:
python Scripts/automation/export_plant3d_metadata.py
python Scripts/automation/convert_metadata_to_csv.py
python Scripts/automation/import_data_tables.py
```

> **Note**: `export_plant3d_metadata.py` requires AutoCAD Plant 3D to be installed. The import scripts require the Unreal Editor to be running.
