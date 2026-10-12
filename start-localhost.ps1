# PowerShell launcher for portfolio localhost server
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting Readuanul Farid Fahim Portfolio on Localhost" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "Using uv to run development server..." -ForegroundColor Green
    uv run serve.py
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Using python to run development server..." -ForegroundColor Green
    python serve.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Write-Host "Using py to run development server..." -ForegroundColor Green
    py serve.py
} elseif (Test-Path "$env:USERPROFILE\.local\bin\python3.14.exe") {
    Write-Host "Using local python3.14 to run development server..." -ForegroundColor Green
    & "$env:USERPROFILE\.local\bin\python3.14.exe" serve.py
} else {
    Write-Host "Error: No Python or uv runtime found. Please install Python." -ForegroundColor Red
    Pause
}
