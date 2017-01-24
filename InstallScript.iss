﻿; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "DentalClientBase"
#define MyAppPublisher "Ali Saad Developments"
#define MyAppURL "alisaad05@gmail.com"

; !!!!! MyAppExeName should the same as given in py2exe setup (dest_base)
; !!!!! if (dest_base) is not specified, the exe will have the same name as the original python script
#define MyAppExeName "DentalClientBase.exe"
#define MyAppVersion GetFileVersion("dist\DentalClientBase.exe")

#define DISTRIB "dist"
#define INSTALLER "installer"

#define DATA_TCL "tcl"
#define DATA_MPL "mpl-data"
#define DATA_QT "imageformats"
#define DATA_APP "res"


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{642E6A9F-C3AE-4EC3-B09D-12AA9F67887A}   
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile={#INSTALLER}\text_licence.txt
; InfoBeforeFile={#INSTALLER}\text_before.txt
; InfoAfterFile={#INSTALLER}\text_after.txt
Compression=lzma
SolidCompression=yes
SetupIconFile={#DATA_APP}\logonew.ico
UninstallDisplayIcon={#DATA_APP}\logonew.ico
OutputBaseFilename=DCB-x64Setup-v{#MyAppVersion}
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "{#DISTRIB}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
;Source: "{#DISTRIB}\{#DATA_TCL}\*"; DestDir: "{app}\{#DATA_TCL}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DATA_APP}\*"; DestDir: "{app}\{#DATA_APP}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DISTRIB}\*.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#DISTRIB}\*.dll"; DestDir: "{app}"; Flags: ignoreversion

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{win}\MYPROG.INI"