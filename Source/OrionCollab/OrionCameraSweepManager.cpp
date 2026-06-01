// OrionCameraSweepManager.cpp
#include "OrionCameraSweepManager.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Engine/World.h"
#include "Engine/HitResult.h"
#include "CollisionQueryParams.h"
#include "OrionHierarchyManager.h"

UOrionCameraSweepManager::UOrionCameraSweepManager()
    : SweepSpeed(EOrionSweepSpeed::Medium)
    , MinViewDistance(200.f)
    , MaxViewDistance(2000.f)
    , CollisionAvoidanceRadius(50.f)
    , bIsSweeping(false)
    , SweepProgress(0.f)
    , ElapsedTime(0.f)
    , TargetDuration(2.f)
    , SweepStartLocation(FVector::ZeroVector)
    , SweepStartRotation(FQuat::Identity)
    , SweepEndLocation(FVector::ZeroVector)
    , SweepEndRotation(FQuat::Identity)
    , CurrentTargetID(NAME_None)
    , bUseWaypoint(false)
    , WaypointLocation(FVector::ZeroVector)
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bStartWithTickEnabled = true;
}

void UOrionCameraSweepManager::BeginPlay()
{
    Super::BeginPlay();

    // Bind to the Hierarchy Manager's OnEquipmentSelected delegate
    UOrionHierarchyManager* HierarchyManager = UOrionHierarchyManager::GetHierarchyManagerSubsystem(GetWorld());
    if (HierarchyManager)
    {
        HierarchyManager->OnEquipmentSelected.AddDynamic(this, &UOrionCameraSweepManager::HandleEquipmentSelected);
    }
}

void UOrionCameraSweepManager::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    if (bIsSweeping)
    {
        UpdateSweep(DeltaTime);
    }
}

void UOrionCameraSweepManager::HandleEquipmentSelected(FName EquipmentID)
{
    UOrionHierarchyManager* HierarchyManager = UOrionHierarchyManager::GetHierarchyManagerSubsystem(GetWorld());
    if (HierarchyManager)
    {
        AActor* TargetActor = HierarchyManager->GetEquipmentActor(EquipmentID);
        if (TargetActor)
        {
            SweepToActor(TargetActor, EquipmentID);
        }
    }
}

void UOrionCameraSweepManager::SweepToActor(AActor* TargetActor, FName TargetID)
{
    if (!TargetActor)
    {
        return;
    }

    APawn* OwningPawn = Cast<APawn>(GetOwner());
    if (!OwningPawn)
    {
        return;
    }

    APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController());
    
    // Determine start location and rotation
    FVector StartLoc = OwningPawn->GetActorLocation();
    FQuat StartRot = PC ? FQuat(PC->GetControlRotation()) : FQuat(OwningPawn->GetActorRotation());

    // Calculate end location and rotation looking at the target
    FRotator EndRotator;
    FVector EndLoc = CalculateOptimalCameraLocation(TargetActor, EndRotator);
    FQuat EndRot = FQuat(EndRotator);

    StartSweep(StartLoc, StartRot, EndLoc, EndRot, TargetID);
}

void UOrionCameraSweepManager::SweepToTransform(const FTransform& TargetTransform, FName TargetID)
{
    APawn* OwningPawn = Cast<APawn>(GetOwner());
    if (!OwningPawn)
    {
        return;
    }

    APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController());

    // Determine start location and rotation
    FVector StartLoc = OwningPawn->GetActorLocation();
    FQuat StartRot = PC ? FQuat(PC->GetControlRotation()) : FQuat(OwningPawn->GetActorRotation());

    FVector EndLoc = TargetTransform.GetLocation();
    FQuat EndRot = TargetTransform.GetRotation();

    StartSweep(StartLoc, StartRot, EndLoc, EndRot, TargetID);
}

void UOrionCameraSweepManager::StartSweep(const FVector& StartLoc, const FQuat& StartRot, const FVector& EndLoc, const FQuat& EndRot, FName InTargetID)
{
    SweepStartLocation = StartLoc;
    SweepStartRotation = StartRot;
    SweepEndLocation = EndLoc;
    SweepEndRotation = EndRot;
    CurrentTargetID = InTargetID;

    SweepProgress = 0.f;
    ElapsedTime = 0.f;
    TargetDuration = GetSweepDuration();
    bIsSweeping = true;

    // Plan path with sphere trace collision check
    bUseWaypoint = false;
    UWorld* World = GetWorld();
    if (World)
    {
        FHitResult HitResult;
        FCollisionShape CollisionShape = FCollisionShape::MakeSphere(CollisionAvoidanceRadius);
        FCollisionQueryParams QueryParams;
        QueryParams.AddIgnoredActor(GetOwner()); // Ignore ourselves

        // If sweeping to an equipment actor, ignore it to prevent clipping blocks at final destination
        UOrionHierarchyManager* HierarchyManager = UOrionHierarchyManager::GetHierarchyManagerSubsystem(World);
        if (HierarchyManager && CurrentTargetID != NAME_None)
        {
            AActor* TargetActor = HierarchyManager->GetEquipmentActor(CurrentTargetID);
            if (TargetActor)
            {
                QueryParams.AddIgnoredActor(TargetActor);
            }
        }

        bool bHit = World->SweepSingleByChannel(
            HitResult,
            StartLoc,
            EndLoc,
            FQuat::Identity,
            ECC_Visibility,
            CollisionShape,
            QueryParams
        );

        if (bHit)
        {
            // Plan waypoint offset upwards above the obstruction hit point
            bUseWaypoint = true;
            WaypointLocation = HitResult.Location + FVector(0.f, 0.f, 250.f);
        }
    }

    // Temporarily disable look and movement input during sweep to prevent input fighting
    APawn* OwningPawn = Cast<APawn>(GetOwner());
    if (OwningPawn)
    {
        APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController());
        if (PC)
        {
            PC->SetIgnoreLookInput(true);
            PC->SetIgnoreMoveInput(true);
        }
    }
}

void UOrionCameraSweepManager::UpdateSweep(float DeltaTime)
{
    ElapsedTime += DeltaTime;
    SweepProgress = FMath::Clamp(ElapsedTime / TargetDuration, 0.f, 1.f);

    // Cubic ease-in-out helper
    auto EaseInOutCubic = [](float t) -> float
    {
        return t < 0.5f ? 4.f * t * t * t : 1.f - FMath::Pow(-2.f * t + 2.f, 3.f) / 2.f;
    };

    float t = EaseInOutCubic(SweepProgress);

    // Interpolate location
    FVector CurrentLoc;
    if (bUseWaypoint)
    {
        if (t <= 0.5f)
        {
            float SegAlpha = t * 2.f;
            CurrentLoc = FMath::Lerp(SweepStartLocation, WaypointLocation, SegAlpha);
        }
        else
        {
            float SegAlpha = (t - 0.5f) * 2.f;
            CurrentLoc = FMath::Lerp(WaypointLocation, SweepEndLocation, SegAlpha);
        }
    }
    else
    {
        CurrentLoc = FMath::Lerp(SweepStartLocation, SweepEndLocation, t);
    }

    // Interpolate rotation (Slerp globally to avoid sudden shifts)
    FQuat CurrentRot = FQuat::Slerp(SweepStartRotation, SweepEndRotation, t);

    // Set player position and control rotation
    APawn* OwningPawn = Cast<APawn>(GetOwner());
    if (OwningPawn)
    {
        OwningPawn->SetActorLocation(CurrentLoc, false, nullptr, ETeleportType::TeleportPhysics);
        APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController());
        if (PC)
        {
            PC->SetControlRotation(CurrentRot.Rotator());
        }
        else
        {
            OwningPawn->SetActorRotation(CurrentRot.Rotator());
        }
    }

    // Finish check
    if (SweepProgress >= 1.f)
    {
        bIsSweeping = false;

        // Restore input
        if (OwningPawn)
        {
            APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController());
            if (PC)
            {
                PC->ResetIgnoreLookInput();
                PC->ResetIgnoreMoveInput();
            }
        }

        // Fire complete event
        OnSweepComplete.Broadcast(CurrentTargetID);
    }
}

float UOrionCameraSweepManager::GetSweepDuration() const
{
    switch (SweepSpeed)
    {
        case EOrionSweepSpeed::Fast:
            return 1.0f;
        case EOrionSweepSpeed::Slow:
            return 3.0f;
        case EOrionSweepSpeed::Medium:
        default:
            return 2.0f;
    }
}

FVector UOrionCameraSweepManager::CalculateOptimalCameraLocation(AActor* TargetActor, FRotator& OutRotation) const
{
    FVector Origin;
    FVector BoxExtent;
    TargetActor->GetActorBounds(false, Origin, BoxExtent);

    float SphereRadius = BoxExtent.Size();
    float TargetDistance = SphereRadius * 2.0f; // 2x bounds size is standard for good framing
    float OptimalDistance = FMath::Clamp(TargetDistance, MinViewDistance, MaxViewDistance);

    // Approach from the pawn's current direction relative to target
    APawn* OwningPawn = Cast<APawn>(GetOwner());
    FVector CurrentCamLoc = SweepStartLocation;
    if (OwningPawn)
    {
        CurrentCamLoc = OwningPawn->GetActorLocation();
    }

    FVector Direction = CurrentCamLoc - Origin;
    if (Direction.IsNearlyZero())
    {
        Direction = FVector(1.f, 0.f, 0.5f); // default angle: slightly offset in X and Z
    }
    Direction.Normalize();

    // Adjust Z component to keep camera slightly elevated above the actor for a premium 3/4 high angle
    if (Direction.Z < 0.2f)
    {
        Direction.Z = 0.3f;
        Direction.Normalize();
    }

    FVector TargetLoc = Origin + (Direction * OptimalDistance);
    OutRotation = (Origin - TargetLoc).Rotation();
    return TargetLoc;
}
