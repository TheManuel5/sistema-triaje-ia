@echo off
chcp 65001 > nul
title Sistema de Triaje Clínico - Laragon

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Sistema de Triaje Clínico Asistido por IA          ║
echo ║   Versión 1.0 - Laragon Edition                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "frontend\app.py" (
    echo ❌ Error: No se encuentra app.py
    echo    Ejecutar este script desde la raíz del proyecto
    pause
    exit /b 1
)

echo [1/4] Verificando entornos virtuales...

REM Crear entorno virtual del frontend si no existe
if not exist "frontend\venv" (
    echo    Creando entorno virtual del frontend...
    cd frontend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    echo    ✓ Entorno virtual del frontend existe
)

REM Crear entorno virtual del backend si no existe
if not exist "backend\venv" (
    echo    Creando entorno virtual del backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    echo    ✓ Entorno virtual del backend existe
)

echo.
echo [2/4] Verificando archivo de configuración...

REM Verificar que existe .env
if not exist ".env" (
    echo    ⚠️  Archivo .env no encontrado
    echo    Copiando desde .env.example...
    copy .env.example .env
    echo.
    echo    ⚠️  IMPORTANTE: Edita el archivo .env antes de continuar
    echo    Especialmente configura tu OPENAI_API_KEY
    echo.
    notepad .env
    echo.
    echo    Presiona cualquier tecla cuando hayas guardado .env...
    pause > nul
) else (
    echo    ✓ Archivo .env encontrado
)

echo.
echo [3/4] Iniciando servicios...
echo.

REM Cargar variables del .env
for /f "tokens=1,2 delims==" %%a in (.env) do (
    set %%a=%%b
)

echo    → Iniciando HCE Simulator (Backend)...
start "HCE Simulator - Puerto 8000" cmd /k "cd /d %CD%\backend && venv\Scripts\activate && set DB_HOST=%DB_HOST% && set DB_PORT=%DB_PORT% && set DB_NAME=%DB_NAME% && set DB_USER=%DB_USER% && set DB_PASSWORD=%DB_PASSWORD% && python -m uvicorn hce_simulator:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo    → Iniciando Frontend Streamlit...
start "Streamlit Frontend - Puerto 8501" cmd /k "cd /d %CD%\frontend && venv\Scripts\activate && set DB_HOST=%DB_HOST% && set DB_PORT=%DB_PORT% && set DB_NAME=%DB_NAME% && set DB_USER=%DB_USER% && set DB_PASSWORD=%DB_PASSWORD% && set OPENAI_API_KEY=%OPENAI_API_KEY% && set HCE_API_URL=%HCE_API_URL% && streamlit run app.py"

timeout /t 3 /nobreak > nul

echo    → Iniciando n8n (Workflows) - Opcional...
where n8n > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "n8n Workflows - Puerto 5678" cmd /k "set DB_TYPE=postgresdb && set DB_POSTGRESDB_HOST=%DB_HOST% && set DB_POSTGRESDB_PORT=%DB_PORT% && set DB_POSTGRESDB_DATABASE=%DB_NAME% && set DB_POSTGRESDB_USER=%DB_USER% && set DB_POSTGRESDB_PASSWORD=%DB_PASSWORD% && set N8N_ENCRYPTION_KEY=%N8N_ENCRYPTION_KEY% && set N8N_BASIC_AUTH_ACTIVE=true && set N8N_BASIC_AUTH_USER=%N8N_BASIC_AUTH_USER% && set N8N_BASIC_AUTH_PASSWORD=%N8N_BASIC_AUTH_PASSWORD% && n8n start"
) else (
    echo    ⚠️  n8n no instalado (npm install -g n8n para instalarlo)
)

echo.
echo [4/4] Sistema iniciado correctamente
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                SERVICIOS DISPONIBLES                   ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  Frontend Streamlit:  http://localhost:8501           ║
echo ║  HCE Simulator API:   http://localhost:8000           ║
echo ║  n8n Workflows:       http://localhost:5678           ║
echo ║  PostgreSQL:          localhost:5432                  ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Credenciales de acceso:
echo   Usuario:    admin
echo   Contraseña: admin123
echo.
echo 💡 Tip: Los servicios se ejecutan en ventanas separadas
echo    No cierres esas ventanas mientras uses el sistema
echo.
echo Presiona cualquier tecla para abrir el navegador...
pause > nul

REM Abrir navegador
start http://localhost:8501

echo.
echo Para detener todos los servicios, cierra las ventanas de:
echo   - HCE Simulator
echo   - Streamlit Frontend  
echo   - n8n Workflows
echo.
pause
