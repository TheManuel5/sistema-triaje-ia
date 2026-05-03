-- ========================================
-- DATOS INICIALES PARA TESTING
-- Sistema de Triaje Clínico Asistido por IA
-- ========================================

-- ========================================
-- USUARIOS DE PRUEBA
-- ========================================
-- Contraseñas: todos usan 'admin123' (hasheado con bcrypt)
-- Hash generado: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.

INSERT INTO usuarios (nombre_usuario, nombre_completo, email, password_hash, rol, activo) VALUES
('admin', 'Administrador del Sistema', 'admin@triaje.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'admin', true),
('dr.martinez', 'Dr. Carlos Martínez López', 'carlos.martinez@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'medico', true),
('dra.rodriguez', 'Dra. Ana Rodríguez Silva', 'ana.rodriguez@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'medico', true),
('enf.garcia', 'Enf. María García Torres', 'maria.garcia@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'enfermera', true),
('enf.lopez', 'Enf. José López Pérez', 'jose.lopez@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'triaje', true),
('viewer', 'Usuario Visualizador', 'viewer@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIr/Q8VO9.', 'visualizador', true);

-- ========================================
-- PACIENTES DE PRUEBA
-- ========================================
INSERT INTO pacientes (
    numero_documento, tipo_documento, nombres, apellidos, fecha_nacimiento, genero,
    telefono, email, direccion, distrito, provincia, departamento,
    contacto_emergencia_nombre, contacto_emergencia_telefono, contacto_emergencia_relacion,
    grupo_sanguineo, alergias, enfermedades_cronicas, medicacion_actual,
    seguro_medico, numero_poliza, id_hce_externo
) VALUES
(
    '72345678', 'DNI', 'Juan Carlos', 'Pérez Gonzales', '1985-03-15', 'Masculino',
    '987654321', 'juan.perez@email.com', 'Av. Los Pinos 123', 'San Isidro', 'Lima', 'Lima',
    'María Pérez', '987654322', 'Esposa',
    'O+', 'Penicilina', 'Hipertensión arterial', 'Enalapril 10mg/día',
    'EsSalud', 'ES-12345678', 'HCE-001'
),
(
    '68234567', 'DNI', 'María Elena', 'Rodríguez Vega', '1992-07-22', 'Femenino',
    '965432187', 'maria.rodriguez@email.com', 'Jr. Las Flores 456', 'Miraflores', 'Lima', 'Lima',
    'Pedro Rodríguez', '965432188', 'Padre',
    'A+', 'Ninguna conocida', NULL, NULL,
    'Pacífico Salud', 'PS-87654321', 'HCE-002'
),
(
    '45123456', 'DNI', 'Roberto', 'Sánchez Muñoz', '1978-11-05', 'Masculino',
    '912345678', 'roberto.sanchez@email.com', 'Calle Los Olivos 789', 'Surco', 'Lima', 'Lima',
    'Carmen Muñoz', '912345679', 'Esposa',
    'B+', 'Aspirina', 'Diabetes Mellitus tipo 2', 'Metformina 850mg 2 veces al día',
    'Rimac Seguros', 'RM-45678912', 'HCE-003'
),
(
    '71234567', 'DNI', 'Ana Patricia', 'Torres Quispe', '1995-04-18', 'Femenino',
    '998877665', 'ana.torres@email.com', 'Av. Universitaria 321', 'Los Olivos', 'Lima', 'Lima',
    'Luis Torres', '998877666', 'Hermano',
    'AB+', NULL, NULL, 'Anticonceptivos orales',
    'SIS', 'SIS-71234567', 'HCE-004'
),
(
    '62345671', 'DNI', 'Pedro Luis', 'Ramírez Castro', '1960-09-30', 'Masculino',
    '955443322', 'pedro.ramirez@email.com', 'Jr. Junín 567', 'Cercado de Lima', 'Lima', 'Lima',
    'Rosa Castro', '955443323', 'Esposa',
    'O-', 'Sulfa', 'EPOC, Hipertensión arterial', 'Salbutamol inhalador, Losartán 50mg/día',
    'EsSalud', 'ES-62345671', 'HCE-005'
),
(
    '76543210', 'DNI', 'Carmen Rosa', 'Flores Mendoza', '1988-12-10', 'Femenino',
    '987123456', 'carmen.flores@email.com', 'Av. Brasil 890', 'Jesús María', 'Lima', 'Lima',
    'Alberto Flores', '987123457', 'Esposo',
    'A-', NULL, 'Asma bronquial', 'Salbutamol y Budesonida inhaladores',
    'Mapfre', 'MP-76543210', 'HCE-006'
),
(
    '81234567', 'DNI', 'Luis Alberto', 'Vargas Díaz', '2000-05-25', 'Masculino',
    '923456789', 'luis.vargas@email.com', 'Calle Lima 234', 'Breña', 'Lima', 'Lima',
    'Juana Díaz', '923456790', 'Madre',
    'B-', 'Yodo', NULL, NULL,
    'SIS', 'SIS-81234567', 'HCE-007'
),
(
    'CE123456', 'CE', 'Sofia Alejandra', 'Gómez Paredes', '1990-08-14', 'Femenino',
    '967890123', 'sofia.gomez@email.com', 'Av. Arequipa 1234', 'Lince', 'Lima', 'Lima',
    'Diego Gómez', '967890124', 'Hermano',
    'O+', NULL, NULL, NULL,
    'Particular', NULL, 'HCE-008'
);

-- ========================================
-- TRIAJES DE EJEMPLO
-- ========================================
INSERT INTO triajes (
    id_paciente, id_usuario_triaje, fecha_hora_registro,
    presion_arterial_sistolica, presion_arterial_diastolica, frecuencia_cardiaca,
    frecuencia_respiratoria, temperatura, saturacion_oxigeno,
    motivo_consulta, sintomas_principales, tiempo_evolucion,
    dolor_escala, dolor_ubicacion,
    nivel_urgencia, nivel_urgencia_score, diagnosticos_diferenciales,
    recomendaciones_ia, justificacion_ia, modelo_ia_utilizado,
    estado_triaje, tiempo_espera_minutos
) VALUES
(
    1, 5, CURRENT_TIMESTAMP - INTERVAL '2 hours',
    150, 95, 88, 18, 37.2, 96,
    'Dolor precordial', 'Dolor opresivo en el pecho, sudoración, náuseas', '30 minutos',
    8, 'Tórax anterior',
    'Crítico', 0.92, 'Síndrome coronario agudo, Angina inestable, Infarto agudo de miocardio',
    'Atención médica inmediata. Realizar ECG de 12 derivaciones. Monitorización continua. Considerar activación de código infarto.',
    'Paciente con dolor torácico típico, factores de riesgo cardiovascular conocidos (hipertensión), y presentación clínica compatible con síndrome coronario agudo.',
    'gpt-4-turbo-preview',
    'En Atención', 5
),
(
    2, 5, CURRENT_TIMESTAMP - INTERVAL '4 hours',
    110, 70, 72, 16, 38.5, 98,
    'Fiebre y tos', 'Tos seca, fiebre de 38.5°C, malestar general', '2 días',
    3, 'Garganta',
    'Moderado', 0.48, 'Infección respiratoria alta, Faringitis aguda, COVID-19',
    'Evaluación médica en las próximas 2 horas. Realizar hisopado para COVID-19. Tratamiento sintomático. Indicaciones de aislamiento.',
    'Cuadro febril agudo con síntomas respiratorios, requiere descarte de COVID-19 y evaluación para manejo ambulatorio.',
    'gpt-4-turbo-preview',
    'Atendido', 45
),
(
    3, 5, CURRENT_TIMESTAMP - INTERVAL '6 hours',
    160, 100, 95, 20, 37.8, 94,
    'Hiperglicemia', 'Polidipsia, poliuria, visión borrosa, debilidad', '3 días',
    5, 'General',
    'Alto', 0.78, 'Descompensación diabética, Cetoacidosis diabética, Síndrome hiperglucémico hiperosmolar',
    'Atención prioritaria. Control de glicemia capilar inmediato. Hidratación venosa. Evaluación de gases arteriales y electrolitos.',
    'Paciente diabético conocido con signos de descompensación metabólica, signos vitales alterados y glucemia probable elevada.',
    'gpt-4-turbo-preview',
    'Derivado', 30
),
(
    4, 5, CURRENT_TIMESTAMP - INTERVAL '1 day',
    115, 75, 68, 14, 37.0, 99,
    'Control prenatal', 'Embarazo de 28 semanas, control de rutina', 'N/A',
    0, NULL,
    'Bajo', 0.15, 'Control prenatal normal',
    'Evaluación por ginecología según programación. Signos vitales dentro de parámetros normales para embarazo.',
    'Control prenatal de rutina, paciente estable sin signos de alarma.',
    'gpt-4-turbo-preview',
    'Atendido', 60
),
(
    5, 5, CURRENT_TIMESTAMP - INTERVAL '3 hours',
    140, 85, 92, 22, 37.5, 88,
    'Disnea', 'Dificultad respiratoria, sibilancias, uso de musculatura accesoria', '1 hora',
    6, 'Tórax',
    'Alto', 0.82, 'Crisis asmática, Exacerbación de EPOC, Insuficiencia cardíaca descompensada',
    'Atención inmediata. Nebulización con broncodilatadores. Oxigenoterapia. Valorar corticoides sistémicos. Radiografía de tórax.',
    'Paciente con antecedentes de EPOC, saturación de oxígeno baja, trabajo respiratorio aumentado, compatible con exacerbación aguda.',
    'gpt-4-turbo-preview',
    'En Atención', 10
),
(
    6, 5, CURRENT_TIMESTAMP - INTERVAL '5 hours',
    120, 78, 78, 18, 36.8, 97,
    'Crisis asmática', 'Dificultad para respirar, sibilancias, opresión torácica', '2 horas',
    7, 'Tórax',
    'Alto', 0.75, 'Crisis asmática moderada-severa, Broncoespasmo',
    'Atención prioritaria. Nebulización inmediata. Evaluación de respuesta al tratamiento. Considerar corticoides.',
    'Paciente asmática conocida con crisis actual, requiere manejo inmediato para evitar deterioro.',
    'gpt-4-turbo-preview',
    'Atendido', 20
),
(
    7, 5, CURRENT_TIMESTAMP - INTERVAL '8 hours',
    118, 72, 70, 16, 36.9, 98,
    'Dolor abdominal', 'Dolor en fosa ilíaca derecha, náuseas', '6 horas',
    6, 'Abdomen inferior derecho',
    'Moderado', 0.62, 'Apendicitis aguda, Gastroenteritis, Infección urinaria',
    'Evaluación médica en 1-2 horas. Examen físico completo. Laboratorio (hemograma, PCR). Ecografía abdominal.',
    'Dolor abdominal localizado en fosa ilíaca derecha con características que sugieren proceso inflamatorio, requiere descarte de apendicitis.',
    'gpt-4-turbo-preview',
    'Derivado', 40
),
(
    8, 5, CURRENT_TIMESTAMP - INTERVAL '12 hours',
    112, 70, 65, 14, 36.7, 99,
    'Cefalea', 'Dolor de cabeza frontal, leve', '1 día',
    4, 'Frontal',
    'Bajo', 0.28, 'Cefalea tensional, Migraña sin aura',
    'Evaluación médica según disponibilidad. Analgesia oral. Medidas generales. Signos de alarma.',
    'Cefalea de características benignas, signos vitales normales, baja probabilidad de patología grave.',
    'gpt-4-turbo-preview',
    'Atendido', 90
);

-- ========================================
-- CONFIGURACIÓN DEL SISTEMA
-- ========================================
INSERT INTO configuracion (clave, valor, tipo_dato, descripcion, categoria) VALUES
('tiempo_maximo_espera_critico', '5', 'integer', 'Tiempo máximo de espera en minutos para casos críticos', 'triaje'),
('tiempo_maximo_espera_alto', '15', 'integer', 'Tiempo máximo de espera en minutos para casos de urgencia alta', 'triaje'),
('tiempo_maximo_espera_moderado', '60', 'integer', 'Tiempo máximo de espera en minutos para casos moderados', 'triaje'),
('tiempo_maximo_espera_bajo', '120', 'integer', 'Tiempo máximo de espera en minutos para casos de urgencia baja', 'triaje'),
('notificar_critico_email', 'true', 'boolean', 'Enviar notificación por email para casos críticos', 'notificaciones'),
('notificar_alto_email', 'true', 'boolean', 'Enviar notificación por email para casos de urgencia alta', 'notificaciones'),
('horario_reporte_diario', '07:00', 'string', 'Hora de envío del reporte diario (formato HH:MM)', 'reportes'),
('habilitar_ia_triaje', 'true', 'boolean', 'Habilitar análisis de IA en triaje', 'ia'),
('modelo_ia_default', 'gpt-4-turbo-preview', 'string', 'Modelo de IA por defecto', 'ia'),
('temperatura_ia', '0.3', 'string', 'Temperatura del modelo de IA (0.0 - 1.0)', 'ia'),
('max_tokens_ia', '2000', 'integer', 'Máximo de tokens en respuesta de IA', 'ia'),
('sincronizar_hce_automatico', 'true', 'boolean', 'Sincronizar automáticamente con HCE después de triaje', 'integracion'),
('timeout_hce_segundos', '10', 'integer', 'Timeout en segundos para llamadas a HCE', 'integracion');

-- ========================================
-- NOTIFICACIONES DE EJEMPLO
-- ========================================
INSERT INTO notificaciones (id_triaje, tipo_notificacion, destinatario, asunto, mensaje, estado_envio, fecha_envio) VALUES
(1, 'Email', 'equipo.medico@hospital.com', '⚠️ TRIAJE CRÍTICO - Atención Inmediata Requerida', 
 'Se ha registrado un triaje de nivel CRÍTICO para el paciente Juan Carlos Pérez Gonzales (DNI: 72345678). Motivo: Dolor precordial. Se requiere atención médica inmediata.', 
 'Enviado', CURRENT_TIMESTAMP - INTERVAL '2 hours'),
(3, 'Email', 'equipo.medico@hospital.com', '⚠️ TRIAJE ALTO - Atención Prioritaria', 
 'Se ha registrado un triaje de nivel ALTO para el paciente Roberto Sánchez Muñoz (DNI: 45123456). Motivo: Hiperglicemia. Se requiere atención prioritaria.', 
 'Enviado', CURRENT_TIMESTAMP - INTERVAL '6 hours'),
(5, 'Email', 'equipo.medico@hospital.com', '⚠️ TRIAJE ALTO - Atención Prioritaria', 
 'Se ha registrado un triaje de nivel ALTO para el paciente Pedro Luis Ramírez Castro (DNI: 62345671). Motivo: Disnea. Se requiere atención prioritaria.', 
 'Enviado', CURRENT_TIMESTAMP - INTERVAL '3 hours');

-- ========================================
-- AUDITORÍA DE EJEMPLO
-- ========================================
INSERT INTO auditoria (id_usuario, accion, tabla_afectada, registro_id, datos_nuevos, ip_origen, exitoso) VALUES
(1, 'LOGIN', 'usuarios', 1, '{"usuario": "admin"}', '192.168.1.100', true),
(5, 'INSERT', 'triajes', 1, '{"id_triaje": 1, "nivel_urgencia": "Crítico"}', '192.168.1.101', true),
(5, 'INSERT', 'triajes', 2, '{"id_triaje": 2, "nivel_urgencia": "Moderado"}', '192.168.1.101', true),
(2, 'UPDATE', 'triajes', 1, '{"estado_triaje": "En Atención"}', '192.168.1.102', true);

-- ========================================
-- REPORTES DE EJEMPLO
-- ========================================
INSERT INTO reportes (tipo_reporte, nombre_archivo, fecha_inicio, fecha_fin, generado_por, formato, ruta_archivo, tamanio_kb) VALUES
('Dashboard Operacional', 'reporte_operacional_20250501.pdf', CURRENT_DATE, CURRENT_DATE, 1, 'PDF', '/reportes/operacional_20250501.pdf', 245),
('Dashboard de Gestión', 'reporte_gestion_abril_2025.pdf', '2025-04-01', '2025-04-30', 1, 'PDF', '/reportes/gestion_abril_2025.pdf', 512),
('Exportación de Triajes', 'triajes_abril_2025.csv', '2025-04-01', '2025-04-30', 1, 'CSV', '/reportes/triajes_abril_2025.csv', 87);

-- Fin de datos iniciales
