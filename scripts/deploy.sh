#!/bin/bash

#######################################
# Script de Despliegue Automático
# Sistema de Triaje Clínico Asistido por IA
#######################################

set -e  # Salir si hay errores

echo "========================================="
echo "Sistema de Triaje Clínico Asistido por IA"
echo "Script de Despliegue v1.0"
echo "========================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar requisitos
echo -e "${YELLOW}[1/6] Verificando requisitos...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker y Docker Compose encontrados${NC}"

# Verificar archivo .env
echo -e "${YELLOW}[2/6] Verificando configuración...${NC}"

if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado. Copiando desde .env.example${NC}"
    cp .env.example .env
    echo -e "${RED}❗ IMPORTANTE: Edita el archivo .env con tus credenciales antes de continuar${NC}"
    echo -e "${YELLOW}   nano .env${NC}"
    read -p "Presiona ENTER cuando hayas configurado .env..."
fi

echo -e "${GREEN}✅ Configuración encontrada${NC}"

# Detener contenedores existentes
echo -e "${YELLOW}[3/6] Deteniendo contenedores existentes...${NC}"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✅ Contenedores detenidos${NC}"

# Construir imágenes
echo -e "${YELLOW}[4/6] Construyendo imágenes Docker...${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✅ Imágenes construidas${NC}"

# Iniciar servicios
echo -e "${YELLOW}[5/6] Iniciando servicios...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Servicios iniciados${NC}"

# Esperar a que PostgreSQL esté listo
echo -e "${YELLOW}Esperando a que PostgreSQL esté listo...${NC}"
sleep 10

# Verificar estado
echo -e "${YELLOW}[6/6] Verificando estado de servicios...${NC}"
docker-compose ps

echo ""
echo "========================================="
echo -e "${GREEN}✅ Despliegue completado exitosamente${NC}"
echo "========================================="
echo ""
echo "Servicios disponibles:"
echo "  - Frontend (Streamlit): http://localhost:8501"
echo "  - n8n (Workflows):      http://localhost:5678"
echo "  - HCE Simulator:        http://localhost:8000"
echo "  - PostgreSQL:           localhost:5432"
echo ""
echo "Credenciales por defecto:"
echo "  Usuario: admin"
echo "  Contraseña: admin123"
echo ""
echo "⚠️  IMPORTANTE: Cambia las contraseñas en producción"
echo ""
echo "Para ver logs:"
echo "  docker-compose logs -f [servicio]"
echo ""
echo "Para detener:"
echo "  docker-compose down"
echo ""
