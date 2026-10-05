**Nombre completo y legajo:** Nicolás Viruel — Legajo: 100634

**Materia:** Legislación — Tecnicatura Universitaria en Programación — UTN

**Trabajo:** Actividad Práctica — Unidad 9 — Responsabilidad civil y penal en sistemas informáticos

**Comisión:** TUPaD

**Fecha de entrega:** 28/09/2026

---

## Situación 1 — El sistema de facturación que falló

### 1. ¿Qué tipo de responsabilidad está en juego? ¿Por qué?

Predomina la **responsabilidad civil contractual**: existe un contrato de desarrollo/mantenimiento entre la empresa de limpieza y el programador, y el reclamo ($850.000 más consecuencias frente a AFIP) deriva del **incumplimiento de la obligación de entregar un sistema que calcule correctamente el IVA** (prestación defectuosa / falta de diligencia en la actualización).

No es, en principio, **responsabilidad penal** salvo que se acredite dolo o maniobra fraudulenta; acá hay un **error de programación** en contexto contractual.

La vía **extracontractual** (arts. 1722 ss. CCyCN) podría plantearse solo si el daño se discute **fuera** del marco del contrato (p. ej. perjuicios a terceros no vinculados contractualmente). Frente al cliente directo, la base natural es **contractual** (arts. 1716 y ss. CCyCN: incumplimiento genera reparación del daño).

### 2. ¿Qué elementos necesitarías probar para defenderte?

- **Existencia y alcance del contrato**: qué incluía el mantenimiento, si las actualizaciones urgentes estaban previstas y con qué estándar de calidad/pruebas.
- **Hecho imputable al cliente**: pedido expreso de **actualización de urgencia** sin margen de testing (mails, tickets, actas).
- **Causalidad y mitigación**: que el daño se debió a esa modalidad de entrega y no a una falla previa no reportada; que se **avisó** del riesgo y el cliente aceptó igual.
- **Cuantía del daño**: desglose del monto reclamado y nexo con el error de IVA (evitar sumas especulativas).
- **Conducta diligente parcial**: backups, rollback posible, tiempo de detección y corrección.

### 3. ¿Qué deberías haber hecho antes de implementar la actualización?

- **Change request por escrito** (alcance, plazo, renuncia expresa a pruebas completas si el cliente insiste).
- Despliegue en **ambiente de prueba** aunque sea acotado; checklist fiscal/IVA; **pruebas de regresión** mínimas documentadas.
- **Registro de versión** (commit, release notes) y plan de **rollback**.
- Comunicar por escrito: “sin testing completo aumenta el riesgo de error en facturación”.

### 4. ¿Qué cláusula en el contrato original habría ayudado?

- **Gestión de cambios y aceptación**: entregables por versión, prueba de aceptación y plazo para observaciones.
- **Actualizaciones urgentes**: si el cliente exige omitir pruebas, **libera o limita** responsabilidad por errores derivados de esa decisión (con límite de buena fe y no exoneración por dolo).
- **Limitación de responsabilidad** razonable (daños directos, tope vinculado al honorario), excluyendo lucro cesante imprevisible salvo pacto.
- **Responsabilidad fiscal**: obligación del cliente de **validar** cálculos impositivos con su contador/AFIP antes de producción masiva.

---

## Situación 2 — El acceso “sin querer” al servidor

### 5. ¿Cometiste algún delito? ¿Cuál? (Ley 26.388)

La **Ley 26.388** incorporó al Código Penal delitos informáticos. El ingreso **sin autorización** a un sistema ajeno y el acceso a **datos reservados** puede encuadrar en el **art. 153 bis CP** (acceso ilegítimo a sistemas y datos informáticos), aunque no hayas modificado ni copiado masivamente: la **mera penetración** sin consentimiento del titular del sistema suele ser punible.

Si se considerara acceso a datos especialmente sensibles (tarjetas, datos personales), pueden sumarse figuras relacionadas con **violación de secretos** (art. 157 CP) según cómo se califique la conducta y el acceso a información reservada.

La **curiosidad** o ausencia de ánimo de lucro **no elimina** automáticamente el tipo; puede influir en la valoración penal concreta, pero el riesgo delictual existe.

### 6. ¿Qué deberías hacer jurídicamente?

- **Cesar de inmediato** cualquier acceso; no explorar más ni compartir capturas con terceros.
- **Documentar** fecha, hora, alcance mínimo necesario para acreditar la vulnerabilidad (sin conservar datos personales innecesarios).
- **Notificar de forma responsable** al titular del sistema (empresa vecina) o canal seguro (CERT, abogado, mail al domicilio legal), describiendo la falla **sin divulgar** la base ni los datos.
- **No entregar** a tu cliente la base ajena: eso agrava riesgos civiles y penales.
- Si tu contrato lo exige, **avisar a tu cliente** solo que detectaste un hallazgo **fuera de alcance** y que derivaste el aviso al responsable correspondiente.

### 7. ¿Qué riesgos corre la empresa con la base expuesta? (Ley 25.326)

Como **responsable del archivo** de datos personales (arts. 2 y 9 **Ley 25.326**), debe adoptar **medidas de seguridad** técnicas y organizativas acordes. Una base con 10.000 clientes y tarjetas sin contraseña implica:

- **Incumplimiento** del deber de seguridad y posibles sanciones de la **AAIP** (art. 31 y ss.).
- **Responsabilidad civil** frente a titulares de datos por daños derivados del acceso indebido.
- Obligación de **investigar**, **mitigar** y, en su caso, **notificar** la vulneración según la normativa y criterios de la autoridad (deber de transparencia ante incidentes graves).

### 8. ¿Cambia algo que no modificaste ni te llevaste nada?

**Sí, pero no “libera” del todo.** No robar ni alterar reduce la gravedad respecto de sabotaje o fraude, pero el **acceso no autorizado** ya puede ser relevante penalmente (art. 153 bis). En sede civil, también puede generar **reparación** si se acredita perjuicio o agravamiento del riesgo. El hecho de “solo mirar” es una circunstancia favorable, no una licencia para entrar.

---

## Situación 3 — La app que se cayó en el peor momento

### 9. ¿Responsabilidad si fue culpa del hosting? ¿Transferir el reclamo?

Frente al **restaurante** la relación es **contractual** (mantenimiento y hosting por $15.000/mes): vos sos el **prestador** integrador del servicio que contrataron. Si el contrato no prevé expresamente subcontratar hosting “como está”, el cliente puede **reclamarte a vos** por incumplimiento de disponibilidad (arts. 1716 CCyCN).

Podés **repetir** contra el proveedor de hosting si tenés contrato con cláusula de **indemnidad** o responsabilidad por caídas, pero eso es entre vos y el hosting; **no sustituye** automáticamente tu respuesta al cliente salvo que el contrato con el restaurante diga lo contrario o una cláusula de tercero proveedor claramente pactada.

### 10. ¿Qué tipos de daños reclama? ¿Son todos reclamables?

- **Daño emergente**: pérdida concreta vinculada al hecho (pedidos no concretados ~$120.000) — reclamable si se **prueba** nexo causal y razonabilidad del monto.
- **Lucro cesante**: ganancia dejada de obtener durante la caída — también en sede contractual, con **prueba más exigente** (proyecciones, históricos del sábado noche).
- **Daño a la reputación** (reseñas en Google Maps): puede encuadrarse como **daño moral** o perjuicio reputacional; en personas jurídicas es **discutible y difícil de cuantificar**; requiere prueba del menoscabo y del nexo directo con la caída (no con mala calidad general del servicio).

### 11. ¿Un SLA bien redactado limitaría la exposición?

Sí. Un **SLA** puede fijar:

- **Uptime** mínimo (p. ej. 99,5 %) y **créditos** de servicio (descuento mensual) como **única compensación** por caídas.
- **Exclusión** de lucro cesante, daño indirecto y reputacional salvo dolo.
- **Tope de responsabilidad** (p. ej. monto de un mes de fee).
- Procedimiento de **notificación** de incidentes y ventanas de mantenimiento.

Eso no exime por **dolo** o negligencia grave, pero ordena expectativas y reduce litigios.

### 12. Medidas técnicas preventivas

- Monitoreo 24/7, **alertas**, health checks.
- **Redundancia** (multi-AZ, balanceador, réplica).
- Backups y **plan de recuperación** probado; runbooks.
- Escalado automático; CDN para estáticos.
- Contrato con hosting de **SLA** alineado al que ofrecés al cliente.

---

## Situación 4 — El empleado que se llevó la base de datos

### 13. ¿Qué delitos pudo cometer el ex empleado?

Según los hechos (descarga masiva no autorizada de datos sensibles de salud):

- **Art. 153 bis CP** (Ley 26.388): acceso/copy desde sistema informático **sin autorización** o excediendo la autorizada.
- **Art. 157 CP**: **violación de secretos** (datos reservados de personas; diagnósticos y medicación son claramente sensibles).
- Según uso posterior: **art. 173** (defraudación) si vendiera o usara los datos; **art. 155** (apoderamiento) si se trata de apropiación de información con ánimo de lucro.

La calificación final depende de prueba, pero la descarga previa a la renuncia es **muy grave**.

### 14. ¿Responsabilidad de la empresa y del líder técnico?

- **Civil**: la empresa, como responsable del tratamiento (**Ley 25.326**), responde frente a pacientes por daños por falta de **medidas de seguridad** razonables (art. 9).
- **Administrativa**: sanciones AAIP por archivo mal custodiado.
- **Vos como líder técnico**: no sos “automáticamente” penado por la fuga, pero podés tener **responsabilidad laboral/profesional** si incumpliste deberes de **diligencia** (políticas de acceso, offboarding, alertas) previstos en tu rol; en sede civil, eventual **responsabilidad solidaria** si se acredita culpa in vigilando o in eligendo (depende del encuadre y prueba).

### 15. Obligaciones de la empresa frente a los pacientes (Ley 25.326)

- **Contener** el incidente: revocar credenciales, bloquear exfiltración, recuperar equipos si es posible legalmente.
- **Evaluar** alcance con pericia forense y logs.
- **Notificar a la AAIP** y, cuando corresponda, **comunicar a los titulares** afectados (deber de información ante vulneraciones relevantes).
- Ofrecer **medidas de mitigación** (monitoreo, recomendaciones) y revisar **bases legales** del tratamiento de datos de salud.

### 16. Medidas técnicas y contractuales preventivas

**Técnicas:** mínimo privilegio, RBAC, **bloqueo de exportaciones** masivas, DLP, cifrado en reposo y tránsito, MFA, alertas sobre descargas anómalas, **offboarding** automatizado (baja de accesos el mismo día), auditoría de logs, segmentación de red.

**Contractuales:** NDA y cláusulas de **confidencialidad** y propiedad de datos; política interna de uso aceptada; **cláusula penal** por violación; inventario de activos; capacitación en **Ley 25.326**; procedimiento POE de baja de empleados.

---

## Reflexión final (optativa)

Como programador, la responsabilidad no termina cuando “compila”: cada despliegue, acceso a un sistema ajeno o dato de salud es una decisión con **civil, administrativa y a veces penal**. La prevención —contratos claros, SLA, trazabilidad, seguridad y no curiosear redes ajenas— es la forma más barata de defensa jurídica y profesional.
