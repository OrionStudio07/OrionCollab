import unreal

def inspect():
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt"
    with open(results_path, "w") as f:
        all_names = dir(unreal)
        
        f.write("Matching 'Widget' names in unreal:\n")
        widget_names = [n for n in all_names if "Widget" in n]
        for name in widget_names:
            f.write(f"  - {name}\n")
            
        f.write("\nMatching 'Library' names in unreal:\n")
        lib_names = [n for n in all_names if "Library" in n]
        for name in lib_names:
            f.write(f"  - {name}\n")

if __name__ == "__main__":
    inspect()
