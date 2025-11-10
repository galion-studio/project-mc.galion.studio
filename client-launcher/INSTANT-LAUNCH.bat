@echo off
REM INSTANT LAUNCHER - Super Fast Client
REM No delays, minimal checks, maximum speed

echo ⚡ INSTANT LAUNCHER - Starting...

REM Launch with optimized Python launcher
python instant-launcher.py

REM If error, try quick-launcher as fallback
if errorlevel 1 (
    python quick-launcher.py
)

