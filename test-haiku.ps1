# Quick test of Haiku API

Write-Host "Testing Claude Haiku API..." -ForegroundColor Yellow

$apiKey = $env:ANTHROPIC_API_KEY  # Set your API key in environment variable

$body = @{
    model = "claude-3-5-haiku-20241022"
    max_tokens = 50
    messages = @(
        @{
            role = "user"
            content = "Say hello to galion.studio in 5 words"
        }
    )
} | ConvertTo-Json -Depth 10

$headers = @{
    "x-api-key" = $apiKey
    "anthropic-version" = "2023-06-01"
    "content-type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" -Method Post -Headers $headers -Body $body
    $answer = $response.content[0].text
    
    Write-Host "SUCCESS! AI said: $answer" -ForegroundColor Green
    
    # Send to Minecraft
    docker exec titan-hub rcon-cli "say [Console] API TEST: $answer"
    
    Write-Host ""
    Write-Host "API is working! Haiku model confirmed!" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
}

pause

