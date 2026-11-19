# Despliegue más simple con FastAPI y SQLite

Consulta: 18 de noviembre de 2026. Investigación de alternativas, no modificación del stack aprobado ni elección de proveedor. PostgreSQL sigue siendo la base aprobada hasta que el usuario decida otra cosa.

## La simplificación es válida

React puede compilarse con Vite y sus archivos servirse desde FastAPI. Se puede tener una sola aplicación pública y un solo dominio, aunque haya dos servicios internos (aplicación y base). La documentación actual de FastAPI describe servir el build estático con `app.frontend()`; hay que comprobar la versión instalada antes de usar una API específica. No es necesario que Node siga ejecutándose para servir el build compilado.

Fuente: [frontend estático en FastAPI](https://fastapi.tiangolo.com/tutorial/frontend/).

SQLite puede funcionar bien para una aplicación web pequeña en un servidor. Su archivo requiere almacenamiento persistente, copias consistentes y pruebas de concurrencia: las escrituras sobre un archivo se serializan. La limitación decisiva de un alojamiento gratuito puede ser el disco efímero, no SQLite. Para PRODE conviene probar la carga simultánea antes del inicio de un partido. Migrar luego a PostgreSQL es posible, pero requiere revisar esquema, SQL, concurrencia y trasladar datos; no se promete cambiar sólo una URL.

Fuentes: [usos adecuados de SQLite](https://sqlite.org/whentouse.html) y [copias y archivos SQLite](https://sqlite.org/howtocorrupt.html).

## Cuatro caminos concretos

| Camino | Servicios | Gratuidad y persistencia | Evaluación para PRODE |
|---|---|---|---|
| FastAPI sirve React en Render Free + PostgreSQL en Neon Free | Dos | Puede mantenerse sin pago dentro de cuotas; base independiente del disco efímero de Render. | Es la opción gratuita más directa de las verificadas, y conserva PostgreSQL ya aprobado. El navegador usa una sola dirección. |
| FastAPI sirve React + SQLite en PythonAnywhere | Un proveedor | Free tiene disco, pero ASGI es experimental y debe comprobarse su disponibilidad concreta en la cuenta. | Candidato de prueba técnica; no garantía de una solución gratuita sencilla y estable con dominio propio. |
| FastAPI sirve React + SQLite en Render pago con disco | Un proveedor, un servicio con volumen | El disco sólo está disponible para servicios pagos. | Una opción operativamente compacta si se admite gasto mensual; no satisface presupuesto cero. |
| FastAPI sirve React + SQLite en volumen Railway Free/Trial | Un proveedor, un servicio con volumen | Se anuncia volumen de 0,5 GB y crédito limitado; existen condiciones de retención que deben confirmarse. | Interesante ensayo temporal, sin asumir continuidad gratuita de los datos ni disponibilidad todo el mes. |

### 1. Render + Neon sin separar el frontend

Render Free no puede conservar una base SQLite escrita en su disco local: pierde cambios al reiniciar, desplegar o suspenderse. No soporta discos persistentes, duerme tras 15 minutos sin tráfico y el despertar puede tardar aproximadamente un minuto. Su PostgreSQL gratuito vence a los 30 días. Fuente: [Render Free](https://render.com/docs/free).

Servir la web y API juntas reduce la configuración de dominios, CORS entre ambas y cantidad de despliegues. Una base PostgreSQL externa mantiene los datos fuera del proceso. Neon Free publica actualmente 1 GB y 100 CU-horas por proyecto/mes y suspensión del cómputo tras cinco minutos sin actividad; no significa recursos ilimitados. Fuente: [Neon pricing](https://neon.com/pricing).

La simplicidad tiene una contrapartida: el frontend también puede esperar al despertar de la API. Los recordatorios siguen necesitando una solución explícita que no dependa de un temporizador dentro de un proceso suspendible. No agregar automáticamente un cuarto servicio para resolverlo sin discutir el alcance y las cuotas.

### 2. PythonAnywhere: lo que sí está verificado

La documentación ofrece Free con 512 MiB de disco, una web app, un worker y vencimiento de un mes. Las cuentas nuevas no incluyen la tarea diaria que conservan ciertas cuentas antiguas. Fuente: [Free Accounts Features](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/).

SQLite está disponible para todos. El proveedor advierte que su sistema de archivos de red puede perjudicar rendimiento y bloqueos concurrentes, por lo que no recomienda esa combinación para producción. Es una advertencia específica de su plataforma, no una prohibición general de SQLite en la web. Fuentes: [bases disponibles](https://help.pythonanywhere.com/pages/KindsOfDatabases/) y [rendimiento](https://help.pythonanywhere.com/pages/MySiteIsSlow/).

FastAPI sí tiene una guía ASGI beta. Esa guía declara que no hay mappings de estáticos, la interfaz es limitada y comandos/API pueden cambiar. El precio a largo plazo de ASGI no está definido; su intención de ofrecer una modalidad gratuita no debe tratarse como contrato permanente. Servir los estáticos desde la aplicación evitaría depender del mapping externo, pero esa composición debe probarse. Fuente: [ASGI beta](https://help.pythonanywhere.com/pages/ASGICommandLine/).

El plan gratuito publica la aplicación en un subdominio del proveedor; los planes pagos incluyen dominio propio. Su acceso saliente está limitado a una lista permitida, lo que puede afectar API de fútbol, correos y push. Por ello no propongo adoptarlo sin un ensayo de compatibilidad. Fuentes: [planes](https://www.pythonanywhere.com/pricing/) y [acceso saliente](https://help.pythonanywhere.com/pages/403ForbiddenError/).

No se recomienda cambiar FastAPI por Flask sólo para encajar en un alojamiento; eso sería otra decisión de stack y requeriría evaluar sus consecuencias con el usuario.

### 3. Render pago con disco: compacto pero no gratuito

Render admite disco persistente en servicios pagos; sólo conserva lo guardado bajo el punto de montaje. El volumen lo usa una única instancia y evita escalar horizontalmente ese servicio. Desplegar con volumen implica un breve corte. Las copias deben ser consistentes con SQLite; snapshots del disco no sustituyen por sí solos una restauración de base comprobada. Fuente: [persistent disks](https://render.com/docs/disks).

El precio final requiere sumar cómputo y almacenamiento según el tablero o tarifas vigentes; la página pública consultada no devolvió una tabla de importes verificable, por lo que esta nota no ofrece una cotización. Fuente: [pricing Render](https://render.com/pricing).

### 4. Railway: ensayo de un servicio con volumen, con cautela de retención

Railway anuncia Free sin tarjeta, prueba inicial de USD 5 por hasta 30 días y luego USD 1 mensual en crédito de uso. No es una cuenta ilimitada: RAM, CPU, almacenamiento y transferencia consumen recursos. La ficha Free permite hasta 0,5 GB de RAM por servicio. Fuente: [Railway pricing](https://railway.com/pricing).

Su referencia de volúmenes publica un volumen Free por proyecto de hasta 0,5 GB, persistente en el punto de montaje, sin réplicas y con breve interrupción al redesplegar. Eso permitiría técnicamente almacenar SQLite junto a FastAPI y React compilado en un único servicio. Fuente: [volúmenes Railway](https://docs.railway.com/volumes/reference).

**No prometer conservación gratuita indefinida:** la documentación de Trial dice que los volúmenes creados por cuentas Trial se eliminan 30 días después del vencimiento de sus créditos y recomienda actualizar la cuenta para conservar los datos. Esa condición debe reconciliarse con la oferta Free en la cuenta concreta antes de usarla como única copia del piloto. No se infiere que un pase automático a Free destruya inmediatamente todos los datos; tampoco se infiere que los conserve para siempre. Fuente: [Trial y retención](https://docs.railway.com/pricing/free-trial#data-retention).

La modalidad Serverless puede dormir el servicio tras 5-10 minutos sin tráfico saliente, con arranque en frío y posible 502 en la primera solicitud. No garantiza que USD 1 alcance todo el mes; tareas o tráfico constantes pueden impedir dormir. Los recordatorios no pueden depender de un temporizador en el proceso suspendido. Fuente: [Serverless Railway](https://docs.railway.com/deployments/serverless).

La propuesta se limita a una prueba temporal con datos de ensayo, respaldos externos y revisión de consumo/retención. No queda elegida como alojamiento ni como cambio de base.

## Beneficio estudiantil: DigitalOcean ya no es la respuesta anterior

No debe recomendarse el antiguo crédito estudiantil de USD 200 como beneficio vigente: un aviso de GitHub Education anuncia fin de oferta el 31 de julio de 2026 y vencimiento de créditos el 1 de agosto. DigitalOcean tampoco aparece en la página actual del Pack consultada. Fuentes: [aviso GitHub](https://github.com/orgs/community/discussions/201240) y [Pack actual](https://education.github.com/pack).

La documentación actual de DigitalOcean publica un crédito general de alta de USD 5, con vencimiento a los 90 días, y exige método de pago válido para crear recursos. No se verificó una oferta pública oficial vigente de USD 200 por 60 días: la URL histórica de free trial devolvió 404. Fuente: [signup credit](https://docs.digitalocean.com/platform/billing/signup-credit/).

Un VPS puede alojar React compilado, FastAPI y SQLite juntos, pero concentra administración de Linux, HTTPS, actualizaciones, firewall, arranque, monitoreo y respaldos en quien lo opera. No lo considero el atajo inicial para una persona que busca reducir mantenimiento, aunque puede ser un ejercicio posterior de aprendizaje.

## Recomendación provisional

Para conservar presupuesto cero y datos persistentes sin separar la interfaz, primero evaluaría **FastAPI sirviendo React + PostgreSQL externo**. Reduce la propuesta inicial de tres servicios a dos y evita cambiar la base ya aprobada. Si el usuario prefiere SQLite, empezaría con un ensayo local o temporal y comprobaría un alojamiento con disco real y retención suficiente antes de comprometerlo como MVP público. Railway y PythonAnywhere son candidatos condicionados, no una garantía de que un solo servicio cubra gratis y de manera indefinida FastAPI estable, dominio propio, disco persistente y tareas fiables.

No se crearon cuentas, instalaron dependencias, desplegaron servicios ni cambiaron decisiones aprobadas durante esta investigación.
