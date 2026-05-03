"""
Simulador de Historia Clínica Electrónica (HCE)
API REST con FastAPI para simular integración con sistemas externos
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

app = FastAPI(
    title="HCE Simulator API",
    description="Simulador de Historia Clínica Electrónica para Sistema de Triaje IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PacienteHCE(BaseModel):
    id_hce: str
    numero_documento: str
    nombres: str
    apellidos: str
    fecha_nacimiento: str
    genero: str
    alergias: Optional[List[str]] = []
    enfermedades_cronicas: Optional[List[str]] = []
    medicacion_actual: Optional[List[str]] = []
    ultima_consulta: Optional[str] = None

class TriajeHCE(BaseModel):
    id_triaje: int
    id_hce_paciente: str
    fecha_hora: str
    nivel_urgencia: str
    motivo_consulta: str
    diagnostico: Optional[str] = None
    profesional: str

# Base de datos simulada
pacientes_hce = {
    "HCE-001": {
        "id_hce": "HCE-001",
        "numero_documento": "72345678",
        "nombres": "Juan Carlos",
        "apellidos": "Pérez Gonzales",
        "fecha_nacimiento": "1985-03-15",
        "genero": "Masculino",
        "alergias": ["Penicilina"],
        "enfermedades_cronicas": ["Hipertensión arterial"],
        "medicacion_actual": ["Enalapril 10mg/día"],
        "ultima_consulta": "2025-04-15"
    },
    "HCE-002": {
        "id_hce": "HCE-002",
        "numero_documento": "68234567",
        "nombres": "María Elena",
        "apellidos": "Rodríguez Vega",
        "fecha_nacimiento": "1992-07-22",
        "genero": "Femenino",
        "alergias": [],
        "enfermedades_cronicas": [],
        "medicacion_actual": [],
        "ultima_consulta": "2025-03-10"
    }
}

triajes_recibidos = []

# Endpoints
@app.get("/")
async def root():
    return {
        "servicio": "HCE Simulator API",
        "version": "1.0.0",
        "estado": "activo",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/pacientes/{id_hce}")
async def obtener_paciente(id_hce: str, api_key: str = Header(None)):
    """Obtiene datos de paciente por ID de HCE"""
    if id_hce not in pacientes_hce:
        raise HTTPException(status_code=404, detail="Paciente no encontrado en HCE")
    
    return pacientes_hce[id_hce]

@app.post("/api/triajes")
async def registrar_triaje(triaje: TriajeHCE, api_key: str = Header(None)):
    """Registra un triaje en el sistema HCE"""
    triajes_recibidos.append(triaje.dict())
    return {
        "success": True,
        "mensaje": "Triaje registrado exitosamente en HCE",
        "id_registro": len(triajes_recibidos)
    }

@app.get("/api/triajes")
async def listar_triajes():
    """Lista todos los triajes recibidos"""
    return {
        "total": len(triajes_recibidos),
        "triajes": triajes_recibidos
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
