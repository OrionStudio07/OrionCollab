import urllib.request
import json

def run():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import run_all_tests; "
        "import importlib; "
        "importlib.reload(run_all_tests); "
        "run_all_tests.run()"
    )
    payload = {
        "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        "functionName": "ExecutePythonCommand",
        "parameters": {
            "PythonCommand": command
        }
    }
    
    url = "http://127.0.0.1:30010/remote/object/call"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            print(f"SUCCESS: {resp.read().decode('utf-8')}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run()
