import os
import sys

def read_log():
    log_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/Saved/Logs/OrionCollab.log"
    if not os.path.exists(log_path):
        print(f"Log path does not exist: {log_path}")
        return
        
    print("Reading Unreal Engine Log file...")
    
    # Try reading as UTF-16 first, then fallback to UTF-8
    content = ""
    try:
        with open(log_path, "r", encoding="utf-16") as f:
            content = f.read()
        print("Successfully read log file as UTF-16.")
    except Exception as e_utf16:
        print(f"UTF-16 read failed: {e_utf16}. Trying UTF-8...")
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            print("Successfully read log file as UTF-8.")
        except Exception as e_utf8:
            print(f"UTF-8 read failed: {e_utf8}")
            return
            
    # Print the last 150 lines
    lines = content.splitlines()
    print(f"Total lines in log: {len(lines)}")
    last_lines = lines[-150:]
    
    # Also search for Compile or Error keywords in the last 1000 lines
    search_lines = lines[-1000:]
    errors = [l for l in search_lines if "error" in l.lower() or "failed" in l.lower() or "compile" in l.lower() or "livecoding" in l.lower()]
    
    print("\n--- LAST 100 LINES OF LOG ---")
    for l in last_lines[-100:]:
        print(l)
        
    print("\n--- MATCHING COMPILE / ERROR / LIVECODING LOG ENTRIES (LAST 1000 LINES) ---")
    for e in errors[-50:]:
        print(e)

if __name__ == "__main__":
    read_log()
