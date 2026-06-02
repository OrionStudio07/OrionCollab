// OrionHierarchyTypes.h
#pragma once

#include "CoreMinimal.h"
#include "OrionTypes.h"
#include "GameFramework/Actor.h"
#include "OrionHierarchyTypes.generated.h"

USTRUCT(BlueprintType)
struct FEquipmentNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FName EquipmentID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FString PIDTag;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FString ProcessLine;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    EEquipmentType Type = EEquipmentType::Other;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    TWeakObjectPtr<AActor> WorldActor;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    TArray<FName> ComponentIDs;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    bool bComponentsLoaded = false;
};

USTRUCT(BlueprintType)
struct FRoomNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FName RoomID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    EZoneClassification SafetyZone = EZoneClassification::General;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    int32 Floor = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    TArray<FEquipmentNode> Equipment;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    int32 EquipmentCount = 0;
};

USTRUCT(BlueprintType)
struct FBuildingNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FName BuildingID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    int32 Floors = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    TArray<FRoomNode> Rooms;
};

USTRUCT(BlueprintType)
struct FSearchResult
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Search")
    FName ID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Search")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Search")
    FString Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Search")
    float Relevance = 0.f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Search")
    EEquipmentType EquipmentType = EEquipmentType::Other;
};

UENUM(BlueprintType)
enum class EOrionTreeCategory : uint8
{
    Building    UMETA(DisplayName = "Building"),
    Room        UMETA(DisplayName = "Room"),
    Equipment   UMETA(DisplayName = "Equipment"),
    Component   UMETA(DisplayName = "Component")
};

UCLASS(BlueprintType)
class ORIONCOLLAB_API UOrionTreeItemData : public UObject
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FName NodeID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    EOrionTreeCategory Category = EOrionTreeCategory::Building;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    EEquipmentType EquipmentType = EEquipmentType::Other;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    int32 Depth = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    bool bIsExpanded = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Hierarchy")
    FName ParentID;
};

