# Titan Server - Grafana Reset Script
# Fixes Grafana login issues by resetting to default credentials
# Username: admin | Password: admin

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "  GRAFANA RESET SCRIPT" -ForegroundColor Blue
Write-Host "  Fixing login issues..." -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Step 1: Stop Grafana
Write-Host "[1/6] Stopping Grafana container..." -ForegroundColor Yellow
docker-compose stop grafana
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Grafana stopped" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to stop Grafana" -ForegroundColor Red
}

# Step 2: Remove Grafana container
Write-Host "[2/6] Removing Grafana container..." -ForegroundColor Yellow
docker-compose rm -f grafana
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Container removed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to remove container" -ForegroundColor Red
}

# Step 3: Find and remove Grafana volume
Write-Host "[3/6] Finding and removing Grafana volume..." -ForegroundColor Yellow
$volumes = docker volume ls --format "{{.Name}}" | Select-String "grafana"
if ($volumes) {
    foreach ($volume in $volumes) {
        Write-Host "  Removing volume: $volume" -ForegroundColor Cyan
        docker volume rm $volume 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Volume removed: $volume" -ForegroundColor Green
        } else {
            Write-Host "  ! Volume in use or already removed: $volume" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ! No Grafana volumes found (already clean)" -ForegroundColor Yellow
}

# Step 4: Start Grafana fresh
Write-Host "[4/6] Starting Grafana with fresh configuration..." -ForegroundColor Yellow
docker-compose up -d grafana
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Grafana started" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start Grafana" -ForegroundColor Red
    exit 1
}

# Step 5: Wait for initialization
Write-Host "[5/6] Waiting for Grafana to initialize (60 seconds)..." -ForegroundColor Yellow
for ($i = 60; $i -gt 0; $i--) {
    Write-Host "  $i seconds remaining..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
}
Write-Host "✓ Wait complete" -ForegroundColor Green

# Step 6: Verify Grafana is running
Write-Host "[6/6] Verifying Grafana status..." -ForegroundColor Yellow
$status = docker-compose ps grafana
Write-Host $status
Write-Host ""

# Check logs for startup confirmation
Write-Host "Recent Grafana logs:" -ForegroundColor Cyan
docker-compose logs grafana --tail=10
Write-Host ""

# Final success message
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ GRAFANA RESET COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Login Information:" -ForegroundColor Yellow
Write-Host "  URL:      http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor Cyan
Write-Host "  Password: admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening Grafana in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Open browser
start http://localhost:3000

Write-Host ""
Write-Host "✓ Script complete! Try logging in now." -ForegroundColor Green
Write-Host ""

