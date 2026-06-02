import urllib.request
import json
import sys
import os

def run():
    command = (
        "import sys; "
        "sys.path.append('c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch'); "
        "import test_widget_instantiation; "
        "import importlib; "
        "importlib.reload(test_widget_instantiation); "
        "test_widget_instantiation.test_instantiation()"
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
    
    # Run in editor
    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            res_str = resp.read().decode('utf-8')
    except Exception as e:
        print(f"FAILED to send Remote Control request: {e}")
        sys.exit(1)
        
    # Read diagnostic log file
    diag_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/widget_test_results.txt"
    if os.path.exists(diag_path):
        with open(diag_path, "r") as f:
            log_content = f.read()
        print(log_content)
        
        if "ALL WBP_ORIONROOT INSTANTIATION TESTS PASSED" in log_content:
            print("Widget verification completed successfully!")
            sys.exit(0)
        else:
            print("Widget verification failed! See logs above.")
            sys.exit(1)
    else:
        print("ERROR: Diagnostics file was not generated!")
        sys.exit(1)

if __name__ == "__main__":
    run()
