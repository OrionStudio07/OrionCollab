import unreal

def inspect_settings():
    out_lines = ["--- INSPECTING REMOTE CONTROL SETTINGS ---"]
    
    # Try class paths
    class_paths = [
        "/Script/RemoteControl.RemoteControlSettings",
        "/Script/RemoteControlAPI.RemoteControlSettings",
        "/Script/RemoteControl.URemoteControlSettings",
        "/Script/RemoteControlAPI.URemoteControlSettings",
        "/Script/RemoteControlCommon.RemoteControlSettings"
    ]
    
    rc_settings_class = None
    for path in class_paths:
        try:
            rc_settings_class = unreal.load_class(None, path)
            if rc_settings_class:
                out_lines.append(f"Found class: {path}")
                break
        except Exception as e:
            out_lines.append(f"Error loading {path}: {e}")
            
    if rc_settings_class:
        try:
            cdo = unreal.get_default_object(rc_settings_class)
            if cdo:
                out_lines.append("Properties:")
                # We can inspect the object using dir() or get_editor_property
                for attr in dir(cdo):
                    # We only care about properties we can get/set
                    if attr.startswith('_'):
                        continue
                    try:
                        val = cdo.get_editor_property(attr)
                        out_lines.append(f"  {attr} = {val} ({type(val)})")
                    except Exception:
                        pass
            else:
                out_lines.append("Failed to get CDO!")
        except Exception as e:
            out_lines.append(f"Error getting default object: {e}")
    else:
        out_lines.append("RemoteControlSettings class not found!")

    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_settings_output.txt", "w") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    inspect_settings()
