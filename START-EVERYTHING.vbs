' START EVERYTHING - VBScript launcher (no console windows)
' This works better than CMD on Windows

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get project directory
projectPath = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = projectPath

' 1. Start Docker server
WshShell.Run "docker-compose up -d", 0, True

' Wait for Docker
WScript.Sleep 3000

' 2. Start web control panel (hidden)
WshShell.Run "py web-control-panel\server.py", 0, False

' Wait for server to start
WScript.Sleep 2000

' 3. Start client launcher (visible)
WshShell.Run "py client-launcher\quick-launcher.py", 1, False

' 4. Open browser
WScript.Sleep 1000
WshShell.Run "http://localhost:8080", 1, False

' Show notification
WshShell.Popup "All services started!" & vbCrLf & vbCrLf & "- Minecraft Server" & vbCrLf & "- Control Panel (http://localhost:8080)" & vbCrLf & "- Client Launcher (with Grok AI)", 4, "GALION Started", 64

