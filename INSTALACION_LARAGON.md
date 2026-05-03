# 🚀 Instalación en Laragon (Windows)

## Sistema de Triaje Clínico Asistido por IA

### Requisitos Previos

✅ Laragon instalado (con PostgreSQL habilitado)  
✅ Python 3.10+ instalado  
✅ Node.js 18+ instalado (para n8n)  
✅ Git (opcional)

---

## 📋 Guía de Instalación Paso a Paso

### PASO 1: Configurar PostgreSQL en Laragon

1. **Iniciar PostgreSQL en Laragon**
   - Abrir Laragon
   - Click derecho en Laragon → PostgreSQL → Start
   - Verificar que PostgreSQL esté corriendo (ícono verde)

2. **Crear la Base de Datos**

Opción A - Usando pgAdmin (GUI):
- Abrir pgAdmin desde Laragon
- Conectar a localhost
- Click derecho en "Databases" → Create → Database
  - Database: `triaje_db`
  - Owner: `postgres`
  - Encoding: `UTF8`

Opción B - Usando Terminal:
```bash
# Abrir terminal de Laragon (Menu → Terminal)
psql -U postgres

# Dentro de psql:
CREATE DATABASE triaje_db;
CREATE USER triaje_user WITH PASSWORD 'triaje_pass_2024';
GRANT ALL PRIVILEGES ON DATABASE triaje_db TO triaje_user;
\q
```

3. **Cargar el Schema y Datos de Prueba**

```bash
# Navegar a la carpeta del proyecto
cd C:\laragon\www\sistema-triaje-ia

# Cargar schema
psql -U postgres -d triaje_db -f database/schema.sql

# Cargar datos de prueba
psql -U postgres -d triaje_db -f database/seed_data.sql
```

---

### PASO 2: Instalar Dependencias de Python

1. **Crear entorno virtual (recomendado)**

```bash
cd C:\laragon\www\sistema-triaje-ia\frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

---

### PASO 3: Configurar Variables de Entorno

1. **Crear archivo de configuración**

```bash
cd C:\laragon\www\sistema-triaje-ia
copy .env.example .env
```

2. **Editar `.env` con tus datos**

```env
# Base de datos (PostgreSQL de Laragon)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=triaje_db
DB_USER=postgres
DB_PASSWORD=tu_password_de_laragon

# OpenAI API
OPENAI_API_KEY=sk-tu-api-key-aqui
OPENAI_MODEL=gpt-4-turbo-preview

# HCE Simulator
HCE_API_URL=http://localhost:8000

# n8n
N8N_WEBHOOK_URL=http://localhost:5678/webhook
```

---

### PASO 4: Iniciar el Backend (HCE Simulator)

1. **Abrir nueva terminal de Laragon**

```bash
cd C:\laragon\www\sistema-triaje-ia\backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python -m uvicorn hce_simulator:app --host 0.0.0.0 --port 8000
```

Dejar esta terminal abierta. El HCE Simulator estará en http://localhost:8000

---

### PASO 5: Iniciar el Frontend (Streamlit)

1. **Abrir otra terminal de Laragon**

```bash
cd C:\laragon\www\sistema-triaje-ia\frontend

# Activar entorno virtual
venv\Scripts\activate

# Configurar variables de entorno
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=triaje_db
set DB_USER=postgres
set DB_PASSWORD=tu_password
set OPENAI_API_KEY=sk-tu-api-key

# Iniciar Streamlit
streamlit run app.py
```

Dejar esta terminal abierta. El sistema estará en http://localhost:8501

---

### PASO 6: Instalar y Configurar n8n (Opcional)

1. **Instalar n8n globalmente**

```bash
npm install -g n8n
```

2. **Configurar n8n con PostgreSQL de Laragon**

Crear archivo `n8n-config.env`:

```env
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=triaje_db
DB_POSTGRESDB_USER=postgres
DB_POSTGRESDB_PASSWORD=tu_password
N8N_ENCRYPTION_KEY=n8n-encryption-key-2024
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin123
```

3. **Iniciar n8n**

```bash
# Cargar variables de entorno y ejecutar
n8n start
```

n8n estará en http://localhost:5678

4. **Importar workflows**

- Acceder a http://localhost:5678
- Login con admin/admin123
- Click en "Import Workflow"
- Seleccionar archivos de `n8n-workflows/`
- Configurar credenciales de email/Telegram
- Activar workflows

---

## 🎯 Verificación de la Instalación

### 1. Verificar PostgreSQL

```bash
psql -U postgres -d triaje_db -c "SELECT COUNT(*) FROM usuarios;"
```

Debe retornar: 6 usuarios

### 2. Verificar Backend

Abrir navegador: http://localhost:8000

Debe mostrar:
```json
{
  "servicio": "HCE Simulator API",
  "version": "1.0.0",
  "estado": "activo"
}
```

### 3. Verificar Frontend

Abrir navegador: http://localhost:8501

Debe mostrar la página de login

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 📝 Script de Inicio Rápido (Windows)

Crear archivo `iniciar.bat` en la raíz del proyecto:

```batch
@echo off
echo ========================================
echo Sistema de Triaje Clinico - Laragon
echo ========================================
echo.

echo [1/3] Iniciando HCE Simulator...
start "HCE Simulator" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn hce_simulator:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo [2/3] Iniciando Frontend Streamlit...
start "Streamlit Frontend" cmd /k "cd frontend && venv\Scripts\activate && streamlit run app.py"

timeout /t 3 /nobreak > nul

echo [3/3] Iniciando n8n (opcional)...
start "n8n Workflows" cmd /k "n8n start"

echo.
echo ========================================
echo Sistema iniciado correctamente!
echo ========================================
echo.
echo Frontend:     http://localhost:8501
echo HCE API:      http://localhost:8000
echo n8n:          http://localhost:5678
echo.
echo Presiona cualquier tecla para salir...
pause > nul
```

Ejecutar: doble click en `iniciar.bat`

---

## 🛠️ Solución de Problemas

### Error: "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### Error: "Connection refused" en PostgreSQL

1. Verificar que PostgreSQL esté corriendo en Laragon
2. Verificar puerto en Laragon: Menu → PostgreSQL → Settings
3. Actualizar `DB_PORT` en `.env`

### Error: "streamlit: command not found"

```bash
# Asegurarse de estar en el entorno virtual
cd frontend
venv\Scripts\activate
pip install streamlit
```

### Error: OpenAI API Key inválida

1. Obtener API key en: https://platform.openai.com/api-keys
2. Actualizar en `.env`: `OPENAI_API_KEY=sk-...`
3. Reiniciar Streamlit

---

## 📊 Estructura en Laragon

```
C:\laragon\www\
└── sistema-triaje-ia\
    ├── frontend\
    │   ├── venv\          (entorno virtual Python)
    │   └── app.py
    ├── backend\
    │   ├── venv\          (entorno virtual Python)
    │   └── hce_simulator.py
    ├── database\
    │   ├── schema.sql
    │   └── seed_data.sql
    ├── .env               (configuración)
    └── iniciar.bat        (script de inicio)
```

---

## 🚀 Próximos Pasos

1. ✅ Cambiar contraseñas por defecto
2. ✅ Configurar email para notificaciones
3. ✅ Personalizar parámetros de IA
4. ✅ Importar pacientes reales
5. ✅ Configurar backups de PostgreSQL

---

## 💡 Consejos para Laragon

### Agregar al PATH de Laragon

Laragon → Menu → Tools → Path → Add Python/PostgreSQL

### Crear acceso directo en Laragon

Laragon → Menu → Quick App → Add:
- Nombre: Triaje IA
- URL: http://localhost:8501

### Configurar inicio automático

Crear servicio de Windows o agregar `iniciar.bat` al inicio de Windows

---

## 📞 Soporte

¿Problemas con la instalación en Laragon?

- Verificar logs en cada terminal
- Revisar configuración de PostgreSQL en Laragon
- Asegurar que los puertos 8501, 8000, 5678 estén libres

---

**¡Sistema listo para usar en Laragon! 🎉**
