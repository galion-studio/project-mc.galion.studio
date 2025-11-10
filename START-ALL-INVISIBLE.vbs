' START ALL - Completely Invisible Launcher
' Launches all services without any visible windows
' Double-click this file to start everything silently

Set WshShell = CreateObject("WScript.Shell")

' Change to project directory
projectPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = projectPath

' Start Minecraft server (if not running)
WshShell.Run "docker ps | findstr titan-hub >nul 2>&1 || docker-compose up -d", 0, False

' Wait a moment for Docker to initialize
WScript.Sleep 2000

' Start GUI Developer Console (completely hidden)
WshShell.Run "pythonw dev-console\console_main.py", 0, False

' Start Terminal Console (completely hidden)
WshShell.Run "pythonw console-chat.py", 0, False

' Start Client Launcher (minimized)
If CreateObject("Scripting.FileSystemObject").FileExists("client-launcher\dist\GalionLauncher-Enhanced-Final.exe") Then
    WshShell.Run """client-launcher\dist\GalionLauncher-Enhanced-Final.exe""", 7, False
End If

' Show notification that services started
WshShell.Popup "All services started successfully!" & vbCrLf & vbCrLf & "- Minecraft Server" & vbCrLf & "- AI Control Center" & vbCrLf & "- Terminal Console" & vbCrLf & "- Client Launcher", 3, "GALION Services", 64

