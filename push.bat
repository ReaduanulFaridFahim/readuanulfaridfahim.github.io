@echo off
set "PATH=C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd;%PATH%"
echo ========================================================
echo   Pushing Portfolio to GitHub (main branch)
echo ========================================================
git push -u origin main
pause
