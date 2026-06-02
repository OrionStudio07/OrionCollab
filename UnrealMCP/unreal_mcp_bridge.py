import sys
import json
import urllib.request
import urllib.error

# Configuration
PORT_PRIMARY = 30010
PORT_FALLBACK = 30014
HOST = "127.0.0.1"

def log(msg):
    # Print to stderr since stdout is reserved for JSON-RPC messages
    sys.stderr.write(f"[Unreal-MCP] {msg}\n")
    sys.stderr.flush()

def call_unreal_api(endpoint, method="PUT", data=None):
    jsondata = json.dumps(data).encode("utf-8") if data else None
    
    # Try primary port
    url = f"http://{HOST}:{PORT_PRIMARY}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=jsondata, timeout=2.0) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e_primary:
        log(f"Primary port {PORT_PRIMARY} failed: {e_primary}. Trying fallback port {PORT_FALLBACK}...")
        
        # Try fallback port
        url = f"http://{HOST}:{PORT_FALLBACK}{endpoint}"
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, data=jsondata, timeout=2.0) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e_fallback:
            raise Exception(
                f"Failed to connect to Unreal Engine Remote Control API on both port {PORT_PRIMARY} and {PORT_FALLBACK}.\n"
                f"Ensure Unreal Engine is running, and the 'Remote Control Web Server' plugin is enabled.\n"
                f"Primary Error: {e_primary}\n"
                f"Fallback Error: {e_fallback}"
            )

# Tool Handlers
def handle_exec_command(arguments):
    command = arguments.get("command")
    if not command:
        raise ValueError("Missing 'command' argument")
    
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": "/Temp/Untitled_0.Untitled:OrionHierarchyManager_0",
            "Command": command
        }
    }
    result = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    return {
        "content": [
            {
                "type": "text",
                "text": f"Executed command: '{command}'\nResult: {json.dumps(result)}"
            }
        ]
    }

def handle_exec_python(arguments):
    script = arguments.get("script")
    if not script:
        raise ValueError("Missing 'script' argument")
    
    # Remote control console exec python via command
    command = f"py \"{script}\""
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": "/Temp/Untitled_0.Untitled:OrionHierarchyManager_0",
            "Command": command
        }
    }
    result = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    return {
        "content": [
            {
                "type": "text",
                "text": f"Executed Python script.\nResult: {json.dumps(result)}"
            }
        ]
    }

def handle_get_selected_actors(arguments):
    # Call EditorActorSubsystem CDO to get selected level actors
    payload = {
        "objectPath": "/Script/UnrealEd.Default__EditorActorSubsystem",
        "functionName": "GetSelectedLevelActors",
        "parameters": {}
    }
    result = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    
    # Format the result
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, indent=2)
            }
        ]
    }

def handle_select_actor(arguments):
    actor_label = arguments.get("actor_label")
    if not actor_label:
        raise ValueError("Missing 'actor_label' argument")
    
    # We can select actors using a Python command
    python_script = (
        f"import unreal; "
        f"subsystem = unreal.EditorActorSubsystem(); "
        f"actors = subsystem.get_all_level_actors(); "
        f"to_select = [a for a in actors if a.get_actor_label() == '{actor_label}']; "
        f"subsystem.set_actor_selection_state(to_select[0], True) if to_select else None"
    )
    
    command = f"py \"{python_script}\""
    payload = {
        "objectPath": "/Script/Engine.Default__KismetSystemLibrary",
        "functionName": "ExecuteConsoleCommand",
        "parameters": {
            "WorldContextObject": "/Temp/Untitled_0.Untitled:OrionHierarchyManager_0",
            "Command": command
        }
    }
    result = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    
    return {
        "content": [
            {
                "type": "text",
                "text": f"Selection request for '{actor_label}' completed.\nResult: {json.dumps(result)}"
            }
        ]
    }

def handle_call_function(arguments):
    object_path = arguments.get("object_path")
    function_name = arguments.get("function_name")
    parameters = arguments.get("parameters", {})
    
    if not object_path or not function_name:
        raise ValueError("Missing 'object_path' or 'function_name' argument")
        
    payload = {
        "objectPath": object_path,
        "functionName": function_name,
        "parameters": parameters
    }
    result = call_unreal_api("/remote/object/call", method="PUT", data=payload)
    
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result, indent=2)
            }
        ]
    }

# Tool list definition
TOOLS = [
    {
        "name": "unreal_exec_command",
        "description": "Execute an editor console command inside the Unreal Engine Editor (e.g. 'stat fps', 'log')",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The console command to execute"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "unreal_exec_python",
        "description": "Run a snippet of python code inside Unreal Editor (e.g. print actors, modify assets)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script": {"type": "string", "description": "Python code snippet to execute"}
            },
            "required": ["script"]
        }
    },
    {
        "name": "unreal_get_selected_actors",
        "description": "Get the list of currently selected actors in the level editor",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "unreal_select_actor",
        "description": "Select a specific actor by its Label in the level viewport",
        "inputSchema": {
            "type": "object",
            "properties": {
                "actor_label": {"type": "string", "description": "The Actor Label (Name) in the Outliner"}
            },
            "required": ["actor_label"]
        }
    },
    {
        "name": "unreal_call_function",
        "description": "Call a specific Blueprint or C++ function on a specified object path",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_path": {"type": "string", "description": "Unreal object path (e.g. '/Script/UnrealEd.Default__EditorActorSubsystem')"},
                "function_name": {"type": "string", "description": "The function name to invoke"},
                "parameters": {"type": "object", "description": "Key-value parameters for the function"}
            },
            "required": ["object_path", "function_name"]
        }
    }
]

# Stdio JSON-RPC Loop
def main():
    log("Started Unreal Engine MCP Server.")
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            line = line.strip().lstrip('\ufeff')
            if not line:
                continue
                
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                log("Received malformed JSON-RPC message.")
                continue
                
            req_id = request.get("id")
            method = request.get("method")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "unreal-editor-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            elif method == "notifications/initialized":
                # No response required for notification
                pass
                
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS
                    }
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            elif method == "tools/call":
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                try:
                    if tool_name == "unreal_exec_command":
                        result = handle_exec_command(arguments)
                    elif tool_name == "unreal_exec_python":
                        result = handle_exec_python(arguments)
                    elif tool_name == "unreal_get_selected_actors":
                        result = handle_get_selected_actors(arguments)
                    elif tool_name == "unreal_select_actor":
                        result = handle_select_actor(arguments)
                    elif tool_name == "unreal_call_function":
                        result = handle_call_function(arguments)
                    else:
                        raise ValueError(f"Unknown tool: {tool_name}")
                        
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": result
                    }
                except Exception as ex:
                    log(f"Error executing tool '{tool_name}': {ex}")
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32000,
                            "message": str(ex)
                        }
                    }
                    
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            elif method:
                # Unknown method
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
        except Exception as e:
            log(f"Global loop error: {e}")

if __name__ == "__main__":
    main()
