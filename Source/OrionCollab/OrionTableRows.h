#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "OrionTypes.h"
#include "OrionTableRows.generated.h"

// ──────────────────────────────────────────────
// 2.1 FEquipmentTableRow — Master Equipment Table
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FEquipmentTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Identity")
	FName EquipmentID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Identity")
	FText DisplayName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Identity")
	FString PIDTag;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Identity")
	EEquipmentType EquipmentType = EEquipmentType::Other;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hierarchy")
	FString ProcessLine;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hierarchy")
	FName BuildingID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hierarchy")
	FName RoomID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hierarchy")
	FName ZoneID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specs")
	FString Manufacturer;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specs")
	FString Model;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specs")
	FString SpecsJSON;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Content")
	TArray<FString> DrawingPaths;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Content")
	TSoftClassPtr<AActor> AnimationClass;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
	bool bHasExplode = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Features")
	TArray<FName> MaintenanceComponents;
};

// ──────────────────────────────────────────────
// 2.2 FBuildingTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FBuildingTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building")
	FName BuildingID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building")
	FText DisplayName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building")
	int32 Floors = 1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building")
	FVector LocationOrigin = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building")
	FVector LocationExtent = FVector(1000.f);
};

// ──────────────────────────────────────────────
// 2.3 FRoomTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FRoomTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	FName RoomID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	FName BuildingID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	FText DisplayName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	int32 Floor = 1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	FString Function;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	EZoneClassification SafetyZoneType = EZoneClassification::General;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Room")
	FLinearColor SafetyZoneColor = FLinearColor(0.5f, 0.5f, 0.5f, 0.3f);
};

// ──────────────────────────────────────────────
// 2.4 FProcessLineTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FProcessLineTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ProcessLine")
	FString ProcessLineID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ProcessLine")
	FText DisplayName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ProcessLine")
	TArray<FName> ConnectedEquipment;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ProcessLine")
	FString PIDDocPath;
};

// ──────────────────────────────────────────────
// 2.5 FZoneTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FZoneTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Zone")
	FName ZoneID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Zone")
	FVector BoundsOrigin = FVector::ZeroVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Zone")
	FVector BoundsExtent = FVector(500.f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Zone")
	TArray<FName> ActiveEquipment;
};

// ──────────────────────────────────────────────
// 2.6 FTourWaypointTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FTourWaypointTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	FName WaypointID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	FString TourName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	int32 Sequence = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	FTransform CameraTransform;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	FText InfoText;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tour")
	FSoftObjectPath VOPath;
};

// ──────────────────────────────────────────────
// 2.7 FNPCTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FNPCTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
	FName NPCID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
	ENPCType NPCType = ENPCType::AmbientWorker;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
	FName ZoneID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
	FName AnimationSet;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
	FSoftObjectPath PatrolPath;
};

// ──────────────────────────────────────────────
// 2.8 FInspectionStepTableRow
// ──────────────────────────────────────────────

USTRUCT(BlueprintType)
struct FInspectionStepTableRow : public FTableRowBase
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FName StepID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FName EquipmentID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	int32 Sequence = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FText Description;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FText ExpectedCondition;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FTransform CameraTransform;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inspection")
	FString PhotoRefPath;
};
