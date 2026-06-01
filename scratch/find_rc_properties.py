import unreal

def inspect_settings():
    out_lines = ["--- INSPECTING REMOTE CONTROL PROPERTIES ---"]
    
    path = "/Script/RemoteControlCommon.RemoteControlSettings"
    try:
        rc_settings_class = unreal.load_class(None, path)
        if rc_settings_class:
            cdo = unreal.get_default_object(rc_settings_class)
            if cdo:
                for attr in dir(cdo):
                    if attr.startswith('_'):
                        continue
                    try:
                        val = getattr(cdo, attr)
                        out_lines.append(f"  {attr} = {val} ({type(val)})")
                    except Exception as e:
                        out_lines.append(f"  {attr} = ERROR: {e}")
            else:
                out_lines.append("Failed to get CDO!")
        else:
            out_lines.append("RemoteControlSettings class not found!")
    except Exception as e:
        out_lines.append(f"Global error: {e}")

    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_properties_output.txt", "w") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    inspect_settings()
