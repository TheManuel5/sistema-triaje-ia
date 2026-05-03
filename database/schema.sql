-- ========================================
-- SCHEMA: SISTEMA DE TRIAJE CLÍNICO ASISTIDO POR IA
-- Versión: 1.0
-- Fecha: 2025-01-01
-- ========================================

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ========================================
-- TABLA: USUARIOS
-- ========================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) UNIQUE NOT NULL,
    nombre_completo VARCHAR(200) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN ('admin', 'medico', 'enfermera', 'triaje', 'visualizador')),
    activo BOOLEAN DEFAULT true,
    ultimo_acceso TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA: PACIENTES
-- ========================================
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente SERIAL PRIMARY KEY,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    tipo_documento VARCHAR(10) NOT NULL CHECK (tipo_documento IN ('DNI', 'CE', 'PASAPORTE', 'OTRO')),
    nombres VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20) CHECK (genero IN ('Masculino', 'Femenino', 'Otro', 'Prefiero no decir')),
    telefono VARCHAR(20),
    email VARCHAR(150),
    direccion TEXT,
    distrito VARCHAR(100),
    provincia VARCHAR(100),
    departamento VARCHAR(100),
    contacto_emergencia_nombre VARCHAR(200),
    contacto_emergencia_telefono VARCHAR(20),
    contacto_emergencia_relacion VARCHAR(50),
    grupo_sanguineo VARCHAR(5),
    alergias TEXT,
    enfermedades_cronicas TEXT,
    medicacion_actual TEXT,
    seguro_medico VARCHAR(100),
    numero_poliza VARCHAR(50),
    id_hce_externo VARCHAR(100), -- ID en sistema HCE externo
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT true
);

-- Índices para pacientes
CREATE INDEX idx_pacientes_documento ON pacientes(numero_documento);
CREATE INDEX idx_pacientes_nombres ON pacientes(nombres, apellidos);
CREATE INDEX idx_pacientes_hce ON pacientes(id_hce_externo);

-- ========================================
-- TABLA: TRIAJES
-- ========================================
CREATE TABLE IF NOT EXISTS triajes (
    id_triaje SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL REFERENCES pacientes(id_paciente) ON DELETE CASCADE,
    id_usuario_triaje INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    fecha_hora_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Signos vitales
    presion_arterial_sistolica INTEGER,
    presion_arterial_diastolica INTEGER,
    frecuencia_cardiaca INTEGER,
    frecuencia_respiratoria INTEGER,
    temperatura DECIMAL(4,2),
    saturacion_oxigeno INTEGER,
    peso DECIMAL(5,2),
    talla DECIMAL(5,2),
    
    -- Información clínica
    motivo_consulta TEXT NOT NULL,
    sintomas_principales TEXT,
    tiempo_evolucion VARCHAR(100),
    dolor_escala INTEGER CHECK (dolor_escala BETWEEN 0 AND 10),
    dolor_ubicacion TEXT,
    
    -- Antecedentes inmediatos
    antecedentes_personales TEXT,
    medicamentos_actuales TEXT,
    alergias_conocidas TEXT,
    
    -- Resultados del análisis de IA
    nivel_urgencia VARCHAR(20) NOT NULL CHECK (nivel_urgencia IN ('Bajo', 'Moderado', 'Alto', 'Crítico')),
    nivel_urgencia_score DECIMAL(3,2), -- 0.00 a 1.00
    diagnosticos_diferenciales TEXT,
    recomendaciones_ia TEXT,
    justificacion_ia TEXT,
    modelo_ia_utilizado VARCHAR(50),
    tiempo_respuesta_ia INTEGER, -- en milisegundos
    
    -- Evaluación médica (posterior al triaje)
    diagnostico_final TEXT,
    tratamiento_indicado TEXT,
    examenes_solicitados TEXT,
    derivacion VARCHAR(100), -- Servicio al que se deriva
    estado_triaje VARCHAR(30) DEFAULT 'Pendiente' CHECK (estado_triaje IN ('Pendiente', 'En Atención', 'Atendido', 'Derivado', 'Alta')),
    
    -- Tiempos
    tiempo_espera_minutos INTEGER,
    tiempo_atencion_minutos INTEGER,
    fecha_hora_atencion TIMESTAMP,
    fecha_hora_alta TIMESTAMP,
    
    -- Metadata
    observaciones TEXT,
    sincronizado_hce BOOLEAN DEFAULT false,
    fecha_sincronizacion_hce TIMESTAMP,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para triajes
CREATE INDEX idx_triajes_paciente ON triajes(id_paciente);
CREATE INDEX idx_triajes_fecha ON triajes(fecha_hora_registro);
CREATE INDEX idx_triajes_nivel_urgencia ON triajes(nivel_urgencia);
CREATE INDEX idx_triajes_estado ON triajes(estado_triaje);
CREATE INDEX idx_triajes_usuario ON triajes(id_usuario_triaje);

-- ========================================
-- TABLA: AUDITORÍA
-- ========================================
CREATE TABLE IF NOT EXISTS auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id_usuario),
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(100),
    registro_id INTEGER,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    ip_origen VARCHAR(45),
    user_agent TEXT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exitoso BOOLEAN DEFAULT true,
    mensaje_error TEXT
);

-- Índice para auditoría
CREATE INDEX idx_auditoria_usuario ON auditoria(id_usuario);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha_hora);
CREATE INDEX idx_auditoria_tabla ON auditoria(tabla_afectada);

-- ========================================
-- TABLA: NOTIFICACIONES
-- ========================================
CREATE TABLE IF NOT EXISTS notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_triaje INTEGER REFERENCES triajes(id_triaje) ON DELETE CASCADE,
    tipo_notificacion VARCHAR(50) NOT NULL CHECK (tipo_notificacion IN ('Email', 'SMS', 'Telegram', 'Sistema')),
    destinatario VARCHAR(200) NOT NULL,
    asunto VARCHAR(200),
    mensaje TEXT NOT NULL,
    estado_envio VARCHAR(30) DEFAULT 'Pendiente' CHECK (estado_envio IN ('Pendiente', 'Enviado', 'Fallido', 'Reintentando')),
    fecha_envio TIMESTAMP,
    intentos_envio INTEGER DEFAULT 0,
    error_envio TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para notificaciones
CREATE INDEX idx_notificaciones_triaje ON notificaciones(id_triaje);
CREATE INDEX idx_notificaciones_estado ON notificaciones(estado_envio);

-- ========================================
-- TABLA: CONFIGURACIÓN DEL SISTEMA
-- ========================================
CREATE TABLE IF NOT EXISTS configuracion (
    id_config SERIAL PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo_dato VARCHAR(20) CHECK (tipo_dato IN ('string', 'integer', 'boolean', 'json')),
    descripcion TEXT,
    categoria VARCHAR(50),
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modificado_por INTEGER REFERENCES usuarios(id_usuario)
);

-- ========================================
-- TABLA: REPORTES GENERADOS
-- ========================================
CREATE TABLE IF NOT EXISTS reportes (
    id_reporte SERIAL PRIMARY KEY,
    tipo_reporte VARCHAR(50) NOT NULL,
    nombre_archivo VARCHAR(200) NOT NULL,
    parametros JSONB,
    fecha_inicio DATE,
    fecha_fin DATE,
    generado_por INTEGER REFERENCES usuarios(id_usuario),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    formato VARCHAR(10) CHECK (formato IN ('PDF', 'CSV', 'XLSX')),
    ruta_archivo TEXT,
    tamanio_kb INTEGER
);

-- Índice para reportes
CREATE INDEX idx_reportes_fecha ON reportes(fecha_generacion);
CREATE INDEX idx_reportes_tipo ON reportes(tipo_reporte);

-- ========================================
-- TABLA: SESIONES (para manejo de autenticación)
-- ========================================
CREATE TABLE IF NOT EXISTS sesiones (
    id_sesion UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    token_sesion VARCHAR(255) UNIQUE NOT NULL,
    ip_origen VARCHAR(45),
    user_agent TEXT,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    activa BOOLEAN DEFAULT true,
    fecha_ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para sesiones
CREATE INDEX idx_sesiones_usuario ON sesiones(id_usuario);
CREATE INDEX idx_sesiones_token ON sesiones(token_sesion);
CREATE INDEX idx_sesiones_activa ON sesiones(activa);

-- ========================================
-- VISTAS ÚTILES
-- ========================================

-- Vista: Resumen de triajes por día
CREATE OR REPLACE VIEW vista_triajes_diarios AS
SELECT 
    DATE(fecha_hora_registro) as fecha,
    COUNT(*) as total_triajes,
    COUNT(CASE WHEN nivel_urgencia = 'Crítico' THEN 1 END) as criticos,
    COUNT(CASE WHEN nivel_urgencia = 'Alto' THEN 1 END) as altos,
    COUNT(CASE WHEN nivel_urgencia = 'Moderado' THEN 1 END) as moderados,
    COUNT(CASE WHEN nivel_urgencia = 'Bajo' THEN 1 END) as bajos,
    AVG(tiempo_espera_minutos) as promedio_espera,
    AVG(tiempo_atencion_minutos) as promedio_atencion
FROM triajes
GROUP BY DATE(fecha_hora_registro)
ORDER BY fecha DESC;

-- Vista: Pacientes con triajes recientes
CREATE OR REPLACE VIEW vista_pacientes_recientes AS
SELECT 
    p.id_paciente,
    p.numero_documento,
    p.nombres || ' ' || p.apellidos as nombre_completo,
    p.fecha_nacimiento,
    p.genero,
    p.telefono,
    t.id_triaje,
    t.fecha_hora_registro,
    t.nivel_urgencia,
    t.estado_triaje,
    u.nombre_completo as atendido_por
FROM pacientes p
INNER JOIN triajes t ON p.id_paciente = t.id_paciente
INNER JOIN usuarios u ON t.id_usuario_triaje = u.id_usuario
WHERE t.fecha_hora_registro >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY t.fecha_hora_registro DESC;

-- Vista: Estadísticas por profesional
CREATE OR REPLACE VIEW vista_stats_profesionales AS
SELECT 
    u.id_usuario,
    u.nombre_completo,
    u.rol,
    COUNT(t.id_triaje) as total_triajes,
    COUNT(CASE WHEN t.nivel_urgencia IN ('Crítico', 'Alto') THEN 1 END) as triajes_urgentes,
    AVG(t.tiempo_atencion_minutos) as promedio_tiempo_atencion,
    MAX(t.fecha_hora_registro) as ultimo_triaje
FROM usuarios u
LEFT JOIN triajes t ON u.id_usuario = t.id_usuario_triaje
WHERE u.activo = true
GROUP BY u.id_usuario, u.nombre_completo, u.rol;

-- ========================================
-- FUNCIONES Y TRIGGERS
-- ========================================

-- Función: Actualizar fecha de modificación
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Actualizar fecha de modificación en pacientes
CREATE TRIGGER trigger_pacientes_modificacion
    BEFORE UPDATE ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Trigger: Actualizar fecha de modificación en triajes
CREATE TRIGGER trigger_triajes_modificacion
    BEFORE UPDATE ON triajes
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Función: Calcular edad de paciente
CREATE OR REPLACE FUNCTION calcular_edad(fecha_nac DATE)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(fecha_nac));
END;
$$ LANGUAGE plpgsql;

-- Función: Registrar auditoría automática
CREATE OR REPLACE FUNCTION registrar_auditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO auditoria (accion, tabla_afectada, registro_id, datos_nuevos)
        VALUES ('INSERT', TG_TABLE_NAME, NEW.id_triaje, row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria (accion, tabla_afectada, registro_id, datos_anteriores, datos_nuevos)
        VALUES ('UPDATE', TG_TABLE_NAME, NEW.id_triaje, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO auditoria (accion, tabla_afectada, registro_id, datos_anteriores)
        VALUES ('DELETE', TG_TABLE_NAME, OLD.id_triaje, row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auditoría en triajes
CREATE TRIGGER trigger_auditoria_triajes
    AFTER INSERT OR UPDATE OR DELETE ON triajes
    FOR EACH ROW
    EXECUTE FUNCTION registrar_auditoria();

-- ========================================
-- COMENTARIOS EN TABLAS
-- ========================================
COMMENT ON TABLE usuarios IS 'Usuarios del sistema con diferentes roles de acceso';
COMMENT ON TABLE pacientes IS 'Registro de pacientes con datos demográficos y de contacto';
COMMENT ON TABLE triajes IS 'Registro de triajes realizados con análisis de IA';
COMMENT ON TABLE auditoria IS 'Log de auditoría de todas las operaciones del sistema';
COMMENT ON TABLE notificaciones IS 'Registro de notificaciones enviadas por el sistema';
COMMENT ON TABLE configuracion IS 'Parámetros de configuración del sistema';
COMMENT ON TABLE reportes IS 'Historial de reportes generados';
COMMENT ON TABLE sesiones IS 'Sesiones activas de usuarios para autenticación';

-- ========================================
-- GRANTS Y PERMISOS
-- ========================================
-- Asegurar que el usuario de la aplicación tenga permisos completos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO triaje_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO triaje_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO triaje_user;

-- Fin del schema
