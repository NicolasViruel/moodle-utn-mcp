# Programación 4 – U2 APIs REST con Spring Boot

**Alumno:** Nicolás Viruel

## Proyecto

El código está en el mismo repositorio que U1, extendido:

```
../unidad-1-spring-boot/proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel/
```

## Qué incluye U2 (corregido según devolución)

- API REST de **productos** (7 endpoints)
- API REST de **usuarios** (GET list, GET by id, GET by mail, POST)
- API REST de **pedidos** (GET list, POST)
- API REST de **categorías** (GET list, POST, PUT)
- Entidades con `Set` en relaciones uno-a-muchos (UML)
- `Pedido.addDetallePedido(int, Producto)` y `calcularTotal()` void
- Validaciones con Bean Validation (productos)
- Manejo global de errores (`@RestControllerAdvice`)
- Documentación Swagger/OpenAPI (springdoc 2.5.0)
- Profiles Spring (`dev` / `prod`)

## Consigna Moodle

[`TP1_Api_Rest_Programacion_IV.pdf`](TP1_Api_Rest_Programacion_IV.pdf)

## Entrega

**Moodle:** `Actividad de cierre unidad 2 - APIs REST con Spring Boot`  
**Archivo:** [`Viruel_Nicolas_TP_APIs_REST.zip`](Viruel_Nicolas_TP_APIs_REST.zip)

## Probar la API

```bash
cd ../unidad-1-spring-boot/proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel
mvn spring-boot:run
```

Abrir: http://localhost:8080/swagger-ui.html

### Endpoints clave para la consigna

| Acción | Método | Endpoint |
|--------|--------|----------|
| Crear usuario | POST | `/api/usuarios` |
| Crear pedido | POST | `/api/pedidos` |
| Crear categoría | POST | `/api/categorias` |
| Actualizar categoría | PUT | `/api/categorias/{id}` |
| Buscar usuario por ID | GET | `/api/usuarios/{id}` |
| Buscar usuario por mail | GET | `/api/usuarios/mail/{mail}` |
