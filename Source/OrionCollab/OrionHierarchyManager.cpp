// OrionHierarchyManager.cpp
#include "OrionHierarchyManager.h"
#include "Engine/World.h"
#include "Engine/DataTable.h"
#include "OrionTableRows.h"
#include "OrionMetadataLinker.h"
#include "Async/Async.h"
#include "Misc/App.h"
#include "Misc/CommandLine.h"

DEFINE_LOG_CATEGORY_STATIC(LogOrionHierarchyManager, Log, All);

UOrionHierarchyManager::UOrionHierarchyManager()
    : bTreeBuilt(false)
{
}

void UOrionHierarchyManager::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogOrionHierarchyManager, Log, TEXT("Orion Hierarchy Manager Subsystem Initialized."));
}

void UOrionHierarchyManager::Deinitialize()
{
    Super::Deinitialize();
}

void UOrionHierarchyManager::OnWorldBeginPlay(UWorld& InWorld)
{
    Super::OnWorldBeginPlay(InWorld);
    
    // Automatically trigger hierarchy tree building on world begin play
    BuildTree();
}

UOrionHierarchyManager* UOrionHierarchyManager::GetHierarchyManagerSubsystem(const UObject* WorldContextObject)
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
    return World->GetSubsystem<UOrionHierarchyManager>();
}

void UOrionHierarchyManager::BuildTree()
{
    bTreeBuilt = false;
    BuildingMap.Empty();
    SearchCache.Empty();

    UWorld* World = GetWorld();
    if (!World)
    {
        UE_LOG(LogOrionHierarchyManager, Error, TEXT("BuildTree failed: World is null."));
        return;
    }

    // Load Data Tables on the Game Thread
    UDataTable* BuildingTable = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/Data/DT_Buildings")));
    UDataTable* RoomTable = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/Data/DT_Rooms")));
    UDataTable* EquipmentTable = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/Data/DT_Equipment")));

    if (!BuildingTable || !RoomTable || !EquipmentTable)
    {
        UE_LOG(LogOrionHierarchyManager, Error, TEXT("BuildTree: Failed to load DTs (DT_Buildings, DT_Rooms, or DT_Equipment). Make sure they are imported!"));
        return;
    }

    TArray<FBuildingTableRow*> BuildingRows;
    TArray<FRoomTableRow*> RoomRows;
    TArray<FEquipmentTableRow*> EquipmentRows;

    BuildingTable->GetAllRows<FBuildingTableRow>(TEXT("UOrionHierarchyManager::BuildTree"), BuildingRows);
    RoomTable->GetAllRows<FRoomTableRow>(TEXT("UOrionHierarchyManager::BuildTree"), RoomRows);
    EquipmentTable->GetAllRows<FEquipmentTableRow>(TEXT("UOrionHierarchyManager::BuildTree"), EquipmentRows);

    // Copy rows into standard arrays on the Game Thread so they are safe to parse inside the background thread task
    TArray<FBuildingTableRow> SafeBuildingRows;
    TArray<FRoomTableRow> SafeRoomRows;
    TArray<FEquipmentTableRow> SafeEquipmentRows;

    for (FBuildingTableRow* Row : BuildingRows)
    {
        if (Row) SafeBuildingRows.Add(*Row);
    }
    for (FRoomTableRow* Row : RoomRows)
    {
        if (Row) SafeRoomRows.Add(*Row);
    }
    for (FEquipmentTableRow* Row : EquipmentRows)
    {
        if (Row) SafeEquipmentRows.Add(*Row);
    }

    if (IsRunningCommandlet() || FApp::IsUnattended() || FString(FCommandLine::Get()).Contains(TEXT("-ExecutePythonScript")))
    {
        UE_LOG(LogOrionHierarchyManager, Log, TEXT("Hierarchy Manager: Running tree construction synchronously (Commandlet/Script mode)..."));
        BuildTree_Internal(MoveTemp(SafeBuildingRows), MoveTemp(SafeRoomRows), MoveTemp(SafeEquipmentRows));
        OnTreeReady.Broadcast();
    }
    else
    {
        UE_LOG(LogOrionHierarchyManager, Log, TEXT("Hierarchy Manager: Offloading tree construction for %d buildings, %d rooms, %d equipment to background thread..."),
            SafeBuildingRows.Num(), SafeRoomRows.Num(), SafeEquipmentRows.Num());

        // Execute tree construction asynchronously in a background task
        AsyncTask(ENamedThreads::AnyBackgroundThreadNormalTask, [this, SafeBuildingRows = MoveTemp(SafeBuildingRows), SafeRoomRows = MoveTemp(SafeRoomRows), SafeEquipmentRows = MoveTemp(SafeEquipmentRows)]() mutable
        {
            TMap<FName, FBuildingNode> TempBuildingMap;

            // 1. Initialize Buildings
            for (const FBuildingTableRow& Row : SafeBuildingRows)
            {
                FBuildingNode Node;
                Node.BuildingID = Row.BuildingID;
                Node.DisplayName = Row.DisplayName;
                Node.Floors = Row.Floors;
                TempBuildingMap.Add(Row.BuildingID, Node);
            }

            // 2. Associate Rooms with their parent Buildings
            for (const FRoomTableRow& Row : SafeRoomRows)
            {
                FRoomNode Node;
                Node.RoomID = Row.RoomID;
                Node.DisplayName = Row.DisplayName;
                Node.SafetyZone = Row.SafetyZoneType;
                Node.Floor = Row.Floor;
                Node.EquipmentCount = 0;

                FBuildingNode* ParentBuilding = TempBuildingMap.Find(Row.BuildingID);
                if (ParentBuilding)
                {
                    ParentBuilding->Rooms.Add(Node);
                }
                else
                {
                    UE_LOG(LogOrionHierarchyManager, Warning, TEXT("BuildTree Background Task: Room '%s' references non-existent Building '%s'"),
                        *Row.RoomID.ToString(), *Row.BuildingID.ToString());
                }
            }

            // 3. Associate Equipment nodes with their parent Rooms
            for (const FEquipmentTableRow& Row : SafeEquipmentRows)
            {
                FEquipmentNode Node;
                Node.EquipmentID = Row.EquipmentID;
                Node.DisplayName = Row.DisplayName;
                Node.PIDTag = Row.PIDTag;
                Node.ProcessLine = Row.ProcessLine;
                Node.Type = Row.EquipmentType;
                Node.WorldActor = nullptr; // Resolved on game thread via MetadataLinker
                Node.bComponentsLoaded = false;

                FBuildingNode* ParentBuilding = TempBuildingMap.Find(Row.BuildingID);
                if (ParentBuilding)
                {
                    bool bRoomFound = false;
                    for (FRoomNode& Room : ParentBuilding->Rooms)
                    {
                        if (Room.RoomID == Row.RoomID)
                        {
                            Room.Equipment.Add(Node);
                            Room.EquipmentCount++;
                            bRoomFound = true;
                            break;
                        }
                    }
                    if (!bRoomFound)
                    {
                        UE_LOG(LogOrionHierarchyManager, Warning, TEXT("BuildTree Background Task: Equipment '%s' references non-existent Room '%s' in Building '%s'"),
                            *Row.EquipmentID.ToString(), *Row.RoomID.ToString(), *Row.BuildingID.ToString());
                    }
                }
                else
                {
                    UE_LOG(LogOrionHierarchyManager, Warning, TEXT("BuildTree Background Task: Equipment '%s' references non-existent Building '%s'"),
                        *Row.EquipmentID.ToString(), *Row.BuildingID.ToString());
                }
            }

            // 4. Dispatch back to Game Thread for finalization
            AsyncTask(ENamedThreads::GameThread, [this, TempBuildingMap = MoveTemp(TempBuildingMap), search_count = SafeEquipmentRows.Num()]() mutable
            {
                BuildingMap = MoveTemp(TempBuildingMap);

                // Resolve WorldActor weak pointers using MetadataLinker subsystem on the Game Thread
                UOrionMetadataLinker* Linker = UOrionMetadataLinker::GetMetadataLinkerSubsystem(GetWorld());
                if (Linker)
                {
                    for (auto& BuildingElem : BuildingMap)
                    {
                        for (FRoomNode& Room : BuildingElem.Value.Rooms)
                        {
                            for (FEquipmentNode& Eq : Room.Equipment)
                            {
                                Eq.WorldActor = Linker->GetActorForEquipment(Eq.EquipmentID);
                            }
                        }
                    }
                }

                bTreeBuilt = true;
                UE_LOG(LogOrionHierarchyManager, Log, TEXT("Hierarchy Manager: Tree successfully built. %d Buildings, %d search entries indexed."), BuildingMap.Num(), search_count);
                OnTreeReady.Broadcast();
            });
        });
    }
}

void UOrionHierarchyManager::BuildTree_Internal(TArray<FBuildingTableRow> SafeBuildingRows, TArray<FRoomTableRow> SafeRoomRows, TArray<FEquipmentTableRow> SafeEquipmentRows)
{
    // 1. Initialize Buildings
    for (const FBuildingTableRow& Row : SafeBuildingRows)
    {
        FBuildingNode Node;
        Node.BuildingID = Row.BuildingID;
        Node.DisplayName = Row.DisplayName;
        Node.Floors = Row.Floors;
        BuildingMap.Add(Row.BuildingID, Node);
    }

    // 2. Associate Rooms
    for (const FRoomTableRow& Row : SafeRoomRows)
    {
        FRoomNode Node;
        Node.RoomID = Row.RoomID;
        Node.DisplayName = Row.DisplayName;
        Node.SafetyZone = Row.SafetyZoneType;
        Node.Floor = Row.Floor;
        Node.EquipmentCount = 0;

        FBuildingNode* ParentBuilding = BuildingMap.Find(Row.BuildingID);
        if (ParentBuilding)
        {
            ParentBuilding->Rooms.Add(Node);
        }
    }

    // 3. Associate Equipment
    for (const FEquipmentTableRow& Row : SafeEquipmentRows)
    {
        FEquipmentNode Node;
        Node.EquipmentID = Row.EquipmentID;
        Node.DisplayName = Row.DisplayName;
        Node.PIDTag = Row.PIDTag;
        Node.ProcessLine = Row.ProcessLine;
        Node.Type = Row.EquipmentType;
        Node.WorldActor = nullptr;
        Node.bComponentsLoaded = false;

        FBuildingNode* ParentBuilding = BuildingMap.Find(Row.BuildingID);
        if (ParentBuilding)
        {
            for (FRoomNode& Room : ParentBuilding->Rooms)
            {
                if (Room.RoomID == Row.RoomID)
                {
                    Room.Equipment.Add(Node);
                    Room.EquipmentCount++;
                    break;
                }
            }
        }
    }

    // Resolve WorldActor weak pointers using MetadataLinker subsystem on the Game Thread
    UOrionMetadataLinker* Linker = UOrionMetadataLinker::GetMetadataLinkerSubsystem(GetWorld());
    if (Linker)
    {
        for (auto& BuildingElem : BuildingMap)
        {
            for (FRoomNode& Room : BuildingElem.Value.Rooms)
            {
                for (FEquipmentNode& Eq : Room.Equipment)
                {
                    Eq.WorldActor = Linker->GetActorForEquipment(Eq.EquipmentID);
                }
            }
        }
    }

    bTreeBuilt = true;
    UE_LOG(LogOrionHierarchyManager, Log, TEXT("Hierarchy Manager: Tree successfully built. %d Buildings, %d search entries indexed."), BuildingMap.Num(), SafeEquipmentRows.Num());
}

TArray<FBuildingNode> UOrionHierarchyManager::GetBuildingList() const
{
    TArray<FBuildingNode> OutBuildings;
    BuildingMap.GenerateValueArray(OutBuildings);
    return OutBuildings;
}

TArray<FRoomNode> UOrionHierarchyManager::GetRoomsByBuilding(FName BuildingID) const
{
    const FBuildingNode* FoundBuilding = BuildingMap.Find(BuildingID);
    if (FoundBuilding)
    {
        return FoundBuilding->Rooms;
    }
    return TArray<FRoomNode>();
}

TArray<FEquipmentNode> UOrionHierarchyManager::GetEquipmentByRoom(FName RoomID) const
{
    for (const auto& Elem : BuildingMap)
    {
        for (const FRoomNode& Room : Elem.Value.Rooms)
        {
            if (Room.RoomID == RoomID)
            {
                return Room.Equipment;
            }
        }
    }
    return TArray<FEquipmentNode>();
}

TArray<FName> UOrionHierarchyManager::GetComponentsByEquipment(FName EquipmentID)
{
    for (auto& Elem : BuildingMap)
    {
        for (FRoomNode& Room : Elem.Value.Rooms)
        {
            for (FEquipmentNode& Eq : Room.Equipment)
            {
                if (Eq.EquipmentID == EquipmentID)
                {
                    // Lazy-load component list on expand/request
                    if (!Eq.bComponentsLoaded)
                    {
                        UDataTable* EquipmentTable = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), nullptr, TEXT("/Game/CollaborativeViewer/Data/DT_Equipment")));
                        if (EquipmentTable)
                        {
                            FEquipmentTableRow* Row = EquipmentTable->FindRow<FEquipmentTableRow>(EquipmentID, TEXT("UOrionHierarchyManager::GetComponentsByEquipment"));
                            if (Row)
                            {
                                Eq.ComponentIDs = Row->MaintenanceComponents;
                            }
                        }
                        Eq.bComponentsLoaded = true;
                    }
                    return Eq.ComponentIDs;
                }
            }
        }
    }
    return TArray<FName>();
}

TArray<FSearchResult> UOrionHierarchyManager::SearchAll(const FString& Query)
{
    FString CleanQuery = Query.TrimStartAndEnd();
    if (CleanQuery.IsEmpty())
    {
        return TArray<FSearchResult>();
    }

    // 1. Check in-memory cache for repeat queries to bypass calculation
    const TArray<FSearchResult>* Cached = SearchCache.Find(CleanQuery);
    if (Cached)
    {
        UE_LOG(LogOrionHierarchyManager, Log, TEXT("SearchAll: Cache hit for query '%s' (%d results found)."), *CleanQuery, Cached->Num());
        return *Cached;
    }

    TArray<FSearchResult> Results;
    FString LowerQuery = CleanQuery.ToLower();

    UE_LOG(LogOrionHierarchyManager, Log, TEXT("SearchAll starting for query '%s'. BuildingMap size: %d"), *LowerQuery, BuildingMap.Num());

    // 2. Iterate through all nodes to build matches
    for (const auto& BuildingElem : BuildingMap)
    {
        const FBuildingNode& Building = BuildingElem.Value;
        FString BName = Building.DisplayName.ToString().ToLower();

        // Match Building DisplayName
        if (BName.Contains(LowerQuery))
        {
            FSearchResult Res;
            Res.ID = Building.BuildingID;
            Res.DisplayName = Building.DisplayName;
            Res.Category = TEXT("Building");
            Res.Relevance = BName == LowerQuery ? 1.f : 0.8f;
            Results.Add(Res);
        }

        for (const FRoomNode& Room : Building.Rooms)
        {
            FString RName = Room.DisplayName.ToString().ToLower();

            // Match Room DisplayName
            if (RName.Contains(LowerQuery))
            {
                FSearchResult Res;
                Res.ID = Room.RoomID;
                Res.DisplayName = Room.DisplayName;
                Res.Category = TEXT("Room");
                Res.Relevance = RName == LowerQuery ? 1.f : 0.8f;
                Results.Add(Res);
            }

            UE_LOG(LogOrionHierarchyManager, Log, TEXT("Checking Room '%s'. Equipment count: %d"), *Room.RoomID.ToString(), Room.Equipment.Num());

            for (const FEquipmentNode& Eq : Room.Equipment)
            {
                FString EqName = Eq.DisplayName.ToString().ToLower();
                FString EqTag = Eq.PIDTag.ToLower();
                FString EqLine = Eq.ProcessLine.ToLower();

                bool bMatched = false;
                float RelScore = 0.f;

                UE_LOG(LogOrionHierarchyManager, Log, TEXT("Checking Equipment ID '%s', DisplayName '%s', Tag '%s'"), *Eq.EquipmentID.ToString(), *EqName, *EqTag);

                // Case-insensitive Substring Matching (Fast Path)
                if (EqName == LowerQuery || EqTag == LowerQuery || EqLine == LowerQuery)
                {
                    bMatched = true;
                    RelScore = 1.0f;
                }
                else if (EqName.Contains(LowerQuery) || EqTag.Contains(LowerQuery) || EqLine.Contains(LowerQuery))
                {
                    bMatched = true;
                    RelScore = 0.8f;
                }

                // Fuzzy Levenshtein Distance Matching (Fuzzy Path, Distance <= 3)
                if (!bMatched)
                {
                    int32 MinDist = 99;

                    // 1. Check full strings
                    MinDist = FMath::Min(MinDist, CalculateLevenshteinDistance(LowerQuery, EqName));
                    if (!EqTag.IsEmpty())
                    {
                        MinDist = FMath::Min(MinDist, CalculateLevenshteinDistance(LowerQuery, EqTag));
                    }
                    MinDist = FMath::Min(MinDist, CalculateLevenshteinDistance(LowerQuery, Eq.EquipmentID.ToString().ToLower()));

                    // 2. Check individual tokenized words (to match "mixr" -> "mixer" inside "Ribbon Mixer #1" or "Mixer_01")
                    TArray<FString> Tokens;
                    {
                        TArray<FString> Temp;
                        EqName.ParseIntoArray(Temp, TEXT(" "));
                        Tokens.Append(Temp);
                    }
                    if (!EqTag.IsEmpty())
                    {
                        TArray<FString> Temp;
                        EqTag.ParseIntoArray(Temp, TEXT("_"));
                        Tokens.Append(Temp);
                        
                        Temp.Empty();
                        EqTag.ParseIntoArray(Temp, TEXT("-"));
                        Tokens.Append(Temp);
                    }
                    {
                        TArray<FString> Temp;
                        Eq.EquipmentID.ToString().ToLower().ParseIntoArray(Temp, TEXT("_"));
                        Tokens.Append(Temp);
                        
                        Temp.Empty();
                        Eq.EquipmentID.ToString().ToLower().ParseIntoArray(Temp, TEXT("-"));
                        Tokens.Append(Temp);
                    }

                    for (const FString& Token : Tokens)
                    {
                        if (!Token.IsEmpty())
                        {
                            int32 TokenDist = CalculateLevenshteinDistance(LowerQuery, Token);
                            UE_LOG(LogOrionHierarchyManager, Log, TEXT("  Token: '%s', Dist to '%s': %d"), *Token, *LowerQuery, TokenDist);
                            MinDist = FMath::Min(MinDist, TokenDist);
                        }
                    }

                    UE_LOG(LogOrionHierarchyManager, Log, TEXT("  MinDist calculated: %d"), MinDist);

                    if (MinDist <= 3)
                    {
                        bMatched = true;
                        RelScore = 0.5f;
                    }
                }

                if (bMatched)
                {
                    FSearchResult Res;
                    Res.ID = Eq.EquipmentID;
                    Res.DisplayName = Eq.DisplayName;
                    Res.Category = TEXT("Equipment");
                    Res.Relevance = RelScore;
                    Res.EquipmentType = Eq.Type;
                    Results.Add(Res);
                }
            }
        }
    }

    // 3. Sort results by relevance descending
    Results.Sort([](const FSearchResult& A, const FSearchResult& B)
    {
        return A.Relevance > B.Relevance;
    });

    // 4. Populate Cache
    SearchCache.Add(CleanQuery, Results);

    return Results;
}

AActor* UOrionHierarchyManager::GetEquipmentActor(FName EquipmentID) const
{
    UOrionMetadataLinker* Linker = UOrionMetadataLinker::GetMetadataLinkerSubsystem(GetWorld());
    if (Linker)
    {
        return Linker->GetActorForEquipment(EquipmentID);
    }
    return nullptr;
}

int32 UOrionHierarchyManager::CalculateLevenshteinDistance(const FString& S1, const FString& S2) const
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
