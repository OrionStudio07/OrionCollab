# Configuration Reference

## OrionConfig.json

Each client deployment is configured via a single `OrionConfig.json` file located at `Scripts/config/OrionConfig.json`. The application loads this file at startup and falls back to embedded defaults if it's missing or malformed.

---

## Full Schema

```json
{
  "$schema": "OrionConfig/v1",
  "client": {
    "company_name": "Morde Foods",
    "plant_name": "P2 Manufacturing Plant",
    "logo_path": "Content/CollaborativeViewer/UMG/Textures/Logo.png",
    "accent_color": "#00D4AA"
  },
  "modes": {
    "showcase": true,
    "training": false,
    "operations": true
  },
  "features": {
    "minimap": true,
    "guided_tour": true,
    "npc_workers": true,
    "session_recording": false,
    "simulation_data": false
  },
  "optimization": {
    "lumen_enabled": true,
    "vr_mode": "pc_tethered",
    "target_fps_desktop": 60,
    "target_fps_vr": 72
  },
  "save_game": {
    "save_file_prefix": "Orion",
    "auto_save_interval_seconds": 300
  }
}
```

---

## Field Reference

### `client` — Branding

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `company_name` | string | `"Orion Studios"` | Displayed in the top bar and launcher |
| `plant_name` | string | `"Demo Plant"` | Plant identifier shown alongside company name |
| `logo_path` | string | `""` | Path to client logo texture (relative to project) |
| `accent_color` | string | `"#00D4AA"` | Hex color used for UI highlights and borders |

### `modes` — Feature Gating

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `showcase` | bool | `true` | Enable Mode A — Showcase (investor tours) |
| `training` | bool | `false` | Enable Mode B — Training (v2, reserved) |
| `operations` | bool | `true` | Enable Mode C — Operations (engineering) |

### `features` — Optional Capabilities

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `minimap` | bool | `true` | 2D overhead minimap with floor selector |
| `guided_tour` | bool | `true` | Scripted camera tour with waypoints |
| `npc_workers` | bool | `true` | Animated NPC workers in zones |
| `session_recording` | bool | `false` | Camera path + interaction recording |
| `simulation_data` | bool | `false` | Live simulation data overlay (v2) |

### `optimization` — Performance

| Field | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `lumen_enabled` | bool | `true` | — | Lumen GI (disable for VR performance) |
| `vr_mode` | string | `"pc_tethered"` | `pc_tethered`, `disabled` | VR platform target |
| `target_fps_desktop` | int | `60` | 30–144 | Desktop framerate target |
| `target_fps_vr` | int | `72` | 30–144 | VR framerate target |

### `save_game` — Persistence

| Field | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `save_file_prefix` | string | `"Orion"` | — | Prefix for save file names |
| `auto_save_interval_seconds` | int | `300` | 60–3600 | Auto-save frequency |

---

## Swapping Clients

To configure for a new client:
1. Update `client` fields (company name, plant name, logo, accent color)
2. Toggle `modes` to enable/disable available modes
3. Toggle `features` based on client requirements
4. Adjust `optimization` for target hardware
5. In development builds, changes are hot-reloaded automatically
