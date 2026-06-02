import urllib.request
import json
import time

def run():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import test_tree_data; "
        "import importlib; "
        "importlib.reload(test_tree_data); "
        "test_tree_data.test()"
    )
    payload = {
        "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        "functionName": "ExecutePythonCommand",
        "parameters": {
            "PythonCommand": command
        }
    }
    
    url = "http://127.0.0.1:30010/remote/object/call"
    
    print("Waiting for Unreal Editor Remote Control Web Server to start...")
    for i in range(30):
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                print(f"SUCCESS: Editor is up! Response: {resp.read().decode('utf-8')}")
                return True
        except Exception as e:
            time.sleep(1.0)
            
    print("ERROR: Unreal Editor did not start or respond in time.")
    return False

if __name__ == "__main__":
    run()
