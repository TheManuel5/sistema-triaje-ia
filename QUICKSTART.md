# 🚀 Guía de Inicio Rápido

## Sistema de Triaje Clínico Asistido por IA

### Instalación en 5 Minutos

#### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/sistema-triaje-ia.git
cd sistema-triaje-ia

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus credenciales

# 3. Desplegar
./scripts/deploy.sh

# 4. Acceder al sistema
# Frontend: http://localhost:8501
# Usuario: admin | Contraseña: admin123
```

#### Opción 2: Manual (Sin Docker)

```bash
# 1. Instalar PostgreSQL 15+
sudo apt install postgresql postgresql-contrib

# 2. Crear base de datos
sudo -u postgres psql
CREATE DATABASE triaje_db;
CREATE USER triaje_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE triaje_db TO triaje_user;
\q

# 3. Inicializar esquema
psql -U triaje_user -d triaje_db -f database/schema.sql
psql -U triaje_user -d triaje_db -f database/seed_data.sql

# 4. Instalar Python dependencies
cd frontend
pip install -r requirements.txt

# 5. Configurar variables de entorno
export DB_HOST=localhost
export DB_NAME=triaje_db
export DB_USER=triaje_user
export DB_PASSWORD=tu_password
export OPENAI_API_KEY=sk-tu-api-key

# 6. Ejecutar aplicación
streamlit run app.py
```

### Configuración Inicial

#### 1. OpenAI API Key

Obtener en: https://platform.openai.com/api-keys

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

#### 2. Configurar n8n

1. Acceder a http://localhost:5678
2. Crear cuenta inicial
3. Importar workflows desde `n8n-workflows/`
4. Configurar credenciales de email/Telegram
5. Activar workflows

#### 3. Primer Triaje

1. Login en http://localhost:8501
2. Usuario: `admin` | Contraseña: `admin123`
3. Ir a "Nuevo Triaje"
4. Seleccionar paciente de prueba
5. Ingresar signos vitales
6. Describir síntomas
7. Click en "Analizar con IA"
8. Guardar triaje

### Verificación del Sistema

```bash
# Estado de servicios Docker
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Test de conexión a BD
python scripts/test_connection.py

# Health checks
curl http://localhost:8501/_stcore/health
curl http://localhost:8000/health
curl http://localhost:5678/healthz
```

### Solución Rápida de Problemas

#### Error de Conexión a BD

```bash
# Reiniciar PostgreSQL
docker-compose restart postgres

# Ver logs
docker-compose logs postgres
```

#### Frontend no carga

```bash
# Reiniciar Streamlit
docker-compose restart streamlit

# Verificar logs
docker-compose logs streamlit
```

#### OpenAI no responde

```bash
# Verificar API key
echo $OPENAI_API_KEY

# Test manual
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Próximos Pasos

1. ✅ Cambiar contraseñas por defecto
2. ✅ Configurar backups automáticos
3. ✅ Personalizar workflows de n8n
4. ✅ Ajustar parámetros de IA
5. ✅ Importar pacientes reales
6. ✅ Configurar HTTPS para producción

### Soporte

- 📧 Email: soporte@triaje-ia.com
- 📚 Documentación: `docs/`
- 🐛 Issues: GitHub Issues
- 💬 Telegram: [Grupo de soporte]

---

**¡Listo para comenzar! 🎉**
