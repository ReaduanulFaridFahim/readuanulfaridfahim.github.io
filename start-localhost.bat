@echo off
title Readuanul Farid Fahim Portfolio - Local Server
cd /d "%~dp0"

echo ========================================================
echo   Starting Readuanul Farid Fahim Portfolio on Localhost
echo ========================================================
echo.

where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using uv runner...
    uv run serve.py
    goto :end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using python runner...
    python serve.py
    goto :end
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Using py runner...
    py serve.py
    goto :end
)

echo Warning: Neither uv nor python was found in PATH.
echo Trying standard python3.14 path...
if exist "%USERPROFILE%\.local\bin\python3.14.exe" (
    "%USERPROFILE%\.local\bin\python3.14.exe" serve.py
    goto :end
)

echo Error: Python or uv could not be located.
echo Please install Python or uv to run the local server.
pause

:end
