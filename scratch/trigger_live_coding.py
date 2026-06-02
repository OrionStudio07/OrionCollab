import unreal

def run():
    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        print("ERROR: Could not get editor world!")
        return
        
    print("Triggering LiveCoding.Compile console command...")
    unreal.SystemLibrary.execute_console_command(world, "LiveCoding.Compile")
    print("Console command sent successfully.")

if __name__ == "__main__":
    run()
