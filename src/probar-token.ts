import { MoodleRestClient } from "./moodle-rest.js";
import { loadProjectEnv } from "./load-env.js";

loadProjectEnv();

const client = MoodleRestClient.fromEnvironment();
if (!client) {
  console.error("Falta configuración REST.");
  console.error("Creá un .env desde .env.example con MOODLE_REST_ORIGIN y MOODLE_REST_TOKEN.");
  process.exit(1);
}

try {
  const status = MoodleRestClient.status();
  console.log(`✓ REST configurado contra ${status.origin}`);
  const courses = await client.myCourses();
  console.log(`✓ ${courses.length} materia(s):\n`);
  for (const course of courses) {
    console.log(`  [id ${course.id}] ${course.name}`);
  }
  console.log("\nToken OK. Ya podés usar el MCP con modo REST.");
} catch (error) {
  console.error(`\n✗ Falló: ${error instanceof Error ? error.message : String(error)}\n`);
  console.error("Revisá que el token esté completo y vigente, y que MOODLE_REST_ORIGIN sea exactamente https://tup.sied.utn.edu.ar");
  process.exit(1);
}
