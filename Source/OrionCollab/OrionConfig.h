// OrionConfig.h
#pragma once

#include "CoreMinimal.h"
#include "OrionConfig.generated.h"

USTRUCT(BlueprintType)
struct FOrionClientConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Client")
    FString CompanyName = TEXT("Orion Studios");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Client")
    FString PlantName = TEXT("Demo Plant");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Client")
    FString LogoPath = TEXT("");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Client")
    FLinearColor AccentColor = FLinearColor(0.f, 0.831f, 0.667f, 1.f);  // #00D4AA
};

USTRUCT(BlueprintType)
struct FOrionModeConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Modes")
    bool bShowcase = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Modes")
    bool bTraining = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Modes")
    bool bOperations = true;
};

USTRUCT(BlueprintType)
struct FOrionFeatureConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    bool bMinimap = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    bool bGuidedTour = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    bool bNPCWorkers = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    bool bSessionRecording = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    bool bSimulationData = false;
};

USTRUCT(BlueprintType)
struct FOrionOptimizationConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Optimization")
    bool bLumenEnabled = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Optimization")
    FString VRMode = TEXT("pc_tethered");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Optimization")
    int32 TargetFPSDesktop = 60;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Optimization")
    int32 TargetFPSVR = 72;
};

USTRUCT(BlueprintType)
struct FOrionSaveConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveGame")
    FString SaveFilePrefix = TEXT("Orion");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveGame")
    int32 AutoSaveIntervalSeconds = 300;
};

USTRUCT(BlueprintType)
struct FOrionConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Client")
    FOrionClientConfig Client;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Modes")
    FOrionModeConfig Modes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
    FOrionFeatureConfig Features;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Optimization")
    FOrionOptimizationConfig Optimization;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveGame")
    FOrionSaveConfig SaveGame;
};
