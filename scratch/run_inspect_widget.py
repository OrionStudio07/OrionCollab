import urllib.request
import json

def run():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import stop_pie; "
        "import importlib; "
        "importlib.reload(stop_pie); "
        "stop_pie.stop()"
    )
    payload = {
        "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
        "functionName": "ExecutePythonCommand",
        "parameters": {
            "PythonCommand": command
        }
    }
    url = "http://127.0.0.1:30010/remote/object/call"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    try:
        urllib.request.urlopen(req, timeout=5.0)
        print("PIE stopped successfully!")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run()
