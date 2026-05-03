# Sistema de Triaje Clínico Asistido por IA

## 📋 Descripción General

Sistema completo de triaje clínico que integra Inteligencia Artificial para asistir en la clasificación de pacientes según nivel de urgencia. Incluye integración con Historias Clínicas Electrónicas (HCE), automatización de flujos de trabajo con n8n, y dashboards interactivos para análisis operacional y de gestión.

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Frontend      │◄────►│   n8n           │◄────►│   PostgreSQL    │
│   (Streamlit)   │      │   (Workflows)   │      │   (Base Datos)  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
        │                        │                          │
        │                        │                          │
        ▼                        ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   OpenAI API    │      │   HCE Simulada  │      │   Reportes PDF  │
│   (Triaje IA)   │      │   (REST API)    │      │   (fpdf2)       │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## 🚀 Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | Streamlit 1.31+ |
| Backend | n8n (workflows de automatización) |
| Base de Datos | PostgreSQL 15+ |
| IA | OpenAI GPT-4 / GPT-3.5-turbo |
| Reportes | fpdf2, Plotly |
| Containerización | Docker, Docker Compose |

## 📁 Estructura del Proyecto

```
sistema-triaje-ia/
├── frontend/               # Aplicación Streamlit
│   ├── app.py             # Aplicación principal
│   ├── pages/             # Páginas del sistema
│   ├── components/        # Componentes reutilizables
│   ├── utils/             # Utilidades y helpers
│   └── requirements.txt   # Dependencias Python
├── backend/               # Scripts backend y APIs
│   ├── hce_simulator.py   # Simulador HCE
│   └── requirements.txt
├── database/              # Scripts de base de datos
│   ├── schema.sql         # Esquema de tablas
│   ├── seed_data.sql      # Datos de prueba
│   └── migrations/        # Migraciones
├── n8n-workflows/         # Workflows exportados
│   ├── triaje_notificacion.json
│   ├── sincronizacion_hce.json
│   └── reporte_diario.json
├── docs/                  # Documentación
│   ├── manual_usuario.md
│   ├── manual_instalacion.md
│   └── api_documentation.md
├── scripts/               # Scripts de despliegue
│   ├── deploy.sh
│   ├── setup_db.sh
│   └── test_connection.py
├── docker-compose.yml     # Orquestación de contenedores
├── .env.example           # Variables de entorno ejemplo
└── README.md              # Este archivo
```

## 🔧 Requisitos Previos

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+
- PostgreSQL 15+ (o usar el contenedor Docker)
- Cuenta de OpenAI con API Key

## ⚡ Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sistema-triaje-ia.git
cd sistema-triaje-ia
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
nano .env  # Editar con tus credenciales
```

Variables principales:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=triaje_db
DB_USER=triaje_user
DB_PASSWORD=tu_password_seguro

# OpenAI
OPENAI_API_KEY=sk-tu-api-key-aqui

# n8n
N8N_ENCRYPTION_KEY=tu_clave_encriptacion
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=tu_password

# Email (para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
```

### 3. Despliegue con Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar que los servicios estén corriendo
docker-compose ps
```

Servicios disponibles:
- **Streamlit Frontend**: http://localhost:8501
- **n8n Workflows**: http://localhost:5678
- **PostgreSQL**: localhost:5432
- **HCE Simulator**: http://localhost:8000

### 4. Inicializar la base de datos

```bash
# Ejecutar script de inicialización
./scripts/setup_db.sh

# O manualmente:
docker-compose exec postgres psql -U triaje_user -d triaje_db -f /docker-entrypoint-initdb.d/schema.sql
docker-compose exec postgres psql -U triaje_user -d triaje_db -f /docker-entrypoint-initdb.d/seed_data.sql
```

### 5. Importar workflows de n8n

1. Acceder a n8n: http://localhost:5678
2. Crear cuenta inicial (usuario/contraseña de .env)
3. Importar workflows desde carpeta `n8n-workflows/`:
   - `triaje_notificacion.json`
   - `sincronizacion_hce.json`
   - `reporte_diario.json`

### 6. Acceder al sistema

Abrir navegador en: **http://localhost:8501**

Credenciales por defecto:
- Usuario: `admin`
- Contraseña: `admin123` (cambiar en producción)

## 📚 Funcionalidades Principales

### 1. Módulo de Pacientes
- ✅ Registro de pacientes con datos demográficos
- ✅ Búsqueda y visualización de historial
- ✅ Integración con HCE externa

### 2. Triaje Clínico con IA
- ✅ Captura de signos vitales
- ✅ Registro de síntomas y antecedentes
- ✅ Análisis automático con IA (OpenAI GPT-4)
- ✅ Clasificación de urgencia (Bajo, Moderado, Alto, Crítico)
- ✅ Recomendaciones clínicas automáticas

### 3. Automatización con n8n
- ✅ Notificaciones automáticas para casos críticos
- ✅ Sincronización con HCE externa
- ✅ Reportes diarios por email
- ✅ Alertas por Telegram (opcional)

### 4. Dashboards y Reportes
- ✅ Dashboard Operacional (tiempo real)
- ✅ Dashboard de Gestión (métricas agregadas)
- ✅ Exportación a PDF
- ✅ Gráficos interactivos con Plotly
- ✅ Filtros por fecha, profesional, nivel de urgencia

### 5. Seguridad y Auditoría
- ✅ Autenticación de usuarios
- ✅ Registro de auditoría de todas las acciones
- ✅ Encriptación de datos sensibles
- ✅ Control de acceso por roles

## 🧪 Ejecutar Tests

```bash
# Tests unitarios
cd frontend
pytest tests/

# Test de integración
python scripts/test_connection.py

# Test de carga (opcional)
locust -f tests/load_test.py
```

## 📊 Uso del Sistema

### Registrar un Triaje

1. Ir a "Nuevo Triaje" en el menú lateral
2. Seleccionar o registrar paciente
3. Ingresar signos vitales
4. Describir síntomas principales
5. Hacer clic en "Analizar con IA"
6. Revisar recomendaciones
7. Guardar triaje

### Generar Reportes

1. Ir a "Reportes" en el menú lateral
2. Seleccionar tipo de dashboard (Operacional/Gestión)
3. Configurar filtros de fecha
4. Visualizar gráficos interactivos
5. Exportar a PDF si es necesario

### Configurar Workflows en n8n

1. Acceder a http://localhost:5678
2. Activar workflows importados
3. Configurar credenciales de email/Telegram
4. Probar ejecución manual
5. Activar ejecución automática

## 🔒 Seguridad

### Consideraciones de Producción

1. **Cambiar contraseñas por defecto**
2. **Usar HTTPS** con certificados SSL
3. **Configurar firewall** para PostgreSQL
4. **Habilitar backups** automáticos
5. **Implementar rate limiting**
6. **Configurar logs** centralizados
7. **Actualizar dependencias** regularmente

### Backup de Base de Datos

```bash
# Backup manual
docker-compose exec postgres pg_dump -U triaje_user triaje_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker-compose exec -T postgres psql -U triaje_user triaje_db < backup_20250501.sql
```

## 🐛 Solución de Problemas

### El frontend no se conecta a la base de datos

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps postgres

# Revisar logs
docker-compose logs postgres

# Verificar conectividad
docker-compose exec streamlit python scripts/test_connection.py
```

### n8n no ejecuta workflows

```bash
# Verificar estado de n8n
docker-compose logs n8n

# Reiniciar servicio
docker-compose restart n8n

# Verificar credenciales en workflows
```

### Error de API OpenAI

```bash
# Verificar que la API key esté configurada
docker-compose exec streamlit env | grep OPENAI

# Probar conexión
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## 📈 Métricas de Rendimiento

- Tiempo de respuesta IA: ~2-5 segundos
- Capacidad: 1000+ triajes/día
- Concurrencia: 50+ usuarios simultáneos
- Disponibilidad objetivo: 99.5%

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: [Tu Nombre]
- **Arquitecto de Software**: [Nombre]
- **Experto en IA**: [Nombre]

## 📞 Soporte

- **Email**: soporte@triaje-ia.com
- **Documentación**: https://docs.triaje-ia.com
- **Issues**: https://github.com/tu-usuario/sistema-triaje-ia/issues

## 🗺️ Roadmap

### Versión 2.0 (Q3 2025)
- [ ] Integración con FHIR estándar
- [ ] App móvil (React Native)
- [ ] Soporte multiidioma
- [ ] Machine Learning local (sin OpenAI)

### Versión 2.1 (Q4 2025)
- [ ] Reconocimiento de voz
- [ ] Análisis de imágenes médicas
- [ ] Integración con dispositivos IoT

---

**Desarrollado con ❤️ para mejorar la atención médica**
