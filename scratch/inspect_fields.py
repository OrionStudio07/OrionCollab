import unreal

def inspect_fields():
    out_lines = ["--- INSPECTING REMOTE CONTROL FIELDS ---"]
    
    path = "/Script/RemoteControlCommon.RemoteControlSettings"
    try:
        rc_settings_class = unreal.load_class(None, path)
        if rc_settings_class:
            out_lines.append(f"Class: {path}")
            fields = rc_settings_class.list_fields()
            out_lines.append(f"Fields count: {len(fields)}")
            
            cdo = unreal.get_default_object(rc_settings_class)
            if cdo:
                for field in fields:
                    try:
                        val = cdo.get_editor_property(field)
                        out_lines.append(f"  {field} = {val} ({type(val)})")
                    except Exception as e:
                        out_lines.append(f"  {field} = ERROR: {e}")
            else:
                out_lines.append("Failed to get CDO!")
        else:
            out_lines.append("RemoteControlSettings class not found!")
    except Exception as e:
        out_lines.append(f"Global error: {e}")

    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/rc_fields_output.txt", "w") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    inspect_fields()
