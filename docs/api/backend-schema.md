# Backend Schema Reference

> Complete Data Table schemas, struct definitions, and enum values. See the full specification in [backend_schema.md](../../GoverningDocuments/backend_schema.md).

---

## Data Tables Overview

| Data Table | Row Struct | Purpose | Estimated Rows |
|-----------|------------|---------|---------------|
| `DT_Equipment` | `FOrionEquipmentRow` | Equipment specs, P&ID tags, process lines | ~200 |
| `DT_Buildings` | `FOrionBuildingRow` | Building definitions and metadata | ~5 |
| `DT_Rooms` | `FOrionRoomRow` | Room classifications, safety zones, floor assignments | ~30 |
| `DT_ProcessLines` | `FOrionProcessLineRow` | Process line routing and flow data | ~500 |
| `DT_Zones` | `FOrionZoneRow` | Trigger volume zones for animations/NPC activation | ~20 |
| `DT_NPCs` | `FOrionNPCRow` | NPC worker definitions and zone assignments | ~15 |
| `DT_TourWaypoints` | `FOrionTourWaypointRow` | Guided tour camera positions and info panels | ~20 |
| `DT_InspectionSteps` | `FOrionInspectionStepRow` | Per-equipment inspection checklist items | ~100 |

---

## Key Enums

### EOrionMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | `MODE_LAUNCHER` | Role selection and settings |
| 1 | `MODE_SHOWCASE` | Investor/visitor presentation mode |
| 2 | `MODE_OPERATIONS` | Engineering/maintenance mode |
| 3 | `MODE_TRAINING` | Reserved for v2 |

### EOrionRole
| Value | Name | Accessible Modes |
|-------|------|-----------------|
| 0 | `ROLE_VIEWER` | Showcase only |
| 1 | `ROLE_ENGINEER` | Showcase + Operations |
| 2 | `ROLE_ADMIN` | All modes |

### EEquipmentType
| Value | Name | Icon |
|-------|------|------|
| 0 | `Pump` | 🔄 |
| 1 | `Vessel` | 🏗️ |
| 2 | `HeatExchanger` | 🌡️ |
| 3 | `Mixer` | ⚙️ |
| 4 | `Conveyor` | ➡️ |
| 5 | `Valve` | 🔧 |
| 6 | `Instrument` | 📊 |
| 7 | `Pipe` | 🔵 |
| 8 | `Structure` | 🏛️ |
| 9 | `Electrical` | ⚡ |

### EZoneClassification
| Value | Name | Safety Level |
|-------|------|-------------|
| 0 | `Clean` | Standard |
| 1 | `Chemical` | PPE Required |
| 2 | `Electrical` | Restricted |
| 3 | `Confined` | Permit Required |

---

## Core Struct: FOrionEquipmentRow

```cpp
USTRUCT(BlueprintType)
struct FOrionEquipmentRow : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY() FName EquipmentID;
    UPROPERTY() FText DisplayName;
    UPROPERTY() FString PIDTag;
    UPROPERTY() FString ProcessLine;
    UPROPERTY() EEquipmentType Type;
    UPROPERTY() FName BuildingID;
    UPROPERTY() FName RoomID;
    UPROPERTY() FString Manufacturer;
    UPROPERTY() FString Model;
    UPROPERTY() FString Material;
    UPROPERTY() float FlowRate;
    UPROPERTY() float Temperature;
    UPROPERTY() float Pressure;
    UPROPERTY() FString MaintenanceInterval;
    UPROPERTY() FString LastMaintenanceDate;
    UPROPERTY() TArray<FName> ComponentIDs;
};
```
