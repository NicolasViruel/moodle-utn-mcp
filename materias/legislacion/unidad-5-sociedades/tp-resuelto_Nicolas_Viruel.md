# TRABAJO PRÁCTICO — Sociedades y organización en IT

**Materia:** Legislación  
**Unidad 5:** Sociedades, emprendimientos y derecho económico básico  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN

---

## Escenario (recordatorio)

Tres desarrolladores crean una app de turnos médicos. Arrancan sin estructura legal ni contratos; la app crece, hay ingresos y un fallo en producción genera pérdidas a un cliente. Surgen conflictos sobre propiedad del software, ganancias, decisiones y responsabilidad.

---

## Actividad 1 — Análisis del proyecto

### 1. ¿En qué etapa se encuentra el proyecto: informal u organizada?

Está en etapa **informal** al inicio, pero el caso muestra que **ya debería estar organizada** y no lo está. Siguen operando como grupo ad hoc aunque hay usuarios, ingresos y un cliente empresarial afectado. La informalidad persiste cuando el negocio ya exige reglas claras.

### 2. ¿Qué cambios indican que el proyecto dejó de ser solo técnico?

- Hay **usuarios reales** y **ingresos**.
- Aparece un **cliente empresa** con expectativas contractuales.
- Un error en producción produce **daño económico** a terceros.
- Surgen **conflictos entre socios** sobre dueño del código, reparto y quién responde.

Eso ya no es “proyecto de garage”: es operación comercial con impacto externo.

### 3. ¿Por qué el crecimiento exige una nueva forma de organización?

Porque aumentan los **riesgos** (técnicos, contractuales y patrimoniales), las **decisiones** dejan de ser triviales y hace falta definir **roles, propiedad intelectual, reparto de utilidades y quién responde** ante clientes. Sin organización formal, cada conflicto se resuelve a gritos y no hay certeza jurídica para clientes ni para el equipo.

---

## Actividad 2 — Organización y sociedades

### 1. ¿Qué problemas genera la falta de formalización?

- **Incertidumbre sobre la titularidad** del software y del código.
- **Conflictos** en ganancias y decisiones (todo “verbal”).
- **Responsabilidad difusa**: nadie sabe quién responde al cliente.
- **Dificultad para contratar**, facturar y acceder a crédito.
- **Riesgo personal ilimitado** si responden como personas físicas sin estructura societaria.

### 2. ¿Qué tipo de organización sería recomendable?

Para un emprendimiento IT en crecimiento con tres integrantes y facturación a clientes, suele recomendarse una **sociedad** que limite responsabilidad y permita repartir cuotas y roles, por ejemplo **S.R.L.** o **S.A.S.** (según escala, inversión y plan de crecimiento). Mantener solo relaciones freelance sueltas entre los tres **no** alcanza cuando comparten producto, marca e ingresos.

### 3. ¿Qué ventajas aporta la creación de una sociedad?

- **Personalidad jurídica** propia (distinta de cada socio).
- **Reglas escritas** (estatuto, acuerdo de socios).
- **Responsabilidad patrimonial** acotada al aporte (en sociedades de capital).
- **Claridad en titularidad** del software y cesión/licencia de desarrollos.
- **Mejor imagen** frente a clientes y posibilidad de contratar en forma regular.

### 4. ¿Cómo cambia la responsabilidad al pasar de freelance a sociedad?

Como **freelance** cada uno responde por su contrato y puede quedar expuesto con su patrimonio personal según el encuadre. En una **sociedad**, las obligaciones comerciales y muchas frente a clientes se canalizan en la **persona jurídica**; los socios responden dentro del marco legal y los acuerdos internos (con excepciones por dolo, fraude o garantías personales). La responsabilidad deja de ser “tres individuos mezclados” y pasa a ser **organización formal con reglas**.

---

## Actividad 3 — Responsabilidad en el proyecto

### 1. ¿Existe responsabilidad por las pérdidas generadas?

**Sí.** Si el sistema falló en producción y causó daño económico a un cliente, puede configurarse **responsabilidad contractual** (incumplimiento de SLA, calidad, disponibilidad) y eventualmente **extracontractual** según el encuadre del vínculo con el cliente.

### 2. ¿Qué tipo de responsabilidad podría aplicarse?

- **Contractual** frente al cliente (reparación, indemnización según contrato).
- **Civil** por daños y perjuicios si no hay cláusulas claras o si el daño excede lo pactado.
- **Entre socios**: responsabilidad interna por mala praxis, falta de QA o decisiones de deploy sin controles (según acuerdos y roles).

### 3. ¿Quién debería responder frente al cliente?

Frente al cliente debería responder **quien contrató** (idealmente la **sociedad** o la persona jurídica que facturó). Internamente, si el fallo fue por deploy, falta de pruebas o deudas técnicas, puede corresponder al **equipo técnico** y a quien tenía **rol de release/QA**, pero la cara visible al cliente debe estar definida contractualmente.

### 4. ¿Cómo influye la falta de acuerdos?

Sin contratos ni estatuto no hay claridad sobre **límites de responsabilidad**, **propiedad del código**, **procesos de calidad** ni **reparto de costos** de un siniestro. Eso **agrava** el conflicto interno y debilita la defensa frente al cliente.

---

## Actividad 4 — Decisiones y gestión del proyecto

### 1. ¿Qué decisiones no se tomaron correctamente?

- Definir **titularidad** del software.
- Acordar **reparto de ingresos** y aportes.
- Establecer **gobernanza** (quién decide producto, deploy, soporte).
- Firmar **contratos** entre integrantes y con clientes.
- Definir **estándares de calidad** y responsabilidad por producción.

### 2. ¿En qué momento deberían haberse tomado?

Al **primer ingreso**, al **primer cliente pago** y, como mínimo, **antes de producción crítica** con datos sensibles (turnos médicos). La formalización societaria conviene cuando dejan de ser “proyecto” y pasan a **operación comercial**.

### 3. ¿Por qué el problema no es técnico sino organizativo?

Porque el fallo técnico es el **disparador**, pero la crisis se agrava por **falta de roles, acuerdos y responsables claros**. Un bug en producción es gestionable con procesos; sin organización se convierte en pelea entre socios y riesgo legal.

### 4. ¿Cómo impacta en el futuro del proyecto?

Sin corrección, el proyecto puede **perder clientes**, **enfrentar demandas**, **fragmentarse** (socios que se van) o **detener el desarrollo**. Con organización, puede **seguir creciendo** con reglas y confianza.

---

## Actividad integradora final — Propuesta

| Eje | Propuesta |
|-----|-----------|
| **Estructura** | Constituir **S.A.S.** o **S.R.L.** con tres socios; contrato social + acuerdo de socios complementario. |
| **Roles** | Socio A: producto/negocio; Socio B: arquitectura y calidad; Socio C: operaciones y soporte. Decisiones técnicas críticas (producción) con **doble validación** B+C. |
| **Decisiones** | Mayoría simple en operación; unanimidad en deuda técnica mayor, cambios de stack y nuevos socios. |
| **Ingresos** | Reparto según **cuotas societarias** y cláusula de **retención** (% a reserva legal y contingencias) antes de distribuir utilidades. |
| **Riesgos** | Contratos con clientes (SLA, limitación de responsabilidad razonable), seguro de responsabilidad civil si escala, CI/CD con pruebas, registro de IP en la sociedad. |
| **Conflictos** | Cláusula de **mediación**, registro de aportes (código, horas, capital), y **cesión de desarrollos** a la sociedad. |

---

## Cierre

El caso muestra el pasaje típico de un emprendimiento IT de lo **informal** a lo **institucional**. La materia enseña que el código no alcanza: hace falta **sociedad, roles y responsabilidad** para sostener el crecimiento.
