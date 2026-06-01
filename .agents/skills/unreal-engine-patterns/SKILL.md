---
name: unreal-engine-patterns
description: Master Unreal Engine gameplay programming patterns including C++ macro standards, actor lifecycles, delegates, subsystems, and performance optimization. Use when building Unreal games, implementing gameplay systems, or developing plugins.
---

# Unreal Engine Patterns

Production gameplay programming patterns for Unreal Engine, covering C++ architecture, gameplay framework, delegate events, and optimization best practices.

## When to Use This Skill

- Developing games and gameplay systems in C++ or Blueprints
- Creating custom Unreal Engine plugins or editor tools
- Structuring actor classes, components, and subsystems
- Setting up performance-focused memory and garbage collection structures
- Implementing event-driven game logic using delegates

## Core Concepts

### 1. Blueprints vs C++ Architecture Guidelines

A hybrid approach is the gold standard in Unreal Engine:
- **C++**: Base architecture, heavy math, network replication, data-heavy systems, and core interfaces.
- **Blueprints**: Content configuration, UI bindings, sound/particle spawning, cosmetic adjustments, and rapid prototyping.

```
UObject (Base Engine class)
├── AActor (Spawnable in the world, supports Components)
│   ├── AGameModeBase (Rules, flow, and spawning logic)
│   ├── APawn (Possessable actor by controllers)
│   │   └── ACharacter (Pawn with CharacterMovementComponent)
│   └── APlayerController (Interface between human and Pawn)
└── UActorComponent (Reusable modular behavior)
    └── USceneComponent (Component with a transform/position)
```

### 2. Core Unreal C++ Class Structure

```cpp
// MyCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MyCharacter.generated.h"

UCLASS(Blueprintable)
class MCP_API AMyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMyCharacter();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // Exposed variable with category and read/write permissions
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
    float MaxHealth;

    // Callable from Blueprints, implemented in C++
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TakeDamageAmount(float DamageAmount);

    // Native implementation, customizable in Blueprints
    UFUNCTION(BlueprintNativeEvent, Category = "Combat")
    void OnDeath();
    virtual void OnDeath_Implementation();
};
```

```cpp
// MyCharacter.cpp
#include "MyCharacter.h"

AMyCharacter::AMyCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    MaxHealth = 100.0f;
}

void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();
}

void AMyCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void AMyCharacter::TakeDamageAmount(float DamageAmount)
{
    MaxHealth = FMath::Max(MaxHealth - DamageAmount, 0.0f);
    if (MaxHealth <= 0.0f)
    {
        OnDeath();
    }
}

void AMyCharacter::OnDeath_Implementation()
{
    // Default C++ implementation, can be overridden/extended in Blueprints
}
```

## Detailed Patterns and Worked Examples

Detailed pattern documentation lives in `references/details.md`. Read that file when you need robust examples of delegates, subsystems, state machines, and optimization patterns.
