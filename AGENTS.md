# PRODE · Instrucciones para agentes

<!-- active-stack:agent-instruction -->

MVP web de prodes con React, TypeScript y Vite, FastAPI y PostgreSQL. El acceso es mediante Google con Supabase Auth.

Consultá el [Discovery](discovery/discovery.md) para el alcance y las reglas de producto, el [roadmap](CHANGES.md) para el orden del trabajo y el [registro de skills](.atl/skill-registry.md) para elegir las guías locales según la tarea.

## Reglas del proyecto

- **Código.** Usá TypeScript en modo estricto y `PascalCase` para los componentes de React. Anotá los tipos en los límites públicos de FastAPI y declará los modelos de entrada y salida.
- **Datos deportivos.** Validá las respuestas del proveedor en el backend y compartí los registros de partidos entre calendario y prodes. Probá que los reintentos y las correcciones recalculen los puntos sin duplicarlos.
- **Acceso.** Mantené el calendario público. FastAPI debe validar la identidad, la pertenencia al prode y los permisos para cada acción privada.
- **Pruebas.** Simulá la API deportiva en las pruebas automatizadas. Usá PostgreSQL de prueba para verificar restricciones, transacciones y migraciones. Comprobá cobertura y demora con el proveedor real por separado.
- **Cierre de pronósticos.** Usá la hora del servidor y el horario vigente del partido. Al guardar una jornada, persistí los pronósticos válidos que sigan abiertos e identificá los que se rechazaron por cierre.
- **Secretos.** Configurá las credenciales fuera del código. Mantené las claves privadas de la API deportiva, PostgreSQL y Supabase en el entorno del servidor, fuera de `VITE_*` y de los logs.

<!-- /active-stack:agent-instruction -->

