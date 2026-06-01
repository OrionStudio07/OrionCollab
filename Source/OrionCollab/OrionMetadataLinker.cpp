// OrionMetadataLinker.cpp
#include "OrionMetadataLinker.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Engine/DataTable.h"
#include "OrionTableRows.h"
#include "GameFramework/Actor.h"
#include "Engine/StaticMeshActor.h"

DEFINE_LOG_CATEGORY_STATIC(LogOrionMetadataLinker, Log, All);

UOrionMetadataLinker::UOrionMetadataLinker()
{
}

void UOrionMetadataLinker::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Orion Metadata Linker Subsystem Initialized."));
}

void UOrionMetadataLinker::Deinitialize()
{
	Super::Deinitialize();
}

void UOrionMetadataLinker::OnWorldBeginPlay(UWorld& InWorld)
{
	Super::OnWorldBeginPlay(InWorld);
	
	// Automatically run matching on level load
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Level loaded. Triggering RunMatching() automatically..."));
	RunMatching();
}

UOrionMetadataLinker* UOrionMetadataLinker::GetMetadataLinkerSubsystem(const UObject* WorldContextObject)
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
	return World->GetSubsystem<UOrionMetadataLinker>();
}

FMatchReport UOrionMetadataLinker::RunMatching()
{
	FMatchReport Report;
	MatchedActorsMap.Empty();
	UnmatchedActors.Empty();

	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogOrionMetadataLinker, Error, TEXT("RunMatching failed: World is null."));
		CurrentReport = Report;
		return Report;
	}

	// 1. Load the DT_Equipment table
	UDataTable* EquipmentTable = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/Data/DT_Equipment")));
	if (!EquipmentTable)
	{
		UE_LOG(LogOrionMetadataLinker, Warning, TEXT("RunMatching: Could not load DT_Equipment. Make sure it exists."));
		CurrentReport = Report;
		return Report;
	}

	TArray<FEquipmentTableRow*> EquipmentRows;
	EquipmentTable->GetAllRows<FEquipmentTableRow>(TEXT("UOrionMetadataLinker::RunMatching"), EquipmentRows);
	
	if (EquipmentRows.Num() == 0)
	{
		UE_LOG(LogOrionMetadataLinker, Warning, TEXT("RunMatching: DT_Equipment has no rows."));
		CurrentReport = Report;
		return Report;
	}

	// 2. Scan all actors in the world
	TArray<AActor*> CandidateActors;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor || Actor->IsTemplate() || !IsValid(Actor))
		{
			continue;
		}

		// Filter out engine/infrastructure classes to speed up matching
		FString ClassName = Actor->GetClass()->GetName();
		if (ClassName.StartsWith(TEXT("HUD")) || 
			ClassName.StartsWith(TEXT("PlayerController")) || 
			ClassName.StartsWith(TEXT("GameMode")) || 
			ClassName.StartsWith(TEXT("CameraActor")) || 
			ClassName.StartsWith(TEXT("WorldSettings")) || 
			ClassName.StartsWith(TEXT("Light")) || 
			ClassName.StartsWith(TEXT("Brush")) ||
			ClassName.StartsWith(TEXT("Precomputed")) ||
			ClassName.StartsWith(TEXT("NavMesh")) ||
			ClassName.StartsWith(TEXT("DirectionalLight")) ||
			ClassName.StartsWith(TEXT("Sky")) ||
			ClassName.StartsWith(TEXT("Atmosphere")))
		{
			continue;
		}

		// Datasmith actors typically have a "Datasmith" tag or are StaticMeshActors
		if (Actor->ActorHasTag(TEXT("Datasmith")) || Actor->IsA(AStaticMeshActor::StaticClass()))
		{
			CandidateActors.Add(Actor);
		}
	}

	Report.TotalActors = CandidateActors.Num();
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Scanning %d candidate actors for metadata linking..."), Report.TotalActors);

	// Helper storage to check if an actor has been matched
	TSet<AActor*> MatchedActorsSet;

	// Loop over all candidate actors to find the best match in the Data Table
	for (AActor* Actor : CandidateActors)
	{
		FString CleanActorName = GetActorCleanName(Actor);
		if (CleanActorName.IsEmpty())
		{
			FMatchResult UnmatchedResult;
			UnmatchedResult.Confidence = EMatchConfidence::Unmatched;
			UnmatchedResult.ActorLabel = Actor->GetName();
#if WITH_EDITOR
			UnmatchedResult.ActorLabel = Actor->GetActorLabel();
#endif
			Report.Results.Add(UnmatchedResult);
			UnmatchedActors.Add(Actor);
			continue;
		}

		FEquipmentTableRow* BestRow = nullptr;
		EMatchConfidence BestConfidence = EMatchConfidence::Unmatched;
		int32 BestScore = 0; // exact = 3, contains = 2, fuzzy = 1

		for (FEquipmentTableRow* Row : EquipmentRows)
		{
			if (!Row) continue;

			FString EqID = Row->EquipmentID.ToString().ToLower();
			FString PID = Row->PIDTag.ToLower();

			// Exact Match
			if (CleanActorName == EqID || (!PID.IsEmpty() && CleanActorName == PID))
			{
				BestRow = Row;
				BestConfidence = EMatchConfidence::Exact;
				BestScore = 3;
				break; // Exact is the highest possible confidence, we can stop searching for this actor
			}

			// Contains Match
			if (BestScore < 2)
			{
				if (CleanActorName.Contains(EqID) || EqID.Contains(CleanActorName) ||
					(!PID.IsEmpty() && (CleanActorName.Contains(PID) || PID.Contains(CleanActorName))))
				{
					BestRow = Row;
					BestConfidence = EMatchConfidence::Contains;
					BestScore = 2;
				}
			}

			// Fuzzy Levenshtein Match (Distance <= 3)
			if (BestScore < 1)
			{
				int32 DistEq = CalculateLevenshteinDistance(CleanActorName, EqID);
				int32 DistPID = PID.IsEmpty() ? 99 : CalculateLevenshteinDistance(CleanActorName, PID);

				if (DistEq <= 3 || DistPID <= 3)
				{
					BestRow = Row;
					BestConfidence = EMatchConfidence::Fuzzy;
					BestScore = 1;
				}
			}
		}

		FMatchResult Result;
		Result.ActorLabel = Actor->GetName();
#if WITH_EDITOR
		Result.ActorLabel = Actor->GetActorLabel();
#endif

		if (BestConfidence != EMatchConfidence::Unmatched && BestRow != nullptr)
		{
			Result.EquipmentID = BestRow->EquipmentID;
			Result.MatchedActor = Actor;
			Result.Confidence = BestConfidence;

			// Add tag to the actor
			Actor->Tags.AddUnique(BestRow->EquipmentID);

			// Populate caches
			MatchedActorsMap.Add(BestRow->EquipmentID, Actor);
			MatchedActorsSet.Add(Actor);

			if (BestConfidence == EMatchConfidence::Fuzzy)
			{
				Report.Ambiguous++;
			}
			else
			{
				Report.Matched++;
			}
		}
		else
		{
			Result.Confidence = EMatchConfidence::Unmatched;
			UnmatchedActors.Add(Actor);
			Report.Unmatched++;
		}

		Report.Results.Add(Result);
	}

	if (Report.TotalActors > 0)
	{
		Report.MatchRate = (float)(Report.Matched + Report.Ambiguous) / (float)Report.TotalActors;
	}

	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Metadata matching complete. Report:"));
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Total Actors Scanned: %d"), Report.TotalActors);
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Matched: %d, Ambiguous: %d, Unmatched: %d"), Report.Matched, Report.Ambiguous, Report.Unmatched);
	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Match Rate: %.2f%%"), Report.MatchRate * 100.f);

	CurrentReport = Report;

	// Broadcast matching complete
	OnMatchingComplete.Broadcast(CurrentReport);

	return Report;
}

AActor* UOrionMetadataLinker::GetActorForEquipment(FName EquipmentID) const
{
	const TWeakObjectPtr<AActor>* FoundActorPtr = MatchedActorsMap.Find(EquipmentID);
	if (FoundActorPtr && FoundActorPtr->IsValid())
	{
		return FoundActorPtr->Get();
	}
	return nullptr;
}

TArray<AActor*> UOrionMetadataLinker::GetUnmatchedActors() const
{
	TArray<AActor*> OutArray;
	for (const TWeakObjectPtr<AActor>& ActorPtr : UnmatchedActors)
	{
		if (ActorPtr.IsValid())
		{
			OutArray.Add(ActorPtr.Get());
		}
	}
	return OutArray;
}

void UOrionMetadataLinker::ManualLink(AActor* Actor, FName EquipmentID)
{
	if (!Actor || EquipmentID.IsNone())
	{
		return;
	}

	UE_LOG(LogOrionMetadataLinker, Log, TEXT("Manually linking Actor '%s' to EquipmentID '%s'"), *Actor->GetName(), *EquipmentID.ToString());

	// 1. Remove previous matches for this Actor or EquipmentID
	MatchedActorsMap.Remove(EquipmentID);
	UnmatchedActors.Remove(Actor);

	// Remove previous equipment tags from the actor if any
	TArray<FName> TagsToRemove;
	for (const FName& Tag : Actor->Tags)
	{
		if (Tag != EquipmentID && Tag != TEXT("Datasmith"))
		{
			// Check if this tag represents another equipment ID
			TagsToRemove.Add(Tag);
		}
	}
	for (const FName& Tag : TagsToRemove)
	{
		Actor->Tags.Remove(Tag);
	}

	// 2. Setup the new match
	Actor->Tags.AddUnique(EquipmentID);
	MatchedActorsMap.Add(EquipmentID, Actor);

	// 3. Rebuild the MatchReport Results array
	bool bFound = false;
	FString CleanName = Actor->GetName();
#if WITH_EDITOR
	CleanName = Actor->GetActorLabel();
#endif

	for (FMatchResult& Result : CurrentReport.Results)
	{
		if (Result.ActorLabel == CleanName)
		{
			Result.EquipmentID = EquipmentID;
			Result.MatchedActor = Actor;
			Result.Confidence = EMatchConfidence::Exact; // Manually linked counts as Exact
			bFound = true;
			break;
		}
	}

	if (!bFound)
	{
		FMatchResult NewResult;
		NewResult.EquipmentID = EquipmentID;
		NewResult.MatchedActor = Actor;
		NewResult.Confidence = EMatchConfidence::Exact;
		NewResult.ActorLabel = CleanName;
		CurrentReport.Results.Add(NewResult);
	}

	// Recalculate totals
	int32 Total = CurrentReport.TotalActors;
	int32 Matched = 0;
	int32 Ambiguous = 0;
	int32 Unmatched = 0;

	for (const FMatchResult& Result : CurrentReport.Results)
	{
		if (Result.Confidence == EMatchConfidence::Exact || Result.Confidence == EMatchConfidence::Contains)
		{
			Matched++;
		}
		else if (Result.Confidence == EMatchConfidence::Fuzzy)
		{
			Ambiguous++;
		}
		else
		{
			Unmatched++;
		}
	}

	CurrentReport.Matched = Matched;
	CurrentReport.Ambiguous = Ambiguous;
	CurrentReport.Unmatched = Unmatched;
	if (Total > 0)
	{
		CurrentReport.MatchRate = (float)(Matched + Ambiguous) / (float)Total;
	}

	// Broadcast matching complete with updated report
	OnMatchingComplete.Broadcast(CurrentReport);
}

FString UOrionMetadataLinker::GetActorCleanName(AActor* Actor) const
{
	if (!Actor) return FString();

	FString Name = Actor->GetName();
#if WITH_EDITOR
	Name = Actor->GetActorLabel();
#endif

	// Convert to lowercase
	Name = Name.ToLower();

	// Strip common prefixes
	if (Name.StartsWith(TEXT("sm_")))
	{
		Name.RightChopInline(3);
	}
	else if (Name.StartsWith(TEXT("bp_")))
	{
		Name.RightChopInline(3);
	}
	else if (Name.StartsWith(TEXT("staticmeshactor_")))
	{
		Name.RightChopInline(16);
	}

	// Strip common Datasmith/Unreal suffixes like _uaid_... or numeric suffix
	// For example, if there is a suffix _1, _01, etc.
	int32 SuffixIndex;
	if (Name.FindLastChar(TEXT('_'), SuffixIndex))
	{
		FString Suffix = Name.RightChop(SuffixIndex + 1);
		if (Suffix.IsNumeric() || Suffix.StartsWith(TEXT("uaid")))
		{
			Name = Name.Left(SuffixIndex);
		}
	}

	return Name.TrimStartAndEnd();
}

int32 UOrionMetadataLinker::CalculateLevenshteinDistance(const FString& S1, const FString& S2) const
{
	int32 Len1 = S1.Len();
	int32 Len2 = S2.Len();

	if (Len1 == 0) return Len2;
	if (Len2 == 0) return Len1;

	TArray<TArray<int32>> DP;
	DP.SetNum(Len1 + 1);
	for (int32 i = 0; i <= Len1; ++i)
	{
		DP[i].SetNum(Len2 + 1);
		DP[i][0] = i;
	}
	for (int32 j = 0; j <= Len2; ++j)
	{
		DP[0][j] = j;
	}

	for (int32 i = 1; i <= Len1; ++i)
	{
		for (int32 j = 1; j <= Len2; ++j)
		{
			if (S1[i - 1] == S2[j - 1])
			{
				DP[i][j] = DP[i - 1][j - 1];
			}
			else
			{
				DP[i][j] = 1 + FMath::Min3(
					DP[i - 1][j],     // Deletion
					DP[i][j - 1],     // Insertion
					DP[i - 1][j - 1]  // Substitution
				);
			}
		}
	}

	return DP[Len1][Len2];
}
