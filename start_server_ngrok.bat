@echo off
title 🌐 Servidor Flask + ngrok
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  🚀 INICIANDO SERVIDOR FLASK                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📂 Navegando para o diretório do servidor...
cd /d "%~dp0"

echo 🔄 Verificando se o servidor já está rodando...
tasklist | findstr "python.exe" >nul
if %errorlevel% == 0 (
    echo ⚠️  Um processo Python já está em execução
    echo 🛑 Encerrando processos Python anteriores...
    taskkill /f /im python.exe >nul 2>&1
    timeout 2 >nul
)

echo.
echo 🚀 Iniciando servidor Flask...
start /b python server.py --silent

echo ⏳ Aguardando servidor inicializar (5 segundos)...
timeout 5 >nul

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔗 INICIANDO NGROK                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🌐 Expondo servidor publicamente via ngrok...
echo 📋 A URL pública será exibida abaixo:
echo.

ngrok http 127.0.0.1:5000