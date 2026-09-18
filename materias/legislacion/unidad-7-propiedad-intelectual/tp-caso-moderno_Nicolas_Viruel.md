# TRABAJO PRÁCTICO — Caso moderno (IA y derechos de autor)

**Materia:** Legislación  
**Unidad 7:** Propiedad intelectual  
**Actividad:** Casos modernos — *The New York Times v. OpenAI / Microsoft*  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN

---

## Contexto del caso (2023–actualidad)

The New York Times demandó a **OpenAI** y **Microsoft**, alegando que artículos periodísticos protegidos se usaron **sin autorización** para entrenar modelos de lenguaje (ChatGPT y relacionados), generando respuestas que **reproducen o compiten** con el contenido original y afectan su modelo de negocio.

---

## Análisis

### ¿Qué está en juego?

- **Derecho de autor** sobre obras periodísticas.
- **Uso de obras para entrenamiento** de IA (¿copia? ¿transformación? ¿fair use / excepción?).
- **Competencia desleal** si el modelo devuelve fragmentos sustancialmente iguales.
- **Responsabilidad** de quien provee el servicio (OpenAI/Microsoft) vs. usuario final.

### Enseñanzas para futuros programadores

1. **No asumir que “está en internet” es libre de usar** para entrenar, fine-tunear o reempaquetar productos comerciales.
2. **Documentar datasets**: origen, licencias, filtros de copyright, registros de scraping.
3. **Separar entornos**: datos de clientes, datos públicos y datos con restricción contractual (NDA, TOS).
4. **Revisar Términos de Servicio** de APIs de IA antes de integrarlas en productos.
5. **Diseñar con compliance**: opt-in, atribución, bloqueo de regurgitación literal, auditoría de prompts/salidas.
6. **Propiedad del código generado**: definir en contratos laborales/comerciales quién es titular y bajo qué licencia.

### Precauciones al encarar un proyecto con IA

| Riesgo | Precaución |
|--------|------------|
| Entrenar con obras protegidas | Usar datasets con licencia explícita o contenido propio. |
| Filtraciones de prompts con datos sensibles | Políticas de no subir secretos comerciales ni datos personales. |
| Salidas que copian textos | Evaluación automática de similitud, límites de cita, revisión humana. |
| Dependencia de un proveedor | Cláusulas de indemnización, plan B, modelos self-hosted cuando aplique. |

---

## Conclusión

El caso NYT v. OpenAI marca la frontera entre **innovación en IA** y **derechos de autores tradicionales**. Para un programador, la lección práctica es: **tratar datos y modelos como activos regulados**, no como material gratis. La precaución legal es parte del **MVP serio**, igual que la seguridad y la calidad.
