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

## Cómo trabajar un cambio

1. Elegí un trabajo del roadmap, comprobá sus dependencias y acordá quién lo lleva. Abrí una rama por tarea desde `main` actualizado y compartí el cambio con un PR hacia `main`.
2. Para ajustes chicos, registrá en el issue o PR qué cambia, el resultado esperado y cómo verificarlo. Un solo Markdown alcanza si hace falta un documento. Enlazá decisiones que ya estén en el Discovery o en una especificación.
3. Usá OpenSpec cuando el cambio agregue comportamiento, toque reglas de negocio o requiera coordinar contratos entre frontend y backend. Consultá `openspec list --json` y `openspec status --change <nombre> --json`. Seguí los artefactos que el esquema solicite y mantené cada uno breve. Una investigación sin cambios de comportamiento puede declarar `skip_specs: true`.
4. Antes de implementar, acordá el alcance y los criterios de aceptación. Aplicá las tareas verificables, marcá sólo las comprobadas y explicá en el PR cómo las probaste y qué quedó pendiente. Coordiná antes de cambiar migraciones o contratos compartidos.

<!-- /active-stack:agent-instruction -->

