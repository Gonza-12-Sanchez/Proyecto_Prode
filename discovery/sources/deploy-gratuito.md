# Despliegue gratuito de PRODE - investigación técnica

Fecha de consulta: 18 de noviembre de 2026. Fuentes oficiales públicas y Context7. Propuesta para evaluar, no proveedores adoptados ni despliegue realizado. Stack aprobado: React/TypeScript/Vite, FastAPI y PostgreSQL.

## Esquema candidato

El navegador descarga la interfaz desde Cloudflare Pages; esa interfaz llama por HTTPS a FastAPI en Render; sólo FastAPI se conecta a PostgreSQL gestionado en Supabase o Neon. El dominio se conserva en Namecheap y sus registros DNS apuntan al alojamiento correspondiente. La base no se expone al navegador mediante credenciales administrativas.

Para un piloto resulta razonable evaluar esta separación: la interfaz puede cargar aunque la API esté despertando. Otra posibilidad es que FastAPI sirva también el frontend compilado: reduce servicios y problemas de orígenes, pero toda la web depende del arranque y disponibilidad del mismo servicio. La elección sigue abierta.

## Frontend: Cloudflare Pages

Pages integra repositorios Git y puede compilar/desplegar al recibir cambios. Free permite 500 builds mensuales, uno simultáneo, con máximo de 20 minutos por build. Admite hasta 100 dominios personalizados por proyecto. Son límites de despliegue, no un número de usuarios de PRODE. Las Pages Functions consumen cuotas Workers; no equivale a alojar un proceso FastAPI convencional en Pages.

Fuentes: [límites Pages](https://developers.cloudflare.com/pages/platform/limits/) y [Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/).

El dominio raíz, por ejemplo `example.com`, requiere una zona y nameservers Cloudflare. Para un subdominio como `app.example.com`, puede conservarse el DNS en otro proveedor y configurar un CNAME después de asociarlo al proyecto Pages. Esto no transfiere el registro del dominio desde Namecheap. Antes de cambiar DNS se deben conservar los registros de correo y otros servicios existentes. El proceso de activación verifica el dominio y su certificado; no basta con inventar un CNAME sin registrar el dominio en Pages.

Fuente: [dominios personalizados Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/).

Vite genera un directorio `dist` que puede publicarse como archivos estáticos. La dirección pública de la API es configuración del frontend; no es un secreto. `VITE_*` queda incluido en el código enviado al navegador: nunca colocar allí contraseñas PostgreSQL, claves de proveedor de fútbol ni credenciales administrativas.

Fuentes: [despliegue Vite](https://vite.dev/guide/static-deploy) y [variables Vite](https://vite.dev/guide/env-and-mode).

## API: Render Free

Render documenta el despliegue de FastAPI como Web Service Python desde un repositorio, con comando de instalación y arranque que escucha en el puerto asignado por la plataforma. El comando concreto debe ajustarse a la estructura real del proyecto; todavía no hay una configuración nueva aprobada para PRODE.

Fuentes: [FastAPI en Render](https://render.com/docs/deploy-fastapi) y [despliegues Render](https://render.com/docs/deploys).

Free se suspende tras 15 minutos sin tráfico entrante y despierta con una solicitud; la reactivación puede tomar aproximadamente un minuto. Ofrece 750 horas de instancia por workspace y mes. El almacenamiento local es efímero: no guardar allí la base, fotos persistentes o copias únicas. Los límites de transferencia y compilación dependen del workspace. Render indica que Free es para pruebas y no lo recomienda para producción; su PostgreSQL gratuito expira a los 30 días. Por eso proponemos estudiar una base externa para el piloto.

Fuente: [condiciones Render Free](https://render.com/docs/free).

El alojamiento gestionado puede publicar cambios automáticamente desde una rama Git conectada. Esto no significa que las pruebas o migraciones ya estén configuradas: hay que diseñar y ejecutar esas verificaciones antes de activar publicación automática. HTTPS y configuración de dominio se revisan dentro del proceso de puesta en marcha.

## PostgreSQL: dos candidatos

| Candidato | Oferta gratuita consultada | Limitación operativa que importa |
|---|---|---|
| Supabase Free | 500 MB de base y 5 GB de transferencia saliente incluidos; máximo de dos proyectos activos. | Puede pausarse después de una semana de inactividad. No contar con los respaldos diarios administrados de planes pagos. |
| Neon Free | 1 GB de almacenamiento y 100 CU-horas mensuales por proyecto, según la página actual. | Compute se reduce a cero tras cinco minutos de inactividad y consume cuota cuando está activo. El historial gratuito de recuperación es limitado. |

Fuentes: [Supabase pricing](https://supabase.com/pricing) y [Neon pricing](https://neon.com/pricing). Consultar condiciones de la cuenta al crearla: las cuotas pueden cambiar. Los CU-hora de Neon miden capacidad de cómputo, no equivalen directamente a 100 horas de disponibilidad ni a un límite de personas.

Supabase es atractivo si también interesa evaluar autenticación o almacenamiento gestionados; no obliga a reemplazar FastAPI. Para el plan Free, su documentación recomienda exportar regularmente y conservar copias fuera del proveedor. El respaldo de base tampoco incluye automáticamente los archivos de su Storage.

Fuente: [backups Supabase](https://supabase.com/docs/guides/platform/backups).

Neon es una opción para concentrarse en PostgreSQL gestionado. La página vigente indica historial Free de hasta seis horas o 1 GB de cambios y un snapshot. Esa ventana corta no sustituye una política de respaldo independiente, una restauración probada ni una retención acordada para producción.

Fuente: [Neon pricing](https://neon.com/pricing).

### Conectividad y pooling

La URL de conexión y contraseña viven sólo en variables secretas de la API. Se requiere conexión cifrada según instrucciones del proveedor y un número acotado de conexiones. En Supabase, la conexión directa usa IPv6 salvo complemento IPv4; si el alojamiento usa sólo IPv4, el pooler en modo sesión es una alternativa. El modo transacción tiene limitaciones de estado de sesión y prepared statements: verificar driver/ORM antes de elegirlo, especialmente con clientes async. Neon también ofrece URLs con pooling; no asumir que todas las conexiones o comandos de migración son intercambiables.

Fuentes: [conectar Supabase](https://supabase.com/docs/guides/database/connecting-to-postgres) y [pooling Neon](https://neon.com/docs/connect/connection-pooling).

Si frontend y API tienen distintos orígenes, FastAPI debe permitir explícitamente el origen de la web mediante CORS. CORS organiza el acceso desde navegadores; no reemplaza autenticación, permisos ni validación del cierre de pronósticos.

Fuente: [CORS FastAPI](https://fastapi.tiangolo.com/tutorial/cors/).

## Recordatorios: el punto delicado del costo cero

No confiar en un temporizador dentro de un Render Free que puede dormir. Un candidato independiente es un Worker mínimo con Cron Trigger, que llame periódicamente a un endpoint autenticado de la API. Debe ser trabajo real de recordatorios y no un ping para mantener artificialmente despierto el alojamiento. Es una propuesta por validar, no una integración lista.

Workers Free publica 100.000 solicitudes diarias y cinco Cron Triggers por cuenta. El límite de CPU por invocación es de 10 ms; esperar red no cuenta como CPU. Un Cron tiene un máximo de 15 minutos de tiempo de pared. El cron usa horarios UTC. Esto permite evaluar una llamada HTTP liviana que espere el despertar de la API, pero hay que probar tiempos, errores, cuotas y reintentos.

Fuentes: [límites Workers](https://developers.cloudflare.com/workers/platform/limits/) y [Cron Triggers](https://developers.cloudflare.com/workers/configuration/cron-triggers/).

No promete entrega exacta: la API puede tardar en arrancar, el proveedor push o el dispositivo pueden demorar y las cuotas pueden interrumpir tareas. Se necesitan ventanas de aviso, registro de envíos y deduplicación; la llamada repetida no debe duplicar notificaciones. Un scheduler tampoco resuelve por sí mismo permisos push, compatibilidad ni los datos de horarios. Para operación comercial se recomienda evaluar cómputo y tareas disponibles continuamente, con supervisión y recuperación de fallos.

**Interacción entre cuotas:** consultar Neon cada minuto puede impedir que el compute llegue a suspenderse tras sus cinco minutos de inactividad. Una capacidad hipotética de 0,25 CU activa durante 720 horas consumiría 180 CU-horas, por encima de las 100 gratuitas publicadas. Es un ejemplo de cálculo, no una medición ni una configuración elegida. La propuesta debe acotar ejecuciones a ventanas relevantes o planificar avisos por eventos; medir uso real y reprogramar si cambia un partido. No dar por resuelto el costo cero con polling permanente. Fuente de cuota y suspensión: [Neon pricing](https://neon.com/pricing).

## Recomendación provisional

1. Evaluar Pages para frontend, Render Free para la API y comparar Supabase/Neon para PostgreSQL sin comprometer un proveedor todavía.
2. Empezar el ensayo de despliegue con una ruta de salud y datos de prueba; luego comprobar un recorrido completo con datos persistentes.
3. Probar migración, respaldo y restauración antes de depender del piloto. Una reversión del código no revierte automáticamente cambios de base.
4. Resolver recordatorios en una prueba técnica específica; no ocultar sus límites detrás de la etiqueta gratuito.
5. Mantener producción comercial como etapa distinta: capacidad suficiente, respaldos, alertas, separación de ambientes, manejo de secretos y tareas fiables. El stack no exige cambiar por pasar a pago.

No se crearon cuentas, cambiaron DNS, instalaron dependencias ni desplegaron servicios durante esta investigación.
