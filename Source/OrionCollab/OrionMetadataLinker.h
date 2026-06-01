// OrionMetadataLinker.h
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "OrionTypes.h"
#include "OrionMetadataLinker.generated.h"

class AActor;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMatchingComplete, const FMatchReport&, Report);

/**
 * UOrionMetadataLinker
 * World subsystem that auto-matches Datasmith-imported actors to Data Table rows.
 */
UCLASS(BlueprintType, Blueprintable)
class ORIONCOLLAB_API UOrionMetadataLinker : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	UOrionMetadataLinker();

	// Begin USubsystem Interface
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
	virtual void OnWorldBeginPlay(UWorld& InWorld) override;
	// End USubsystem Interface

	UFUNCTION(BlueprintCallable, Category = "Orion|Matching", meta = (WorldContext = "WorldContextObject"))
	static UOrionMetadataLinker* GetMetadataLinkerSubsystem(const UObject* WorldContextObject);

	/** Auto-match Datasmith-imported actors to Data Table rows */
	UFUNCTION(BlueprintCallable, Category = "Orion|Matching")
	FMatchReport RunMatching();

	/** Gets the actor matched to a specific EquipmentID */
	UFUNCTION(BlueprintCallable, Category = "Orion|Matching", BlueprintPure)
	AActor* GetActorForEquipment(FName EquipmentID) const;

	/** Gets all actors that could not be matched */
	UFUNCTION(BlueprintCallable, Category = "Orion|Matching", BlueprintPure)
	TArray<AActor*> GetUnmatchedActors() const;

	/** Manually link an actor to an EquipmentID */
	UFUNCTION(BlueprintCallable, Category = "Orion|Matching")
	void ManualLink(AActor* Actor, FName EquipmentID);

	/** Delegate fired when matching completes */
	UPROPERTY(BlueprintAssignable, Category = "Orion|Matching")
	FOnMatchingComplete OnMatchingComplete;

protected:
	UPROPERTY(BlueprintReadOnly, Category = "Orion|Matching")
	FMatchReport CurrentReport;

	// In-memory mapping from EquipmentID to actor
	UPROPERTY()
	TMap<FName, TWeakObjectPtr<AActor>> MatchedActorsMap;

	// In-memory array of unmatched actors
	UPROPERTY()
	TArray<TWeakObjectPtr<AActor>> UnmatchedActors;

private:
	FString GetActorCleanName(AActor* Actor) const;
	int32 CalculateLevenshteinDistance(const FString& S1, const FString& S2) const;
};
