@echo off
REM ============================================================
REM  Double-clique ce fichier pour pousser le projet sur GitHub
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0push_github.ps1"
pause
