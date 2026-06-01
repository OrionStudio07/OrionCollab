// OrionHierarchyManager.h
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "OrionHierarchyTypes.h"
#include "OrionTableRows.h"
#include "OrionHierarchyManager.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnTreeReady);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEquipmentSelected, FName, EquipmentID);

/**
 * UOrionHierarchyManager
 * World subsystem for equipment hierarchy building and fuzzy search.
 */
UCLASS(BlueprintType, Blueprintable)
class ORIONCOLLAB_API UOrionHierarchyManager : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UOrionHierarchyManager();

    // Begin USubsystem Interface
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    virtual void OnWorldBeginPlay(UWorld& InWorld) override;
    // End USubsystem Interface

    /** Gets the OrionHierarchyManager world subsystem */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy", meta = (WorldContext = "WorldContextObject"))
    static UOrionHierarchyManager* GetHierarchyManagerSubsystem(const UObject* WorldContextObject);

    /** Triggers the asynchronous building of the hierarchy tree */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy")
    void BuildTree();

    /** Returns all building nodes in the tree */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy", BlueprintPure)
    TArray<FBuildingNode> GetBuildingList() const;

    /** Returns all rooms belonging to a building */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy", BlueprintPure)
    TArray<FRoomNode> GetRoomsByBuilding(FName BuildingID) const;

    /** Returns all equipment belonging to a room */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy", BlueprintPure)
    TArray<FEquipmentNode> GetEquipmentByRoom(FName RoomID) const;

    /** Returns component FNames for an equipment node (lazy-loaded) */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy")
    TArray<FName> GetComponentsByEquipment(FName EquipmentID);

    /** Searches the entire plant hierarchy with case-insensitive and Levenshtein fuzzy matching */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy")
    TArray<FSearchResult> SearchAll(const FString& Query);

    /** Resolves the world space AActor mapped to an EquipmentID */
    UFUNCTION(BlueprintCallable, Category = "Orion|Hierarchy", BlueprintPure)
    AActor* GetEquipmentActor(FName EquipmentID) const;

    /** Fires when the tree building process is completed */
    UPROPERTY(BlueprintAssignable, Category = "Orion|Hierarchy")
    FOnTreeReady OnTreeReady;

    /** Fires when a user selects an equipment node in the tree */
    UPROPERTY(BlueprintAssignable, Category = "Orion|Hierarchy")
    FOnEquipmentSelected OnEquipmentSelected;

protected:
    // In-memory mapping from BuildingID to BuildingNode
    UPROPERTY(BlueprintReadOnly, Category = "Orion|Hierarchy")
    TMap<FName, FBuildingNode> BuildingMap;

    // Cache to store previous search query results to avoid repeat work
    TMap<FString, TArray<FSearchResult>> SearchCache;

    // Indicates if the hierarchy tree has finished building
    UPROPERTY(BlueprintReadOnly, Category = "Orion|Hierarchy")
    bool bTreeBuilt = false;

private:
    int32 CalculateLevenshteinDistance(const FString& S1, const FString& S2) const;
    void BuildTree_Internal(TArray<FBuildingTableRow> BuildingRows, TArray<FRoomTableRow> RoomRows, TArray<FEquipmentTableRow> EquipmentRows);
};
