## 12. Despliegue gratuito: responsabilidades y alternativas

Desplegar significa preparar una versión y publicarla en servicios accesibles por Internet. El frontend React muestra pantallas en el navegador; FastAPI valida la identidad, aplica permisos y reglas; PostgreSQL conserva datos compartidos. El dominio es una dirección, no el alojamiento ni la base. Por ejemplo, al guardar un pronóstico, la web llama a FastAPI, que comprueba sesión, pertenencia y horario antes de persistir el dato.

Vite genera archivos para distribuir. FastAPI puede servir ese build: separar responsabilidades no obliga a usar proveedores distintos ni a mantener Node ejecutándose para entregar React. [Vite](https://vite.dev/guide/static-deploy) y [frontend con FastAPI](https://fastapi.tiangolo.com/tutorial/frontend/).

| Ruta evaluada | Composición | Ventaja y compromiso |
|---|---|---|
| Tres servicios | React en Pages; API en Render; PostgreSQL en Neon o Supabase. | La interfaz abre aunque la API despierte; más paneles, orígenes y publicaciones que coordinar. |
| Dos servicios | FastAPI sirve React en Render; PostgreSQL externo. | Una dirección y publicación de aplicación; la web también puede esperar si Render duerme. |
| Un servicio con SQLite | FastAPI sirve React y guarda un archivo en volumen persistente. | Reduce componentes, pero debe verificarse alojamiento, persistencia, copias y concurrencia. No fue adoptado. |

La sugerencia inicial Pages + Render + Neon era orientativa. Tras elegir Supabase Auth también conviene evaluar Supabase para PostgreSQL y reunir identidad/datos, pero **no se eligió aún el proveedor de la base ni del alojamiento**. No necesitamos Neon y Supabase PostgreSQL simultáneamente.

### Proveedores gratuitos comparados

| Candidato | Función | Condiciones verificadas el 18/11/2026 |
|---|---|---|
| Cloudflare Pages | Build, publicación de archivos web, HTTPS y dominio propio. | 500 compilaciones mensuales, una simultánea. No ejecuta nuestro proceso Python convencional. |
| Render Free | Ejecutar FastAPI; variables, registros y despliegues. | Duerme tras 15 minutos sin tráfico; despertar alrededor de un minuto. 750 horas por workspace/mes; disco efímero. PostgreSQL Free expira a los 30 días. |
| Neon Free | PostgreSQL gestionado para la API. | 1 GB y 100 CU-horas por proyecto/mes. Suspende cómputo tras cinco minutos de inactividad; recuperación gratuita limitada. |
| Supabase PostgreSQL Free | PostgreSQL y panel de servicios opcionales. | 500 MB y 5 GB de transferencia saliente; posible pausa por baja actividad de una semana. Copias propias para la operación acordada. |

Fuentes: [Pages](https://developers.cloudflare.com/pages/platform/limits/), [Render](https://render.com/docs/free), [Neon](https://neon.com/pricing), [Supabase](https://supabase.com/pricing) y [backups](https://supabase.com/docs/guides/platform/backups). Las cuotas cambian y no equivalen a jugadores concurrentes: se revisarán y medirán antes del piloto.

Render documenta que sin método de pago ciertos excesos suspenden servicios o bloquean compilaciones; con método de pago pueden existir cargos suplementarios según recurso/configuración. Costo cero requiere revisar condiciones y consumo. Neon suspende cómputo conservando datos; Supabase puede requerir restaurar un proyecto pausado. Ninguno sustituye pruebas y respaldos independientes.

### SQLite y persistencia

SQLite puede servir para una web pequeña: varios lectores, escrituras serializadas y transacciones breves. PRODE tendría que probar guardados concurrentes cerca del inicio del partido. Necesita disco persistente y copias consistentes. Migrar después a PostgreSQL requiere revisar esquema, SQL, concurrencia y datos; no se promete cambiar sólo una URL. [SQLite](https://www.sqlite.org/whentouse.html).

Render Free pierde archivos locales en reinicios/despliegues; su volumen persistente requiere un servicio pago. Railway anuncia volumen Free de 0,5 GB y créditos, pero advierte eliminación de volúmenes creados en Trial 30 días después de expirar créditos. Sólo candidato a ensayo condicionado, no permanencia gratuita garantizada. PythonAnywhere ofrece almacenamiento gratuito y ASGI beta, con límites de dominio, red y operación que deben probarse. [Render discos](https://render.com/docs/disks), [Railway volumen](https://docs.railway.com/volumes/reference), [retención](https://docs.railway.com/pricing/free-trial#data-retention), [PythonAnywhere ASGI](https://help.pythonanywhere.com/pages/ASGICommandLine/).

PostgreSQL sigue aprobado. SQLite no fue elegido y tampoco se descarta universalmente. Un VPS puede reunir todo, pero agrega administración de sistema, certificados, actualizaciones, acceso y recuperación; no se seleccionó como atajo inicial.

## 13. Autenticación aprobada: sólo Google mediante Supabase Auth

El usuario eligió para el MVP únicamente acceso con cuenta Google gestionado por Supabase Auth. No se ofrece registro por correo/contraseña propio de PRODE ni recuperación de una contraseña PRODE. La aprobación corresponde a la actualización solicitada el 18 de noviembre de 2026; la integración todavía no está implementada.

| Alternativa comparada | Qué implica | Situación |
|---|---|---|
| Login propio con contraseñas | Gestionar registro, hashes, confirmación, recuperación, sesiones y controles contra abuso. | No elegido para el MVP. |
| Google directo | Google confirma identidad; PRODE debe gestionar sus cuentas/sesiones y permisos. | Alternativa discutida, no integración elegida. |
| Supabase Auth con Google | Integra la identidad Google y gestiona acceso/sesiones; FastAPI valida y autoriza las operaciones. | Método aprobado del MVP. |

Google no es por sí solo todo el sistema de usuarios de PRODE. El usuario verá Continuar con Google en la interfaz de PRODE; Google acredita la identidad y Supabase Auth gestiona su sesión. FastAPI valida la credencial y conserva las comprobaciones de pertenencia, rol, administración y cierre de cada pronóstico. [Supabase Google](https://supabase.com/docs/guides/auth/social-sign-in/auth-google) y [Google: verificación en servidor](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token).

### Recorrido previsto

1. La persona elige Continuar con Google y su cuenta.
2. Google confirma su identidad mediante la integración configurada en Supabase Auth.
3. PRODE reconoce o crea su perfil asociado a una identidad verificada estable.
4. FastAPI valida la sesión y autoriza cada acción sobre el torneo correspondiente.
5. La interfaz contempla cierre de sesión, sesión vencida y acceso denegado; renovación, revocación y almacenamiento concreto se definirán en arquitectura.

PRODE conserva perfil, torneos y pronósticos; no recibe ni almacena la contraseña de Google. No basta un correo, nombre o rol enviado por el navegador. La relación con el perfil local no debe depender sólo de un correo editable: se utilizará un identificador estable verificado, con diseño técnico pendiente. Un usuario autenticado no puede acceder por ello a cualquier torneo.

Supabase publica proveedores sociales y 50.000 usuarios activos mensuales de autenticación dentro del nivel gratuito; no significa capacidad de jugadores simultáneos. Elegir Supabase Auth no adopta automáticamente Supabase PostgreSQL, Render o Pages. [Planes](https://supabase.com/pricing).

Los participantes del piloto necesitarán cuenta Google. El soporte ante pérdida de acceso y la relación con su perfil deben definirse; otros métodos podrán evaluarse posteriormente, sin agregarlos como requisito oculto del MVP. Para futuros clientes empresariales no se presume que todos usarán Google.

Si en una evolución se habilitan contraseñas, se usan hashes con sal, no cifrado reversible para leerlas. Si se habilitan flujos por correo, se configura envío para usuarios reales: el SMTP por defecto de Supabase es limitado a pruebas/destinatarios autorizados. El MVP actual no requiere recuperar una contraseña PRODE inexistente. [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) y [Supabase SMTP](https://supabase.com/docs/guides/auth/auth-smtp).

Para iOS se revisará la regla vigente 4.8: en los casos alcanzados de login social exige una alternativa equivalente con garantías de privacidad, con excepciones. No se presenta como obligación absoluta de un proveedor específico en cualquier aplicación. [Apple Login Services](https://developer.apple.com/app-store/review/guidelines/#login-services).

## 14. Operación del despliegue, recordatorios y producción móvil

### Configuración y puesta en marcha propuestas

El dominio puede seguir registrado en Namecheap. Empezaríamos con URLs temporales; para Pages, un subdominio admite CNAME con DNS externo, mientras el dominio raíz requiere zona/nameservers Cloudflare. Antes de cambiar DNS se revisan correo y servicios existentes. [Dominios Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/).

La URL pública de la API puede aparecer en React; contraseñas PostgreSQL y claves administrativas sólo viven en secretos del servidor o publicación. Las variables VITE_* se incorporan al JavaScript del navegador y no sirven para secretos. Si web/API tienen distintos orígenes, CORS permite los previstos, pero no reemplaza autenticación ni permisos. Se comprobarán HTTPS, conexión cifrada, región y límites de conexiones. [Vite variables](https://vite.dev/guide/env-and-mode/), [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/), [conexión a Supabase](https://supabase.com/docs/guides/database/connecting-to-postgres).

| Paso de ensayo | Comprobación propuesta, todavía no ejecutada |
|---|---|
| Reproducir localmente frontend, API y base con datos de ensayo. | Instrucciones de herramientas, versiones y configuración sin secretos en el repositorio. |
| Crear base remota, configurar secretos y aplicar migraciones. | Guardar/leer un dato mediante FastAPI. |
| Publicar API y web, revisar salud y registros. | Utilizar el flujo desde otro dispositivo por HTTPS. |
| Actualizar o reiniciar el servicio. | Los datos persistidos sobreviven. |
| Asociar el dominio y controlar publicaciones. | URL y certificado correctos; una prueba fallida impide la publicación en el flujo definido. |
| Exportar y restaurar en un destino separado. | Recuperación comprobada antes del piloto. |

Conectar Git puede habilitar autodespliegue, pero no configura por sí solo pruebas que bloqueen versiones defectuosas. El mantenimiento cubre operación del juego, dependencias, migraciones, errores, cuotas, dominio y copias. Revertir código no revierte automáticamente el esquema ni recupera datos; restaurar una copia puede perder cambios posteriores. [FastAPI despliegue](https://fastapi.tiangolo.com/deployment/concepts/) y [PostgreSQL respaldo](https://www.postgresql.org/docs/current/backup-dump.html).

### Recordatorios y disponibilidad gratuita

No basta un temporizador dentro de una API que se suspende. Se evaluará programación independiente o gestionada, con trabajo persistido, reintentos, historial y deduplicación. Cloudflare Cron es un candidato por validar, no una solución aprobada. [Cron](https://developers.cloudflare.com/workers/configuration/cron-triggers/).

Consultas constantes pueden impedir que la base suspenda cómputo. Como ejemplo matemático, 0,25 CU activos durante 720 horas consumen 180 CU-horas, por encima de las 100 gratuitas publicadas por Neon; no es una medición de PRODE. Conviene estudiar ventanas/eventos y medir. La entrega también depende de arranque, cuotas, permisos, red y dispositivo; no se promete puntualidad exacta ni se plantea tráfico artificial para mantener despierto el hosting.

Para Web Push en iPhone, Apple documenta la experiencia en apps añadidas a la pantalla de inicio, con permisos, desde iOS 16.4. Debe probarse en dispositivos reales. [Apple Web Push](https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers).

La API de fútbol es otra dependencia: alojamiento gratis no asegura resultados de la temporada vigente. El fallback aprobado sigue siendo carga administrativa de resultados reales, no simulados en un torneo real.

### Evolución a producción móvil y comercial

La app Android/iPhone será otro cliente de FastAPI; API y PostgreSQL seguirán alojados en Internet. Publicar en tiendas distribuye la aplicación, no aloja nuestros servidores ni la base. Web y móvil pueden usar la misma API; sus cambios deben ser compatibles con versiones móviles que los usuarios aún no actualizaron.

Expo/React Native sigue como candidato, no tecnología móvil aprobada. Si se elige, habrá desarrollo, pruebas en dispositivos, compilación, firma, distribución beta, revisión y publicación. Las actualizaciones remotas sólo cubren cambios compatibles; código nativo, permisos o SDK pueden requerir un nuevo binario. [Expo build](https://docs.expo.dev/build/introduction/), [envío](https://docs.expo.dev/submit/introduction/) y [runtime](https://docs.expo.dev/eas-update/runtime-versions/).

Los precios base consultados son Google Play USD 25 de registro único y Apple Developer USD 99/año, sujetos a región/impuestos y verificación al publicar. No son gastos del piloto web ni presupuesto aprobado. Nuevas cuentas personales Google alcanzadas por su política requieren al menos 12 testers continuos durante 14 días antes de solicitar producción, sin aprobación automática. TestFlight permite probar cada build hasta 90 días. [Google cuenta](https://support.google.com/googleplay/android-developer/answer/6112435?hl=es), [pruebas](https://support.google.com/googleplay/android-developer/answer/14151465?hl=es), [Apple inscripción](https://developer.apple.com/help/account/membership/program-enrollment/) y [TestFlight](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/).

Para vender a empresas o suscriptores se acordarán capacidad, disponibilidad, respuesta ante fallos, separación de ambientes y datos, tareas, copias, alertas y presupuesto. Una recomendación inicial es API/base gestionadas con recursos acordes al uso, evitando pausas críticas; un plan pago tampoco significa ausencia de fallos. El stack puede mantenerse. VPS añade administración de sistema, HTTPS, actualizaciones y recuperación; no está elegido. Suscripciones, roles empresariales, precios, moneda, cobros, SSO y marca blanca no se presuponen implementados ni aprobados.

## 15. Ruta práctica de aprendizaje

El responsable conoce bases de JavaScript/TypeScript, Python/FastAPI, HTML/CSS y SQL, busca experiencia completa y todavía no desplegó un producto comercial. Proponemos aprender con ensayos pequeños y datos ficticios, sin necesitar un curso entero de infraestructura antes de empezar.

| Orden | Recurso | Qué aprender y practicar |
|---|---|---|
| 1 | MDN Internet y dominios, en español. | Cliente/servidor, DNS y HTTPS; dibujar el recorrido desde URL hasta datos. |
| 2 | Vite despliegue, en inglés. | Compilar una pantalla, publicarla y actualizar un texto. |
| 3 | FastAPI despliegue, en español con partes en inglés. | Publicar API mínima; leer registros y entender inicio, puerto y reinicio. |
| 4 | PostgreSQL respaldo/restauración. | Guardar, exportar y recuperar datos de ensayo en una base distinta. |
| 5 | Full Stack Open, parte 11 CI/CD. | Automatizar comprobaciones y controlar una publicación. |
| 6 | Docker y Full Stack Open, parte 12. | Imágenes, contenedores, entornos reproducibles y datos persistentes. |
| 7 | Expo build/distribución, al decidir móvil. | Instalar una beta que use la API de pruebas. |

Enlaces: [MDN Internet](https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/How_does_the_Internet_work), [MDN dominios](https://developer.mozilla.org/es/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_domain_name), [Vite](https://vite.dev/guide/static-deploy), [FastAPI](https://fastapi.tiangolo.com/es/deployment/), [PostgreSQL](https://www.postgresql.org/docs/current/backup-dump.html), [Full Stack Open 11](https://fullstackopen.com/es/part11/introduccion_a_ci_cd/), [Docker](https://docs.docker.com/get-started/), [Full Stack Open 12](https://fullstackopen.com/es/part12/) y [Expo](https://docs.expo.dev/build/introduction/).

Full Stack Open es gratuito pero no es de cero absoluto: su parte 11 recomienda completar al menos las partes 0 a 5 y presupone programación/web/Git. Algunos apartados siguen en inglés. Sus ejemplos Node.js no obligan a cambiar FastAPI: se aprovechan los conceptos. Las páginas son de acceso gratuito; ciertos ejercicios o herramientas tienen condiciones de cuenta propias. [Prerrequisitos](https://fullstackopen.com/es/part0/informacion_general/).

**Primer ejercicio propuesto:** conectar una pantalla, una API y una tabla de ensayo; publicar un cambio; reconocer y corregir un error; recuperar una copia. No se ha ejecutado ese ejercicio ni creado cuentas, DNS o infraestructura durante esta actualización documental.

