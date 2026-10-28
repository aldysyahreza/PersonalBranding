@echo off
cd /d "%~dp0"
node scripts\launcher.mjs --uninstall-autostart
pause
