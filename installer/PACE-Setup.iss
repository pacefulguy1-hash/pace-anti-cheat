#define MyAppName "PACE Anti-Cheat"
#define MyAppVersion "0.2.0-beta"
#define MyAppPublisher "PACE Project"
#define MyAppExeName "PACE.exe"

[Setup]
AppId={{DDB61A2E-0C75-4BEA-8F47-5FEF9FC8B8E2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\PACE
DefaultGroupName=PACE
DisableProgramGroupPage=yes
OutputDir=..\releases
OutputBaseFilename=PACE-Setup-0.2.0-beta
SetupIconFile=..\app\assets\pace.ico
UninstallDisplayIcon={app}\PACE.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
VersionInfoVersion=0.2.0.0
VersionInfoCompany=PACE Project
VersionInfoDescription=PACE Windows Security Companion
VersionInfoProductName=PACE Anti-Cheat

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\PACE.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\PACE Anti-Cheat"; Filename: "{app}\PACE.exe"
Name: "{autodesktop}\PACE Anti-Cheat"; Filename: "{app}\PACE.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\PACE.exe"; Description: "Launch PACE Anti-Cheat"; Flags: postinstall nowait skipifsilent
