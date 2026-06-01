import json
import urllib.request

HOST = "127.0.0.1"
PORT = 30010

def call_unreal_api(endpoint, method="PUT", data=None):
    jsondata = json.dumps(data).encode("utf-8") if data else None
    url = f"http://{HOST}:{PORT}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=jsondata, timeout=2.0) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error calling {url}: {e}")
        return None

def test_rc():
    # 1. Test running execute command via KismetSystemLibrary
    print("Testing command execution via KismetSystemLibrary.ExecuteConsoleCommand...")
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": None,
            "Command": "py \"import unreal; print('REMOTE CONTROL PYTHON WORKED!')\"",
            "SpecificPlayer": None
        }
    }
    cmd_res = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    print("Command Result:", cmd_res)

if __name__ == "__main__":
    test_rc()
