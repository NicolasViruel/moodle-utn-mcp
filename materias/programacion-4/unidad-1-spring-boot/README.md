# Programación 4 – U1 Fundamentos Spring Boot

**Alumno:** Nicolás Viruel

## Archivos

| Archivo / carpeta | Descripción |
|-------------------|-------------|
| `consigna.pdf` | TP original de Moodle |
| `Trabajo practico 1.zip` | Entrega original |
| `proyecto-entregado/` | Proyecto extraído del ZIP |

## Entrega en Moodle

**Actividad:** `Actividad de cierre unidad 1 - Fundamentos Spring Boot 🎯🏁`  
**Formato:** `.zip` del proyecto

## Revisión del proyecto entregado

Proyecto: `proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel/`

| Requisito | Estado |
|-----------|--------|
| Spring Web, JPA, Lombok, H2, DevTools | OK |
| Capa DTOs completa | OK |
| 2 usuarios, 3 pedidos (≥2 detalles), 3 categorías, 10 productos | OK |
| DI por constructor en services/controller | OK |
| Estereotipos @Service, @Repository, @Component | OK |
| `application.properties` | OK |
| Profiles (dev/prod) | Opcional – no incluido |

## Ejecución local

```bash
cd proyecto-entregado/sistema-gestion-pedidos-nicolas-viruel
mvn spring-boot:run
```

Endpoints: `/api/usuarios`, `/api/pedidos`, `/api/categorias`, `/api/productos`

## Re-empaquetar para Moodle

Comprimir la carpeta `sistema-gestion-pedidos-nicolas-viruel` (sin `target/` si existe).
