# ============================================================================
# RENAME PROJECT DIRECTORY
# ============================================================================
#
# This script renames the project directory from:
#   project-mc-serv-mc.galion.studio
# to:
#   project-mc.galion.studio
#
# ============================================================================

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "RENAME PROJECT DIRECTORY" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory name
$currentDir = Split-Path -Leaf (Get-Location)

Write-Host "Current directory: $currentDir"
Write-Host ""

if ($currentDir -ne "project-mc-serv-mc.galion.studio") {
    Write-Host "ERROR: This script must be run from the project-mc-serv-mc.galion.studio directory" -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "This will rename the project directory from:" -ForegroundColor Yellow
Write-Host "  FROM: project-mc-serv-mc.galion.studio" -ForegroundColor White
Write-Host "  TO:   project-mc.galion.studio" -ForegroundColor Green
Write-Host ""
Write-Host "WARNING: Make sure no files are open in the directory!" -ForegroundColor Yellow
Write-Host ""

$response = Read-Host "Do you want to continue? (Y/N)"
if ($response -ne "Y" -and $response -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Renaming directory..." -ForegroundColor Cyan
Write-Host ""

try {
    # Move to parent directory
    Set-Location ..
    
    # Rename the directory
    Rename-Item -Path "project-mc-serv-mc.galion.studio" -NewName "project-mc.galion.studio" -ErrorAction Stop
    
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Directory renamed" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Old name: project-mc-serv-mc.galion.studio" -ForegroundColor Gray
    Write-Host "New name: project-mc.galion.studio" -ForegroundColor Green
    Write-Host ""
    
    $newPath = Join-Path (Get-Location) "project-mc.galion.studio"
    Write-Host "New path: $newPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now open the project in the new location." -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host "ERROR: Failed to rename directory" -ForegroundColor Red
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error message: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "- No files are open from this directory" -ForegroundColor White
    Write-Host "- No command prompts are in this directory" -ForegroundColor White
    Write-Host "- No applications are using files from this directory" -ForegroundColor White
    Write-Host "- You have permission to rename the directory" -ForegroundColor White
    Write-Host ""
}

Read-Host "Press Enter to exit"

