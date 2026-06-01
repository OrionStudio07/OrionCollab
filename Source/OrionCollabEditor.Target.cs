using UnrealBuildTool;
using System.Collections.Generic;

public class OrionCollabEditorTarget : TargetRules
{
	public OrionCollabEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("OrionCollab");
	}
}
