# EchoCode installer for Windows
# Usage: irm https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoCode/install.ps1 | iex

$ErrorActionPreference = "Stop"

$repo = "EchoWorker/EchoAIStore"
$installDir = if ($env:ECHOCODE_INSTALL_DIR) { $env:ECHOCODE_INSTALL_DIR } else { "$env:USERPROFILE\.echoai\bin" }
$archive = "echocode-windows-x64.zip"

# Get latest EchoCode release (filter by echocode- tag prefix)
Write-Host "Fetching latest release..."
$releases = Invoke-RestMethod "https://api.github.com/repos/$repo/releases"
$release = $releases | Where-Object { $_.tag_name -like "echocode-*" } | Select-Object -First 1

if (-not $release) {
    Write-Error "Could not find any EchoCode release"
    exit 1
}

$version = $release.tag_name
$asset = $release.assets | Where-Object { $_.name -eq $archive }

if (-not $asset) {
    Write-Error "Could not find $archive in release $version"
    exit 1
}

$url = $asset.browser_download_url
Write-Host "Downloading EchoCode $version..."

# Download and extract
$tmp = New-TemporaryFile | Rename-Item -NewName { $_.Name + ".zip" } -PassThru
Invoke-WebRequest -Uri $url -OutFile $tmp.FullName

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Expand-Archive -Path $tmp.FullName -DestinationPath $installDir -Force
Remove-Item $tmp.FullName

Write-Host ""
Write-Host "✅ EchoCode $version installed to $installDir\echo-code.exe" -ForegroundColor Green

# Add to PATH if not already there
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$installDir;$currentPath", "User")
    Write-Host ""
    Write-Host "Added $installDir to user PATH." -ForegroundColor Yellow
    Write-Host "Restart your terminal for PATH changes to take effect."
}

Write-Host ""

# Copy example config if no config exists
$configDir = "$env:USERPROFILE\.echoai"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

if (-not (Test-Path "$configDir\echocode.toml")) {
    $exampleUrl = "https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoCode/echocode.example.toml"
    try {
        Invoke-WebRequest -Uri $exampleUrl -OutFile "$configDir\echocode.toml" -ErrorAction Stop
        Write-Host "📝 Created $configDir\echocode.toml from example." -ForegroundColor Yellow
    } catch {
        Write-Host "⚠️  Could not download example config. Create $configDir\echocode.toml manually." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Get started:"
Write-Host "  1. Edit ~/.echoai/echocode.toml — set your API key and model"
Write-Host "  2. echo-code                     # Start interactive session"
