# Guía – Cuestionario Práctica U3 (Evidencia Digital)

**Materia:** Legislación  
**Unidad 3:** Evidencia Digital  
**Alumno:** Nicolás Viruel  
**Actividad Moodle:** `CUESTIONARIO - EVIDENCIA DIGITAL`

> Basado en el material oficial *Unidad_3_Evidencia digital tup.pdf*.  
> El cuestionario se corrige automáticamente: leé cada situación y elegí la opción que mejor refleje el material.

---

## Conceptos clave (memorizar)

### Evidencia digital

Cualquier **información almacenada o transmitida en formato digital** que puede servir para probar un hecho: archivos, mensajes, publicaciones, logs, historial de sistemas, etc.

**No alcanza con “tener un dato”**: hay que poder explicar **qué es**, **de dónde proviene** y **cómo se conservó**.

### Origen

Debe identificarse **de qué cuenta, dispositivo, aplicación o sistema** proviene (usuario, URL, recurso verificable). Si el origen es confuso o no verificable, **la evidencia se debilita**.

### Integridad

La evidencia **no fue alterada** desde que se obtuvo hasta que se presenta.

- **Integridad ≠ verdad**: un archivo puede estar íntegro y contener info falsa.
- Integridad = **es el mismo objeto digital**, no que el contenido sea cierto.

### Trazabilidad (registro mínimo / cadena de custodia)

Registro de **quién** la obtuvo, **cuándo**, **cómo**, **dónde** se guardó y **quién accedió** después. Ordena el caso y reduce impugnaciones.

### Hash (ej. SHA-256)

- Cálculo sobre un archivo → cadena alfanumérica (“huella”).
- Si el archivo cambia mínimamente, **el hash cambia**.
- Sirve para verificar **integridad técnica** del archivo.
- **NO prueba**: autoría humana, intención ni veracidad del contenido.

### Integridad vs autenticidad vs veracidad

| Concepto | Pregunta que responde |
|----------|------------------------|
| **Integridad** | ¿Fue alterado el archivo? |
| **Autenticidad / origen** | ¿Es lo que dice ser y de dónde dice venir? |
| **Veracidad** | ¿Es cierto lo que dice el contenido? |

---

## Protocolo Res. 232/2023 (5 etapas)

1. **Identificación** – qué evidencia se busca y cuál es su origen  
2. **Recolección** – obtenerla sin perder contexto ni alterarla  
3. **Preservación** – resguardar el original, trabajar sobre copias  
4. **Procesamiento** – ordenar y analizar  
5. **Presentación** – descripción clara, anexos y registros  

*(Se profundiza en Unidad 4.)*

---

## Mini-informe técnico-jurídico (estructura mínima)

Debe incluir, cuando corresponda:

1. **Identificación** de la evidencia (archivo, dispositivo, cuenta, conversación…)  
2. **Origen** (cuenta, sistema, URL, fuente)  
3. **Forma de obtención** (fecha, hora, persona, procedimiento)  
4. **Medidas de preservación** (original, copias, control de accesos)  
5. **Hash** (algoritmo + valor)  
6. **Hallazgos relevantes** (descripción objetiva, sin exagerar)  
7. **Conclusión técnico-jurídica** (integridad, trazabilidad, si hacen falta verificaciones extra)

---

## Errores frecuentes (suelen ser respuestas incorrectas)

- Capturas **recortadas** sin usuario, URL, fecha u hora  
- Material **desordenado** sin registro del recorrido  
- **Trabajar sobre el original** (abrir, editar, guardar sin conservar la versión inicial)  
- Solo capturas cuando el caso exige **verificación complementaria** (autoría discutida)  
- No identificar con precisión **qué perfil, página o archivo** se quiere acreditar  

---

## Jurisprudencia (casos del material)

### Novopixe (civil – capturas Facebook)

- Actora acompañó acta notarial + capturas de Facebook para probar incumplimiento.  
- La Cámara: captura **puede ser insuficiente** si no individualiza el recurso web ni permite verificar el origen con robustez.  
- **Conclusión:** incumplimiento no acreditado con certeza suficiente.

**Si preguntan por qué falló la prueba:** origen no verificable / no se identificó con precisión el recurso web.

### NN – Sala III CABA (penal – hash)

- Evidencia principal: capturas del celular de la denunciante.  
- Defensa: nulidad por **inconsistencia en el hash** → supuesta ruptura de cadena de custodia.  
- Tribunal: el hash está ligado a la **integridad**; hay que ver si hubo **afectación concreta y verificable**, no basta una irregularidad formal.  
- **Rechazó la nulidad** porque no hubo impacto real demostrado en la confiabilidad.

**Clave:** irregularidad formal en el hash ≠ automáticamente nulidad; importa el **impacto real** en la prueba.

### L.G.L. c/ Z.R.E.F. – SCJ Mendoza (WhatsApp)

- Demandado ofreció capturas de WhatsApp + pidió pericia para cotejar con pendrive.  
- La Corte admitió pericia **acotada** para cotejar archivos del pendrive con las capturas.  
- **Clave:** cuando hay controversia sobre autenticidad, recortes o contexto → hace falta **verificación complementaria** (pericia de cotejo).

---

## Respuestas típicas del cuestionario (patrones)

### “¿Qué garantiza el hash?”
→ **Integridad del archivo** (que no fue alterado).  
**No** garantiza veracidad, autoría ni intención.

### “¿Integridad significa que el contenido es verdadero?”
→ **Falso.** Integridad solo dice que es el mismo archivo, no que lo que dice sea cierto.

### “¿Qué debilita una captura de pantalla?”
→ Recorte sin contexto, sin fecha/hora/usuario/URL, sin registro de obtención, imposibilidad de verificar origen.

### “¿Qué medida ayuda a preservar evidencia?”
→ Conservar el **original**, generar **copias**, calcular **hash al momento de la obtención**, documentar **quién/cuándo/cómo**, limitar accesos.

### “¿Una captura alcanza siempre como prueba?”
→ **No.** Depende de poder verificar origen e integridad; a veces se necesita pericia u otra verificación.

### “¿Qué es trazabilidad?”
→ Registro del recorrido: quién obtuvo la evidencia, cuándo, cómo, dónde se guardó y quién accedió después.

### “¿Qué NO debe hacerse con la evidencia original?”
→ Abrirla, editarla o guardarla sin conservar la versión inicial intacta.

### “¿Para qué sirve un mini-informe?”
→ Documentar de forma ordenada qué se examinó, cómo se obtuvo y qué medidas se tomaron; **no reemplaza** una pericia cuando esta es necesaria.

### Situaciones prácticas (ejemplos)

**Caso A:** Alguien imprime un WhatsApp recortado sin mostrar contacto ni fecha.  
→ Problemas: **origen**, **trazabilidad**, posible **falta de integridad/contexto**.

**Caso B:** Se calcula SHA-256 al obtener un PDF y coincide al presentarlo meses después.  
→ Soporta **integridad**; no prueba que el PDF diga la verdad.

**Caso C:** Hash distinto al comparar copia con original.  
→ Indica que el archivo **fue modificado** (se rompió integridad).

**Caso D:** Error de tipeo en el número de hash en el acta, pero el archivo no cambió y hay otros respaldos.  
→ Puede ser **irregularidad formal** sin afectación concreta (como en caso NN).

---

## Checklist antes de enviar

- [ ] Identifiqué en cada situación: **origen**, **integridad**, **trazabilidad**
- [ ] Distinguí si preguntan por **hash** (integridad) o por **veracidad/autoría**
- [ ] Revisé si el caso menciona **capturas**, **pericia** o **Res. 232/2023**
- [ ] En jurisprudencia: Novopixe = origen débil; NN = hash/impacto concreto; Mendoza = cotejo/pericia

---

*Cuando estés en el cuestionario, podés copiar cada pregunta con sus opciones y te indico la respuesta exacta.*
