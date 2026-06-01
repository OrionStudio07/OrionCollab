// OrionCameraSweepManager.h
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "OrionTypes.h"
#include "OrionCameraSweepManager.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSweepComplete, FName, TargetID);

UCLASS(ClassGroup=(Orion), BlueprintType, Blueprintable, meta=(BlueprintSpawnableComponent))
class ORIONCOLLAB_API UOrionCameraSweepManager : public UActorComponent
{
    GENERATED_BODY()

public:
    UOrionCameraSweepManager();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /** Starts sweeping the camera to target actor */
    UFUNCTION(BlueprintCallable, Category = "Orion|CameraSweep")
    void SweepToActor(AActor* TargetActor, FName TargetID = NAME_None);

    /** Starts sweeping the camera to a target world transform */
    UFUNCTION(BlueprintCallable, Category = "Orion|CameraSweep")
    void SweepToTransform(const FTransform& TargetTransform, FName TargetID = NAME_None);

    /** Event handler for equipment selection from hierarchy manager */
    UFUNCTION(BlueprintCallable, Category = "Orion|CameraSweep")
    void HandleEquipmentSelected(FName EquipmentID);

    /** Sweep speed configuration */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|CameraSweep")
    EOrionSweepSpeed SweepSpeed;

    /** Minimum distance the camera will frame the actor from */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|CameraSweep")
    float MinViewDistance;

    /** Maximum distance the camera will frame the actor from */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|CameraSweep")
    float MaxViewDistance;

    /** Radius used for sphere tracing to detect obstructions */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|CameraSweep")
    float CollisionAvoidanceRadius;

    /** Fired when the camera sweep is complete */
    UPROPERTY(BlueprintAssignable, Category = "Orion|CameraSweep")
    FOnSweepComplete OnSweepComplete;

    /** Returns whether the camera is currently in a sweep animation */
    UFUNCTION(BlueprintCallable, Category = "Orion|CameraSweep", BlueprintPure)
    bool IsSweeping() const { return bIsSweeping; }

    /** Calculates the optimal camera location and rotation looking at an actor */
    UFUNCTION(BlueprintCallable, Category = "Orion|CameraSweep", BlueprintPure)
    FVector CalculateOptimalCameraLocation(AActor* TargetActor, FRotator& OutRotation) const;

private:
    void StartSweep(const FVector& StartLoc, const FQuat& StartRot, const FVector& EndLoc, const FQuat& EndRot, FName InTargetID);
    void UpdateSweep(float DeltaTime);
    float GetSweepDuration() const;

    bool bIsSweeping;
    float SweepProgress; // 0.0 to 1.0
    float ElapsedTime;
    float TargetDuration;

    FVector SweepStartLocation;
    FQuat SweepStartRotation;
    FVector SweepEndLocation;
    FQuat SweepEndRotation;
    FName CurrentTargetID;

    // Waypoint state for collision avoidance
    bool bUseWaypoint;
    FVector WaypointLocation;
};
