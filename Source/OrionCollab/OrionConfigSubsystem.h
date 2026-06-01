// OrionConfigSubsystem.h
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "OrionConfig.h"
#include "OrionConfigSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnConfigReloaded);

/**
 * UOrionConfigSubsystem
 * Handles loading, validation, and hot-reloading of the client's OrionConfig.json configuration.
 */
UCLASS(BlueprintType, Blueprintable)
class ORIONCOLLAB_API UOrionConfigSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    UOrionConfigSubsystem();

    // Begin USubsystem Interface
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    // End USubsystem Interface

    /** Loads the OrionConfig.json file from the project directory. */
    UFUNCTION(BlueprintCallable, Category = "Orion|Config")
    bool LoadConfig();

    /** Gets the currently active configuration. */
    UFUNCTION(BlueprintCallable, Category = "Orion|Config", BlueprintPure)
    const FOrionConfig& GetConfig() const { return CurrentConfig; }

    /** Returns whether the last configuration load was successful without using defaults. */
    UFUNCTION(BlueprintCallable, Category = "Orion|Config", BlueprintPure)
    bool IsConfigValid() const { return bIsConfigValid; }

    /** Delegate fired whenever the configuration is reloaded (dev/editor builds only). */
    UPROPERTY(BlueprintAssignable, Category = "Orion|Config")
    FOnConfigReloaded OnConfigReloaded;

protected:
    UPROPERTY(BlueprintReadOnly, Category = "Orion|Config")
    FOrionConfig CurrentConfig;

    UPROPERTY(BlueprintReadOnly, Category = "Orion|Config")
    bool bIsConfigValid;

    /** Absolute path to the config file */
    FString ConfigFilePath;

private:
    bool ParseConfigFromJson(const FString& JsonString, FOrionConfig& OutConfig);
    void ValidateConfig(FOrionConfig& ConfigToValidate);

#if !UE_BUILD_SHIPPING
    FDelegateHandle OnDirectoryChangedDelegateHandle;
    void SetupDirectoryWatcher();
    void CleanupDirectoryWatcher();
    void OnConfigFileChanged(const TArray<struct FFileChangeData>& FileChanges);
#endif
};
