#pragma once

#include "CoreMinimal.h"
#include "OrionTypes.generated.h"

// ──────────────────────────────────────────────
// Mode System
// ──────────────────────────────────────────────

UENUM(BlueprintType)
enum class EOrionMode : uint8
{
    MODE_LAUNCHER    = 0  UMETA(DisplayName = "Launcher"),
    MODE_SHOWCASE    = 1  UMETA(DisplayName = "Showcase"),
    MODE_OPERATIONS  = 2  UMETA(DisplayName = "Operations"),
    MODE_TRAINING    = 3  UMETA(DisplayName = "Training (v2)")
};

UENUM(BlueprintType)
enum class EOrionRole : uint8
{
    ROLE_VIEWER   = 0  UMETA(DisplayName = "Viewer"),
    ROLE_ENGINEER = 1  UMETA(DisplayName = "Engineer"),
    ROLE_ADMIN    = 2  UMETA(DisplayName = "Admin")
};

// ──────────────────────────────────────────────
// Equipment & Zone Classification
// ──────────────────────────────────────────────

UENUM(BlueprintType)
enum class EEquipmentType : uint8
{
    Pump          UMETA(DisplayName = "Pump"),
    Vessel        UMETA(DisplayName = "Vessel"),
    Conveyor      UMETA(DisplayName = "Conveyor"),
    Mixer         UMETA(DisplayName = "Mixer"),
    Valve         UMETA(DisplayName = "Valve"),
    Instrument    UMETA(DisplayName = "Instrument"),
    HeatExchanger UMETA(DisplayName = "Heat Exchanger"),
    Tank          UMETA(DisplayName = "Tank"),
    Motor         UMETA(DisplayName = "Motor"),
    Compressor    UMETA(DisplayName = "Compressor"),
    Filter        UMETA(DisplayName = "Filter"),
    Pipe          UMETA(DisplayName = "Pipe"),
    Structure     UMETA(DisplayName = "Structure"),
    Electrical    UMETA(DisplayName = "Electrical"),
    Other         UMETA(DisplayName = "Other")
};

UENUM(BlueprintType)
enum class EZoneClassification : uint8
{
    General    UMETA(DisplayName = "General"),
    Clean      UMETA(DisplayName = "Clean Room"),
    Chemical   UMETA(DisplayName = "Chemical"),
    Electrical UMETA(DisplayName = "Electrical"),
    Confined   UMETA(DisplayName = "Confined Space"),
    Hazardous  UMETA(DisplayName = "Hazardous")
};

UENUM(BlueprintType)
enum class ENPCType : uint8
{
    AmbientWorker  UMETA(DisplayName = "Ambient Worker"),
    TourGuide      UMETA(DisplayName = "Tour Guide"),
    SecurityGuard  UMETA(DisplayName = "Security Guard")
};

UENUM(BlueprintType)
enum class EMaintenanceStatus : uint8
{
    OK       UMETA(DisplayName = "OK"),
    Due      UMETA(DisplayName = "Due"),
    Overdue  UMETA(DisplayName = "Overdue"),
    Unknown  UMETA(DisplayName = "Unknown")
};

UENUM(BlueprintType)
enum class EMatchConfidence : uint8
{
    Exact     UMETA(DisplayName = "Exact Match"),
    Contains  UMETA(DisplayName = "Contains Match"),
    Fuzzy     UMETA(DisplayName = "Fuzzy Match"),
    Unmatched UMETA(DisplayName = "Unmatched")
};

UENUM(BlueprintType)
enum class ESectionFillMode : uint8
{
    Solid         UMETA(DisplayName = "Solid Fill"),
    Hatching45    UMETA(DisplayName = "45° Hatching"),
    CrossHatching UMETA(DisplayName = "Cross Hatching"),
    ColorByType   UMETA(DisplayName = "Color by Equipment Type")
};

UENUM(BlueprintType)
enum class EMeasurementUnit : uint8
{
    Meters      UMETA(DisplayName = "Meters"),
    Feet        UMETA(DisplayName = "Feet"),
    Millimeters UMETA(DisplayName = "Millimeters")
};

UENUM(BlueprintType)
enum class ESnapType : uint8
{
    None         UMETA(DisplayName = "None"),
    Vertex       UMETA(DisplayName = "Vertex"),
    Edge         UMETA(DisplayName = "Edge"),
    Midpoint     UMETA(DisplayName = "Midpoint"),
    Center       UMETA(DisplayName = "Center"),
    Face         UMETA(DisplayName = "Face"),
    Intersection UMETA(DisplayName = "Intersection")
};

UENUM(BlueprintType)
enum class EAnnotationCategory : uint8
{
    General        UMETA(DisplayName = "General"),
    Safety         UMETA(DisplayName = "Safety"),
    Maintenance    UMETA(DisplayName = "Maintenance"),
    DesignReview   UMETA(DisplayName = "Design Review")
};

class AActor;

USTRUCT(BlueprintType)
struct FMatchResult
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	FName EquipmentID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	TWeakObjectPtr<AActor> MatchedActor;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	EMatchConfidence Confidence = EMatchConfidence::Unmatched;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	FString ActorLabel;
};

USTRUCT(BlueprintType)
struct FMatchReport
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	int32 TotalActors = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	int32 Matched = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	int32 Ambiguous = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	int32 Unmatched = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	float MatchRate = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Orion|Matching")
	TArray<FMatchResult> Results;
};

