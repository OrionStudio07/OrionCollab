using UnrealBuildTool;

public class OrionCollab : ModuleRules
{
	public OrionCollab(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
		PublicDependencyModuleNames.AddRange(new string[] { 
			"Core", 
			"CoreUObject", 
			"Engine", 
			"InputCore", 
			"Slate", 
			"SlateCore", 
			"UMG",
			"Json",
			"JsonUtilities",
			"DirectoryWatcher"
		});

		PrivateDependencyModuleNames.AddRange(new string[] {  });
	}
}
