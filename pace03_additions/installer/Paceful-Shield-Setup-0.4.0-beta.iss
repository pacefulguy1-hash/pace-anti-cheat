#define MyAppName "Paceful Shield"
#define MyAppVersion "0.4.0-beta"
#define MyAppPublisher "Paceful Shield Project"
#define MyAppExeName "PacefulShield04.exe"

[Setup]
AppId={{A6E1BD92-69C6-493E-889E-F6444A008514}
AppName={#MyAppName} 0.4 Beta
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Paceful Shield 0.4 Beta
DefaultGroupName=Paceful Shield 0.4 Beta
DisableProgramGroupPage=yes
OutputDir=..\releases
OutputBaseFilename=Paceful-Shield-Setup-0.4.0-beta
SetupIconFile=..\app\assets\paceful-shield.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
VersionInfoVersion=0.4.0.0
VersionInfoCompany=Paceful Shield Project
VersionInfoDescription=Paceful Shield Windows Security Companion 0.4 Beta
VersionInfoProductName=Paceful Shield

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut named Pace"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "..\dist\PacefulShield04.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Paceful Shield 0.4 Beta"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Pace"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Paceful Shield"; Flags: postinstall nowait skipifsilent
