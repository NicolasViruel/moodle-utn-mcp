# TRABAJO PRÁCTICO 2 — Tabla de relación y cumplimiento

**Materia:** Legislación  
**Unidad 10:** Protección de datos personales y Habeas Data  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN  
**Fecha:** 5 de octubre de 2026

---

## Objetivo

Relacionar **ISO/IEC 25010** (calidad del producto software), **ISO/IEC 27001** (seguridad de la información) y el cumplimiento de la **Ley 25.326** (protección de datos personales / Habeas Data) al desarrollar software que trata datos personales.

---

## Tabla de correlación

| ISO/IEC 25010 (calidad del software) | ISO/IEC 27001:2022 (referencia SGSI) | Cumplimiento Ley 25.326 / Habeas Data |
|--------------------------------------|--------------------------------------|----------------------------------------|
| **Seguridad — Confidencialidad:** el software no expone datos a quien no debe verlos. | **Anexo A — Control de acceso** (identidad, autenticación, derechos mínimos). | Art. 9 y 10: medidas de seguridad y confidencialidad acordes al riesgo; deber de custodiar datos. |
| **Seguridad — Integridad:** los datos no se alteran sin autorización. | **Protección de la información** (registro, integridad, logs). | Art. 4: datos exactos, actualizados y pertinentes; evitar tratamientos que distorsionen titularidad. |
| **Seguridad — No repudio / trazabilidad** (apoyo a confianza del servicio). | **Registro y monitoreo** de eventos de seguridad. | Arts. 14–16: posibilidad de acreditar tratamientos y responder acciones de acceso, rectificación, supresión. |
| **Fiabilidad — Disponibilidad:** el servicio que trata datos está accesible cuando corresponde. | **Continuidad del negocio** y copias de seguridad. | Art. 9: medidas que eviten pérdida o indisponibilidad indebida de archivos de datos personales. |
| **Adecuación funcional — Completitud / corrección:** el sistema hace lo que debe con los datos. | **Desarrollo seguro** y requisitos de seguridad en el ciclo de vida. | Arts. 5–6: tratamiento conforme a finalidad informada; consentimiento o base legal válida. |
| **Compatibilidad — Interoperabilidad** (APIs, integraciones). | **Seguridad en relaciones con proveedores** y transferencias. | Arts. 11 y 25: cesión y transferencia internacional solo con consentimiento o excepciones legales y garantías. |
| **Mantenibilidad — Modularidad / analizabilidad** | **Arquitectura segura** y gestión de cambios. | Registro de bases ante AAIP (Dec. 1558/2001); documentación de finalidad y categorías de datos. |
| **Usabilidad — Reconocimiento de errores / protección frente a uso incorrecto** | **Formación y concienciación** en seguridad. | Art. 7: informar al titular de forma clara sobre finalidad y derechos antes del tratamiento. |
| **Rendimiento — Comportamiento temporal** (sin degradar controles de seguridad). | **Capacidad y monitoreo** sin sacrificar controles. | Principio de **calidad** (art. 4): no conservar más datos ni más tiempo del necesario (minimización operativa). |
| **Portabilidad — Capacidad de instalación / reemplazo** | **Gestión de activos** y borrado seguro. | Art. 16 inc. 3: **supresión** cuando el titular lo solicite y proceda; destrucción segura de soportes. |

---

## Síntesis profesional

Certificar o alinear el software con **ISO/IEC 25010** no reemplaza la **Ley 25.326**, pero la **característica “seguridad”** y la **fiabilidad** del producto se refuerzan con un **SGSI ISO 27001**. En proyectos que manejan datos personales (apps de crédito, salud, turnos), conviene diseñar requisitos de calidad y controles de seguridad **en la misma matriz**: así la “calidad del software” incluye **confianza digital** exigida por Habeas Data, no solo performance o pantallas.

**Referencia normativa:** Ley 25.326; Decreto 1558/2001; ISO/IEC 25010:2011/2023; ISO/IEC 27001:2022.
