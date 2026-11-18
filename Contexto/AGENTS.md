## 1. Comportamiento del Agente y Resolución de Tareas
- **Chain of Thought (Razonamiento Explícito):** Antes de escribir o modificar código, explica explícitamente paso a paso tu lógica y cómo planeas resolver la tarea.
- **Fail Early (Resolución de Ambigüedades):** Si un requerimiento está incompleto, carece de contexto o tiene múltiples interpretaciones viables, DETENTE. Haz las preguntas necesarias al usuario antes de asumir o inventar una solución.
- **Confirmación Estratégica:** Solicita autorización explícita ANTES de: alterar esquemas de bases de datos, refactorizar la arquitectura global, modificar endpoints existentes o eliminar archivos. Las correcciones de sintaxis o refactorizaciones de funciones menores pueden hacerse de forma autónoma.

## 2. Orquestación y Subagentes (CRÍTICO)
Para cualquier solicitud que requiera múltiples pasos o tareas distintas, NO intentes resolver todo en el hilo principal. Utiliza el siguiente patrón de delegación:
- **Aislamiento de Tareas:** Divide las solicitudes grandes en tareas discretas (ej. investigación, configuración, implementación, testing).
- **Delegación Estricta:** 
  - *Lectura/Exploración:* Usa subagentes de exploración (ej. `@Explore` en OpenCode o hilos de investigación en Antigravity) para rastrear el código base o leer documentación.
  - *Escritura/Ejecución:* Asigna modificaciones de código o instalaciones a subagentes asíncronos paralelos enfocados exclusivamente en un objetivo.
- **Especialización del Subagente (Role-Prompting):** Cuando instancies un subagente, NO le des un prompt genérico. Inyéctale un rol hiper-específico basado en la tarea (ej. "Eres un DBA Senior analizando cuellos de botella en PostgreSQL..." en lugar de "Revisa este SQL").
- **Dependencias:** No inicies subagentes de escritura si dependen de datos de un subagente de exploración que aún no ha terminado.
- **Reporte Predecible:** Los subagentes no deben devolver explicaciones largas. Oblígalos a retornar resúmenes estructurados (ej. archivos afectados, dependencias instaladas, errores encontrados) al hilo principal.

## 3. Uso de Herramientas (Skills)
- **Preferencia de Herramientas:** Antes de intentar escribir un script desde cero para resolver un problema de infraestructura o despliegue, verifica si existe una Skill o herramienta integrada (búsqueda web, ejecución de terminal, JSON Hooks) que pueda hacer el trabajo de forma más eficiente. Ayuda de la skill instalada "find skill"
- **Validación de Entorno:** Siempre que uses una herramienta que modifique el entorno (como ejecutar comandos en bash/terminal), muestra el comando exacto que vas a ejecutar y pide confirmación si no estás 100% seguro de su impacto destructivo.

## 4. Arquitectura y Metodología
- **Spec-Driven Development (SDD):** Escribe siempre las especificaciones primero. Define los contratos de la API, los modelos de datos y los esquemas de validación (Pydantic) antes de implementar la lógica de negocio.
- **Modularidad y SOLID:** Respeta el principio de responsabilidad única. Separa estrictamente la lógica de negocio, las rutas (routers), los modelos y los esquemas en archivos y directorios independientes. MANTÉN el `main.py` lo más limpio posible.
- **Trazabilidad de Base de Datos:** Toda alteración en el diseño relacional debe acompañarse de su script SQL exacto o el comando de migración correspondiente (ej. Alembic) para facilitar el despliegue limpio y estructurado (ej. vía Docker).

## 5. Estándares de Código (Python / FastAPI)
- **Política de Idiomas:** Escribe TODOS los nombres de variables, funciones, clases, tablas, comentarios del código y commits exclusivamente en **INGLÉS** para mantener el estándar de la industria. Las explicaciones por chat con el usuario mantenlas en **ESPAÑOL**.
- **Tipado Estricto (Type Hints):** Utiliza tipado estricto en el 100% de las funciones de Python y exprime las validaciones de Pydantic para garantizar robustez y correcta autogeneración en Swagger.
- **Manejo de Errores Explícito:** PROHIBIDO utilizar bloques `try/except` genéricos. Captura errores específicos y retorna siempre los códigos de estado HTTP adecuados (400, 401, 403, 404, 500) utilizando `HTTPException` con mensajes descriptivos.
- **Seguridad por Defecto (Zero Hardcoding):** NUNCA escribas contraseñas, tokens, claves de API o cadenas de conexión a la base de datos en texto plano. Utiliza siempre variables de entorno (`.env`) para leer configuraciones sensibles.
