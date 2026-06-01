import unreal

def enable_settings():
    out_lines = ["--- ENABLING REMOTE CONTROL SETTINGS ---"]
    
    path = "/Script/RemoteControlCommon.RemoteControlSettings"
    try:
        rc_settings_class = unreal.load_class(None, path)
        if rc_settings_class:
            cdo = unreal.get_default_object(rc_settings_class)
            if cdo:
                # Enable Console Command Remote Execution
                try:
                    cdo.set_editor_property("bAllowConsoleCommandRemoteExecution", True)
                    out_lines.append("bAllowConsoleCommandRemoteExecution set to True")
                except Exception as e:
                    out_lines.append(f"Failed to set bAllowConsoleCommandRemoteExecution: {e}")
                
                # Enable Remote Python Execution
                try:
                    cdo.set_editor_property("bEnableRemotePythonExecution", True)
                    out_lines.append("bEnableRemotePythonExecution set to True")
                except Exception as e:
                    out_lines.append(f"Failed to set bEnableRemotePythonExecution: {e}")
                
                # Try saving settings to config
                try:
                    cdo.save_config()
                    out_lines.append("Settings saved via save_config()")
                except Exception as e:
                    out_lines.append(f"Failed to save_config(): {e}")
            else:
                out_lines.append("Failed to get CDO!")
        else:
            out_lines.append("RemoteControlSettings class not found!")
    except Exception as e:
        out_lines.append(f"Global error: {e}")

    with open("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/enable_rc_output.txt", "w") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    enable_settings()
