# Skill Registry

Las rutas son relativas a la raíz del repositorio. El orquestador selecciona las guías que correspondan a cada tarea del MVP. Ampliar la selección cuando un trabajo concreto lo requiera.

## User Skills

| Trigger | Skill | Path |
|---|---|---|
| Definir la política visual y los componentes compartidos | `design-system` | `.agents/skills/design-system/SKILL.md` |
| Implementar endpoints y dependencias de FastAPI | `fastapi` | `.agents/skills/fastapi/SKILL.md` |
| Implementar tareas de un change | `openspec-apply-change` | `.agents/skills/openspec-apply-change/SKILL.md` |
| Archivar un change completado | `openspec-archive-change` | `.agents/skills/openspec-archive-change/SKILL.md` |
| Explorar decisiones antes de implementar | `openspec-explore` | `.agents/skills/openspec-explore/SKILL.md` |
| Preparar propuesta, diseño, especificaciones y tareas | `openspec-propose` | `.agents/skills/openspec-propose/SKILL.md` |
| Incorporar requisitos a las especificaciones principales | `openspec-sync-specs` | `.agents/skills/openspec-sync-specs/SKILL.md` |
| Actualizar los documentos de un change existente | `openspec-update-change` | `.agents/skills/openspec-update-change/SKILL.md` |
| Verificar recorridos de usuario en el navegador | `playwright-cli` | `.agents/skills/playwright-cli/SKILL.md` |
| Revisar permisos, entradas y secretos | `security-and-hardening` | `.agents/skills/security-and-hardening/SKILL.md` |
| Implementar Google Auth y validar sesiones y tokens | `supabase` | `.agents/skills/supabase/SKILL.md` |
| Diseñar y revisar tablas, migraciones, permisos y consultas de PostgreSQL | `supabase-postgres-best-practices` | `.agents/skills/supabase-postgres-best-practices/SKILL.md` |
| Implementar comportamiento con pruebas primero | `test-driven-development` | `.agents/skills/test-driven-development/SKILL.md` |
| Configurar desarrollo y compilación del frontend | `vite` | `.agents/skills/vite/SKILL.md` |

## Compact Rules

Copiar al brief los bloques que correspondan a la tarea.

### design-system
- Resolver y persistir una sola política visual
- Preservar estados previos de la fundación
- Construir o auditar tokens y componentes
- Marcar elementos provisorios y obtener aprobación explícita
- Reusar la revisión aprobada y elevar revisión si cambian tokens

### fastapi
- Usar Annotated para dependencias y parámetros
- Declarar esquema público mediante tipo de retorno o response_model
- Centralizar prefijos y tags en APIRouter
- Usar rutas async solamente con operaciones compatibles
- Evitar Ellipsis y RootModel donde la guía los desaconseja

### openspec-apply-change
- Confirmar el change elegido y consultar status
- Leer contextFiles enumerados por el CLI
- Trabajar en tareas concretas y conservar alcance
- Marcar checkboxes sólo al satisfacer su criterio
- Pausar ante divergencias de especificación o decisiones pendientes

### openspec-archive-change
- Elegir el change concreto y consultar su estado
- Revisar artefactos y tareas pendientes
- Evaluar deltas antes de sincronizar
- Consultar si corresponde sincronizar y archivar según la opción confirmada
- Preservar metadata y confirmar destino final

### openspec-explore
- Consultar el estado real del proyecto
- Resolver decisiones que bloquean a las siguientes
- Distinguir hipótesis de decisiones confirmadas
- Fundar sugerencias en evidencia del repositorio
- Permanecer en exploración sin editar implementación

### openspec-propose
- Crear el change con el CLI
- Tomar rutas y requisitos desde las instrucciones del CLI
- Leer artefactos dependientes antes de escribir
- Preparar todos los artefactos transitivos necesarios
- Entregar el plan para revisión antes de aplicar

### openspec-sync-specs
- Identificar el change y sus deltas con el CLI
- Resolver rutas dentro del árbol de specs
- Aplicar altas, cambios, bajas y renombres en la especificación canónica
- Preservar requisitos y escenarios que no cambian
- Validar las especificaciones luego de integrar

### openspec-update-change
- Resolver artefactos existentes mediante el CLI
- Revisar el alcance y dependencias afectados
- Confirmar revisiones antes de escribir
- Actualizar artefactos existentes sin avanzar el frente de generación
- Mantener sincronizados plan, diseño, tareas y especificaciones

### playwright-cli
- Abrir una sesión para el navegador del ensayo
- Capturar un snapshot antes de elegir elementos
- Refrescar referencias si cambia el DOM
- Comprobar consola y red si falla interacción
- Guardar evidencia y cerrar la sesión al finalizar

### security-and-hardening
- Identificar activos, límites de confianza y acceso esperado
- Validar entradas en el límite del sistema
- Parametrizar consultas
- Codificar salidas y exigir HTTPS
- Mantener secretos fuera de código y registros

### supabase
- Consultar changelog y documentación vigente
- Verificar el comportamiento tras cambiar auth o base
- Validar tokens con APIs del servidor adecuadas al contexto
- Guardar las claves privilegiadas fuera del cliente
- Revisar exposición de Data API y RLS como controles separados

### supabase-postgres-best-practices
- Consultar las reglas de la categoría SQL que se está editando
- Priorizar consultas, conexiones, seguridad y esquema
- Validar planes de ejecución en optimizaciones
- Dimensionar pooling y conexiones para el entorno
- Comprobar políticas RLS y permisos de lectura y escritura

### test-driven-development
- Escribir una prueba de comportamiento antes de producción
- Ejecutarla y confirmar que falla por la causa esperada
- Implementar lo mínimo para pasar
- Confirmar resultado verde con ejecución real
- Refactorizar conservando todas las pruebas verdes

### vite
- Preferir configuración ESM con vite.config.ts
- Verificar plugins y compatibilidad con la versión instalada
- Separar configuración del servidor local y compilación
- Usar variables públicas del cliente sólo para datos no secretos
- Validar con build y preview cuando corresponda

## Project Conventions

| File | Path | Notes |
|---|---|---|
| Discovery | `discovery/discovery.md` | Fuente canónica de las decisiones del MVP. |
| Roadmap | `CHANGES.md` | Trabajo, dependencias y verificaciones. |

El proyecto todavía no tiene un archivo de instrucciones de agentes en la raíz.
