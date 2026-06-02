import sys
import os
import traceback

def run():
    sys.path.append("c:/Users/SHO/Documents/Unreal Projects/OrionCollab")
    sys.path.append("c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch")
    
    results_path = "c:/Users/SHO/Documents/Unreal Projects/OrionCollab/scratch/test_results.txt"
    
    # Redirect stdout to capture all test print outputs
    class Logger:
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open(results_path, "w")
        def write(self, message):
            if self.terminal is not None:
                try:
                    self.terminal.write(message)
                except Exception:
                    pass
            self.log.write(message)
        def flush(self):
            if self.terminal is not None:
                try:
                    self.terminal.flush()
                except Exception:
                    pass
            self.log.flush()
            
    sys.stdout = Logger()
    sys.stderr = sys.stdout
    
    try:
        print("==================================================")
        print("         ORION PLATFORM PHASE GATE TESTS          ")
        print("==================================================")
        
        modules = [
            ("Config Subsystem", "test_config_subsystem"),
            ("Mode Manager", "test_mode_manager"),
            ("Metadata Linker", "test_metadata_linker"),
            ("Hierarchy Manager", "test_hierarchy_manager"),
            ("Search System", "test_search_ui"),
            ("Minimap Logic", "test_minimap_logic")
        ]
        
        for name, mod_name in modules:
            print(f"\n>>> Running {name} Tests...")
            try:
                mod = __import__(mod_name)
                import importlib
                importlib.reload(mod)
                mod.run_tests()
                print(f"CHAR_CHECK: {name} Tests PASSED!")
            except Exception as e:
                print(f"CHAR_CHECK: {name} Tests FAILED!")
                traceback.print_exc()
                
        print("\n==================================================")
        print("              PHASE GATE TESTS COMPLETE           ")
        print("==================================================")
        
    except Exception as e:
        print("GLOBAL RUN FAILURE:")
        traceback.print_exc()
        
    finally:
        # Restore stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

if __name__ == "__main__":
    run()
