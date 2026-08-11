# Programación 4 – U2 APIs REST con Spring Boot

**Alumno:** Nicolás Viruel

## Proyecto

El código está en el mismo repositorio que U1, extendido:

```
../unidad-1-spring-boot/proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel/
```

## Qué incluye U2

- API REST completa de **productos** (7 endpoints)
- Validaciones con Bean Validation
- Manejo global de errores (`@RestControllerAdvice`)
- Documentación Swagger/OpenAPI
- Profiles Spring (`dev` / `prod`) – mejora de U1

## Consigna Moodle

Descargar desde: `Trabajo práctico de API REST con Spring Boot`  
PDF: `TP1_Api_Rest_Programacion_IV.pdf`

## Entrega

**Moodle:** `Actividad de cierre unidad 2 - APIs REST con Spring Boot`  
**Archivo listo:** [`Viruel_Nicolas_TP_APIs_REST.zip`](Viruel_Nicolas_TP_APIs_REST.zip) (también copiado en el Escritorio)

## Actividades teóricas pendientes (Moodle)

- [ ] Actividad I + cuestionario (REST y primeros endpoints)
- [ ] Actividad II + cuestionario (DTOs, capas, validación)
- [ ] Actividad III + cuestionario (errores, persistencia, Swagger)
- [ ] Autoevaluación U2
- [ ] Encuesta de cierre U2

## Probar la API

```bash
cd ../unidad-1-spring-boot/proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel
mvn spring-boot:run
```

Abrir: http://localhost:8080/swagger-ui.html
