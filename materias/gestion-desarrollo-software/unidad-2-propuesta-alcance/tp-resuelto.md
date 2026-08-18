# TRABAJO PRÁCTICO – UNIDAD 2
## Propuesta, alcance y gestión de interesados

**Materia:** Gestión de Desarrollos de Software  
**Unidad 2:** Propuesta, alcance y gestión de un proyecto  
**Alumno:** Nicolás Viruel

---

## Caso de estudio: HealthConnect

La clínica privada **HealthConnect** quiere una plataforma web para que los pacientes soliciten, reprogramen y cancelen turnos médicos en línea. Hoy todo se hace por teléfono, con demoras y turnos perdidos. La dirección pide la solución en **4 meses**, con **presupuesto acotado**, cumpliendo **normativa de privacidad de datos médicos** y permitiendo que el **personal administrativo** lo use sin dificultades técnicas.

---

## Actividad 1: Gestión del Alcance

### 1. Definición de Inclusiones y Exclusiones

#### a) Inclusiones (3)

1. **Portal web de autogestión de turnos para pacientes:** registro/login, búsqueda de disponibilidad por especialidad/médico, reserva, reprogramación y cancelación de turnos con confirmación por pantalla y/o correo.
2. **Panel administrativo para recepción:** visualización de agenda diaria/semanal, alta de profesionales y horarios, y gestión manual de turnos cuando un paciente llama o concurre presencialmente.
3. **Cumplimiento básico de privacidad de datos médicos:** autenticación segura, control de acceso por rol (paciente / administrativo / médico), registro de acciones sensibles y almacenamiento de datos clínicos mínimos necesarios para la reserva (sin historial clínico completo en esta etapa).

#### b) Exclusiones (3)

1. **Historia clínica electrónica (HCE) completa:** no se desarrollará carga de diagnósticos, estudios, recetas digitales ni evolución clínica; solo lo necesario para gestionar la cita.
2. **App móvil nativa (iOS/Android):** la solución será **web responsive**; no se incluyen publicaciones en stores ni desarrollo mobile nativo.
3. **Integración con obras sociales / facturación / pagos online:** no se implementará liquidación de prestaciones, autorizaciones de OS ni cobro de consultas dentro del sistema.

### 2. Prevención del Scope Creep

1. **Documento de alcance firmado + proceso de Change Request:** antes de iniciar el desarrollo, la dirección de la clínica valida por escrito inclusiones, exclusiones y entregables por sprint. Cualquier pedido nuevo (ej. “sumemos videoconsulta” o “que mande WhatsApp”) entra por un formulario de cambio con impacto en **tiempo, costo y calidad**, y solo se aprueba si hay ajuste formal de plazo/presupuesto.
2. **Backlog priorizado con criterio MoSCoW y demo quincenal:** en cada iteración se muestra solo lo acordado como *Must*. Las ideas “interesantes pero no pactadas” van a una lista de *Won’t/Could* para una fase futura, evitando que el cliente incorpore funcionalidades durante la demo sin pasar por gestión de cambios.

---

## Actividad 2: Gestión de Interesados (Stakeholders)

### 1. Matriz de Clasificación (4 stakeholders)

| Stakeholder | Tipo | Rol / interés principal | Influencia | Expectativa clave |
|-------------|------|-------------------------|------------|-------------------|
| **Project Manager / Líder de proyecto** | Interno | Coordina plan, alcance, riesgos y comunicación | Alta | Entregar a tiempo, dentro de presupuesto y sin desvíos de alcance |
| **Equipo de desarrollo (dev + QA)** | Interno | Diseña, implementa y prueba la plataforma | Media-Alta | Requerimientos claros, prioridades estables y acceso a ambiente de prueba |
| **Dirección de HealthConnect (Gerencia)** | Externo | Sponsor; define plazos, presupuesto y prioridades de negocio | Muy alta | Reducir llamadas telefonicas, mejorar experiencia del paciente en 4 meses |
| **Personal administrativo / recepción** | Externo | Usuario operativo diario del panel de turnos | Media | Sistema simple, rápido de aprender, que no duplique trabajo ni genere errores en la agenda |

*(También son stakeholders externos relevantes los **pacientes** y un eventual **responsable legal/auditoría de datos**; para la consigna se detallan los cuatro anteriores.)*

### 2. Estrategia de comunicación – Dirección de HealthConnect (stakeholder externo)

**Objetivo:** alinear expectativas sobre plazo (4 meses), presupuesto acotado y alcance MVP, y mantener visibilidad del avance sin saturar reuniones.

**Estrategia concreta:**

- **Kick-off formal (semana 1):** presentación del documento de alcance, cronograma por hitos y riesgos iniciales; acuerdo explícito de exclusiones (sin HCE, sin app nativa, sin facturación).
- **Reporte ejecutivo quincenal (1 página):** avance % por hito, turnos funcionales demo, riesgos abiertos y decisiones pendientes; enviado por mail + reunión de 30 minutos.
- **Canal único de priorización:** la gerencia no pide cambios por WhatsApp al dev; todo pasa por el PM, que evalúa impacto y responde en 48 h con alternativas (aceptar cambio con extensión, posponer a fase 2, o rechazar por restricción de presupuesto/tiempo).
- **Demo al cierre de cada sprint:** validación visual de funcionalidades terminadas; lo no mostrado no se considera entregado.

---

## Actividad 3: Riesgos, Supuestos, Restricciones y Criterios de Aceptación

### 1. Supuestos y Restricciones

#### a) Supuestos (2)

1. **El personal administrativo tiene acceso a PC con navegador actualizado e internet estable** en recepción para operar el panel web sin necesidad de capacitación intensiva en informática.
2. **La clínica dispondrá de información base ordenada** (listado de médicos, especialidades y grilla horaria) antes o durante las primeras semanas del proyecto, para no bloquear el desarrollo del módulo de reservas.

#### b) Restricciones (2)

1. **Tiempo:** la solución debe estar lista en un **plazo máximo de 4 meses** desde el inicio del proyecto (restricción de cronograma).
2. **Legal / normativa:** el sistema debe cumplir **estrictamente** las regulaciones locales de **privacidad de datos médicos** (restricción legal/compliance), lo que condiciona diseño de seguridad, permisos y tratamiento de datos personales sensibles.

*(También aparece explícita la restricción de **presupuesto acotado** y la de **usabilidad para personal no técnico**.)*

### 2. Criterios de aceptación – Reserva de Turnos (formato BDD)

**Criterio 1 – Reserva exitosa**

- **Dado que** un paciente autenticado consulta la disponibilidad de un médico con turnos libres en la especialidad elegida  
- **Cuando** selecciona un horario disponible y confirma la reserva  
- **Entonces** el sistema registra el turno a su nombre, lo descuenta de la agenda y muestra confirmación en pantalla (y/o envía notificación al correo registrado)

**Criterio 2 – Prevención de doble reserva**

- **Dado que** un horario ya fue reservado por otro paciente  
- **Cuando** un segundo paciente intenta reservar el mismo horario con el mismo médico  
- **Entonces** el sistema no permite confirmar la operación e informa que el turno ya no está disponible, ofreciendo alternativas de horarios libres

### 3. Uso reflexivo de la Inteligencia Artificial

#### a) ¿Qué aportes específicos puede generar la IA en esta etapa inicial?

- **Borrador del documento de visión** y resumen ejecutivo del problema (dolor actual telefónico, objetivos de negocio).
- **Listado preliminar de stakeholders**, riesgos y supuestos a partir del enunciado del caso, acelerando el trabajo del PM.
- **Propuestas de criterios de aceptación en formato BDD** para funcionalidades como reserva, cancelación y reprogramación, que luego el equipo adapta al dominio real.
- **Identificación de requisitos no funcionales** típicos (seguridad, privacidad, usabilidad) en proyectos de salud.

#### b) ¿Por qué no debe entregarse directamente al cliente sin validación del equipo?

Porque la IA **no conoce el contexto real** de HealthConnect: puede inventar integraciones, subestimar restricciones legales argentinas, proponer un alcance irreal para 4 meses o usar lenguaje demasiado genérico. También puede **omitir exclusiones críticas** y generar ambigüedades que después derivan en scope creep.

El equipo de desarrollo y el PM deben **validar factibilidad técnica, costos, plazos y compliance** con datos reales de la clínica antes de presentar cualquier documento al cliente. La IA es un asistente para el borrador; la **responsabilidad profesional** del contenido final es del equipo humano.

---

*Documento elaborado para la entrega en Moodle – Unidad 2 - Práctica (assign id 14811).*
