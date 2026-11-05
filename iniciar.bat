@echo off
cd /d "%~dp0"
echo Iniciando a API (porta 8000)...
start "API - nao feche" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --reload"
echo Iniciando o site (porta 5500)...
start "Site - nao feche" cmd /k "cd /d "%~dp0frontend" && python -m http.server 5500"
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:5500
