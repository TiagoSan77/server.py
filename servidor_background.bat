@echo off
echo 🚀 Iniciando servidor em background...
echo 📍 Servidor será executado em: http://127.0.0.1:5000
echo ⚡ Esta janela será fechada mas o servidor continuará ativo

REM Usar PowerShell para executar o servidor em background e manter o processo independente
powershell -Command "Start-Process python -ArgumentList 'server.py --silent' -WindowStyle Hidden"

echo ✅ Servidor iniciado em background!
echo 🌐 Acesse: http://127.0.0.1:5000
echo.

REM Fechar esta janela
exit