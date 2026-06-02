import urllib.request
import json

def test():
    # Call ExecuteConsoleCommand on UKismetSystemLibrary CDO
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": "/Temp/Untitled_0.Untitled:OrionHierarchyManager_0", # a valid world context object path from scratch/paths_output.txt
            "Command": "LiveCoding.Compile"
        }
    }
    
    url = "http://127.0.0.1:30010/remote/object/call"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            print(f"SUCCESS: {resp.read().decode('utf-8')}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test()
