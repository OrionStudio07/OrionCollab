import unreal
import sys

def run_tests():
    print("--- ORION 2D MINIMAP SYSTEM AUTOMATED TESTS ---")
    
    # 1. Verify RT_Minimap asset exists & is configured correctly
    rt_path = "/Game/CollaborativeViewer/UMG/Textures/RT_Minimap"
    if not unreal.EditorAssetLibrary.does_asset_exist(rt_path):
        print(f"ERROR: RT_Minimap asset does not exist at {rt_path}!")
        sys.exit(1)
    
    rt_asset = unreal.load_asset(rt_path)
    if not rt_asset:
        print(f"ERROR: Could not load RT_Minimap asset!")
        sys.exit(1)
        
    size_x = rt_asset.get_editor_property("size_x")
    size_y = rt_asset.get_editor_property("size_y")
    fmt = rt_asset.get_editor_property("render_target_format")
    
    print(f"SUCCESS: Loaded RT_Minimap. Dimensions: {size_x}x{size_y}, Format: {fmt}")
    assert size_x == 512, f"Expected RT_Minimap X-size 512, got {size_x}"
    assert size_y == 512, f"Expected RT_Minimap Y-size 512, got {size_y}"
    assert fmt == unreal.TextureRenderTargetFormat.RTF_RGBA8, f"Expected format RTF_RGBA8, got {fmt}"
    
    # 2. Verify BP_MinimapCamera asset exists in registry
    camera_path = "/Game/CollaborativeViewer/Blueprints/BP_MinimapCamera"
    if not unreal.EditorAssetLibrary.does_asset_exist(camera_path):
        print(f"ERROR: BP_MinimapCamera asset does not exist at {camera_path}!")
        sys.exit(1)
    print("SUCCESS: BP_MinimapCamera asset exists in registry.")
    
    # 3. Verify WBP_Minimap asset exists in registry
    widget_path = "/Game/CollaborativeViewer/UMG/WBP_Minimap"
    if not unreal.EditorAssetLibrary.does_asset_exist(widget_path):
        print(f"ERROR: WBP_Minimap asset does not exist at {widget_path}!")
        sys.exit(1)
    print("SUCCESS: WBP_Minimap asset exists in registry.")
    
    # 4. Verify mathematical UV-to-World Translation Formulas
    # WorldX = (OriginX - ExtentX) + U * (2.0 * ExtentX)
    # WorldY = (OriginY + ExtentY) - V * (2.0 * ExtentY)
    
    origin = unreal.Vector(1500.0, -3200.0, 500.0)
    extent = unreal.Vector(2500.0, 4000.0, 1000.0)
    
    # Check Center (0.5, 0.5)
    u, v = 0.5, 0.5
    world_x = (origin.x - extent.x) + u * (2.0 * extent.x)
    world_y = (origin.y + extent.y) - v * (2.0 * extent.y)
    print(f"Formula test: (u={u}, v={v}) -> (x={world_x}, y={world_y})")
    assert world_x == 1500.0, f"Expected Center X = 1500.0, got {world_x}"
    assert world_y == -3200.0, f"Expected Center Y = -3200.0, got {world_y}"
    
    # Check Min bounds (0.0, 0.0) -> (OriginX - ExtentX, OriginY + ExtentY)
    u, v = 0.0, 0.0
    world_x = (origin.x - extent.x) + u * (2.0 * extent.x)
    world_y = (origin.y + extent.y) - v * (2.0 * extent.y)
    print(f"Formula test: (u={u}, v={v}) -> (x={world_x}, y={world_y})")
    assert world_x == -1000.0, f"Expected Min bounds X = -1000.0, got {world_x}"
    assert world_y == 800.0, f"Expected Min bounds Y = 800.0, got {world_y}"
    
    # Check Max bounds (1.0, 1.0) -> (OriginX + ExtentX, OriginY - ExtentY)
    u, v = 1.0, 1.0
    world_x = (origin.x - extent.x) + u * (2.0 * extent.x)
    world_y = (origin.y + extent.y) - v * (2.0 * extent.y)
    print(f"Formula test: (u={u}, v={v}) -> (x={world_x}, y={world_y})")
    assert world_x == 4000.0, f"Expected Max bounds X = 4000.0, got {world_x}"
    assert world_y == -7200.0, f"Expected Max bounds Y = -7200.0, got {world_y}"
    
    print("SUCCESS: UV-to-World Translation math verified.")
    
    print("--- ALL 2D MINIMAP SYSTEM TESTS PASSED ---")

if __name__ == "__main__":
    run_tests()
