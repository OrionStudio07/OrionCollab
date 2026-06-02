import unreal

def list_assets():
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = registry.get_assets_by_path("/Game/CollaborativeViewer/UMG", recursive=True)
    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/assets.txt", "w") as f:
        for a in assets:
            f.write(f"{a.asset_name} ({a.package_name})\n")
    print("SUCCESS: Listed all UMG assets.")

if __name__ == "__main__":
    list_assets()
