# SIMPLE BUG LOGGER - Works immediately!
# Monitors chat for bug reports and saves them

$bugFile = "bug-reports.txt"

Write-Host "`n🐛 BUG REPORT LOGGER - RUNNING`n" -ForegroundColor Yellow
Write-Host "Monitoring chat for bug reports..." -ForegroundColor Cyan
Write-Host "Players type: 'BUG: description' in chat`n" -ForegroundColor White
Write-Host "All reports saved to: $bugFile`n" -ForegroundColor Green

# Send instruction to players
docker exec titan-hub rcon-cli "say [System] Bug Report: Type 'BUG: your issue' in chat"

# Monitor logs
$job = Start-Job -ScriptBlock {
    docker logs -f titan-hub 2>&1
}

while ($true) {
    $logs = Receive-Job $job
    
    if ($logs) {
        foreach ($line in $logs) {
            # Look for bug reports: <player> BUG: description
            if ($line -match '<([^>]+)>\s+BUG:\s*(.+)') {
                $player = $matches[1]
                $bug = $matches[2].Trim()
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                
                # Create report
                $report = @"
[$timestamp] Reporter: $player
Description: $bug
----------------------------------------
"@
                
                # Save to file
                Add-Content -Path $bugFile -Value $report
                
                # Show in console
                Write-Host "`n🐛 NEW BUG REPORT:" -ForegroundColor Red
                Write-Host "   From: $player" -ForegroundColor Yellow
                Write-Host "   Bug: $bug`n" -ForegroundColor White
                
                # Confirm in Minecraft
                docker exec titan-hub rcon-cli "say [System] ✓ Bug report saved! Thank you $player"
            }
        }
    }
    
    Start-Sleep -Milliseconds 500
}

