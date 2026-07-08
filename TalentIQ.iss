#define MyAppName      "TalentIQ"
#define MyAppVersion   "0.1.0"
#define MyAppPublisher "TalentIQ Health Partners"
#define MyAppURL       "https://talentiq.health"

[Setup]
AppId={{6F3A2B1C-D4E5-4F60-A7B8-C9D0E1F23456}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=TalentIQ_Setup_v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\python\pythonw.exe

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "english";    MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho no Ambiente de Trabalho"; GroupDescription: "Opcoes adicionais:"

[Files]
; Bundled Python runtime
Source: "dist_installer\python\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs

; TalentIQ application files
Source: "dist_installer\app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs

; Launcher script
Source: "installer_launcher.vbs"; DestDir: "{app}"; DestName: "TalentIQ.vbs"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\TalentIQ"; \
      Filename: "{sys}\wscript.exe"; \
      Parameters: """{app}\TalentIQ.vbs"""; \
      WorkingDir: "{app}"; \
      Comment: "Iniciar TalentIQ — Recrutamento Inteligente"

; Desktop shortcut
Name: "{userdesktop}\TalentIQ"; \
      Filename: "{sys}\wscript.exe"; \
      Parameters: """{app}\TalentIQ.vbs"""; \
      WorkingDir: "{app}"; \
      Tasks: desktopicon; \
      Comment: "Iniciar TalentIQ — Recrutamento Inteligente"

[Run]
Filename: "{sys}\wscript.exe"; \
          Parameters: """{app}\TalentIQ.vbs"""; \
          Description: "Iniciar TalentIQ agora"; \
          Flags: postinstall nowait skipifsilent

[UninstallDelete]
; Remove user data only if the user requests it — data lives in AppData, not here
Type: dirifempty; Name: "{app}"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  SettingsDir: String;
  SettingsFile: String;
begin
  if CurStep = ssPostInstall then begin
    // Create %APPDATA%\TalentIQ directory so the app can write data on first run
    SettingsDir := ExpandConstant('{userappdata}\TalentIQ');
    if not DirExists(SettingsDir) then
      CreateDir(SettingsDir);
    // Create empty settings.json with Grok API key placeholder
    SettingsFile := SettingsDir + '\settings.json';
    if not FileExists(SettingsFile) then
      SaveStringToFile(SettingsFile,
        '{"GROK_API_KEY": "", "_comment": "Cole aqui a sua chave Grok xAI"}',
        False);
  end;
end;
