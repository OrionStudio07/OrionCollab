// OrionConfigSubsystem.cpp
#include "OrionConfigSubsystem.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

#if !UE_BUILD_SHIPPING
#include "DirectoryWatcherModule.h"
#include "IDirectoryWatcher.h"
#include "Modules/ModuleManager.h"
#endif

DEFINE_LOG_CATEGORY_STATIC(LogOrionConfig, Log, All);

/** Helper function to convert hex color string (#RRGGBB) to FLinearColor */
static FLinearColor HexToColor(const FString& HexString, const FLinearColor& DefaultColor)
{
    if (HexString.Len() != 7 || !HexString.StartsWith(TEXT("#")))
    {
        return DefaultColor;
    }
    
    for (int32 i = 1; i < 7; ++i)
    {
        TCHAR Char = HexString[i];
        if (!((Char >= '0' && Char <= '9') || (Char >= 'A' && Char <= 'F') || (Char >= 'a' && Char <= 'f')))
        {
            return DefaultColor;
        }
    }
    
    int32 R = FParse::HexDigit(HexString[1]) * 16 + FParse::HexDigit(HexString[2]);
    int32 G = FParse::HexDigit(HexString[3]) * 16 + FParse::HexDigit(HexString[4]);
    int32 B = FParse::HexDigit(HexString[5]) * 16 + FParse::HexDigit(HexString[6]);
    
    return FLinearColor(R / 255.f, G / 255.f, B / 255.f, 1.f);
}

UOrionConfigSubsystem::UOrionConfigSubsystem()
    : bIsConfigValid(false)
{
}

void UOrionConfigSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    // Resolve the absolute path to OrionConfig.json in the project root
    ConfigFilePath = FPaths::Combine(FPaths::ProjectDir(), TEXT("OrionConfig.json"));
    ConfigFilePath = FPaths::ConvertRelativePathToFull(ConfigFilePath);

    UE_LOG(LogOrionConfig, Log, TEXT("Initializing Orion Config Subsystem. Target path: %s"), *ConfigFilePath);

    // Initial load
    LoadConfig();

#if !UE_BUILD_SHIPPING
    SetupDirectoryWatcher();
#endif
}

void UOrionConfigSubsystem::Deinitialize()
{
#if !UE_BUILD_SHIPPING
    CleanupDirectoryWatcher();
#endif

    Super::Deinitialize();
}

bool UOrionConfigSubsystem::LoadConfig()
{
    if (ConfigFilePath.IsEmpty())
    {
        ConfigFilePath = FPaths::Combine(FPaths::ProjectDir(), TEXT("OrionConfig.json"));
        ConfigFilePath = FPaths::ConvertRelativePathToFull(ConfigFilePath);
    }

    FOrionConfig LoadedConfig;
    bIsConfigValid = false;

    if (!FPaths::FileExists(ConfigFilePath))
    {
        UE_LOG(LogOrionConfig, Warning, TEXT("Config file not found at %s! Using default configuration."), *ConfigFilePath);
        ValidateConfig(CurrentConfig); // Ensure defaults are sanitized
        return false;
    }

    FString JsonString;
    if (!FFileHelper::LoadFileToString(JsonString, *ConfigFilePath))
    {
        UE_LOG(LogOrionConfig, Warning, TEXT("Failed to read config file at %s! Using default configuration."), *ConfigFilePath);
        ValidateConfig(CurrentConfig);
        return false;
    }

    if (!ParseConfigFromJson(JsonString, LoadedConfig))
    {
        UE_LOG(LogOrionConfig, Warning, TEXT("Failed to parse malformed JSON in config file at %s! Using default configuration."), *ConfigFilePath);
        ValidateConfig(CurrentConfig);
        return false;
    }

    ValidateConfig(LoadedConfig);
    CurrentConfig = LoadedConfig;
    bIsConfigValid = true;

    UE_LOG(LogOrionConfig, Log, TEXT("Configuration loaded successfully from %s."), *ConfigFilePath);
    UE_LOG(LogOrionConfig, Log, TEXT("Client Company: %s, Plant Name: %s"), *CurrentConfig.Client.CompanyName, *CurrentConfig.Client.PlantName);
    
    return true;
}

bool UOrionConfigSubsystem::ParseConfigFromJson(const FString& JsonString, FOrionConfig& OutConfig)
{
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

    if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
    {
        return false;
    }

    // 1. Client Category
    if (JsonObject->HasField(TEXT("client")))
    {
        TSharedPtr<FJsonObject> ClientObj = JsonObject->GetObjectField(TEXT("client"));
        if (ClientObj.IsValid())
        {
            ClientObj->TryGetStringField(TEXT("company_name"), OutConfig.Client.CompanyName);
            ClientObj->TryGetStringField(TEXT("plant_name"), OutConfig.Client.PlantName);
            ClientObj->TryGetStringField(TEXT("logo_path"), OutConfig.Client.LogoPath);
            
            FString HexColorStr;
            if (ClientObj->TryGetStringField(TEXT("accent_color"), HexColorStr))
            {
                OutConfig.Client.AccentColor = HexToColor(HexColorStr, OutConfig.Client.AccentColor);
            }
        }
    }

    // 2. Modes Category
    if (JsonObject->HasField(TEXT("modes")))
    {
        TSharedPtr<FJsonObject> ModesObj = JsonObject->GetObjectField(TEXT("modes"));
        if (ModesObj.IsValid())
        {
            ModesObj->TryGetBoolField(TEXT("showcase"), OutConfig.Modes.bShowcase);
            ModesObj->TryGetBoolField(TEXT("training"), OutConfig.Modes.bTraining);
            ModesObj->TryGetBoolField(TEXT("operations"), OutConfig.Modes.bOperations);
        }
    }

    // 3. Features Category
    if (JsonObject->HasField(TEXT("features")))
    {
        TSharedPtr<FJsonObject> FeaturesObj = JsonObject->GetObjectField(TEXT("features"));
        if (FeaturesObj.IsValid())
        {
            FeaturesObj->TryGetBoolField(TEXT("minimap"), OutConfig.Features.bMinimap);
            FeaturesObj->TryGetBoolField(TEXT("guided_tour"), OutConfig.Features.bGuidedTour);
            FeaturesObj->TryGetBoolField(TEXT("npc_workers"), OutConfig.Features.bNPCWorkers);
            FeaturesObj->TryGetBoolField(TEXT("session_recording"), OutConfig.Features.bSessionRecording);
            FeaturesObj->TryGetBoolField(TEXT("simulation_data"), OutConfig.Features.bSimulationData);
        }
    }

    // 4. Optimization Category
    if (JsonObject->HasField(TEXT("optimization")))
    {
        TSharedPtr<FJsonObject> OptObj = JsonObject->GetObjectField(TEXT("optimization"));
        if (OptObj.IsValid())
        {
            OptObj->TryGetBoolField(TEXT("lumen_enabled"), OutConfig.Optimization.bLumenEnabled);
            OptObj->TryGetStringField(TEXT("vr_mode"), OutConfig.Optimization.VRMode);
            
            double TempDouble = 0.0;
            if (OptObj->TryGetNumberField(TEXT("target_fps_desktop"), TempDouble))
            {
                OutConfig.Optimization.TargetFPSDesktop = (int32)TempDouble;
            }
            if (OptObj->TryGetNumberField(TEXT("target_fps_vr"), TempDouble))
            {
                OutConfig.Optimization.TargetFPSVR = (int32)TempDouble;
            }
        }
    }

    // 5. SaveGame Category
    if (JsonObject->HasField(TEXT("save_game")))
    {
        TSharedPtr<FJsonObject> SaveObj = JsonObject->GetObjectField(TEXT("save_game"));
        if (SaveObj.IsValid())
        {
            SaveObj->TryGetStringField(TEXT("save_file_prefix"), OutConfig.SaveGame.SaveFilePrefix);
            
            double TempDouble = 0.0;
            if (SaveObj->TryGetNumberField(TEXT("auto_save_interval_seconds"), TempDouble))
            {
                OutConfig.SaveGame.AutoSaveIntervalSeconds = (int32)TempDouble;
            }
        }
    }

    return true;
}

void UOrionConfigSubsystem::ValidateConfig(FOrionConfig& ConfigToValidate)
{
    // company_name validation
    if (ConfigToValidate.Client.CompanyName.IsEmpty())
    {
        ConfigToValidate.Client.CompanyName = TEXT("Orion Studios");
    }

    // plant_name validation
    if (ConfigToValidate.Client.PlantName.IsEmpty())
    {
        ConfigToValidate.Client.PlantName = TEXT("Demo Plant");
    }

    // logo_path validation
    if (!ConfigToValidate.Client.LogoPath.IsEmpty())
    {
        // Resolve path relative to project folder or project content folder
        FString FullLogoPath = FPaths::Combine(FPaths::ProjectDir(), ConfigToValidate.Client.LogoPath);
        if (!FPaths::FileExists(FullLogoPath))
        {
            FString ContentLogoPath = FPaths::Combine(FPaths::ProjectContentDir(), ConfigToValidate.Client.LogoPath);
            if (!FPaths::FileExists(ContentLogoPath))
            {
                UE_LOG(LogOrionConfig, Warning, TEXT("Logo file not found at %s or %s. Clearing logo path."), *FullLogoPath, *ContentLogoPath);
                ConfigToValidate.Client.LogoPath = TEXT("");
            }
        }
    }

    // target_fps_desktop and target_fps_vr validation: clamp within [30, 144]
    ConfigToValidate.Optimization.TargetFPSDesktop = FMath::Clamp(ConfigToValidate.Optimization.TargetFPSDesktop, 30, 144);
    ConfigToValidate.Optimization.TargetFPSVR = FMath::Clamp(ConfigToValidate.Optimization.TargetFPSVR, 30, 144);

    // auto_save_interval_seconds validation: clamp to minimum of 10 seconds
    ConfigToValidate.SaveGame.AutoSaveIntervalSeconds = FMath::Max(ConfigToValidate.SaveGame.AutoSaveIntervalSeconds, 10);
}

#if !UE_BUILD_SHIPPING
void UOrionConfigSubsystem::SetupDirectoryWatcher()
{
    FDirectoryWatcherModule& DirectoryWatcherModule = FModuleManager::LoadModuleChecked<FDirectoryWatcherModule>(TEXT("DirectoryWatcher"));
    IDirectoryWatcher* DirectoryWatcher = DirectoryWatcherModule.Get();
    if (DirectoryWatcher)
    {
        FString WatcherDirectory = FPaths::GetPath(ConfigFilePath);
        UE_LOG(LogOrionConfig, Log, TEXT("Registering directory watcher for config folder: %s"), *WatcherDirectory);

        IDirectoryWatcher::FDirectoryChanged Delegate = IDirectoryWatcher::FDirectoryChanged::CreateUObject(this, &UOrionConfigSubsystem::OnConfigFileChanged);
        DirectoryWatcher->RegisterDirectoryChangedCallback_Handle(
            WatcherDirectory,
            Delegate,
            OnDirectoryChangedDelegateHandle
        );
    }
}

void UOrionConfigSubsystem::CleanupDirectoryWatcher()
{
    if (OnDirectoryChangedDelegateHandle.IsValid() && FModuleManager::Get().IsModuleLoaded(TEXT("DirectoryWatcher")))
    {
        FDirectoryWatcherModule& DirectoryWatcherModule = FModuleManager::LoadModuleChecked<FDirectoryWatcherModule>(TEXT("DirectoryWatcher"));
        IDirectoryWatcher* DirectoryWatcher = DirectoryWatcherModule.Get();
        if (DirectoryWatcher)
        {
            FString WatcherDirectory = FPaths::GetPath(ConfigFilePath);
            DirectoryWatcher->UnregisterDirectoryChangedCallback_Handle(WatcherDirectory, OnDirectoryChangedDelegateHandle);
        }
        OnDirectoryChangedDelegateHandle.Reset();
    }
}

void UOrionConfigSubsystem::OnConfigFileChanged(const TArray<FFileChangeData>& FileChanges)
{
    for (const FFileChangeData& Change : FileChanges)
    {
        FString ChangedFile = FPaths::ConvertRelativePathToFull(Change.Filename);
        if (ChangedFile == ConfigFilePath)
        {
            UE_LOG(LogOrionConfig, Log, TEXT("Config file change detected! Reloading..."));
            
            // Reload the configuration
            bool bSuccess = LoadConfig();
            
            // Broadcast reloaded delegate
            OnConfigReloaded.Broadcast();
            break;
        }
    }
}
#endif
