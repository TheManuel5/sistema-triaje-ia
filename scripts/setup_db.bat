@echo off
chcp 65001 > nul
title Configuración Base de Datos - Sistema Triaje

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Configuración de Base de Datos PostgreSQL           ║
echo ║   Sistema de Triaje Clínico Asistido por IA          ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar que PostgreSQL esté disponible
where psql > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: PostgreSQL no encontrado en el PATH
    echo.
    echo Soluciones:
    echo   1. Asegúrate que PostgreSQL esté iniciado en Laragon
    echo   2. Agrega PostgreSQL al PATH desde Laragon: Menu ^> Tools ^> Path ^> Add PostgreSQL
    echo   3. Reinicia esta ventana
    echo.
    pause
    exit /b 1
)

echo ✓ PostgreSQL encontrado
echo.

REM Solicitar datos de conexión
set /p DB_USER="Usuario PostgreSQL (default: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_NAME="Nombre de la base de datos (default: triaje_db): "
if "%DB_NAME%"=="" set DB_NAME=triaje_db

echo.
echo ════════════════════════════════════════════════════════
echo.
echo [1/4] Creando base de datos '%DB_NAME%'...
echo.

REM Intentar crear la base de datos
psql -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Base de datos creada exitosamente
) else (
    echo    ⚠️  La base de datos ya existe o hubo un error
)

echo.
echo [2/4] Creando usuario 'triaje_user'...
echo.

psql -U %DB_USER% -c "CREATE USER triaje_user WITH PASSWORD 'triaje_pass_2024';" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Usuario creado exitosamente
) else (
    echo    ⚠️  El usuario ya existe o hubo un error
)

echo.
echo [3/4] Otorgando permisos...
echo.

psql -U %DB_USER% -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO triaje_user;" 2>nul
psql -U %DB_USER% -d %DB_NAME% -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO triaje_user;" 2>nul
psql -U %DB_USER% -d %DB_NAME% -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO triaje_user;" 2>nul

echo    ✓ Permisos otorgados

echo.
echo [4/4] Cargando esquema y datos...
echo.

REM Verificar que existen los archivos SQL
if not exist "database\schema.sql" (
    echo ❌ Error: No se encuentra database\schema.sql
    pause
    exit /b 1
)

if not exist "database\seed_data.sql" (
    echo ❌ Error: No se encuentra database\seed_data.sql
    pause
    exit /b 1
)

echo    → Cargando esquema (tablas, vistas, triggers)...
psql -U %DB_USER% -d %DB_NAME% -f database\schema.sql
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Esquema cargado exitosamente
) else (
    echo    ❌ Error al cargar esquema
    pause
    exit /b 1
)

echo.
echo    → Cargando datos de prueba...
psql -U %DB_USER% -d %DB_NAME% -f database\seed_data.sql
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Datos de prueba cargados exitosamente
) else (
    echo    ❌ Error al cargar datos
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════
echo.
echo ✅ Base de datos configurada exitosamente!
echo.
echo Detalles de conexión:
echo   Host:     localhost
echo   Puerto:   5432
echo   Database: %DB_NAME%
echo   Usuario:  %DB_USER%
echo.
echo Datos de prueba cargados:
echo   ✓ 6 usuarios (admin, médicos, enfermeras)
echo   ✓ 8 pacientes de ejemplo
echo   ✓ 8 triajes de ejemplo
echo.
echo Usuarios de acceso al sistema:
echo   admin       / admin123  (Administrador)
echo   dr.martinez / admin123  (Médico)
echo   enf.garcia  / admin123  (Enfermera)
echo   enf.lopez   / admin123  (Triaje)
echo.
echo ════════════════════════════════════════════════════════
echo.

REM Verificar contenido
echo Verificando instalación...
echo.
psql -U %DB_USER% -d %DB_NAME% -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"
echo.
psql -U %DB_USER% -d %DB_NAME% -c "SELECT COUNT(*) as total_usuarios FROM usuarios;"
psql -U %DB_USER% -d %DB_NAME% -c "SELECT COUNT(*) as total_pacientes FROM pacientes;"
psql -U %DB_USER% -d %DB_NAME% -c "SELECT COUNT(*) as total_triajes FROM triajes;"
echo.

echo Presiona cualquier tecla para continuar...
pause > nul
