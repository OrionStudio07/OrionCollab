import unreal
import os

def test():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/test_results.txt"
    with open(results_path, "w") as f:
        f.write("--- SEARCHING UNREAL NAMESPACE FOR ORION TYPES ---\n")
        all_names = dir(unreal)
        orion_names = [n for n in all_names if "Orion" in n or "Tree" in n]
        f.write(f"Orion/Tree matching names in unreal: {orion_names}\n")
        
        # Explicit check for key classes and enums
        check_types = [
            "OrionTreeCategory",
            "OrionTreeItemData",
            "OrionHierarchyManager",
            "OrionHierarchyTypes"
        ]
        for t in check_types:
            has_type = hasattr(unreal, t)
            f.write(f"unreal has {t}: {has_type}\n")
            if has_type:
                f.write(f"  dir({t}): {dir(getattr(unreal, t))}\n")

if __name__ == "__main__":
    test()
