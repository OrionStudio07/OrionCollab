import urllib.request
import json
import sys

def start_mcp_server(port=8000):
    print(f"INFO: Sending request to start Unreal MCP Server on port {port}...")
    
    # Payload for ExecuteConsoleCommand
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": "/Temp/Untitled_0.Untitled:OrionHierarchyManager_0",
            "Command": f"ModelContextProtocol.StartServer {port}"
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
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            response_content = resp.read().decode("utf-8")
            print(f"SUCCESS: Remote execution completed. Response: {response_content}")
            return True
    except Exception as e:
        print(f"ERROR: Failed to trigger console command: {e}")
        return False

if __name__ == "__main__":
    port_to_start = 8000
    if len(sys.argv) > 1:
        try:
            port_to_start = int(sys.argv[1])
        except ValueError:
            pass
            
    success = start_mcp_server(port_to_start)
    sys.exit(0 if success else 1)
