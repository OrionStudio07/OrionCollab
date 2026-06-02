# Orion Studios — C++ Implementation Patterns

Used by @cpp-engineer. Scope is strictly limited to three systems.

---

## Scope Gate

Before writing any C++, verify the task is one of:

1. `OrionTypes.h` — enum and struct type definitions only
2. `BP_HierarchyManager` search — SearchAll(), fuzzy matching, TMap cache
3. `BP_SnapManager` — vertex buffer queries, edge/midpoint detection

If the task is NOT in this list → redirect to @blueprint-engineer.
Blueprint is primary. C++ is the exception.

---

## OrionTypes.h — Enum Pattern

Every enum must follow this pattern exactly (backend_schema.md Section 1):

```cpp
// OrionTypes.h
#pragma once
#include "CoreMinimal.h"
#include "OrionTypes.generated.h"

UENUM(BlueprintType)
enum class EEnumName : uint8
{
    VALUE_ONE = 0  UMETA(DisplayName = "Display Name"),
    VALUE_TWO = 1  UMETA(DisplayName = "Display Name")
};
```

Rules:
- Copy enum values VERBATIM from backend_schema.md Section 1
- Never reorder, rename, or add values without flagging
- All enums: `UENUM(BlueprintType)` and `: uint8`
- All values: `UMETA(DisplayName = "...")` exactly as shown in spec

---

## HierarchyManager Search — Required Implementation

```cpp
// Required per trd.md Section 3.2:

// Search index fields (all must be indexed):
//   DisplayName, PIDTag, ProcessLine, RoomName, BuildingName

// Matching algorithm:
//   1. Case-insensitive substring match (highest priority)
//   2. Levenshtein distance ≤ 3 (fuzzy, flagged as ambiguous)

// Cache:
//   TMap<FString, TArray<FSearchResult>> QueryCache;
//   Always check cache before running search

// Threading:
//   BuildTree() → background thread (AsyncTask or UE5 task graph)
//   SearchAll() → background thread OR cache hit on game thread
//   NEVER run 6500-entry scan on game thread

// Performance target:
//   <200ms for any query across 6500 entries (trd.md Section 9)

// FSearchResult must contain:
//   FName EquipmentID
//   FText DisplayName
//   FString PIDTag
//   EMatchConfidence MatchType  (Exact / Contains / Fuzzy / Unmatched)
```

---

## SnapManager — Required Implementation

```cpp
// Required per trd.md and flow_diagrams.md Flow 5:

// Snap priority order:
//   1. Vertex    — within 5cm  → diamond indicator
//   2. Midpoint  — within 2.5cm of edge midpoint → circle indicator
//   3. Edge      — within 5cm  → point indicator
//   4. BBox Center — within 5cm → square indicator
//   5. None      — raw hit position

// Mesh access requirement:
//   Must read UStaticMesh vertex buffer at runtime
//   Transform vertices: local space → world space
//   Flag if mesh is not CPU-accessible: [VERIFY CPU ACCESS]

// ESnapType values (from OrionTypes.h):
//   None, Vertex, Edge, Midpoint, Center, Face, Intersection
```

---

## C++ Output Format

```
FILE: [filename.h / filename.cpp]
SPEC REF: [backend_schema.md / trd.md section]

[Complete file content]

COMPILE NOTES:
  Required includes: [list]
  Required .Build.cs module deps: [list]
  Unverified UE5 APIs: [list — each marked [VERIFY IN UE5.8 SOURCE]]

GATE CHECK:
  □ Compiles with zero errors
  □ All enum values match backend_schema.md verbatim
  □ All UPROPERTY/UFUNCTION macros correct
  □ Blueprint-accessible (BlueprintType on all types)
  □ No external library dependencies
```

---

## UE5 Macro Requirements

```cpp
// Struct:
USTRUCT(BlueprintType)
struct ORION_API FMyStruct : public FTableRowBase
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CategoryName")
    FName FieldName;
};

// Class:
UCLASS()
class ORION_API UMyClass : public UWorldSubsystem
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category = "Orion")
    void MyFunction();
};

// Delegate:
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(
    FDelegateName, EType, Param1, FName, Param2);

UPROPERTY(BlueprintAssignable)
FDelegateName OnSomethingHappened;
```
