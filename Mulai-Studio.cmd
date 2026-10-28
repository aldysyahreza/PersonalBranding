@echo off
cd /d "%~dp0"
node scripts\launcher.mjs %*
if errorlevel 1 pause
