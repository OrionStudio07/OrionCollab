// OrionModeManager.h
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "OrionTypes.h"
#include "OrionModeManager.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnModeChanged, EOrionMode, OldMode, EOrionMode, NewMode);

/**
 * UOrionModeManager
 * Global mode state management world subsystem.
 */
UCLASS(BlueprintType, Blueprintable)
class ORIONCOLLAB_API UOrionModeManager : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UOrionModeManager();

    // Begin USubsystem Interface
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    virtual void OnWorldBeginPlay(UWorld& InWorld) override;
    // End USubsystem Interface

    /** Gets the Mode Manager subsystem */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode", meta = (WorldContext = "WorldContextObject"))
    static UOrionModeManager* GetModeManagerSubsystem(const UObject* WorldContextObject);

    /** Transitions to a new mode, validating permissions and triggering delegates */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode")
    void SetMode(EOrionMode NewMode);

    /** Gets the currently active mode */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode", BlueprintPure)
    EOrionMode GetCurrentMode() const;

    /** Sets the current user's role */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode")
    void SetCurrentRole(EOrionRole NewRole);

    /** Gets the current user's role */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode", BlueprintPure)
    EOrionRole GetCurrentRole() const;

    /** Checks if a role is permitted to enter a specific mode */
    UFUNCTION(BlueprintCallable, Category = "Orion|Mode", BlueprintPure)
    bool CanAccessMode(EOrionMode Mode, EOrionRole Role) const;

    /** Delegate fired when the active mode changes */
    UPROPERTY(BlueprintAssignable, Category = "Orion|Mode")
    FOnModeChanged OnModeChanged;

protected:
    UPROPERTY(BlueprintReadOnly, Category = "Orion|Mode")
    EOrionMode CurrentMode;

    UPROPERTY(BlueprintReadOnly, Category = "Orion|Mode")
    EOrionRole CurrentRole;

private:
    // Stashed variables that survive level load transitions
    static EOrionMode StashedMode;
    static EOrionRole StashedRole;
    static bool bHasStashedState;
};
