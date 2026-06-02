import unreal

def stop():
    print("Force stopping PIE...")
    unreal.EditorLevelLibrary.editor_end_play()
    print("PIE stopped successfully.")

if __name__ == "__main__":
    stop()
