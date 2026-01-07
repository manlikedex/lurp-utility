; ----------------------------------------------------
; LURP Cache Clear Utility - Installer Script
; Updated for Version 1.1
; ----------------------------------------------------

[Setup]
AppName=LURP Cache Clear Utility
AppVersion=1.1
AppPublisher=LURP
DefaultDirName={pf}\LURP Cache Clear Utility
DefaultGroupName=LURP Cache Clear Utility
OutputDir=.
OutputBaseFilename=LURP_CacheClear_Installer_v1.1
SetupIconFile=app\resources\LURP_logo.ico
UninstallDisplayIcon={app}\LURP-CacheClear.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
; Your compiled EXE from PyInstaller
Source: "installer\LURP-CacheClear.exe"; DestDir: "{app}"; Flags: ignoreversion

; Include app logo for shortcuts
Source: "app\resources\LURP_logo.ico"; DestDir: "{app}"; Flags: ignoreversion

; Optional: Include UI resources if needed
Source: "app\resources\LURP_logo.png"; DestDir: "{app}\resources"; Flags: ignoreversion
Source: "app\resources\style.qss"; DestDir: "{app}\resources"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\LURP Cache Clear Utility"; Filename: "{app}\LURP-CacheClear.exe"; IconFilename: "{app}\LURP_logo.ico"

; Desktop shortcut (optional)
Name: "{commondesktop}\LURP Cache Clear Utility"; Filename: "{app}\LURP-CacheClear.exe"; IconFilename: "{app}\LURP_logo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional Options:"; Flags: unchecked
