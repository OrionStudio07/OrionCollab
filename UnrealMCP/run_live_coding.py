import urllib.request
import json

def run():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import trigger_live_coding; "
        "import importlib; "
        "importlib.reload(trigger_live_coding); "
        "trigger_live_coding.run()"
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
        print("Live coding compilation triggered successfully inside editor!")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run()
