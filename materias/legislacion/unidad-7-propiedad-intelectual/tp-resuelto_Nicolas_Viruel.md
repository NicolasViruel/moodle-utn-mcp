# TRABAJO PRÁCTICO — Propiedad intelectual (casos judiciales)

**Materia:** Legislación  
**Unidad 7:** Propiedad intelectual  
**Alumno:** Nicolás Viruel  
**Comisión:** TUPaD – UTN

---

## Caso 1: Google v. Oracle (2010–2021)

### 1. ¿Qué acusó Oracle a Google de haber copiado?

Oracle sostuvo que Google **copió la estructura de las APIs de Java** (declaraciones de paquetes, clases y métodos — la “API declaring code”) para implementar Android, sin licencia, vulnerando derechos de autor sobre esa organización del entorno Java.

### 3. ¿Cuántas líneas estuvieron en disputa?

En el proceso se discutieron **aproximadamente 11.500 líneas** de código declarativo de APIs (cifra referida en el litigio; el debate legal fue más amplio que “líneas totales del SO”).

### 4. ¿Para qué sistema utilizó Google ese código?

Para el ecosistema **Android**: permitir que desarrolladores usaran un entorno familiar tipo Java en dispositivos móviles.

### 5. ¿Por qué la reutilización de APIs es importante para los desarrolladores?

Porque evita reinventar interfaces básicas, facilita **compatibilidad**, reduce costos de aprendizaje y permite que aplicaciones distintas **interoperen** con plataformas existentes.

### 6. ¿Qué significa interoperabilidad en software?

Capacidad de que **sistemas distintos se comuniquen y funcionen juntos** usando interfaces conocidas (APIs, formatos, protocolos) sin depender de un único proveedor cerrado.

### 7. ¿Por qué la Corte Suprema de EE.UU. consideró fair use?

Porque entendió que reimplementar la **API declarativa** para un **uso transformador** (Android móvil, nuevo mercado) con fines compatibles, y sin sustituir el mercado de Java SE en PC, podía encuadrar en **fair use** — especialmente dado el carácter funcional/interoperable de las APIs.

### 8. ¿Qué problemas generaría hacer las APIs totalmente propietarias?

Monopolios de plataforma, **bloqueo de competencia**, más costos para devs, menos innovación compatible y riesgo de **lock-in** tecnológico.

### 9. Ventajas de usar APIs existentes al desarrollar una app

Menor tiempo de desarrollo, ecosistema de librerías, documentación existente, integración con servicios de terceros y expectativas estándar de usuarios y clientes.

### 10. ¿Copiar estructuras de APIs debería ser legal?

**Posición argumentada:** Sí, **con límites**. Debe permitirse la **reimplementación declarativa** para interoperar (como en el fallo), pero **no** copiar implementaciones completas ni violar marcas/licencias expresas. El equilibrio protege inversión sin frenar la competencia técnica.

---

## Caso 2: Viacom v. YouTube (2007–2012)

### 11. ¿Por qué Viacom demandó a YouTube?

Por **infracción de derechos de autor**: contenido protegido (programas, clips) subido por usuarios **sin autorización**, con YouTube obteniendo beneficio de la plataforma.

### 12. ¿Qué tipo de contenido estaba en conflicto?

Obras audiovisuales protegidas (series, sketches, material de TV) **subidas por terceros** a la plataforma.

### 13. ¿Qué monto reclamaba Viacom?

Aproximadamente **1.000 millones de dólares** en daños alegados.

### 14. ¿Qué ley fue clave?

La **DMCA** (*Digital Millennium Copyright Act*, EE.UU.).

### 15. ¿Qué es el “safe harbor”?

Régimen que **limita la responsabilidad** de intermediarios (plataformas) por contenido de usuarios si cumplen ciertos deberes (política de retiro, agente de notificaciones, etc.).

### 16. Condiciones para no ser responsables por contenido de usuarios

- No tener **conocimiento efectivo** de infracción específica sin actuar.
- Implementar política de **notice and takedown**.
- No obtener beneficio directo de infracciones que controla.
- Designar **agente** para recibir notificaciones.

### 17. Rol del takedown notice

Permite al titular de derechos **notificar** contenido infractor; la plataforma debe **retirar** oportunamente para mantener el safe harbor.

### 18. Riesgos si las plataformas fueran responsables automáticamente

Cierre de servicios de hosting, **censura preventiva**, menos espacios para UGC, innovación social y repositorios de código/contenido colaborativo.

### 19. Medidas si crearas una plataforma tipo red social o repo

Política de copyright clara, canal de **denuncias**, procedimiento de **takedown**, registro de agente, logs, términos de uso, moderación tras notificación, educación a usuarios, y cumplimiento local (DMCA si opera en EE.UU., Ley 11.723 / 25.036 en Argentina según caso).

### 20. ¿El sistema actual favorece más a tech o a creadores?

**Equilibrio tendencial a plataformas** en EE.UU. por safe harbor, pero con herramientas para creadores (takedown). En la práctica, **escala y recursos legales** suelen favorecer a grandes tech; los creadores dependen de notificar y negociar licencias. Argumento: hace falta **transparencia** y reparto justo de ingresos.

---

## Preguntas integradoras

### 21. Comparación Google/Oracle vs Viacom/YouTube

**En común:** límites de **propiedad intelectual** en el ecosistema digital; tension entre **innovación** y **exclusividad**.  
**Diferencia:** Google/Oracle discute **reimplementación de APIs** (fair use, interoperabilidad). Viacom/YouTube discute **contenido subido por terceros** y responsabilidad de **intermediarios** (safe harbor).

### 22. Influencia en el trabajo diario de un programador

Define si podés **reusar interfaces**, integrar SDKs, publicar librerías, usar snippets, y qué **riesgo** hay al clonar repos, scrapear o entrenar modelos con datos ajenos. También condiciona políticas de **compliance** en la empresa.

### 23. Equilibrio deseado

Entre **proteger inversión** del autor/empresa y **permitir interoperabilidad, investigación y competencia**. En software, muchas interfaces son **funcionales**; el derecho de autor no debería monopolizar ideas, solo expresiones concretas.

### 24. ¿Leyes actualizadas frente al software?

**Parcialmente no.** Leyes pre-digitales y tratados no contemplan bien **APIs**, **IA generativa**, **training data** y **open source**. Hace falta actualización y jurisprudencia reciente (como NYT v. OpenAI) muestra el vacío.

### 25. Propuesta de mejora legislativa

Introducir **excepción explícita de interoperabilidad** para APIs declarativas; reglas claras de **licencias open source** en contratos públicos; y marco de **uso de datos para entrenamiento de IA** con opt-out, transparencia y compensación proporcional para obras protegidas.
