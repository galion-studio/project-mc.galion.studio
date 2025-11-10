# PowerShell script to push to GitHub

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\Gigabyte\Documents\project-mc-serv-mc.galion.studio"

# Push to GitHub
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ SUCCESS! Code pushed to GitHub" -ForegroundColor Green
    Write-Host ""
    
    # Create and push release tag
    Write-Host "Creating release tag..." -ForegroundColor Cyan
    git tag -a v1.0.0-alpha -m "Initial alpha release"
    git push origin v1.0.0-alpha
    
    Write-Host ""
    Write-Host "✓ COMPLETE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View at: https://github.com/galion-studio/project-mc.galion.studio" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you created the repository on GitHub first:" -ForegroundColor Yellow
    Write-Host "https://github.com/organizations/galion-studio/repositories/new" -ForegroundColor White
    Write-Host "Name: project-mc.galion.studio" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"

