@echo off
title Microphone Volume Keeper
cd /d "%~dp0"

echo Starting Microphone Volume Keeper...
python src/microphone_volume_keeper.py

if errorlevel 1 (
    echo.
    echo Error starting the application.
    echo Make sure Python and dependencies are installed.
    echo.
    pause
)
