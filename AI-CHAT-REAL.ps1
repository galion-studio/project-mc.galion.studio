# TITAN AI CHAT - PowerShell Edition
# Fixed and working version

$API_KEY = $env:ANTHROPIC_API_KEY  # Set your API key in environment variable
$seen = @{}

function Send-MinecraftMessage {
    param($message)
    docker exec titan-hub rcon-cli "say [Console] $message" 2>$null | Out-Null
    Write-Host "-> $message" -ForegroundColor Cyan
}

function Ask-Claude {
    param($question)
    
    $body = @{
        model = "claude-3-5-haiku-20241022"
        max_tokens = 80
        system = "Answer in MAX 20 words. Be ultra concise for Minecraft chat."
        messages = @(
            @{
                role = "user"
                content = $question
            }
        )
    } | ConvertTo-Json -Depth 10
    
    try {
        $response = Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" -Method Post -Headers @{
            "x-api-key" = $API_KEY
            "anthropic-version" = "2023-06-01"
            "content-type" = "application/json"
        } -Body $body -TimeoutSec 10
        
        return $response.content[0].text
    }
    catch {
        return "API Error"
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  TITAN AI CHAT - LIVE MODE" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Claude Sonnet 4.5 connected" -ForegroundColor Green
Write-Host "Monitoring Minecraft chat..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Send-MinecraftMessage "AI Bridge active! Type to chat!"

# Monitor logs
$job = Start-Job -ScriptBlock {
    docker logs -f titan-hub 2>&1
}

while ($true) {
    $logs = Receive-Job $job
    
    if ($logs) {
        foreach ($line in $logs) {
            if ($line -match '<([^>]+)>\s+(.+)') {
                $player = $matches[1]
                $message = $matches[2].Trim()
                $key = "$player`:$message"
                
                if (-not $seen.ContainsKey($key) -and ($message -match 'console|@ai|hey')) {
                    $seen[$key] = $true
                    
                    Write-Host ""
                    Write-Host "Player: $message" -ForegroundColor Yellow
                    Send-MinecraftMessage "Thinking..."
                    
                    $start = Get-Date
                    $answer = Ask-Claude $message
                    $elapsed = ((Get-Date) - $start).TotalSeconds
                    
                    Write-Host "AI ($elapsed s): $answer" -ForegroundColor Green
                    Write-Host ""
                    
                    Send-MinecraftMessage $answer
                }
            }
        }
    }
    
    Start-Sleep -Milliseconds 500
    
    if ($seen.Count -gt 50) {
        $seen.Clear()
    }
}
