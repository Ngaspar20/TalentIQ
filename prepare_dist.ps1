# prepare_dist.ps1 - Prepares the distribution folder for Inno Setup
# Run from the TalentIQ project root: .\prepare_dist.ps1

$ErrorActionPreference = "Stop"

$pyVer   = "3.11.9"
$pyZip   = "python-$pyVer-embed-amd64.zip"
$pyUrl   = "https://www.python.org/ftp/python/$pyVer/$pyZip"
$distDir = ".\dist_installer"
$pyDir   = "$distDir\python"
$appDir  = "$distDir\app"

Write-Host ""
Write-Host "TalentIQ - Preparar distribuicao"
Write-Host "================================="
Write-Host ""

# 1. Create folders
Write-Host "[1/5] A criar pastas..."
New-Item -ItemType Directory -Force -Path $pyDir | Out-Null
New-Item -ItemType Directory -Force -Path $appDir | Out-Null
Write-Host "      OK"

# 2. Download Python embeddable
if (Test-Path "$pyDir\python.exe") {
    Write-Host "[2/5] Python embeddable ja existe - ignorado."
} else {
    Write-Host "[2/5] A transferir Python $pyVer embeddable (~9 MB)..."
    Invoke-WebRequest -Uri $pyUrl -OutFile "$distDir\$pyZip" -UseBasicParsing
    Expand-Archive "$distDir\$pyZip" -DestinationPath $pyDir -Force
    Remove-Item "$distDir\$pyZip"
    Write-Host "      OK"
}

# 3. Enable site-packages
Write-Host "[3/5] A configurar Python embeddable..."
$pthFile = Get-ChildItem "$pyDir\python*._pth" | Select-Object -First 1
if ($pthFile) {
    $content = Get-Content $pthFile.FullName -Raw
    $content = $content -replace "#import site", "import site"
    Set-Content $pthFile.FullName $content -Encoding ASCII
}
if (-not (Test-Path "$pyDir\Scripts\pip.exe")) {
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "$distDir\get-pip.py" -UseBasicParsing
    & "$pyDir\python.exe" "$distDir\get-pip.py" --no-warn-script-location -q
    Remove-Item "$distDir\get-pip.py"
}
Write-Host "      OK"

# 4. Install packages
Write-Host "[4/5] A instalar pacotes Python (pode demorar 5-10 minutos)..."
$packages = @("streamlit", "plotly", "pandas", "openpyxl", "python-docx", "pdfplumber", "openai")
foreach ($pkg in $packages) {
    Write-Host "      -> $pkg"
    & "$pyDir\python.exe" -m pip install $pkg --no-warn-script-location -q
}
Write-Host "      OK"

# 5. Copy app files
Write-Host "[5/5] A copiar ficheiros da app..."
foreach ($f in @("app.py", "config.py", "qa_agent.py", "launcher.py")) {
    Copy-Item -Path $f -Destination $appDir -Force
}
foreach ($folder in @("pages", "core")) {
    if (Test-Path "$appDir\$folder") { Remove-Item "$appDir\$folder" -Recurse -Force }
    Copy-Item -Path $folder -Destination "$appDir\$folder" -Recurse -Force
}
New-Item -ItemType Directory -Force -Path "$appDir\data" | Out-Null
Copy-Item -Path "data\jobs.json" -Destination "$appDir\data\" -Force
Write-Host "      OK"

Write-Host ""
Write-Host "Pronto! Pasta criada em: $distDir"
Write-Host "Proximo passo: abrir TalentIQ.iss no Inno Setup e premir F9"
Write-Host ""
