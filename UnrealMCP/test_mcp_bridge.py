import subprocess
import json
import sys

def run_bridge_test():
    print("--- STARTING MCP BRIDGE STDIO VERIFICATION ---")
    bridge_script = r"c:\Users\SHO\Documents\Unreal Projects\OrionCollab\UnrealMCP\unreal_mcp_bridge.py"
    
    # Launch subprocess with pipe redirection
    proc = subprocess.Popen(
        [sys.executable, bridge_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 1. Send initialize notification
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }
    
    print("Sending 'initialize' JSON-RPC message...")
    proc.stdin.write(json.dumps(init_request) + "\n")
    proc.stdin.flush()
    
    init_response = proc.stdout.readline()
    print("Received Initialize Response:")
    print(init_response.strip())
    
    # 2. Send tools/list request
    list_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    print("\nSending 'tools/list' JSON-RPC message...")
    proc.stdin.write(json.dumps(list_request) + "\n")
    proc.stdin.flush()
    
    list_response = proc.stdout.readline()
    print("Received Tools List Response:")
    list_data = json.loads(list_response.strip())
    print(json.dumps(list_data, indent=2))
    
    # 3. Call unreal_exec_command tool to execute a console command
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "unreal_exec_command",
            "arguments": {
                "command": "stat fps"
            }
        }
    }
    
    print("\nSending 'tools/call' for 'unreal_exec_command' (stat fps)...")
    proc.stdin.write(json.dumps(call_request) + "\n")
    proc.stdin.flush()
    
    call_response = proc.stdout.readline()
    print("Received Tools Call Response:")
    print(call_response.strip())
    
    # Terminate process cleanly
    proc.stdin.close()
    proc.terminate()
    proc.wait()
    
    stderr_content = proc.stderr.read()
    if stderr_content:
        print("\nStderr Logs from Bridge:")
        print(stderr_content)
        
    print("\n--- MCP BRIDGE STDIO VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    run_bridge_test()
