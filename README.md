# moodle-utn-mcp

Servidor MCP local por stdio para los orígenes aprobados de Moodle UTN `https://tup.sied.utn.edu.ar` y `https://utnsannicolas.quinttos.com`.

Ofrece dos modos de acceso:

- **Modo navegador:** login visible en Quinttos y lectura de lo que Moodle renderiza para el usuario autenticado.
- **Modo REST (opcional):** token personal en `.env` para listar materias, notas, contenidos y vencimientos sin abrir el navegador en cada consulta.

## Alcance y seguridad

- Los únicos destinos permitidos son `https://tup.sied.utn.edu.ar` y `https://utnsannicolas.quinttos.com`. El navegador bloquea cualquier otro origen.
- `moodle_browser_login` abre Chromium visible en Quinttos. Las credenciales se ingresan solo en ese sitio; ninguna herramienta MCP acepta usuario ni contraseña.
- La sesión del navegador vive solo en memoria del proceso. No se guardan cookies, tokens, capturas ni credenciales en disco, logs, stdout ni en el repositorio.
- El token REST se envía únicamente en el cuerpo POST a `/webservice/rest/server.php`. Nunca se expone en URLs ni en las respuestas de las herramientas.
- Las lecturas son de solo lectura. La única operación que cambia estado local es `moodle_browser_logout` (cierra el navegador y descarta la sesión en memoria).
- El archivo `.env` está en `.gitignore`. **Nunca subas tu token a Git.**

Reiniciar el MCP siempre exige un nuevo login manual en modo navegador. El modo REST reutiliza el token configurado en `.env`.

## Requisitos

- Node.js 20 o superior
- Playwright Chromium:

```powershell
npx playwright install chromium
```

## Instalación y verificación

```bash
npm install
npx playwright install chromium
npm test
npm run smoke
```

`npm run smoke` ejecuta la sonda pública sin autenticación e imprime un reporte JSON.

## Modo REST (recomendado)

Configurá un `.env` en la raíz del proyecto (copiá desde `.env.example`):

```env
MOODLE_REST_ORIGIN=https://tup.sied.utn.edu.ar
MOODLE_REST_TOKEN=tu_token_aqui
```

También se aceptan los nombres de MCP-TUPAD: `MOODLE_URL` y `MOODLE_TOKEN`.

### Cómo obtener el token

No abras `https://tup.sied.utn.edu.ar/login/token.php` en el navegador: es una API, no una página.

En PowerShell, con **tu DNI** (no el email de Quinttos) y tu contraseña de Moodle:

```powershell
$body = @{
  username = "TU_DNI"
  password = "TU_CONTRASENA_MOODLE"
  service  = "moodle_mobile_app"
}
Invoke-RestMethod -Uri "https://tup.sied.utn.edu.ar/login/token.php" -Method Post -Body $body
```

La respuesta `{ "token": "..." }` va en `.env` como `MOODLE_REST_TOKEN`.

Verificá la conexión:

```bash
npm run probar-token
```

Deberías ver tu listado de materias con sus IDs.

## Ejecutar como servidor MCP

```bash
npm start
```

El servidor usa stdio. Configurá tu cliente MCP con:

```json
{
  "mcpServers": {
    "moodle-utn": {
      "command": "node",
      "args": ["C:\\ruta\\absoluta\\a\\moodle-utn-mcp\\dist\\index.js"],
      "cwd": "C:\\ruta\\absoluta\\a\\moodle-utn-mcp",
      "type": "stdio"
    }
  }
}
```

Después de cambiar `.env`, reiniciá el servidor MCP en Cursor u otro cliente.

## Herramientas

### Públicas

#### `moodle_probe_capabilities`

Sin parámetros. Informa identidad pública de Moodle, reachability de `/login/index.php` y recuerda usar el flujo de login local.

### Modo REST (requiere `.env`)

#### `moodle_rest_status`

Sin parámetros. Indica si el modo REST está configurado (sin exponer el token).

#### `moodle_rest_my_courses`

Sin parámetros. Lista materias del token con `id`, `name` y `shortName`.

#### `moodle_rest_upcoming_deadlines`

Sin parámetros. Eventos del calendario en los próximos 90 días.

#### `moodle_rest_course_content`

Parámetro: `{ "courseId": <número> }` (ID devuelto por `moodle_rest_my_courses`). Secciones y metadatos de recursos. No descarga archivos.

#### `moodle_rest_course_grades`

Parámetro: `{ "courseId": <número> }`. Notas y devoluciones visibles del usuario del token.

#### `moodle_rest_course_forums`

Parámetro: `{ "courseId": <número> }`. Metadatos de foros y avisos cuando el campus los expone.

### Modo navegador

#### `moodle_browser_login`

Sin parámetros. Abre el login de Quinttos en Chromium visible.

#### `moodle_browser_status`

Sin parámetros. Devuelve `not_started`, `awaiting_login`, `sso_ready`, `authenticated` o `closed`.

#### `moodle_read_my_profile`

Sin parámetros. Lee campos visibles del perfil Moodle del usuario autenticado.

#### `moodle_read_my_courses`

Sin parámetros. Lista materias visibles con nombre y URL exacta `/course/view.php`.

#### `moodle_read_course_activities`

Parámetro: `{ "course": "<título exacto o URL exacta>" }`. Actividades visibles con título, tipo, URL, estado de entrega y fecha límite si Moodle la muestra.

#### `moodle_browser_logout`

Sin parámetros. Cierra sesión en Moodle si es posible, cierra el navegador y descarta la sesión local.

## Flujo típico con REST

1. `moodle_rest_my_courses` → obtener el `id` de la materia (ej. Base de Datos 2 = `45`).
2. `moodle_rest_course_grades` con ese `courseId` → ver notas.
3. `moodle_rest_course_content` → ver unidades y recursos.
4. `moodle_rest_upcoming_deadlines` → ver vencimientos.

## Dependencias

- `@modelcontextprotocol/sdk` 1.29.0 — SDK oficial MCP para TypeScript.
- `playwright` 1.58.2 — automatización del navegador Chromium.
- `zod` 3.24.2 — validación de esquemas del SDK.
- `typescript` 5.8.3 y `@types/node` 22.15.3 — compilación.
