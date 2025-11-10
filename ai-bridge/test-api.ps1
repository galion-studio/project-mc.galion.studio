# Test Claude API directly

$API_KEY = $env:ANTHROPIC_API_KEY  # Set your API key in environment variable

Write-Host "Testing Claude API..." -ForegroundColor Yellow

$body = @{
    model = "claude-sonnet-4-20250514"
    max_tokens = 50
    messages = @(
        @{
            role = "user"
            content = "Say hello in 5 words"
        }
    )
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" -Method Post -Headers @{
        "x-api-key" = $API_KEY
        "anthropic-version" = "2023-06-01"
        "content-type" = "application/json"
    } -Body $body

    $answer = $response.content[0].text
    
    Write-Host "Success! AI said: $answer" -ForegroundColor Green
    
    # Send to Minecraft
    docker exec titan-hub rcon-cli "say [Console] API TEST: $answer"
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Yellow
}

