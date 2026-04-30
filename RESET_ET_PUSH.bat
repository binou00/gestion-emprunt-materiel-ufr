@echo off
REM Double-clique pour nettoyer + pousser sur GitHub depuis zero
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0RESET_ET_PUSH.ps1"
pause
