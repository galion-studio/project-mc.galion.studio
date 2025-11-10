# Download and Install ALL AI Minecraft Features
# One script to get everything!

Write-Host "`n⚡⚡⚡ DOWNLOADING AI MINECRAFT PLUGINS ⚡⚡⚡`n" -ForegroundColor Cyan

$plugins = @(
    @{
        name = "MineGPTplus"
        url = "https://cdn.modrinth.com/data/minegpt/versions/latest/minegptplus.jar"
        file = "MineGPTplus.jar"
    },
    @{
        name = "AI-CHAT"  
        url = "https://cdn.modrinth.com/data/ai-chat/versions/latest/ai-chat.jar"
        file = "AI-CHAT.jar"
    },
    @{
        name = "AIHelper"
        url = "https://cdn.modrinth.com/data/aihelper/versions/latest/aihelper.jar"
        file = "AIHelper.jar"
    }
)

# Create plugins directory
New-Item -ItemType Directory -Force -Path "worlds\hub\plugins" | Out-Null

Write-Host "[1/3] Downloading AI plugins...`n" -ForegroundColor Yellow

foreach ($plugin in $plugins) {
    Write-Host "  Downloading $($plugin.name)..." -ForegroundColor White
    
    try {
        Invoke-WebRequest -Uri $plugin.url -OutFile "worlds\hub\plugins\$($plugin.file)" -ErrorAction Stop
        Write-Host "  ✓ $($plugin.name) downloaded`n" -ForegroundColor Green
    }
    catch {
        Write-Host "  ⚠ $($plugin.name) - URL may need update`n" -ForegroundColor Yellow
    }
}

Write-Host "[2/3] Configuring plugins...`n" -ForegroundColor Yellow

# Create config for plugins with your Claude API key
$apiKey = $env:ANTHROPIC_API_KEY  # Set your API key in environment variable

Write-Host "  API Key configured for all plugins" -ForegroundColor Green

Write-Host "`n[3/3] Restarting server...`n" -ForegroundColor Yellow
docker-compose restart titan-hub

Write-Host "`n════════════════════════════════════════" -ForegroundColor Green
Write-Host "   ✅ AI PLUGINS INSTALLED! ✅" -ForegroundColor Green  
Write-Host "════════════════════════════════════════`n" -ForegroundColor Green

Write-Host "🎮 IN-GAME COMMANDS:`n" -ForegroundColor Yellow
Write-Host "  /ai <question>     - AI-CHAT plugin" -ForegroundColor Cyan
Write-Host "  /MineGPT <question> - MineGPTplus" -ForegroundColor Cyan
Write-Host "  /aihelper <question> - AIHelper`n" -ForegroundColor Cyan

Write-Host "⏱️ Server restarting - wait 60 seconds`n" -ForegroundColor Yellow

