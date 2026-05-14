# EchoAI installer for Windows
# Usage: irm https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.ps1 | iex

$ErrorActionPreference = "Stop"

$repo = "EchoWorker/EchoAIStore"
$installDir = if ($env:ECHOAI_INSTALL_DIR) { $env:ECHOAI_INSTALL_DIR } else { "$env:USERPROFILE\.echoai\bin" }
$archive = "echoai-windows-x64.zip"

# Get latest EchoAI release (filter by echoai- tag prefix)
Write-Host "Fetching latest release..."
$releases = Invoke-RestMethod "https://api.github.com/repos/$repo/releases"
$release = $releases | Where-Object { $_.tag_name -like "echoai-*" } | Select-Object -First 1

if (-not $release) {
    Write-Error "Could not find any EchoAI release"
    exit 1
}

$version = $release.tag_name
$asset = $release.assets | Where-Object { $_.name -eq $archive }

if (-not $asset) {
    Write-Error "Could not find $archive in release $version"
    exit 1
}

$url = $asset.browser_download_url
Write-Host "Downloading EchoAI $version..."

# Download and extract
$tmp = New-TemporaryFile | Rename-Item -NewName { $_.Name + ".zip" } -PassThru
Invoke-WebRequest -Uri $url -OutFile $tmp.FullName

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Expand-Archive -Path $tmp.FullName -DestinationPath $installDir -Force
Remove-Item $tmp.FullName

Write-Host ""
Write-Host "✅ EchoAI $version installed to $installDir\echoai.exe" -ForegroundColor Green

# Add to PATH if not already there
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$installDir;$currentPath", "User")
    Write-Host ""
    Write-Host "Added $installDir to user PATH." -ForegroundColor Yellow
    Write-Host "Restart your terminal for PATH changes to take effect."
}

Write-Host ""
Write-Host "Get started:"
Write-Host "  echoai gateway    # Start the server"
Write-Host "  echoai agent      # Interactive REPL"
