import subprocess
import json
import sys

def test_bridge():
    print("--- STARTING UNREAL MCP BRIDGE TEST ---")
    
    # Spawn the unreal_mcp_bridge.py script
    cmd = [
        "C:/Users/SHO/AppData/Local/Programs/Python/Python312/python.exe",
        "c:/Users/SHO/Documents/Unreal Projects/MCP/Scripts/unreal_mcp_bridge.py"
    ]
    
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 1. Send initialize notification
    init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    print("Sending initialize request...")
    proc.stdin.write(json.dumps(init_req) + "\n")
    proc.stdin.flush()
    
    # Read response
    init_res_line = proc.stdout.readline()
    print("Received initialize response:")
    try:
        init_res = json.loads(init_res_line)
        print(json.dumps(init_res, indent=2))
    except Exception as e:
        print("Raw Response:", init_res_line)
        print("Error parsing JSON:", e)

    # 2. Send tools/list request
    list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    print("\nSending tools/list request...")
    proc.stdin.write(json.dumps(list_req) + "\n")
    proc.stdin.flush()
    
    # Read response
    list_res_line = proc.stdout.readline()
    print("Received tools/list response:")
    try:
        list_res = json.loads(list_res_line)
        print(json.dumps(list_res, indent=2))
    except Exception as e:
        print("Raw Response:", list_res_line)
        print("Error parsing JSON:", e)

    # Clean up
    proc.terminate()
    proc.wait()
    
    # Print stderr logs
    stderr_content = proc.stderr.read()
    if stderr_content:
        print("\nBridge Stderr Output:")
        print(stderr_content)
        
    print("--- UNREAL MCP BRIDGE TEST COMPLETED ---")

if __name__ == "__main__":
    test_bridge()
