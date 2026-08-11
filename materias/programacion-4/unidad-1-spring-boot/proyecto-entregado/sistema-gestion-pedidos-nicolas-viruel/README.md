# Sistema de Gestión de Pedidos – Spring Boot

**Alumno:** Nicolás Viruel  
**Materia:** Programación IV – UTN TUP

Proyecto base **U1 (Fundamentos Spring Boot)** extendido con **U2 (APIs REST)**.

## Mejora U1 – Spring Profiles

| Profile | Uso |
|---------|-----|
| `dev` (default) | SQL visible, consola H2, carga datos de prueba |
| `prod` | Sin consola H2, logging reducido, sin seed automático |

```bash
# Desarrollo (default)
mvn spring-boot:run

# Producción
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

## U2 – API REST de Productos (7 endpoints)

| Método | Endpoint | Descripción | HTTP |
|--------|----------|-------------|------|
| GET | `/api/productos` | Listar todos | 200 |
| GET | `/api/productos/disponibles` | Solo disponibles | 200 |
| GET | `/api/productos/{id}` | Obtener por ID | 200 / 404 |
| POST | `/api/productos` | Crear producto | 201 / 400 |
| PUT | `/api/productos/{id}` | Actualización completa | 200 / 404 |
| PATCH | `/api/productos/{id}` | Actualización parcial | 200 / 404 |
| DELETE | `/api/productos/{id}` | Eliminar | 204 / 404 |

### Otros endpoints (U1)

- `GET /api/categorias`
- `GET /api/usuarios`
- `GET /api/pedidos`

### Documentación Swagger

- UI: http://localhost:8080/swagger-ui.html
- OpenAPI JSON: http://localhost:8080/api-docs

### Consola H2 (solo profile `dev`)

- http://localhost:8080/h2-console
- JDBC: `jdbc:h2:mem:pedidosdb` | user: `sa` | password: (vacío)

## Ejemplo POST – crear producto

```json
{
  "nombre": "Notebook",
  "precio": 850000,
  "descripcion": "14 pulgadas",
  "stock": 5,
  "imagen": "notebook.jpg",
  "disponible": true,
  "categoriaId": 1
}
```

## Ejemplo PATCH – actualizar solo precio

```json
{
  "precio": 799999
}
```

## Ejecución

```bash
mvn spring-boot:run
mvn test
```

## Entrega U2 en Moodle

**Actividad:** `Actividad de cierre unidad 2 - APIs REST con Spring Boot`  
**Archivo:** `Viruel_Nicolas_TP_APIs_REST.zip` (sin carpeta `target/`)

```powershell
# Desde la carpeta del proyecto
Compress-Archive -Path * -DestinationPath ..\..\..\..\Viruel_Nicolas_TP_APIs_REST.zip
```

## Estructura relevante U2

```
controller/ProductoController.java    → REST + Swagger
service/ProductoService.java          → lógica de negocio
exception/GlobalExceptionHandler.java → errores 400/404/500
dto/producto/ProductoPatch.java       → DTO para PATCH
config/OpenApiConfig.java             → documentación
```
