# Titan Server - Set No Premium Mode
# Allows cracked/non-premium Minecraft clients to connect
# WARNING: This disables Mojang authentication!

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "  SETTING NO PREMIUM MODE" -ForegroundColor Blue
Write-Host "  (Cracked Client Support)" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

Write-Host "⚠️  WARNING: This will disable Mojang authentication!" -ForegroundColor Yellow
Write-Host "⚠️  Anyone can join with any username!" -ForegroundColor Yellow
Write-Host "⚠️  Use whitelist or plugins for security!" -ForegroundColor Yellow
Write-Host ""

# Update .env file if it exists
if (Test-Path ".env") {
    Write-Host "[1/3] Updating .env file..." -ForegroundColor Yellow
    
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace "ONLINE_MODE=true", "ONLINE_MODE=false"
    $envContent = $envContent -replace "ENFORCE_SECURE_PROFILE=true", "ENFORCE_SECURE_PROFILE=false"
    Set-Content ".env" $envContent
    
    Write-Host "✓ .env updated" -ForegroundColor Green
} else {
    Write-Host "[1/3] Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env created" -ForegroundColor Green
}

# Restart servers to apply changes
Write-Host "[2/3] Restarting game servers..." -ForegroundColor Yellow
docker-compose restart titan-hub titan-survival
Write-Host "✓ Servers restarting" -ForegroundColor Green

# Wait for restart
Write-Host "[3/3] Waiting for servers to restart (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host "✓ Restart complete" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ NO PREMIUM MODE ENABLED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Changes applied:" -ForegroundColor Yellow
Write-Host "  • online-mode=false" -ForegroundColor Cyan
Write-Host "  • Authentication disabled" -ForegroundColor Cyan
Write-Host "  • Cracked clients can now connect" -ForegroundColor Cyan
Write-Host ""
Write-Host "Security recommendations:" -ForegroundColor Yellow
Write-Host "  • Enable whitelist: /whitelist on" -ForegroundColor Cyan
Write-Host "  • Use authentication plugins (AuthMe, etc.)" -ForegroundColor Cyan
Write-Host "  • Monitor for suspicious activity" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Players can now connect with cracked clients!" -ForegroundColor Green
Write-Host ""

