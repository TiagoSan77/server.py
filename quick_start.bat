@echo off
cd /d "%~dp0"
start /b python server.py --silent
timeout 3 >nul
ngrok http 127.0.0.1:5000