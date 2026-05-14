# EchoAI installer for Windows
# Usage: irm https://raw.githubusercontent.com/EchoWorker/EchoAI/main/scripts/install.ps1 | iex

$ErrorActionPreference = "Stop"

$repo = "EchoWorker/EchoAIStore"
$installDir = if ($env:ECHOAI_INSTALL_DIR) { $env:ECHOAI_INSTALL_DIR } else { "$env:USERPROFILE\.echoai\bin" }
$archive = "echoai-windows-x64.zip"

# Get latest version
Write-Host "Fetching latest release..."
$release = Invoke-RestMethod "https://api.github.com/repos/$repo/releases/latest"
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
