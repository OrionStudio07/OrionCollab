# Blueprint Logic Specification: BP_ConfigLoader
**Parent Class:** `Object`  
**Location:** `/Game/CollaborativeViewer/Blueprints/GameInstance/BP_ConfigLoader`

This document details the variables, structs, function graphs, and event logic for `BP_ConfigLoader` to load, parse, and validate `OrionConfig.json` at startup.

---

## 1. Struct Definitions (Blueprint Structs)

Create the following Blueprint Structs under `/Game/CollaborativeViewer/Blueprints/GameInstance/Structs/`:

### `FOrionClientConfig`
* `CompanyName` (String): Default = `"Orion Studios"`
* `PlantName` (String): Default = `"Demo Plant"`
* `LogoPath` (String): Default = `""`
* `AccentColor` (LinearColor): Default = `(0.0, 0.831, 0.667, 1.0)` (Hex `#00D4AA`)

### `FOrionModeConfig`
* `bShowcase` (Boolean): Default = `true`
* `bTraining` (Boolean): Default = `false`
* `bOperations` (Boolean): Default = `true`

### `FOrionFeatureConfig`
* `bMinimap` (Boolean): Default = `true`
* `bGuidedTour` (Boolean): Default = `true`
* `bNPCWorkers` (Boolean): Default = `true`
* `bSessionRecording` (Boolean): Default = `false`
* `bSimulationData` (Boolean): Default = `false`

### `FOrionOptimizationConfig`
* `bLumenEnabled` (Boolean): Default = `true`
* `VRMode` (String): Default = `"pc_tethered"`
* `TargetFPSDesktop` (Integer): Default = `60`
* `TargetFPSVR` (Integer): Default = `72`

### `FOrionSaveConfig`
* `SaveFilePrefix` (String): Default = `"Orion"`
* `AutoSaveIntervalSeconds` (Integer): Default = `300`

### `FOrionConfig`
* `Client` (`FOrionClientConfig`)
* `Modes` (`FOrionModeConfig`)
* `Features` (`FOrionFeatureConfig`)
* `Optimization` (`FOrionOptimizationConfig`)
* `SaveGame` (`FOrionSaveConfig`)

---

## 2. Variables & Delegates

### Variables
* `Config` (`FOrionConfig`): Access type: Private, Read-Only externally. Holds the active validated configuration.

### Delegates
* `OnConfigReloaded`: Multicast Delegate with no parameters. Fired when `OrionConfig.json` is reloaded in developer builds.

---

## 3. Function Implementations

### `Initialize` (Triggered from `BP_OrionGameInstance::Init`)
1. Create/Construct `BP_ConfigLoader` Object.
2. Store reference on `BP_OrionGameInstance`.
3. Call `LoadConfig()`.
4. In **Developer/Debug builds**, spawn the file watcher to enable hot-reload.

### `LoadConfig()`
Loads the JSON configuration file from `FPaths::ProjectDir() / "OrionConfig.json"`.

#### Event/Node Flow:
1. **Get File Path**: Combine `Get Project Directory` with string `"OrionConfig.json"`.
2. **Check File Existence**: Call `Does File Exist` (from Blueprint File Utilities / Engine File Library).
   * **If FALSE**: Call `LoadEmbeddedDefaults()`, log warning: `"OrionConfig.json not found, using embedded defaults."`, and exit.
3. **Load JSON Object**: Call `Load JSON from File` node from the *JSON Blueprint Utilities* plugin.
   * **If FALSE/Failed to Parse**: Call `LoadEmbeddedDefaults()`, log warning: `"OrionConfig.json is malformed, using embedded defaults."`, and exit.
4. **Parse Sections**:
   * Call `Get Object Field` on the root JSON object for fields: `"client"`, `"modes"`, `"features"`, `"optimization"`, `"save_game"`.
   * For each object, extract individual fields using `Get String Field`, `Get Bool Field`, and `Get Integer Field` nodes.
5. **Validate and Assign**:
   * Pass each extracted struct value into `ValidateConfigFields()`.
   * Set the `Config` variable with the resulting validated struct.
6. **Apply Branding**: Notify root widget to update UI themes.

### `ValidateConfigFields(FOrionConfig InputConfig, FOrionConfig& OutputConfig)`
Validates and clamps fields to prevent errors.

* **Client Branding Validation**:
  * Check if `InputConfig.Client.CompanyName` is empty. If yes, replace with `"Orion Studios"`.
  * Check if `InputConfig.Client.PlantName` is empty. If yes, replace with `"Demo Plant"`.
  * **Accent Color Regex Match**: Validate `InputConfig.Client.AccentColor` hex format using a utility function (verify it starts with `#` and is followed by 6 hex characters). If invalid, fallback to `(0.0, 0.831, 0.667, 1.0)`.
* **Optimization Clamping**:
  * Clamp `InputConfig.Optimization.TargetFPSDesktop` between `30` and `144`.
  * Clamp `InputConfig.Optimization.TargetFPSVR` between `30` and `144`.
  * Validate `InputConfig.Optimization.VRMode` (must be `"pc_tethered"` or `"disabled"`). Default to `"pc_tethered"`.
* **SaveGame Validation**:
  * Clamp `InputConfig.SaveGame.AutoSaveIntervalSeconds` between `60` and `3600`.
  * Check if `InputConfig.SaveGame.SaveFilePrefix` is empty. If yes, set to `"Orion"`.

---

## 4. Developer Hot-Reload (Dev Only)

In `WITH_EDITOR` contexts, `BP_ConfigLoader` registers a directory/file watch hook:
1. When `OrionConfig.json` modification is captured:
   - Call `LoadConfig()`.
   - Broadcast `OnConfigReloaded` delegate.
2. Subscribed widgets and managers catch the event to refresh dynamic assets (e.g. logo textures, color branding tints, and widget enable states) instantly without restarting the Editor session.
