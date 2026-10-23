#define MyAppName "PACE"
#define MyAppVersion "0.3.0-beta"
#define MyAppPublisher "PACE Project"
#define MyAppExeName "PACE03.exe"

[Setup]
AppId={{7D8DD19E-4A62-40D8-A4C9-6C11C57D0C03}
AppName={#MyAppName} 0.3 Beta
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\PACE 0.3 Beta
DefaultGroupName=PACE 0.3 Beta
DisableProgramGroupPage=yes
OutputDir=..\releases
OutputBaseFilename=PACE-Setup-0.3.0-beta
SetupIconFile=..\app\assets\pace.ico
UninstallDisplayIcon={app}\PACE03.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
VersionInfoVersion=0.3.0.0
VersionInfoCompany=PACE Project
VersionInfoDescription=PACE Windows Security Companion 0.3 Beta
VersionInfoProductName=PACE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\PACE03.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\PACE 0.3 Beta"; Filename: "{app}\PACE03.exe"
Name: "{autodesktop}\PACE 0.3 Beta"; Filename: "{app}\PACE03.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\PACE03.exe"; Description: "Launch PACE 0.3 Beta"; Flags: postinstall nowait skipifsilent
