; -------------------------------------------------------
;  LURP Utility Suite — Professional Installer
;  Built with Inno Setup
; -------------------------------------------------------

[Setup]
AppName=LURP Utility Suite
AppVersion=1.1
AppPublisher=LURP Roleplay
AppPublisherURL=https://discord.gg/6zw4yZMn2w
DefaultDirName={pf}\LURP Utility Suite
DefaultGroupName=LURP Utility Suite
OutputDir=.
OutputBaseFilename=LURP_Installer
SetupIconFile="LURP_logo.bmp"
WizardSmallImageFile="LURP_logo.bmp"
UninstallDisplayIcon={app}\LURP-CacheClear.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableDirPage=no
DisableProgramGroupPage=yes
LicenseFile="license.txt"

; -------------------------------------------------------
; FILES TO INSTALL
; -------------------------------------------------------

[Files]
; Your EXE compiled by PyInstaller
Source: "LURP-CacheClear.exe"; DestDir: "{app}"; Flags: ignoreversion

; Logo used for shortcuts + installer branding
Source: "LURP_logo.bmp"; DestDir: "{app}"; Flags: ignoreversion

; Optional: include local changelog or config
; Source: "..\app\resources\changelog.txt"; DestDir: "{app}"

; -------------------------------------------------------
; SHORTCUTS
; -------------------------------------------------------

[Icons]
Name: "{group}\LURP Utility Suite"; Filename: "{app}\LURP-CacheClear.exe"; IconFilename: "{app}\LURP_logo.ico"
Name: "{commondesktop}\LURP Utility Suite"; Filename: "{app}\LURP-CacheClear.exe"; IconFilename: "{app}\LURP_logo.ico"; Tasks: desktopicon

; -------------------------------------------------------
; USER OPTIONS
; -------------------------------------------------------

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional Options:"

; -------------------------------------------------------
; UI CUSTOMIZATION
; -------------------------------------------------------

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel1=Welcome to the LURP Utility Suite Installer
WelcomeLabel2=This will install the LURP Utility Suite on your computer.
FinishedLabelNoIcons=The installation of LURP Utility Suite is complete.

[CustomMessages]
english.InstallingMainApp=Installing LURP Utility Suite...

; -------------------------------------------------------
; ELEGANT INSTALLED PAGES
; -------------------------------------------------------

[Run]
Filename: "{app}\LURP-CacheClear.exe"; Description: "Launch LURP Utility Suite now"; Flags: nowait postinstall skipifsilent
