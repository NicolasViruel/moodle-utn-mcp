# TRABAJO PRÁCTICO – UNIDAD 3
## Métricas y estimación en proyectos de TI

**Materia:** Gestión de Desarrollos de Software  
**Unidad 3:** Métricas y estimación en proyectos de TI  
**Alumno:** Nicolás Viruel

---

## Caso de estudio: Asignación Automática de Repartidores

Una empresa de logística urbana desarrolla un módulo que recibe órdenes de compra, calcula la ruta más corta y notifica al repartidor más cercano en **menos de 3 segundos**. El equipo estimó **10 días** de trabajo; un modelo de IA con datos históricos sugiere **14–18 días** por la complejidad de las pruebas de integración con APIs de mapas.

---

## Parte 1: Métricas de software y criterios de calidad

### 1. Clasificación de métricas

#### a) Métrica de Proceso – control de demoras en entregas

**Lead Time de historias completadas (días desde “En progreso” hasta “Done” en el tablero).**

Mide cuánto tarda el flujo real de desarrollo en cerrar cada ítem. Si el lead time crece sprint a sprint, hay cuellos de botella (code review, pruebas de integración con mapas, dependencias externas) que explican demoras antes de que impacten al cliente.

#### b) Métrica de Proyecto – desvío de plazos

**Schedule Performance Index (SPI) = EV / PV** (valor ganado / valor planificado).

Compara el avance real del cronograma contra lo planificado. Un SPI < 1 indica retraso acumulado; en este módulo permitiría detectar temprano si los 10 días iniciales eran optimistas frente al hito de “integración con API de mapas + pruebas de carga”.

#### c) Métrica de Producto – velocidad de respuesta

**Percentil 95 del tiempo de respuesta del endpoint de asignación (p95 latency), medido en segundos.**

Garantiza que la funcionalidad cumple el SLA de negocio (< 3 s). Se mide en ambiente de staging/producción con tráfico simulado y monitoreo continuo (APM), no solo en pruebas unitarias.

### 2. Criterios de calidad aplicados al módulo

#### Eficiencia

El sistema debe utilizar recursos (CPU, llamadas a la API de mapas, consultas a base de datos) de forma óptima para cumplir la asignación y notificación en el umbral acordado. Se traduce en optimizar el algoritmo de proximidad, cachear geocodificaciones frecuentes y evitar recomputar rutas completas cuando basta con estimar distancia euclidiana para el ranking inicial.

#### Confiabilidad

El módulo debe operar de forma estable ante fallas parciales (timeout de la API de mapas, repartidor que pierde conexión, picos de pedidos). Implica reintentos controlados, cola de asignaciones pendientes, registro de errores y mecanismos de fallback (reasignación automática o derivación a operador) sin perder pedidos ni duplicar notificaciones.

---

## Parte 2: Criterios de aceptación

**Funcionalidad clave:** *El sistema debe asignar un pedido al repartidor más cercano y notificarlo en menos de 3 segundos.*

### 3. Formato Checklist (2 criterios)

**Criterio 1 – Asignación exitosa con repartidores disponibles**

- [ ] Existe al menos un repartidor disponible y conectado en la zona del pedido.
- [ ] El sistema identifica al repartidor más cercano según la ubicación actual y la ruta estimada.
- [ ] Se registra la asignación del pedido al repartidor seleccionado en la base de datos.
- [ ] El repartidor recibe la notificación (push/app) en **menos de 3 segundos** desde que ingresó la orden.
- [ ] El estado del pedido pasa a “Asignado” y queda visible para monitoreo operativo.

**Criterio 2 – Medición del SLA de 3 segundos**

- [ ] Con carga nominal de prueba (N pedidos concurrentes definidos en el plan de QA), el **100 %** de las asignaciones exitosas completan el flujo asignación + notificación en **≤ 3 segundos** (medido server-side).
- [ ] Si alguna asignación supera 3 segundos, el sistema registra métrica/traza para análisis (timestamp inicio/fin, latencia API mapas).
- [ ] El reporte de prueba documenta p95 y máximo observado en la corrida de aceptación.

### 4. Formato Given / When / Then – sin repartidores disponibles

**Criterio 3 – Pedido sin repartidor en zona**

- **Dado** que ingresó una orden de compra válida con dirección de entrega geolocalizada  
- **Cuando** no hay repartidores disponibles (offline, ocupados o fuera de radio) en el momento de la asignación  
- **Entonces** el sistema **no** asigna el pedido a ningún repartidor, marca el pedido como “Pendiente de asignación”, registra el motivo, notifica al panel operativo/backoffice y **no** envía notificación push a repartidores; el pedido queda elegible para reintento automático cuando haya disponibilidad.

---

## Parte 3: Estimación de tiempos con PERT e IA

### 5. Cálculo PERT

Valores:

| Escenario | Valor |
|-----------|-------|
| Optimista (O) | 8 días |
| Más probable (M) | 12 días |
| Pesimista (P) | 22 días |

**Fórmula:** E = (O + 4M + P) / 6

**Cálculo:** E = (8 + 4×12 + 22) / 6 = (8 + 48 + 22) / 6 = **78 / 6 = 13 días**

**Tiempo esperado (E): 13 días laborables.**

### 6. Análisis comparativo (IA vs. tradicional)

| Fuente | Estimación |
|--------|------------|
| Equipo (inicial) | 10 días |
| PERT | 13 días |
| Modelo IA (históricos) | 14–18 días |

La estimación inicial de **10 días** suele ser **optimista**: contempla el desarrollo “feliz” del algoritmo de proximidad pero **subestima** pruebas de integración con APIs de mapas, manejo de concurrencia, observabilidad del SLA de 3 s y escenarios borde (sin repartidores, timeouts, reintentos). **PERT (13 días)** incorpora variabilidad explícita; la **IA (14–18)** refuerza ese rango con evidencia de proyectos similares que tardaron más por la fase de QA/integración.

Usar **datos históricos** evita el riesgo de comprometer un plazo irreal con el negocio, recortar pruebas para “entregar a tiempo” y desplegar un módulo que incumple el SLA o falla en producción — generando retrabajo, incidentes operativos y pérdida de confianza del cliente interno (logística/operaciones).
