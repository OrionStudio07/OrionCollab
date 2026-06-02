import urllib.request
import json
import sys

def execute():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import run_pie; "
        "import importlib; "
        "importlib.reload(run_pie); "
        "run_pie.run_pie_test()"
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
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            res_str = resp.read().decode('utf-8')
            print(f"SUCCESS: {res_str}")
            res_obj = json.loads(res_str)
            if res_obj.get("ReturnValue") == True:
                print("Play-in-Editor test run executed successfully!")
            else:
                print("Play-in-Editor test run failed!")
                sys.exit(1)
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    execute()
