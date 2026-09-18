# TRABAJO PRÁCTICO — Legislación Laboral IT

**Materia:** Legislación  
**Unidad 6:** Laboral IT  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN

---

## Escenario (recordatorio)

Startup de turnos médicos con tres desarrolladores: uno en relación de dependencia, otro monotributista con horario fijo y órdenes, otro freelance por proyecto; todos en remoto. Hay mensajes fuera de horario, la empresa no provee herramientas, y uno descarga la base de usuarios para un proyecto personal.

---

## Actividad 1 — Análisis del vínculo laboral

### 1. ¿Qué tipo de relación laboral tiene cada desarrollador?

| Integrante | Encuadre aparente | Análisis |
|------------|-------------------|----------|
| **Desarrollador 1** | **Relación de dependencia** | Contrato laboral clásico: subordinación, habitualidad y remuneración en nómina. |
| **Desarrollador 2** | **Monotributo**, pero con indicios de **dependencia encubierta** | Factura como autónomo pero cumple horario fijo y recibe órdenes → se parece más a empleado que a prestador independiente. |
| **Desarrollador 3** | **Freelance / contratación por proyecto** | Encuadre coherente si hay objeto definido, plazos, entregables y autonomía técnica real. |

### 2. ¿Existe alguna situación irregular?

**Sí.** La del **desarrollador 2** es la más riesgosa: puede configurarse **falsedad de contrato** o relación laboral no registrada si la subordinación es real. Eso expone a la startup a **multas**, **regularización retroactiva** y obligaciones laborales impagas (aguinaldo, vacaciones, aportes).

### 3. Diferencias entre dependencia, freelance y contratación por proyecto

- **Dependencia:** subordinación jurídica, horario, continuidad, aportes y derechos laborales plenos.
- **Freelance autónomo:** organiza su trabajo, asume riesgo de su actividad, factura por servicios (sin subordinación real).
- **Por proyecto:** objeto acotado (módulo, MVP), plazo y entregables; no implica relación permanente salvo que en la práctica sea continua y subordinada.

### 4. ¿Qué riesgos existen en una relación mal definida?

- Reclamos por **diferencias salariales** y cargas sociales.
- Conflictos con **AFIP** y ministerio de Trabajo.
- **Responsabilidad solidaria** de la empresa.
- Incertidumbre para el trabajador (sin cobertura real).

---

## Actividad 2 — Teletrabajo y condiciones laborales

Referencia: **Ley 27.555** de teletrabajo en Argentina.

### 1. ¿Se respetan las condiciones del teletrabajo según la legislación?

**Parcialmente o mal.** Trabajan en remoto, pero faltan definiciones formales: acuerdo de teletrabajo, condiciones de jornada, provisión de herramientas y registro de modalidad. La ley exige **regulación escrita** y respeto de derechos laborales aunque el trabajo sea a distancia.

### 2. ¿Se cumple el derecho a la desconexión digital?

**No.** Los mensajes fuera del horario laboral muestran **violación del derecho a desconectar** (Ley 27.555). El empleador no puede exigir disponibilidad permanente salvo reglas claras y excepciones justificadas.

### 3. ¿Qué obligaciones del empleador no se están cumpliendo?

- **Proveer herramientas** o compensar su costo cuando corresponda.
- **Capacitación** en uso seguro de equipos y datos (contexto médico).
- **Registro** de la modalidad de teletrabajo.
- **Respeto de jornada** y desconexión.
- **Condiciones de salud y seguridad** en el entorno remoto (deber de información y prevención).

### 4. ¿Qué problemas genera la falta de organización en el teletrabajo?

Burnout, errores por fatiga, **filtraciones de datos**, dificultad para auditar horas, conflictos sobre disponibilidad y **exposición legal** si hay incidentes de seguridad.

---

## Actividad 3 — Confidencialidad y datos

### 1. ¿Es correcta la conducta del desarrollador que descarga la base de datos?

**No.** Es un uso **no autorizado** de datos personales y confidenciales del empleador/cliente, aunque sea “para probar” un proyecto personal.

### 2. ¿Qué obligación se incumple?

- **Deber de confidencialidad** laboral (y eventual **NDA**).
- **Deber de lealtad** hacia el empleador.
- Obligaciones de **tratamiento lícito** de datos personales.

### 3. ¿Qué normativa regula esta situación en Argentina?

- **Ley 25.326** de Protección de Datos Personales (principios de licitud, finalidad, confidencialidad, seguridad).
- Normativa laboral sobre **secreto profesional** y deberes del empleado.
- Posibles reglas sectoriales por datos de **salud** (datos sensibles).

### 4. ¿Qué consecuencias pueden derivarse?

- **Sanción disciplinaria** o despido con justa causa.
- **Acciones civiles** por daños.
- **Denuncia ante la autoridad de protección de datos** (DNPDP / AAIP según competencia).
- **Responsabilidad penal** en casos graves (acceso indebido a datos).

---

## Actividad integradora final — Propuesta

| Tema | Medida propuesta |
|------|------------------|
| **Contratación** | Dev 1: relación de dependencia formal + adenda teletrabajo Ley 27.555. Dev 2: **regularizar** (dependencia) o reestructurar como autonomía real (sin horario ni órdenes permanentes). Dev 3: contrato por proyecto con entregables y propiedad intelectual definida. |
| **Teletrabajo** | Acuerdo escrito, horario núcleo, **derecho a desconexión**, política de mensajería, provisión o reintegro de equipos, VPN y MFA. |
| **Confidencialidad y datos** | NDA firmado, política de acceso mínimo, ambientes de prueba **anonimizados**, prohibición de exportar BD a equipos personales, logging de accesos, capacitación Ley 25.326. |

---

## Cierre

El caso muestra que en IT **no alcanza con “todos remotos”**: hay que encuadrar bien cada vínculo, cumplir **teletrabajo** y tratar datos de usuarios —más aún en salud— con **confidencialidad** estricta.
