**Nombre completo y legajo:** Nicolás Viruel — Legajo: 100634

**Materia:** Legislación — Tecnicatura Universitaria en Programación — UTN

**Trabajo:** TP Unidad 8 — Análisis de Contrato de Desarrollo de Software

**Comisión:** TUPaD

**Fecha de entrega:** 23/09/2026

---

## 1. Identificación de cláusulas

| Cláusula | Nombre | ¿Qué regula? | Tipo de cláusula |
|----------|--------|--------------|------------------|
| PRIMERA | Partes contratantes | Identificación, domicilio y representantes de TechSoluciones S.R.L. y Comercial del Litoral S.A. | **Formal** |
| SEGUNDA | Objeto | Alcance funcional del sistema (facturación, stock, clientes, reportes) y remisión al Anexo I | **Esencial** |
| TERCERA | Plazo de desarrollo | Cronograma por etapas (~6 meses) y condición suspensiva por demora del cliente | **Accesoria** (modalidad de ejecución) |
| CUARTA | Precio y pago | Monto total y calendario 30/40/30 | **Esencial** |
| QUINTA | Propiedad intelectual | Titularidad en la desarrolladora; licencia de uso al cliente; no entrega de fuente | **Esencial** (afecta objeto económico del negocio) |
| SEXTA | Confidencialidad | Deber de reserva recíproco por 2 años post finalización | **Accesoria** |
| SÉPTIMA | Garantía | Corrección de fallas imputables al desarrollo por 90 días | **Accesoria** |
| OCTAVA | Rescisión | Resolución por incumplimiento con preaviso 15 días y pago de trabajos realizados | **Resolutoria** |
| NOVENA | Domicilio y jurisdicción | Fueros de Paraná | **Formal** |
| DÉCIMA | Conformidad | Firma en dos ejemplares | **Formal** |

---

## 2. Elementos esenciales del contrato (art. 957 CCyC)

| Elemento | ¿Dónde aparece? | ¿Correctamente contemplado? | ¿Por qué? |
|----------|-----------------|----------------------------|-----------|
| **Consentimiento** | Cláusula DÉCIMA (firma de ambos representantes) | **Sí**, en principio | Hay manifestación de voluntad; falta detalle sobre **aceptación por etapas** y actas de conformidad, lo que puede generar disputas sobre si hubo consentimiento sobre entregables parciales. |
| **Capacidad** | PRIMERA (S.R.L. con socio gerente; S.A. con presidente) | **Sí** | Se identifican personas con aparente representación legal; en la práctica convendría acreditar **poderes** o estatutos. |
| **Objeto** | SEGUNDA + Anexo I | **Parcialmente** | El objeto es lícito, determinado y posible, pero depende de un anexo no reproducido; sin Anexo I el objeto puede ser **indeterminado** en requisitos técnicos. |
| **Causa** | Conjunto SEGUNDA + CUARTA | **Sí** | Causa onerosa: el cliente obtiene software a cambio de precio; la desarrolladora percibe honorarios a cambio del servicio. |
| **Forma** | Contrato escrito firmado (DÉCIMA) | **Sí** para este tipo de contrato | No exige forma especial más allá del acuerdo escrito; adecuado para desarrollo a medida entre empresas. |

---

## 3. Evaluación de redacción por cláusula

| Cláusula | ¿Bien redactada? | Justificación / problemas prácticos |
|----------|------------------|-------------------------------------|
| PRIMERA | **Sí** | Datos identificatorios claros. Riesgo menor: no se adjunta constancia de inscripción/registro. |
| SEGUNDA | **Parcial** | Módulos listados, pero sin criterios de aceptación ni SLA; disputas sobre “terminado”. |
| TERCERA | **Parcial** | Plazos “aproximados”; suspensión unilateral si el cliente demora — puede abusarse para extender sin costo. |
| CUARTA | **No** | Monto **$120.000** irrisorio para 6 meses de desarrollo; no menciona **IVA**, indexación, hitos vinculados a **aceptación** ni intereses por mora. |
| QUINTA | **No** | Cliente paga pero no es titular ni recibe fuente; **lock-in** y dificultad para mantener/evolucionar el sistema. |
| SEXTA | **Parcial** | Confidencialidad genérica; no define **datos personales** (Ley 25.326) ni devolución/destrucción al terminar. |
| SÉPTIMA | **Parcial** | Solo 90 días; solo fallas “imputables”; no cubre **vulnerabilidades**, actualizaciones ni soporte. |
| OCTAVA | **Parcial** | Rescisión vaga (“incumplimiento”); pago de trabajos realizados sin **criterio de medición** ni entrega de lo ya pagado. |
| NOVENA | **Sí** | Jurisdicción clara; podría sumarse mediación previa. |
| DÉCIMA | **Sí** | Formalidad de cierre adecuada. |

---

## 4. Reformulación de tres cláusulas deficientes

### Cláusula elegida N°1 — CUARTA (Precio y pago)

**Texto original:** Precio total $120.000; 30% firma, 40% inicio Etapa 3, 30% entrega final.

**Reformulación propuesta:**

> **CUARTA – PRECIO Y CONDICIONES DE PAGO.** El precio total del desarrollo asciende a **pesos [MONTO EN CIFRAS Y LETRAS] más IVA**, conforme factura tipo A/B según corresponda. Los pagos se efectuarán contra **acta de conformidad** de cada hito: (i) 25% a la firma; (ii) 25% aprobación del diseño funcional y técnico (Anexo I); (iii) 25% puesta en producción de facturación y stock; (iv) 25% aceptación final según protocolo de pruebas (Anexo II). La mora del CLIENTE devengará intereses a la tasa activa del Banco Nación. Ningún hito se considerará adeudado si el entregable no supera las pruebas acordadas.

---

### Cláusula elegida N°2 — QUINTA (Propiedad intelectual)

**Texto original:** Software propiedad de la desarrolladora; licencia de uso; sin código fuente.

**Reformulación propuesta:**

> **QUINTA – PROPIEDAD INTELECTUAL Y CÓDIGO FUENTE.** El software específico desarrollado para la CLIENTE (excluidos frameworks, librerías de terceros y know-how preexistente de la DESARROLLADORA) será de **titularidad conjunta** o, alternativamente, de titularidad de la CLIENTE, otorgándose a la DESARROLLADORA licencia interna limitada solo para soporte. La DESARROLLADORA entregará **código fuente**, scripts de despliegue y documentación técnica en repositorio acordado dentro de los cinco (5) días hábiles de la aceptación final. Queda prohibido usar datos o módulos confidenciales de la CLIENTE en otros proyectos sin autorización escrita.

---

### Cláusula elegida N°3 — SÉPTIMA (Garantía)

**Texto original:** 90 días; corrección de errores imputables al desarrollo.

**Reformulación propuesta:**

> **SÉPTIMA – GARANTÍA Y SOPORTE.** Por doce (12) meses desde la aceptación final, la DESARROLLADORA corregirá **defectos de conformidad** con el Anexo I sin cargo adicional, con tiempos de respuesta: críticos 8 h hábiles, mayores 48 h, menores 5 días. Se incluye al menos una (1) actualización de seguridad por vulnerabilidad media/alta. Lo no cubierto por garantía podrá contratarse bajo **acuerdo de mantenimiento** con tarifas previamente publicadas. La garantía no se suspende por uso normal del sistema en producción.

---

## 5. Temas ausentes relevantes

| Tema ausente | ¿Por qué debería estar? |
|--------------|-------------------------|
| **Criterios de aceptación y pruebas (UAT)** | Sin protocolo de aceptación, el cliente no puede rechazar entregables defectuosos ni definir cuándo se debe el 30% final. |
| **Gestión de cambios (change requests)** | Todo proyecto real tiene cambios de alcance; sin cláusula de **adicionales**, precio y plazo se discuten informalmente y terminan en juicio. |
| **Protección de datos personales y seguridad** | El sistema maneja clientes y facturación; hace falta rol de responsable, medidas de seguridad, notificación de incidentes y devolución de datos al fin del contrato (Ley 25.326 y buenas prácticas). |

*(Otros útiles: subcontratación, continuidad/backup, limitación de responsabilidad proporcional, fuerza mayor, propiedad de datos del cliente.)*

---

## 6. Cláusula Quinta y Ley 11.723

### ¿Qué dice la Ley 11.723?

En Argentina, la **Ley 11.723** protege las obras del intelecto. El **software** se trata como obra literaria (interpretación doctrinaria y jurisprudencial consolidada): nace la protección con la **creación** y el titular es quien detenta el derecho de autor, salvo contrato laboral o encargo distinto. Permite **contratos de cesión o licencia**; la inscripción en el Registro Nacional del Derecho de Autor refuerza prueba, pero no es condición de existencia del derecho.

### Riesgos para el cliente si la desarrolladora conserva la titularidad y no entrega fuente

- **Dependencia tecnológica (vendor lock-in):** no puede corregir bugs, migrar servidor ni contratar otro proveedor con el código.
- **Riesgo operativo y de continuidad:** si TechSoluciones cierra o deja de responder, el cliente pierde capacidad de evolucionar el sistema que paga por usar.
- **Limitación de garantía real:** sin fuente, auditar vulnerabilidades o cumplir normativa (facturación electrónica AFIP) es más difícil.
- **Valor patrimonial:** el cliente financia el desarrollo pero no capitaliza un activo intangible propio.

### Redacción equilibrada (protege al cliente sin anular a la desarrolladora)

> La CLIENTE será titular del software **a medida** desarrollado para su operatoria. La DESARROLLADORA conserva derechos sobre su **know-how**, librerías genéricas reutilizables y componentes previos. Se otorga a la DESARROLLADORA licencia no exclusiva, gratuita y perpetua para reutilizar módulos genéricos despersonalizados. El código fuente se depositará en escrow o se entregará a la CLIENTE con la aceptación final. Precio y plazo del contrato reflejan esta cesión parcial de derechos patrimoniales.

---

## 7. Perspectiva del programador principal de TechSoluciones

**¿Firmaría tal como está?** **No**, sin negociar.

**Tres cambios antes de firmar:**

1. **Precio y pagos (CUARTA):** el monto y los hitos desvinculados de aceptación exponen a cobrar de menos y a cobrar litigios; alinear pagos a entregables verificables protege al equipo y evita scope creep gratis.

2. **Propiedad intelectual (QUINTA):** mantener todo el código en la S.R.L. puede parecer ventajoso, pero en la práctica genera **rechazo de clientes corporativos** y responsabilidad ilimitada de soporte; un reparto claro (cliente = a medida, dev = framework) reduce conflictos.

3. **Garantía y alcance (SEGUNDA + SÉPTIMA):** definir **Anexo I** con requisitos, pruebas y límites de soporte; ampliar garantía razonable con SLAs evita que “cualquier cambio pedido por WhatsApp” se interprete como bug incluido.

**Justificación:** como dev líder, necesito **alcance cerrado**, **pagos atados a hitos** y **reglas de PI** que permitan mantener el producto sin quedar atrapado en demandas indefinidas ni en un contrato económicamente inviable ($120.000).
