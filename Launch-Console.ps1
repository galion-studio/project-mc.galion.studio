# ================================================================
# 🚀 PowerShell Launcher - Transparent Developer Console
# Easy launch from PowerShell terminal
# ================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  🚀 TRANSPARENT DEVELOPER CONSOLE LAUNCHER" -ForegroundColor Green
Write-Host "  mc.galion.studio - Full Configuration Control" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] 🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = & py --version 2>&1
    Write-Host "  ✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python not found!" -ForegroundColor Red
    Write-Host "  📥 Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "[2/4] 📦 Checking dependencies..." -ForegroundColor Yellow
$packages = @("customtkinter", "python-dotenv", "colorama")
$missing = @()

foreach ($package in $packages) {
    try {
        & py -c "import $($package.Replace('-', '_'))" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $package installed" -ForegroundColor Green
        } else {
            $missing += $package
        }
    } catch {
        $missing += $package
    }
}

if ($missing.Count -gt 0) {
    Write-Host "  ⚠️  Missing packages: $($missing -join ', ')" -ForegroundColor Yellow
    Write-Host "  📥 Installing..." -ForegroundColor Yellow
    & py -m pip install -r requirements.txt
}

# Validate configuration
Write-Host ""
Write-Host "[3/4] 🔧 Validating configuration..." -ForegroundColor Yellow
if (Test-Path ".env.grok") {
    Write-Host "  ✅ .env.grok found" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  .env.grok not found" -ForegroundColor Yellow
    Write-Host "  💡 Will use default values" -ForegroundColor Cyan
}

# Launch console
Write-Host ""
Write-Host "[4/4] 🚀 Launching Transparent Console..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  ✅ CONSOLE STARTING..." -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to dev-console directory and launch
Set-Location dev-console
& py transparent_console.py

Write-Host ""
Write-Host "✅ Console closed." -ForegroundColor Green
Write-Host ""

