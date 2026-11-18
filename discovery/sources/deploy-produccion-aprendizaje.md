# PRODE - Despliegue móvil, producción y ruta de aprendizaje

**Investigación:** 18 de noviembre de 2026.  
**Estado:** material educativo y recomendaciones para evaluar; no selecciona proveedores ni modifica el Discovery aprobado.  
**Alcance:** fuentes primarias públicas. No se crearon cuentas, no se desplegó infraestructura y no se comprobó un producto implementado.

## 1. La aplicación móvil no reemplaza al servidor

La web actual tiene tres responsabilidades separadas: React muestra la interfaz en el navegador; FastAPI aplica las reglas y atiende peticiones; PostgreSQL conserva los datos compartidos. En una futura app móvil cambia el cliente, pero la API y la base continúan alojadas en Internet.

```text
Ahora:   navegador con React  --HTTPS--> FastAPI --> PostgreSQL
Después: navegador con React  --HTTPS--> misma API --> misma base
         app Android/iPhone   --HTTPS--^
```

El teléfono no debe llevar la contraseña de PostgreSQL ni claves administrativas. La API verifica quién es el usuario y qué puede hacer, y aplica el cierre de pronósticos y la puntuación. Publicar una app en las tiendas distribuye su programa: no aloja por nosotros FastAPI ni la base de datos. Esta separación es una recomendación arquitectónica para PRODE.

Una actualización del servidor puede publicarse sin que todos instalen una app nueva. Por eso debemos mantener contratos de API compatibles con las versiones móviles que todavía estén instaladas: no eliminar de golpe campos o endpoints que usan. Definir versiones soportadas, cambios graduales y retirada de clientes viejos es trabajo de arquitectura pendiente.

**Fundamentos:** [MDN: cómo funciona la web](https://developer.mozilla.org/es/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works), [MDN: HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Guides/Overview), [FastAPI: conceptos de despliegue](https://fastapi.tiangolo.com/deployment/concepts/).

## 2. Qué significa publicar una app móvil

Expo/React Native es un candidato para la etapa móvil, todavía no una tecnología aprobada del proyecto. Si se eligiera, el recorrido sería:

1. Implementar una interfaz móvil que use la API existente y probarla en dispositivos.
2. Definir identidad de la app, permisos y configuración por ambiente, sin incluir secretos de servidor.
3. Generar el binario Android o iOS. La firma digital identifica al desarrollador y permite actualizar la app; las credenciales requieren gestión y recuperación.
4. Distribuir versiones de prueba mediante los canales de Google Play y TestFlight.
5. Completar fichas, declaraciones y revisión que requiera cada tienda. Subir un archivo no equivale a aprobación ni publicación automática.
6. Liberar versiones de manera controlada y observar errores, funcionamiento y compatibilidad con la API.

Expo ofrece servicios opcionales para compilar y enviar binarios a las tiendas. No obliga a usar ese proveedor para el backend y no elimina los requisitos de Apple o Google. Los cambios de JavaScript compatibles pueden tener un canal de actualización remota; cambios de código nativo, permisos o SDK necesitan un nuevo binario. No se debe presentar la actualización remota como un modo de evitar las políticas de las tiendas.

**Fuentes:** [Expo Build](https://docs.expo.dev/build/introduction/), [Expo Submit](https://docs.expo.dev/submit/introduction/), [Expo Update: alcance y límites](https://docs.expo.dev/eas-update/introduction/), [Expo: compilaciones frente a actualizaciones](https://docs.expo.dev/tutorial/cicd/introduction/).

### Costos y pruebas de tiendas verificados

| Elemento | Información oficial consultada | Aplicación a PRODE |
|---|---|---|
| Google Play Console | Registro de USD 25 una sola vez; condiciones y métodos de pago dependen de la ubicación. | Es un gasto de distribución futuro, no del piloto web. |
| Apple Developer Program | USD 99 por año; el precio puede variar por región y moneda. | Es un gasto recurrente al distribuir la app iOS con ese programa. |
| Nuevas cuentas personales de Google Play | Para cuentas creadas después del 13/11/2023, se exige prueba cerrada con al menos 12 participantes continuos durante 14 días antes de solicitar acceso a producción. La solicitud es revisada. | Preparar usuarios de prueba y tiempo de validación; no asumir lanzamiento inmediato. |
| TestFlight | Permite distribuir betas; cada compilación puede probarse hasta 90 días. | Canal de validación antes de publicar y durante evolución. |

Precios base, sin conversión a pesos ni cálculo fiscal. Verificar de nuevo al publicar. Los requisitos de pruebas no se describen como la obligación de que cada tester abra la app diariamente.

**Fuentes:** [Google: empezar con Play Console](https://support.google.com/googleplay/android-developer/answer/6112435?hl=es), [Google: pruebas de cuentas personales](https://support.google.com/googleplay/android-developer/answer/14151465?hl=es), [Apple: inscripción y precio](https://developer.apple.com/help/account/membership/program-enrollment/), [Apple: TestFlight](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/).

## 3. Qué cambia para producción comercial

Producción significa que hay personas que dependen del sistema, aunque todavía sean pocas. Tener las apps terminadas no resuelve la disponibilidad de la API, la integridad de los datos ni la operación. Para vender a empresas o usuarios con suscripciones debemos acordar expectativas de servicio y capacidad de respuesta.

La recomendación para una primera producción es mantener la arquitectura simple y usar plataforma de aplicaciones más PostgreSQL gestionado. El stack puede seguir siendo React, FastAPI y PostgreSQL; no hace falta cambiarlo por pasar del piloto a un producto pago.

| Forma de alojarlo | Qué delega | Qué sigue a nuestro cargo | Cuándo evaluarla |
|---|---|---|---|
| Plataforma gestionada para API más base gestionada | Parte de ejecución, infraestructura, certificados e interfaz de despliegue, según proveedor y plan. | Reglas, permisos, dependencias, configuración, migraciones, uso, recuperación y pruebas. | Primera producción con poca experiencia de operación. |
| VPS propio | El proveedor entrega una máquina virtual; el alcance adicional depende del servicio. | Sistema operativo, actualizaciones, acceso, procesos/contenedores, proxy, certificados, copias y monitorización. | Cuando exista capacidad operativa y una razón concreta de costo, control o requerimientos. |

Un VPS puede ser económico en factura, pero exige más tiempo y conocimiento. Los servicios gestionados tampoco prometen por sí solos recuperación, seguridad o disponibilidad suficientes: hay que comprobar qué incluye el plan. No se propone un precio total de producción ni una contratación con esta nota.

**Base técnica:** FastAPI enumera HTTPS, arranque, reinicios, procesos, memoria y pasos previos como asuntos de despliegue; los contenedores ayudan a empaquetar, pero no resuelven automáticamente esas responsabilidades. [FastAPI: conceptos](https://fastapi.tiangolo.com/deployment/concepts/), [FastAPI: contenedores](https://fastapi.tiangolo.com/deployment/docker/).

### Preparación operativa propuesta

- Separar desarrollo, pruebas y producción; usar datos de prueba para comprobar cambios antes del piloto o lanzamiento. La forma y costo de un ambiente adicional se evaluarán con los proveedores.
- Automatizar las comprobaciones y el despliegue desde cambios versionados. CI significa comprobar cada cambio; CD prepara o realiza su publicación según el flujo que elijamos. No implica publicar cualquier cambio sin revisión.
- Aplicar migraciones de base de datos de manera controlada. Volver al código anterior no necesariamente revierte cambios o pérdidas de datos.
- Tener copias, retención y procedimiento de recuperación verificables; ensayar una restauración con datos de prueba.
- Registrar errores y operaciones importantes, comprobar salud del servicio y definir a quién avisar. No volcar contraseñas ni tokens en los registros.
- Medir cuotas y consumo, y asignar un responsable de renovar dominio y revisar servicios.
- Operar recordatorios con trabajo persistido y un ejecutor apropiado, con control de duplicados y reintentos. Que FastAPI sirva peticiones no convierte su proceso en un planificador confiable.

Estos son criterios recomendados para desarrollar en la KB/roadmap, no capacidades que ya estén implementadas.

### Recordatorios y notificaciones móviles

La notificación requiere varias piezas: guardar permiso y destino del dispositivo, determinar qué partido sigue pendiente, programar el trabajo, enviarlo y observar el resultado. El servidor no puede depender de que el teléfono o una pestaña permanezcan abiertos. Los sistemas operativos, la conectividad y los permisos intervienen; no se debe prometer entrega exactamente a una hora.

Si se eligiera Expo, su documentación explica la integración con los servicios de notificaciones de Android/iOS y los recibos de entrega. Todavía debemos elegir la solución y probarla en dispositivos reales. [Expo: panorama de notificaciones](https://docs.expo.dev/push-notifications/overview/).

Para suscripciones futuras habrá que definir producto, pagador, plataformas y método de cobro antes de elegir integración. Las reglas de las tiendas para bienes digitales deben comprobarse en ese momento; esta nota no propone un proveedor ni una comisión. La venta a empresas tampoco implica automáticamente necesitar el Apple Developer Enterprise Program: el canal de distribución corporativa se estudiará según el caso.

## 4. Ruta de aprendizaje gratuita y práctica

Conviene aprender publicando ejercicios pequeños antes de poner datos reales de amigos. No hace falta completar todo un curso de infraestructura para empezar.

| Orden | Recurso primario | Qué aprender | Ejercicio recomendado, todavía no ejecutado |
|---|---|---|---|
| 1 | [MDN: cómo funciona la web](https://developer.mozilla.org/es/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works) y [HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Guides/Overview) | Cliente/servidor, DNS, petición/respuesta y HTTPS. Español. | Dibujar la ruta desde el navegador hasta API y base; inspeccionar una petición en herramientas del navegador. |
| 2 | [Vite: publicación estática](https://vite.dev/guide/static-deploy) | Qué genera una compilación y qué se publica; diferencia entre servidor local y hosting. Inglés. | Compilar una web de prueba y publicarla primero con URL temporal del proveedor. |
| 3 | [FastAPI: despliegue](https://fastapi.tiangolo.com/es/deployment/) | Proceso de servidor, HTTPS, reinicios y configuración. Español con algunas secciones parcialmente traducidas. | Publicar una API mínima de prueba y leer sus registros; no implementar autenticación comercial sólo para este ejercicio. |
| 4 | Guías del PostgreSQL gestionado que elijamos | Conexión cifrada, credenciales, conexiones, migraciones y copias. | Guardar y leer un dato de prueba mediante la API; después exportarlo y recuperarlo. |
| 5 | [Full Stack Open: CI/CD, parte 11](https://fullstackopen.com/es/part11/) | Automatizar pruebas y despliegue con GitHub Actions. Material en español y algunos fragmentos en inglés. | Una comprobación automatizada de una app de práctica; luego una publicación controlada. |
| 6 | [Docker: Get started](https://docs.docker.com/get-started/) y [Full Stack Open: contenedores, parte 12](https://fullstackopen.com/es/part12/) | Imágenes, contenedores y ejecución reproducible. Docker en inglés; curso con español. | Ejecutar API y PostgreSQL localmente en contenedores, con datos de prueba persistentes. |
| 7 | [Expo: compilación](https://docs.expo.dev/build/introduction/) y [envío](https://docs.expo.dev/submit/introduction/) | Publicación móvil, una vez decidida la tecnología móvil. Inglés. | Distribuir una beta que consulte la API de pruebas, antes de producción. |

Full Stack Open no es un curso de cero absoluto: trabaja principalmente con React y backend Node.js. La parte 11 recomienda completar al menos las partes 0 a 5 antes de comenzar. Podemos aprovechar sus conceptos de CI/CD sin cambiar FastAPI por Node. Los tutoriales de contenedores pueden tener ejemplos y proveedores que evolucionaron; usarlos para fundamentos y contrastar comandos y planes con la documentación actual.

**Prerrequisitos y alcance del curso:** [Información general de Full Stack Open](https://fullstackopen.com/es/part0/informacion_general/), [introducción a CI/CD y prerrequisitos](https://fullstackopen.com/es/part11/introduccion_a_ci_cd/), [presentación del curso](https://fullstackopen.com/es/).

## 5. Aplicación al proceso de fundación

Propuesta: incorporar un anexo de despliegue y aprendizaje, y convertir su operación mínima en tareas de la futura KB/roadmap. No modifica silenciosamente las reglas aprobadas del juego ni avanza la fase de fundación. Tampoco convierte la posibilidad de usar Expo, un proveedor de alojamiento o un plan pago en una decisión tomada.

El siguiente ejercicio concreto debería ser un despliegue de práctica aislado, pequeño y sin datos reales: web de prueba, API mínima y tabla de prueba. Crear cuentas, cambiar DNS o publicar ese ejercicio se hará cuando el usuario pida ejecutarlo; esta investigación no realizó esas acciones.
