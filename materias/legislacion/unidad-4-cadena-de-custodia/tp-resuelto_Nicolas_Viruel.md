# TRABAJO PRÁCTICO – CADENA DE CUSTODIA
## Evidencia digital: preservación, integridad y trazabilidad

**Materia:** Legislación  
**Unidad 4:** Cadena de Custodia  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN

---

## Caso 1: Copia de archivos sin control de integridad

### ¿Qué riesgos presenta este procedimiento para la integridad de la evidencia?

Trabajar **directamente sobre los originales** y copiar sin registro ni hash genera varios riesgos:

- **Alteración involuntaria:** al abrir, mover o copiar archivos en el sistema operativo activo, pueden modificarse metadatos (fechas de acceso, timestamps) o incluso el contenido si el SO escribe datos temporales.
- **Pérdida de integridad demostrable:** no hay forma técnica de probar después que los archivos copiados son **idénticos** a los originales en el momento de la intervención.
- **Impugnación jurídica:** la defensa puede cuestionar que la evidencia fue manipulada, porque no existe registro ni huella digital que la vincule al estado original.
- **Ruptura de la cadena de custodia:** no queda documentado quién intervino, cuándo, con qué herramientas ni bajo qué condiciones.

En síntesis: la evidencia puede dejar de ser **confiable** aunque el técnico haya actuado de buena fe.

### ¿Qué pasos deberían haberse realizado para obtener una copia forense adecuada?

1. **Documentar el inicio de la intervención:** fecha, hora, responsable, dispositivo, motivo.
2. **Asegurar el original:** desconectarlo de la red si corresponde; evitar escribir sobre el medio fuente.
3. **Obtener una imagen o copia bit a bit** (cuando el soporte lo requiera) o copia verificable con herramientas forenses, **sin alterar el original**.
4. **Calcular y registrar el hash** (por ejemplo SHA-256) de cada archivo o imagen **antes y después** de la copia.
5. **Verificar que los hashes coincidan** entre origen y copia de trabajo.
6. **Registrar en la cadena de custodia** cada acceso, transferencia y almacenamiento posterior.
7. **Analizar siempre sobre la copia**, nunca sobre el original.

Esto se alinea con la **preservación** y la **recolección** previstas en la Res. 232/2023 y con buenas prácticas de la norma ISO/IEC 27037.

### ¿Qué función cumple el valor hash en este caso?

El **hash** es una “huella digital” del archivo: un algoritmo (SHA-256, MD5, etc.) produce una cadena única a partir del contenido.

- Si el archivo cambia **un solo bit**, el hash cambia.
- Permite **demostrar integridad técnica:** “este archivo es exactamente el mismo que se obtuvo en la intervención”.
- **No prueba** autoría, intención ni veracidad del contenido; solo que **no fue alterado** desde el cálculo.

Sin hash, no hay verificación objetiva de integridad.

---

## Caso 2: Teléfono celular encendido y manipulado

### ¿Qué modificaciones podrían producirse sobre la evidencia digital?

Al desbloquear el teléfono y usarlo conectado a la red:

- **Sobrescritura de datos volátiles:** RAM, apps en ejecución, sesiones activas.
- **Nuevos datos generados:** mensajes, notificaciones, actualizaciones de apps, sincronización con la nube que puede **modificar o borrar** evidencia local.
- **Alteración de metadatos:** cambios en “último acceso”, logs del sistema, historial.
- **Activación remota:** bloqueo, borrado remoto (MDM) o cambios desde otro dispositivo vinculado.
- **Pérdida de contexto temporal:** mezcla de actividad posterior al secuestro con la del hecho investigado.

Todo esto compromete **integridad** y **trazabilidad**.

### ¿Cómo debería preservarse inicialmente el dispositivo?

1. **No manipularlo manualmente** antes del procedimiento forense.
2. Si está encendido: **aislarlo de la red** (modo avión, bolsa Faraday o desactivación segura de Wi-Fi/datos sin explorar contenido).
3. Si está apagado: **no encenderlo** hasta estar en entorno controlado con herramientas adecuadas.
4. **Documentar estado inicial:** encendido/apagado, batería, daños físicos, hora de secuestro.
5. **Obtener copia forense completa** (extracción lógica o física según el caso) con herramientas especializadas.
6. **Calcular hash** de la extracción y **trabajar sobre copia**.

### ¿Qué información tendría que quedar registrada en la cadena de custodia?

Registro mínimo por cada intervención/transferencia:

| Dato | Ejemplo |
|------|---------|
| Identificación del dispositivo | Marca, modelo, IMEI, número de serie |
| Fecha y hora | Secuestro, cada acceso, cada traslado |
| Responsable | Nombre, rol, firma o identificación |
| Lugar | Oficina, laboratorio, depósito |
| Estado del dispositivo | Encendido/apagado, medidas de aislamiento |
| Acción realizada | Secuestro, extracción, análisis |
| Hash de la extracción | Algoritmo + valor |
| Condiciones de resguardo | Contenedor, candado, acceso restringido |

---

## Caso 3: Traslado sin registro documental

### ¿Qué principio de la cadena de custodia se ve afectado?

Se afecta principalmente la **trazabilidad** (continuidad y control de la cadena de custodia): no se puede reconstruir **quién tuvo la evidencia, cuándo y bajo qué condiciones** en cada momento.

También se debilitan la **integridad** (riesgo de alteración sin responsable identificable) y la **confiabilidad probatoria**, porque queda un **vacío documental** entre el secuestro y el análisis.

### ¿Por qué resulta importante documentar cada transferencia?

Porque la cadena de custodia debe permitir afirmar que la evidencia:

- **No fue alterada, reemplazada ni perdida** en el camino.
- Estuvo **siempre bajo control** de personas identificadas.
- Puede **explicarse ante un juez** de punta a punta.

Sin registro, cualquier parte puede alegar que la notebook fue manipulada en un traslado no documentado. En materia probatoria, **quien no puede explicar el recorrido de la evidencia pierde credibilidad**.

### ¿Qué datos mínimos debería contener un registro de cadena de custodia?

Por cada entrega/recepción:

1. **Identificación de la evidencia** (número de expediente, descripción del dispositivo, hash si aplica).
2. **Fecha y hora** de la transferencia.
3. **Persona que entrega** y **persona que recibe** (nombre, cargo, firma).
4. **Motivo de la transferencia** (traslado, almacenamiento, pericia).
5. **Estado de la evidencia** (sellos, embalaje, integridad aparente).
6. **Lugar de origen y destino**.
7. **Observaciones** (incidentes, demoras, cambios de embalaje).

---

## Caso 4: Evidencia almacenada en una carpeta compartida

### ¿Qué problemas genera este método de almacenamiento?

- **Acceso no controlado:** varias personas con permiso de edición pueden modificar o borrar archivos sin dejar rastro confiable.
- **Ausencia de trazabilidad:** sin log de accesos, no se sabe quién intervino ni cuándo.
- **Riesgo de sustitución:** un archivo puede reemplazarse por otro con el mismo nombre.
- **Pérdida de integridad demostrable:** no hay garantía de que lo presentado después sea lo obtenido originalmente.
- **Debilitamiento probatorio:** facilita impugnaciones sobre manipulación interna.

Una carpeta compartida **no es un repositorio forense**.

### ¿Qué medidas permitirían preservar la integridad y la trazabilidad de los archivos?

1. **Almacenar en medio dedicado** con acceso restringido (solo personal autorizado).
2. **Permisos de solo lectura** para quienes no deben modificar; auditoría de accesos habilitada.
3. **Calcular y guardar hashes** al momento de ingreso; recalcular antes de cada uso o presentación.
4. **Registrar cadena de custodia** en cada acceso relevante.
5. **Trabajar sobre copias**; reservar originales en resguardo sellado o WORM (Write Once Read Many) cuando sea posible.
6. **Backup verificable** con hashes y control de versiones.
7. **Controles físicos/lógicos:** cifrado, MFA, logs centralizados.

### ¿De qué manera podría verificarse que la evidencia presentada posteriormente coincide con la originalmente obtenida?

- **Comparar el hash** (SHA-256 u otro acordado) del archivo presentado con el hash registrado al momento de la obtención.
- Si coinciden → **integridad técnica** verificada (mismo objeto digital).
- Complementar con **registros de cadena de custodia** que acrediten que nadie tuvo oportunidad de alterar el archivo sin quedar registrado.
- En pericias formales, el perito puede **repetir el procedimiento** y adjuntar constancia de verificación.

---

## Caso 5: Recolección urgente durante un ciberataque

### ¿La urgencia justifica cualquier apartamiento de los protocolos? Fundamentá.

**No justifica cualquier apartamiento**, pero sí puede justificar **adaptaciones proporcionadas y documentadas**.

- La urgencia exige **contener el daño** y **evitar destrucción de evidencia** (logs que se pisan, servicios que se caen).
- Sin embargo, **no autoriza** a manipular evidencia sin registro, trabajar sin control o destruir trazabilidad.
- El criterio es **razonabilidad:** hacer lo mínimo indispensable para preservar, documentar **inmediatamente** qué se hizo y **por qué** no se siguieron todos los pasos ideales, y **completar** el protocolo en cuanto sea posible.

La urgencia explica flexibilidad; **no elimina el deber de documentar y compensar**.

### ¿Qué recaudos deberían adoptarse para compensar las limitaciones iniciales?

1. **Registro detallado en tiempo real:** hora, responsables, acciones, sistemas afectados, herramientas usadas.
2. **Preservación inmediata de lo volátil:** logs, memoria, tráfico de red, capturas de pantalla con timestamp.
3. **Hashes y copias verificables** en cuanto el entorno lo permita.
4. **Separación de roles:** quien contiene el incidente vs. quien preserva evidencia (si es posible).
5. **Cadena de custodia desde el primer momento**, aunque sea en formato provisional.
6. **Pericia o revisión posterior** que reconstruya el procedimiento y valide integridad.
7. **Documentar limitaciones** explícitamente en el informe (qué no se pudo hacer y por qué).

### ¿Qué debería demostrarse para cuestionar jurídicamente la confiabilidad de la evidencia obtenida?

Quien impugna debe mostrar, con argumentos concretos, que:

- Hubo **alteración** o **posibilidad real de alteración** no controlada.
- Existen **vacíos de trazabilidad** (periodos sin responsable identificado).
- Los **hashes no coinciden** o nunca se calcularon.
- El procedimiento fue **arbitrario o negligente**, no merely adaptado a la urgencia.
- Hay **inconsistencias** entre lo documentado y lo presentado.
- Se violaron **derechos** o normas que invalidan la prueba (caducidad, ilegalidad en obtención).

La mera urgencia **no alcanza** para impugnar si el equipo documentó, compensó y demostró integridad después.

---

## Cierre integrador

### ¿Por qué la cadena de custodia resulta indispensable para que una evidencia digital sea confiable y pueda ser valorada jurídicamente?

Porque la evidencia digital es **volátil, reproducible y fácilmente alterable**. El juez no puede “ver” el dispositivo original en la mayoría de los casos: recibe **copias, informes y registros**.

La cadena de custodia permite:

- Reconstruir **de punta a punta** el recorrido de la evidencia.
- Acreditar que **no fue manipulada** sin control.
- Vincular técnicamente el material presentado con el obtenido (**hash**).
- Dar **transparencia** al procedimiento y reducir dudas razonables.

Sin cadena de custodia, aunque el contenido sea relevante, su **valor probatorio se debilita** porque no se puede confiar en su origen ni en su estado.

### ¿Cómo se relacionan integridad, trazabilidad, copia forense, función hash y documentación de las intervenciones?

| Concepto | Rol en el conjunto |
|----------|-------------------|
| **Integridad** | Objetivo: que la evidencia no cambie. Se verifica con hash y se protege con copia forense y resguardo. |
| **Trazabilidad** | Registro de quién, cuándo, cómo y dónde intervino. Da continuidad a la cadena de custodia. |
| **Copia forense** | Medio técnico para **no alterar el original** y analizar sobre réplica verificable. |
| **Función hash** | Herramienta matemática que **demuestra** integridad comparando huellas antes/después. |
| **Documentación** | Soporte escrito de cada intervención; une trazabilidad con integridad y hace auditable todo el proceso. |

**Relación:** se **documenta** cada intervención (trazabilidad), se obtiene **copia forense** del original, se calcula **hash** para fijar integridad, y todo ello permite que la evidencia sea **confiable** al momento de ser **valorada jurídicamente**.

---

## Referencias

- Resolución 232/2023 – Protocolo de recolección y preservación de evidencia digital (Argentina).
- ISO/IEC 27037 – Directrices para identificación, recolección, adquisición y preservación de evidencia digital.
- Convenio de Budapest sobre la Ciberdelincuencia.
- Material Unidad 4 – Cadena de Custodia (Moodle UTN TUP – Legislación).
