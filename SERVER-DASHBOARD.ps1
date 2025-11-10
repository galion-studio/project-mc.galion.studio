# GALION.STUDIO Server Dashboard
# Beautiful console UI with live logs

# Set console properties
$Host.UI.RawUI.WindowTitle = "GALION.STUDIO Server Dashboard"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "White"

# Import server mode modules
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Global variables
$serverProcess = $null
$logFile = "worlds\hub\logs\latest.log"
$lastLogPosition = 0

# Function to draw box
function Draw-Box {
    param(
        [string]$Title,
        [int]$Width = 80,
        [ConsoleColor]$Color = "Cyan"
    )
    
    $oldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    
    Write-Host ("╔" + ("═" * ($Width - 2)) + "╗")
    if ($Title) {
        $padding = [Math]::Max(0, ($Width - $Title.Length - 4) / 2)
        Write-Host ("║" + (" " * $padding) + " $Title " + (" " * ($padding - 1)) + "║")
        Write-Host ("╠" + ("═" * ($Width - 2)) + "╣")
    }
    
    $Host.UI.RawUI.ForegroundColor = $oldColor
}

function Draw-BoxEnd {
    param(
        [int]$Width = 80,
        [ConsoleColor]$Color = "Cyan"
    )
    
    $oldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host ("╚" + ("═" * ($Width - 2)) + "╝")
    $Host.UI.RawUI.ForegroundColor = $oldColor
}

# Function to write colored text
function Write-ColorText {
    param(
        [string]$Text,
        [ConsoleColor]$Color = "White",
        [switch]$NoNewline
    )
    
    $oldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    if ($NoNewline) {
        Write-Host $Text -NoNewline
    } else {
        Write-Host $Text
    }
    $Host.UI.RawUI.ForegroundColor = $oldColor
}

# Function to get server status
function Get-ServerStatus {
    try {
        $pythonStatus = python -c "from server_mode_config import ServerModeManager; from ai_feature_controller import AIFeatureController; m = ServerModeManager(); c = AIFeatureController(); mode = m.get_current_mode(); config = m.get_mode_config(); status = c.get_ai_status(); print(f'{mode.value}|{config[`"host`"]}:{config[`"port`"]}|{config[`"ai_enabled`"]}|{status[`"ai_available`"]}|{status[`"internet_available`"]}')" 2>&1
        
        if ($pythonStatus -match "(\w+)\|([^|]+)\|(\w+)\|(\w+)\|(\w+)") {
            return @{
                Mode = $Matches[1]
                Server = $Matches[2]
                AIEnabled = $Matches[3]
                AIAvailable = $Matches[4]
                Internet = $Matches[5]
            }
        }
    } catch {
        return @{
            Mode = "unknown"
            Server = "localhost:25565"
            AIEnabled = "False"
            AIAvailable = "False"
            Internet = "False"
        }
    }
    
    return @{
        Mode = "local"
        Server = "localhost:25565"
        AIEnabled = "False"
        AIAvailable = "False"
        Internet = "False"
    }
}

# Function to check if server is running
function Test-ServerRunning {
    $javaProcesses = Get-Process java -ErrorAction SilentlyContinue | Where-Object {
        $_.Path -like "*java*" -and $_.MainWindowTitle -notlike ""
    }
    return ($javaProcesses.Count -gt 0)
}

# Function to display main menu
function Show-MainMenu {
    Clear-Host
    
    # Header
    Write-Host ""
    Draw-Box "GALION.STUDIO SERVER DASHBOARD" 80 "Cyan"
    Write-Host ""
    
    # Get server status
    $status = Get-ServerStatus
    $isRunning = Test-ServerRunning
    
    # Server Status Section
    Write-ColorText "  SERVER STATUS:" "Yellow"
    Write-Host "  ────────────────────────────────────────────────────────────────────────"
    
    Write-Host "  Mode: " -NoNewline
    if ($status.Mode -eq "official") {
        Write-ColorText "$($status.Mode.ToUpper())" "Green"
    } else {
        Write-ColorText "$($status.Mode.ToUpper())" "Cyan"
    }
    
    Write-Host "  Address: " -NoNewline
    Write-ColorText $status.Server "White"
    
    Write-Host "  AI Features: " -NoNewline
    if ($status.AIEnabled -eq "True") {
        Write-ColorText "ENABLED" "Green"
    } else {
        Write-ColorText "DISABLED" "Red"
    }
    
    Write-Host "  Internet: " -NoNewline
    if ($status.Internet -eq "True") {
        Write-ColorText "CONNECTED" "Green"
    } else {
        Write-ColorText "OFFLINE" "Yellow"
    }
    
    Write-Host "  Server: " -NoNewline
    if ($isRunning) {
        Write-ColorText "RUNNING ●" "Green"
    } else {
        Write-ColorText "STOPPED ○" "Red"
    }
    
    Write-Host ""
    Write-Host "  ────────────────────────────────────────────────────────────────────────"
    Write-Host ""
    
    # Menu Options
    Write-ColorText "  QUICK ACTIONS:" "Yellow"
    Write-Host ""
    
    Write-ColorText "   [1]" "Cyan" -NoNewline
    Write-Host " Start Local Server (Offline)"
    
    Write-ColorText "   [2]" "Cyan" -NoNewline
    Write-Host " Start Official Server (Online + AI)"
    
    Write-ColorText "   [3]" "Cyan" -NoNewline
    Write-Host " View Live Server Logs"
    
    Write-ColorText "   [4]" "Cyan" -NoNewline
    Write-Host " Configure AI Features"
    
    Write-ColorText "   [5]" "Cyan" -NoNewline
    Write-Host " Switch Server Mode"
    
    Write-ColorText "   [6]" "Cyan" -NoNewline
    Write-Host " Generate New World"
    
    Write-ColorText "   [7]" "Cyan" -NoNewline
    Write-Host " Chat with Grok 4 Fast AI"
    
    Write-ColorText "   [8]" "Cyan" -NoNewline
    Write-Host " Manage Plugins"
    
    Write-ColorText "   [9]" "Cyan" -NoNewline
    Write-Host " Stop Server"
    
    Write-ColorText "   [0]" "Cyan" -NoNewline
    Write-Host " Exit Dashboard"
    
    Write-Host ""
    Draw-BoxEnd 80 "Cyan"
    Write-Host ""
    
    Write-Host "  Select option (0-9): " -NoNewline
}

# Function to chat with Grok AI
function Start-GrokChat {
    Clear-Host
    Draw-Box "GROK 4 FAST AI CHAT" 80 "Magenta"
    Write-Host ""
    
    # Check if AI is available
    Write-ColorText "  Checking AI availability..." "Yellow"
    $aiCheck = python -c "from ai_feature_controller import AIFeatureController; c = AIFeatureController(); import sys; sys.exit(0 if c.is_ai_available() else 1)" 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-ColorText "  ✗ AI Features Not Available" "Red"
        Write-Host ""
        Write-Host "  Reasons:"
        Write-Host "    • Server mode might be LOCAL (AI disabled)"
        Write-Host "    • API keys not configured"
        Write-Host "    • No internet connection"
        Write-Host ""
        Write-Host "  To enable AI:"
        Write-Host "    1. Switch to OFFICIAL mode (option 5)"
        Write-Host "    2. Configure API keys (option 4)"
        Write-Host "    3. Ensure internet connection"
        Write-Host ""
        Draw-BoxEnd 80 "Red"
        Write-Host ""
        Write-Host "  Press any key to return..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        return
    }
    
    Write-ColorText "  ✓ AI Ready!" "Green"
    Write-Host ""
    Write-Host "  ────────────────────────────────────────────────────────────────────────"
    Write-Host ""
    Write-ColorText "  Grok 4 Fast is ready to chat!" "Cyan"
    Write-Host "  Type your questions below. Type 'exit' to return."
    Write-Host ""
    Write-Host "  ────────────────────────────────────────────────────────────────────────"
    Write-Host ""
    
    while ($true) {
        Write-Host ""
        Write-ColorText "  You: " "Green" -NoNewline
        $question = Read-Host
        
        if ($question.ToLower() -eq "exit" -or $question.ToLower() -eq "quit") {
            break
        }
        
        if ([string]::IsNullOrWhiteSpace($question)) {
            continue
        }
        
        Write-Host ""
        Write-ColorText "  Grok is thinking..." "Yellow"
        
        # Escape quotes for Python
        $escapedQuestion = $question -replace '"', '\"'
        
        # Get AI response
        $response = python -c "from ai_feature_controller import AIFeatureController; c = AIFeatureController(); response = c.get_ai_response('$escapedQuestion'); print(response if response else 'AI unavailable')" 2>&1
        
        Write-Host ""
        Write-ColorText "  Grok 4 Fast: " "Magenta" -NoNewline
        Write-Host ""
        Write-Host "  ────────────────────────────────────────────────────────────────────────"
        
        # Format response with word wrap
        $words = $response -split ' '
        $line = "  "
        foreach ($word in $words) {
            if (($line + $word).Length -gt 76) {
                Write-Host $line
                $line = "  " + $word + " "
            } else {
                $line += $word + " "
            }
        }
        if ($line.Trim()) {
            Write-Host $line
        }
        
        Write-Host "  ────────────────────────────────────────────────────────────────────────"
    }
    
    Write-Host ""
    Write-ColorText "  Goodbye! Thanks for chatting with Grok." "Cyan"
    Start-Sleep -Seconds 1
}

# Function to start local server
function Start-LocalServer {
    Clear-Host
    Draw-Box "STARTING LOCAL SERVER" 80 "Green"
    Write-Host ""
    
    Write-ColorText "  Setting server mode to LOCAL..." "Yellow"
    python -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.LOCAL)"
    
    Write-ColorText "  ✓ Mode set to LOCAL" "Green"
    Write-Host ""
    Write-ColorText "  Server Configuration:" "Cyan"
    Write-Host "    • Mode: LOCAL (Offline)"
    Write-Host "    • Address: localhost:25565"
    Write-Host "    • AI Features: DISABLED"
    Write-Host "    • Internet: Not Required"
    Write-Host ""
    
    Draw-BoxEnd 80 "Green"
    Write-Host ""
    
    Write-Host "  Press any key to open server console..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Set-Location worlds\hub
    Start-Process cmd.exe -ArgumentList "/k title GALION.STUDIO LOCAL SERVER && java -Xms4G -Xmx4G -XX:+UseG1GC -jar paper-1.21.1-133.jar nogui"
    Set-Location ..\..
    
    Write-Host ""
    Write-ColorText "  ✓ Server console opened!" "Green"
    Start-Sleep -Seconds 2
}

# Function to start official server
function Start-OfficialServer {
    Clear-Host
    Draw-Box "STARTING OFFICIAL SERVER" 80 "Green"
    Write-Host ""
    
    Write-ColorText "  Checking internet connection..." "Yellow"
    
    $hasInternet = python -c "from server_mode_config import ServerModeManager; import sys; m = ServerModeManager(); sys.exit(0 if m.check_internet_connection() else 1)"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-ColorText "  ✗ No internet connection!" "Red"
        Write-Host "    Official mode requires internet for AI features."
        Write-Host ""
        Draw-BoxEnd 80 "Red"
        Write-Host ""
        Write-Host "  Press any key to return..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        return
    }
    
    Write-ColorText "  ✓ Internet connected" "Green"
    Write-Host ""
    
    Write-ColorText "  Setting server mode to OFFICIAL..." "Yellow"
    python -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.OFFICIAL)"
    
    Write-ColorText "  ✓ Mode set to OFFICIAL" "Green"
    Write-Host ""
    
    Write-ColorText "  Server Configuration:" "Cyan"
    Write-Host "    • Mode: OFFICIAL (Online)"
    Write-Host "    • Address: mc.galion.studio:25565"
    Write-Host "    • AI Features: ENABLED"
    Write-Host "    • Internet: REQUIRED"
    Write-Host ""
    
    Draw-BoxEnd 80 "Green"
    Write-Host ""
    
    Write-Host "  Press any key to open server console..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    Set-Location worlds\hub
    Start-Process cmd.exe -ArgumentList "/k title GALION.STUDIO OFFICIAL SERVER && java -Xms4G -Xmx4G -XX:+UseG1GC -jar paper-1.21.1-133.jar nogui"
    Set-Location ..\..
    
    Write-Host ""
    Write-ColorText "  ✓ Server console opened!" "Green"
    Start-Sleep -Seconds 2
}

# Function to view live logs
function Show-LiveLogs {
    Clear-Host
    Draw-Box "LIVE SERVER LOGS" 80 "Magenta"
    Write-Host ""
    Write-ColorText "  Press 'Q' to return to menu" "Yellow"
    Write-Host ""
    Draw-BoxEnd 80 "Magenta"
    Write-Host ""
    
    $lastPosition = 0
    
    while ($true) {
        if (Test-Path $logFile) {
            $content = Get-Content $logFile -Tail 25
            
            Clear-Host
            Draw-Box "LIVE SERVER LOGS - Updating every 2 seconds" 80 "Magenta"
            Write-Host ""
            Write-ColorText "  Press 'Q' to return to menu" "Yellow"
            Write-Host ""
            Write-Host "  ────────────────────────────────────────────────────────────────────────"
            Write-Host ""
            
            foreach ($line in $content) {
                if ($line -match "\[Server thread/INFO\]") {
                    Write-ColorText "  $line" "Green"
                } elseif ($line -match "\[Server thread/WARN\]") {
                    Write-ColorText "  $line" "Yellow"
                } elseif ($line -match "\[Server thread/ERROR\]") {
                    Write-ColorText "  $line" "Red"
                } elseif ($line -match "Done") {
                    Write-ColorText "  $line" "Cyan"
                } else {
                    Write-Host "  $line"
                }
            }
            
            Write-Host ""
            Write-Host "  ────────────────────────────────────────────────────────────────────────"
            Draw-BoxEnd 80 "Magenta"
        } else {
            Write-ColorText "  No logs found. Server not started yet." "Yellow"
        }
        
        # Check for Q key
        if ($Host.UI.RawUI.KeyAvailable) {
            $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            if ($key.Character -eq 'q' -or $key.Character -eq 'Q') {
                break
            }
        }
        
        Start-Sleep -Seconds 2
    }
}

# Function to stop server
function Stop-Server {
    Clear-Host
    Draw-Box "STOP SERVER" 80 "Red"
    Write-Host ""
    
    $isRunning = Test-ServerRunning
    
    if (-not $isRunning) {
        Write-ColorText "  No server is currently running." "Yellow"
        Write-Host ""
        Draw-BoxEnd 80 "Red"
        Write-Host ""
        Write-Host "  Press any key to return..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        return
    }
    
    Write-ColorText "  WARNING: This will stop all running Minecraft servers!" "Red"
    Write-Host ""
    Write-Host "  Are you sure? (Y/N): " -NoNewline
    $confirm = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Write-Host ""
    
    if ($confirm.Character -eq 'Y' -or $confirm.Character -eq 'y') {
        Write-Host ""
        Write-ColorText "  Stopping servers..." "Yellow"
        Stop-Process -Name java -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        Write-ColorText "  ✓ Servers stopped" "Green"
    } else {
        Write-Host ""
        Write-ColorText "  Cancelled." "Yellow"
    }
    
    Write-Host ""
    Draw-BoxEnd 80 "Red"
    Write-Host ""
    Write-Host "  Press any key to return..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Main loop
while ($true) {
    Show-MainMenu
    $choice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    switch ($choice.Character) {
        '1' { Start-LocalServer }
        '2' { Start-OfficialServer }
        '3' { Show-LiveLogs }
        '4' { 
            Clear-Host
            & ".\SETUP-GROK-NOW.cmd"
            Write-Host ""
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        '5' {
            Clear-Host
            Draw-Box "SWITCH SERVER MODE" 80 "Cyan"
            Write-Host ""
            Write-Host "  [1] LOCAL Mode (Offline)"
            Write-Host "  [2] OFFICIAL Mode (Online + AI)"
            Write-Host ""
            Write-Host "  Select mode (1-2): " -NoNewline
            $modeChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            Write-Host ""
            
            if ($modeChoice.Character -eq '1') {
                python -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.LOCAL)"
                Write-ColorText "  ✓ Mode set to LOCAL" "Green"
            } elseif ($modeChoice.Character -eq '2') {
                python -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.OFFICIAL)"
                Write-ColorText "  ✓ Mode set to OFFICIAL" "Green"
            }
            
            Start-Sleep -Seconds 1
        }
        '6' {
            Clear-Host
            Draw-Box "GENERATE NEW WORLD" 80 "Yellow"
            Write-Host ""
            Write-ColorText "  WARNING: This will DELETE your current world!" "Red"
            Write-Host ""
            Write-Host "  Are you sure? (Y/N): " -NoNewline
            $confirm = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            Write-Host ""
            
            if ($confirm.Character -eq 'Y' -or $confirm.Character -eq 'y') {
                Write-Host ""
                Write-ColorText "  Backing up old world..." "Yellow"
                
                if (Test-Path "worlds\hub\world") {
                    $backupName = "world_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
                    Rename-Item "worlds\hub\world" -NewName $backupName -ErrorAction SilentlyContinue
                }
                
                Remove-Item "worlds\hub\world_nether" -Recurse -Force -ErrorAction SilentlyContinue
                Remove-Item "worlds\hub\world_the_end" -Recurse -Force -ErrorAction SilentlyContinue
                
                Write-ColorText "  ✓ World reset! New world will generate on next start." "Green"
            } else {
                Write-Host ""
                Write-ColorText "  Cancelled." "Yellow"
            }
            
            Write-Host ""
            Draw-BoxEnd 80 "Yellow"
            Write-Host ""
            Write-Host "  Press any key to return..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        '7' { Start-GrokChat }
        '8' {
            Clear-Host
            Draw-Box "PLUGIN MANAGEMENT" 80 "Cyan"
            Write-Host ""
            Write-Host "  Installed Plugins:"
            Write-Host ""
            
            if (Test-Path "worlds\hub\plugins\*.jar") {
                Get-ChildItem "worlds\hub\plugins\*.jar" | ForEach-Object {
                    $size = [math]::Round($_.Length / 1MB, 2)
                    Write-ColorText "    • $($_.Name) ($size MB)" "Green"
                }
            } else {
                Write-ColorText "    No plugins installed yet." "Yellow"
            }
            
            Write-Host ""
            Write-Host "  ────────────────────────────────────────────────────────────────────────"
            Write-Host ""
            Write-Host "  [1] Run Auto Installer"
            Write-Host "  [2] Open Download Guide"
            Write-Host "  [3] Back to Menu"
            Write-Host ""
            Write-Host "  Select (1-3): " -NoNewline
            
            $pChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            
            if ($pChoice.Character -eq '1') {
                Write-Host ""
                Write-Host ""
                python INSTALL-PLUGINS-AUTO.py
                Write-Host ""
                Write-Host "  Press any key to continue..."
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            } elseif ($pChoice.Character -eq '2') {
                Start-Process notepad.exe -ArgumentList "DOWNLOAD-PLUGINS-GUIDE.md"
            }
        }
        '9' { Stop-Server }
        '0' { 
            Clear-Host
            Write-Host ""
            Write-ColorText "  Thanks for using GALION.STUDIO Server Dashboard!" "Cyan"
            Write-Host ""
            Start-Sleep -Seconds 1
            exit 
        }
    }
}

