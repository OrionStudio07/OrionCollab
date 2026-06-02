# Unreal Engine Patterns — Detailed References & Worked Examples

## 1. Event Delegates (Native & Dynamic Multicast)

Delegates let you write decoupled, event-driven systems. Use dynamic multicast delegates when you need exposure to Blueprints (e.g. for audio/visual effects), and native multicast delegates for maximum C++ efficiency.

### Pattern: Dynamic Multicast Delegate (Blueprint Bindable)

```cpp
// HealthComponent.h
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HealthComponent.generated.h"

// Define a dynamic multicast delegate with parameters (used for Blueprint Event Dispatchers)
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnHealthChanged, float, CurrentHealth, float, MaxHealth, AActor*, DamageInstigator);

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MCP_API UHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHealthComponent();

protected:
    virtual void BeginPlay() override;

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Health")
    float MaxHealth;

    UPROPERTY(BlueprintReadOnly, Category = "Health")
    float CurrentHealth;

    // Delegate Instance exposed to Blueprints
    UPROPERTY(BlueprintAssignable, Category = "Events")
    FOnHealthChanged OnHealthChanged;

    UFUNCTION(BlueprintCallable, Category = "Health")
    void ApplyDamage(float Amount, AActor* Instigator);
};
```

```cpp
// HealthComponent.cpp
#include "HealthComponent.h"

UHealthComponent::UHealthComponent()
{
    MaxHealth = 100.0f;
    CurrentHealth = MaxHealth;
}

void UHealthComponent::BeginPlay()
{
    Super::BeginPlay();
    CurrentHealth = MaxHealth;
}

void UHealthComponent::ApplyDamage(float Amount, AActor* Instigator)
{
    if (CurrentHealth <= 0.0f) return;

    CurrentHealth = FMath::Max(CurrentHealth - Amount, 0.0f);
    
    // Broadcast the event to all listeners (C++ & Blueprints)
    OnHealthChanged.Broadcast(CurrentHealth, MaxHealth, Instigator);
}
```

---

## 2. Engine and Game Subsystems

Subsystems provide an easy way to write modular, single-instance classes with automatic lifecycle management, avoiding the downsides of traditional singletons.

### Pattern: Game Instance Subsystem

```cpp
// SaveGameSubsystem.h
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "SaveGameSubsystem.generated.h"

UCLASS()
class MCP_API USaveGameSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    // Automatically called when the game instance starts up
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    // Automatically called when the game instance shuts down
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    void SaveGameData(const FString& SlotName);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    bool LoadGameData(const FString& SlotName);
};
```

```cpp
// SaveGameSubsystem.cpp
#include "SaveGameSubsystem.h"

void USaveGameSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogTemp, Log, TEXT("SaveGameSubsystem Initialized!"));
}

void USaveGameSubsystem::Deinitialize()
{
    UE_LOG(LogTemp, Log, TEXT("SaveGameSubsystem Deinitialized!"));
    Super::Deinitialize();
}

void USaveGameSubsystem::SaveGameData(const FString& SlotName)
{
    // Write save game serialization logic here
}

bool USaveGameSubsystem::LoadGameData(const FString& SlotName)
{
    // Write load game serialization logic here
    return true;
}
```

---

## 3. Smart Pointer Usage and Garbage Collection

To prevent memory leaks and access violations, you must understand Unreal's pointer models.

### UObjects and Garbage Collection
- **Rule**: Any raw pointer to a `UObject` (or classes inheriting from it like `AActor`, `UActorComponent`) **MUST** be decorated with `UPROPERTY()` if held as a class member. If not decorated, the garbage collector will not see the reference and may free the object, leading to a dangling pointer.
- **Rule**: If referencing a transient `UObject` where you do not want to prevent garbage collection, use `TWeakObjectPtr<T>`.

### Non-UObjects (Standard C++ classes)
Use Unreal's custom smart pointers for standard C++ classes:
- `TSharedPtr<T>`: Thread-safe ref-counted shared pointer.
- `TSharedRef<T>`: Shared reference that cannot be null.
- `TWeakPtr<T>`: Weak pointer to prevent reference cycles.
- `TUniquePtr<T>`: Exclusively owned pointer.

```cpp
// Usage Example:
struct FCustomStruct
{
    int32 ID;
    FString Name;
};

// Creating smart pointers
TSharedPtr<FCustomStruct> SharedData = MakeShared<FCustomStruct>();
TUniquePtr<FCustomStruct> UniqueData = MakeUnique<FCustomStruct>();
```

---

## 4. Performance & Best Practices

- **Avoid Blueprints Ticking**: Disable `Tick` on Actors and Components unless absolutely necessary. Instead, use timer handles (`GetWorldTimerManager().SetTimer(...)`) or event-driven delegate bindings.
- **Constructor vs BeginPlay**: Only do default values and structural setups (like component creation using `CreateDefaultSubobject`) in the constructor. Perform actual game logic, lookup, and network binding in `BeginPlay()`.
- **String Handling**: Use `FName` for identifiers and keys (fast comparison), `FText` for user-facing localized text, and `FString` for string manipulation/mutations.
