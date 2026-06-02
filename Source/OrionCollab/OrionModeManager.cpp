// OrionModeManager.cpp
#include "OrionModeManager.h"
#include "Engine/World.h"
#include "Blueprint/UserWidget.h"
#include "Blueprint/WidgetBlueprintLibrary.h"

DEFINE_LOG_CATEGORY_STATIC(LogOrionModeManager, Log, All);

// Initialize static stashed variables
EOrionMode UOrionModeManager::StashedMode = EOrionMode::MODE_LAUNCHER;
EOrionRole UOrionModeManager::StashedRole = EOrionRole::ROLE_VIEWER;
bool UOrionModeManager::bHasStashedState = false;

UOrionModeManager::UOrionModeManager()
    : CurrentMode(EOrionMode::MODE_LAUNCHER)
    , CurrentRole(EOrionRole::ROLE_VIEWER)
{
}

void UOrionModeManager::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogOrionModeManager, Log, TEXT("Orion Mode Manager Subsystem Initialized."));
}

void UOrionModeManager::Deinitialize()
{
    Super::Deinitialize();
    UE_LOG(LogOrionModeManager, Log, TEXT("Orion Mode Manager Subsystem Deinitialized."));
}

void UOrionModeManager::OnWorldBeginPlay(UWorld& InWorld)
{
    Super::OnWorldBeginPlay(InWorld);

    FString WorldName = InWorld.GetName();
    UE_LOG(LogOrionModeManager, Log, TEXT("OnWorldBeginPlay in world: %s"), *WorldName);

    // Reset stashed state when entering the LoginLevel (initial/launcher level)
    if (WorldName.Contains(TEXT("LoginLevel")))
    {
        UE_LOG(LogOrionModeManager, Log, TEXT("LoginLevel detected. Resetting stashed mode and role to defaults."));
        CurrentMode = EOrionMode::MODE_LAUNCHER;
        CurrentRole = EOrionRole::ROLE_VIEWER;
        
        StashedMode = EOrionMode::MODE_LAUNCHER;
        StashedRole = EOrionRole::ROLE_VIEWER;
        bHasStashedState = false;
    }
    // Restore stashed state on other levels (e.g. Main/Sample Level)
    else if (bHasStashedState)
    {
        EOrionMode OldMode = CurrentMode;
        CurrentMode = StashedMode;
        CurrentRole = StashedRole;
        
        UE_LOG(LogOrionModeManager, Log, TEXT("Restoring stashed session state on level load: Mode = %d, Role = %d"), 
            static_cast<int32>(CurrentMode), static_cast<int32>(CurrentRole));

        // Fire delegate to alert any listening entities in the newly loaded level
        OnModeChanged.Broadcast(OldMode, CurrentMode);
    }
    // Direct level play fallback (PIE convenience)
    else
    {
        EOrionMode OldMode = CurrentMode;
        CurrentMode = EOrionMode::MODE_SHOWCASE;
        CurrentRole = EOrionRole::ROLE_ADMIN;
        
        UE_LOG(LogOrionModeManager, Log, TEXT("Direct PIE level play detected without launcher. Defaulting to Showcase mode and Admin role."));
        OnModeChanged.Broadcast(OldMode, CurrentMode);
    }

    // Programmatically spawn WBP_OrionRoot and collapse default CVT UI on level start
    if (InWorld.IsGameWorld())
    {
        UClass* WidgetClass = StaticLoadClass(UUserWidget::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/UMG/WBP_OrionRoot.WBP_OrionRoot_C"));
        if (WidgetClass)
        {
            UUserWidget* RootWidget = CreateWidget<UUserWidget>(&InWorld, WidgetClass);
            if (RootWidget)
            {
                RootWidget->AddToViewport(0);
                UE_LOG(LogOrionModeManager, Log, TEXT("WBP_OrionRoot successfully added to viewport."));
            }
        }

        // Surgical collapse of default CVT template UI to avoid overlaps
        TArray<UUserWidget*> FoundWidgets;
        UWidgetBlueprintLibrary::GetAllWidgetsOfClass(&InWorld, FoundWidgets, UUserWidget::StaticClass(), true);
        for (UUserWidget* Widget : FoundWidgets)
        {
            if (Widget && Widget->GetClass()->GetName().Contains(TEXT("Destop_UI")))
            {
                Widget->SetVisibility(ESlateVisibility::Collapsed);
                UE_LOG(LogOrionModeManager, Log, TEXT("Surgically collapsed default CVT Destop_UI widget."));
            }
        }
    }
}

UOrionModeManager* UOrionModeManager::GetModeManagerSubsystem(const UObject* WorldContextObject)
{
    if (!WorldContextObject)
    {
        return nullptr;
    }
    UWorld* World = WorldContextObject->GetWorld();
    if (!World)
    {
        return nullptr;
    }
    return World->GetSubsystem<UOrionModeManager>();
}

void UOrionModeManager::SetMode(EOrionMode NewMode)
{
    if (CurrentMode == NewMode)
    {
        return;
    }

    if (!CanAccessMode(NewMode, CurrentRole))
    {
        UE_LOG(LogOrionModeManager, Warning, TEXT("Access Denied: Role %d cannot access Mode %d"), 
            static_cast<int32>(CurrentRole), static_cast<int32>(NewMode));
        return;
    }

    EOrionMode OldMode = CurrentMode;
    CurrentMode = NewMode;

    // Stash the state to persist across level transitions
    StashedMode = CurrentMode;
    bHasStashedState = true;

    UE_LOG(LogOrionModeManager, Log, TEXT("Mode changed from %d to %d (Role: %d)"), 
        static_cast<int32>(OldMode), static_cast<int32>(CurrentMode), static_cast<int32>(CurrentRole));

    OnModeChanged.Broadcast(OldMode, CurrentMode);
}

EOrionMode UOrionModeManager::GetCurrentMode() const
{
    return CurrentMode;
}

void UOrionModeManager::SetCurrentRole(EOrionRole NewRole)
{
    CurrentRole = NewRole;
    
    // Stash the role to persist across level transitions
    StashedRole = CurrentRole;
    bHasStashedState = true;

    UE_LOG(LogOrionModeManager, Log, TEXT("Role set to: %d"), static_cast<int32>(CurrentRole));
}

EOrionRole UOrionModeManager::GetCurrentRole() const
{
    return CurrentRole;
}

bool UOrionModeManager::CanAccessMode(EOrionMode Mode, EOrionRole Role) const
{
    // Admin has access to all modes
    if (Role == EOrionRole::ROLE_ADMIN)
    {
        return true;
    }

    // Launcher mode is accessible to everyone
    if (Mode == EOrionMode::MODE_LAUNCHER)
    {
        return true;
    }

    // Showcase mode is accessible to everyone
    if (Mode == EOrionMode::MODE_SHOWCASE)
    {
        return true;
    }

    // Operations mode is only accessible to Admin and Engineer
    if (Mode == EOrionMode::MODE_OPERATIONS)
    {
        return (Role == EOrionRole::ROLE_ENGINEER);
    }

    // Training mode (v2) is only accessible to Admin (Viewer/Engineer do not have access in v1)
    if (Mode == EOrionMode::MODE_TRAINING)
    {
        return false;
    }

    return false;
}
