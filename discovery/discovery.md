# PRODE - Discovery aprobado

**Fecha original:** 17 de noviembre de 2026  
**Actualización:** 18 de noviembre de 2026  
**Revisión:** 2  
**Estado:** aprobación original del usuario el 17 de noviembre; ampliación y acceso sólo por Google autorizados el 18 de noviembre.  
**Alcance del documento:** decisiones de producto y orientación técnica previas a la Knowledge Base, el diseño y el roadmap. No acredita implementación ni finalización de la fundación.

## Resumen ejecutivo

PRODE será un producto de pronósticos de fútbol para competir con amigos y conocidos. Su visión comercial contempla venderlo a empresas para que lo utilicen sus empleados, y ofrecerlo al público general mediante planes o suscripciones por definir. El proyecto no tiene objetivos ni requisitos académicos; el beneficio estudiantil usado para registrar el dominio no altera esa definición.

La primera etapa será un MVP web, cómodo en el celular y jugable por un grupo real, con servicios gratuitos dentro de sus cuotas. Tendrá torneos privados multiliga, invitaciones, carga de una fecha completa, pronósticos independientes por torneo, puntajes, ranking y recordatorios. Se priorizará fútbol argentino. Si una fuente gratuita no ofrece los datos necesarios, un administrador de PRODE podrá cargar resultados. Android e iPhone, noticias, minijuegos y comercialización quedan como evolución posterior.

La base tecnológica aprobada es React + TypeScript + Vite, Python + FastAPI y PostgreSQL. Se aprobó Supabase Auth con Google como único acceso del MVP. FastAPI valida la identidad y los permisos de negocio. No están elegidos los proveedores de alojamiento web/API/PostgreSQL, automatización ni datos de fútbol; elegir Supabase Auth no adopta automáticamente su PostgreSQL. El mantenimiento se incorpora al trabajo del MVP mediante una guía operativa y recuperación de datos probada.

### Alcance de la revisión 2

Se integra la conversación sobre despliegue gratuito, SQLite, producción móvil, mantenimiento y aprendizaje. Se confirma acceso exclusivamente por Google mediante Supabase Auth, sin contraseña propia de PRODE. Las opciones de alojamiento siguen como recomendaciones pendientes; no se afirma que haya infraestructura creada ni código implementado.

## 1. Problema que resuelve

El público inicial ya organiza prodes entre amigos o conocidos. Sus principales molestias son cargar pronósticos manualmente en herramientas dispersas, recordar los partidos y mantener planillas. PRODE busca reunir esa experiencia en un producto compartido: elegir torneos y ligas, cargar resultados previstos con pocas acciones, recibir avisos y comprender los puntos y posiciones sin cálculos manuales.

La propuesta no sustituye la elección de resultados por parte del jugador ni presupone predicciones automáticas con inteligencia artificial. Cada participante decide sus marcadores.

## 2. Usuarios y roles

| Actor | Responsabilidad prevista |
|---|---|
| Participante | Unirse por invitación, cargar y editar sus pronósticos antes del cierre, consultar puntos, ranking y resultados revelados. |
| Creador de torneo | Crear un torneo privado, elegir ligas y su alcance, configurar el criterio de resultado para eliminatorias e invitar a personas. Es un rol contextual al torneo; el detalle de permisos se definirá en la KB. |
| Administrador de PRODE | Cargar resultados cuando haga falta y gestionar correcciones con un registro visible. La administración de resultados es centralizada en la plataforma. |
| Empresa cliente, a futuro | Contratar el producto para sus empleados. Roles internos, aislamiento organizacional, compra y administración de planes están pendientes de definición. |
| Público general, a futuro | Acceder a la oferta comercial individual según planes o suscripciones todavía no definidos. |

El piloto será con amigos y conocidos que ya juegan prodes. No se fijaron tamaño de cohorte, plazo ni métricas numéricas de éxito.

## 3. Casos de uso

1. Como creador, quiero seleccionar ligas y jugar una temporada completa o elegir las jornadas/partidos que cuentan, para adaptar el torneo a mi grupo.
2. Como creador, quiero compartir un enlace o código, para que mis amigos se unan al torneo privado sin aprobación individual.
3. Como participante, quiero cargar una fecha completa desde el celular, para evitar planillas y pantallas repetidas por partido.
4. Como participante, quiero pronosticar de manera independiente en cada torneo, para elegir resultados distintos si el mismo partido aparece en varios.
5. Como participante, quiero recibir un aviso antes de cada partido que no pronostiqué, para no olvidarme de jugar.
6. Como participante, quiero consultar posiciones, mi pronóstico, el resultado válido y los puntos obtenidos, para entender la competencia.
7. Como administrador, quiero cargar y corregir resultados con trazabilidad, para operar el piloto sin depender de una API paga y resolver errores.
8. Como responsable del producto, quiero publicar, actualizar y recuperar el sistema con instrucciones claras, para poder mantenerlo aun sin experiencia previa de operación comercial.

## 4. Competidores y soluciones existentes

La investigación se realizó sobre páginas públicas oficiales el 17 de noviembre de 2026. No se crearon cuentas ni se probaron los recorridos autenticados. Las fichas completas quedan en `discovery/sources/`.

| Referencia | Funciones observadas | Modelo publicado en las fuentes | Aprendizaje para PRODE |
|---|---|---|---|
| Prode En Línea | Juego local/empate/visitante, grupos y rankings, cierre al inicio y revelación posterior. | Precio no publicado en la FAQ consultada; grupos sin límite de integrantes publicado. | Simplificar carga y comprensión de una fecha. |
| Prode.io | Marcadores, código/enlace, pronósticos globales o por grupo, 3 por exacto y 1 por ganador excluyentes, simulador. | Plataforma gratuita según FAQ. | Reglas visibles y congeladas al comenzar; PRODE eligió pronósticos independientes por torneo. |
| Kicktipp | Reglas configurables; ejemplo estándar por tendencia, diferencia y exacto. | La portada anuncia juegos gratuitos hasta 300 jugadores. | La configurabilidad es posible, pero debe ser comprensible; no se adoptan sus límites ni su puntuación. |
| Superbru | Grupos privados, web y apps, puntuación por resultado/cercanía/exacto. | Juego básico gratuito y Premium opcional. | Referencia de evolución móvil y monetización, no evidencia de disposición a pagar por PRODE. |

**Limitación:** la apertura directa de Prode En Línea devolvió HTTP 502; su FAQ oficial se consultó mediante el contenido indexado por el buscador. Los detalles de funciones y precios describen las fuentes en esa fecha y pueden cambiar. No se verificaron rendimiento, retención ni calidad operativa de los competidores.

## 5. Funcionalidades necesarias para la primera versión

- Web adaptada al celular y accesible desde un enlace, con cuentas para distinguir participantes. El único acceso del MVP será Google mediante Supabase Auth, sin correo/contraseña propio de PRODE.
- Creación de torneos privados y elección de varias ligas disponibles.
- Alcance configurable entre temporada completa y selección de jornadas o partidos.
- Invitación por enlace/código y acceso a los torneos en los que participa la persona.
- Carga de fecha completa dentro de cada torneo; edición hasta el inicio correspondiente.
- Pronósticos de marcador propios de cada combinación participante, torneo y partido, sin propagación a otros torneos.
- Cálculo de puntuación, ranking y explicación del resultado utilizado y los puntos asignados.
- Recordatorio antes de cada partido sin pronóstico, configurable en horario/anticipación y desactivable; la anticipación exacta y el mecanismo técnico se resolverán después.
- Administración centralizada para resultados, correcciones y seguimiento de partidos especiales.
- Guía de publicación, actualización, revisión de errores, reversión y respaldo/restauración, con recuperación probada antes del piloto.

No se acordaron límites de ligas ni participantes. Se decidirán posteriormente; los límites históricos Free 10/Premium 50 de las fuentes heredadas no son requisitos vigentes. Las cuotas técnicas de proveedores deberán identificarse por separado.

## 6. Funcionalidades opcionales y evolución

- Aplicaciones distribuidas para Android e iPhone.
- Noticias relevantes de fútbol y minijuegos.
- Oferta para empresas y sus empleados.
- Planes y suscripciones para el público general.
- Otros métodos de autenticación gestionada si se necesitan después; no integran el acceso del MVP.

El MVP inicial será gratuito. No se aprobaron precios, cobros, publicidad, planes empresariales ni funciones pagas concretas. Marca blanca, SSO, paneles de RR. HH., premios, pozos, chat y uso de IA no se consideran requisitos confirmados por esta conversación.

## 7. Reglas de negocio aprobadas

| ID | Regla |
|---|---|
| RN-01 | Un usuario crea un torneo y selecciona las ligas disponibles que se jugarán. |
| RN-02 | El alcance admite temporada completa o selección de jornadas/partidos. Su definición multiliga debe concretarse antes de implementar. |
| RN-03 | El torneo es privado; quien tenga el enlace o código puede unirse, sin aprobación individual del creador. |
| RN-04 | Cada pronóstico es independiente por torneo. Cambiarlo en un torneo no afecta a los demás, aunque se trate del mismo partido. No se aprobó copia automática ni pronóstico global. |
| RN-05 | Marcador exacto: 3 puntos. Ganador o empate correcto sin exacto: 1 punto. Las categorías son excluyentes y no se acumulan. Un pronóstico que no acierta ninguna categoría obtiene 0 puntos. |
| RN-06 | La edición de cada pronóstico se cierra al inicio de su partido. La hora del servidor debe ser la autoridad; su implementación se detalla en arquitectura. |
| RN-07 | Los pronósticos ajenos se revelan recién al comenzar el partido. |
| RN-08 | Ligas, partidos y reglas del torneo quedan congelados cuando comienza su primer partido. Los cambios de calendario del proveedor y temporadas aún incompletas requieren una definición compatible con esta regla. |
| RN-09 | Ranking por puntos totales; a igualdad, gana quien tenga más marcadores exactos. Si persiste la igualdad, comparten posición. La numeración visual de puestos empatados queda pendiente. |
| RN-10 | Se puede ingresar a un torneo iniciado. Sólo se pronostican partidos futuros desde el ingreso y no se reciben puntos retroactivos. |
| RN-11 | El creador elige el criterio de resultado para eliminatorias antes de comenzar el torneo. Las opciones exactas y el tratamiento de alargue/tanda de penales deben definirse; no se asume un criterio global de 90 o 120 minutos. |
| RN-12 | Un partido aplazado conserva estado pendiente. Si aún no comenzó, se permite editar hasta el nuevo inicio. |
| RN-13 | Un partido cancelado definitivamente no asigna puntos. |
| RN-14 | Una corrección de resultado debe recalcular los puntos y el ranking afectados. El registro de correcciones será visible; su detalle de exposición se define después. |
| RN-15 | Un partido suspendido luego de comenzar queda bloqueado y pendiente de resolución. |
| RN-16 | La carga manual y corrección de resultados corresponden a administradores autorizados de PRODE, no a cada creador de torneo. |
| RN-17 | Se envía un recordatorio antes de cada partido que el participante aún no pronosticó; no se debe avisar por pendientes inexistentes. La coordinación del mismo partido en varios torneos requiere definición para evitar avisos repetidos. |
| RN-18 | Único acceso del MVP: cuenta Google mediante Supabase Auth. PRODE conserva perfil y relaciones del juego, no almacena la contraseña Google ni ofrece contraseña propia. FastAPI valida identidad y autoriza cada operación. |

**Ejemplos de puntuación:** pronóstico 2-1 y resultado válido 2-1 otorga 3; pronóstico 2-1 y resultado 1-0 otorga 1; pronóstico 1-1 y resultado 0-0 otorga 1; pronóstico 2-1 y resultado 0-1 otorga 0. Son ejemplos de las categorías aprobadas, no pruebas de una implementación existente.

## 8. Integraciones y orientación técnica

### Stack aprobado

| Capa | Tecnología | Motivo acordado y alcance |
|---|---|---|
| Interfaz web | React + TypeScript | Interfaz interactiva y aprendizaje de componentes, estados y datos tipados. |
| Desarrollo y compilación web | Vite | Preparación de una web que puede desplegarse como archivos estáticos. |
| API y negocio | Python + FastAPI | Profundizar conocimientos existentes y mantener reglas de juego en una API propia, reutilizable por clientes móviles futuros. |
| Persistencia | PostgreSQL | Modelo relacional para participantes, torneos, partidos y pronósticos. Proveedor gestionado por elegir. |

La orientación profesional discutida es una API única dividida en módulos, con una base compartida. El árbol de módulos, contratos, acceso a datos, migraciones y pruebas se concretarán en la KB y los cambios de implementación. No se aprobaron microservicios ni una infraestructura distribuida.

### Servicios por seleccionar

- **Dominio:** registrado en Namecheap mediante un beneficio de GitHub para estudiantes, gratuito por un año según informó el usuario. No se verificaron nombre exacto, fecha de renovación, alojamiento incluido ni configuración DNS.
- **Alojamiento web/API/base:** comparar opciones gratuitas y sus cuotas antes de adoptar una. Cloudflare Pages, Render, Neon y Supabase PostgreSQL se discutieron como candidatos, no como servicios contratados ni seleccionados.
- **Datos de fútbol:** verificar competencia, temporada, horarios y resultados de una API gratuita; se admite carga administrativa alternativa. No introducir datos simulados como resultados reales de un torneo.
- **Recordatorios:** resolver programación, envío, permisos, reintentos y compatibilidad en celulares. Una PWA es candidata para la experiencia instalable, todavía no una elección de implementación cerrada.
- **Identidad aprobada:** sólo Google mediante Supabase Auth. Detalles técnicos del ciclo de sesión pendientes de arquitectura; FastAPI conserva autorización. Correo/contraseña y recuperación de contraseña propia están fuera del MVP. Otros correos sólo se agregarán si se justifican.

### Alternativas comparadas

| Camino | Cuándo convendría | Motivo de la elección actual |
|---|---|---|
| React/Vite con backend principalmente gestionado en Supabase | Priorizar menos infraestructura propia. | Se prefirió construir una API FastAPI para aprender frontend, backend y despliegue, manteniendo servicios gestionados como posibilidad. |
| Expo/React Native desde el comienzo | Priorizar distribución móvil y reutilización de interfaz entre plataformas desde el primer día. | El MVP web permite validar con menos tareas móviles iniciales. Una interfaz React DOM no se convierte automáticamente a React Native. |
| Next.js para la web | Si el portal público, las noticias y el renderizado de contenido pasan a ser centrales. | Para el juego privado inicial se consideró suficiente Vite. No se descarta una revisión si cambia el producto. |

La elección técnica se hizo por ajuste al producto y al aprendizaje buscado, no por una supuesta superioridad universal. El usuario conoce de manera básica JavaScript/TypeScript, Python/FastAPI, HTML/CSS, MySQL y PostgreSQL, y quiere profundizar desarrollo completo. No declaró experiencia previa en React ni despliegues comerciales.

## 9. Restricciones y decisiones de alcance

- Presupuesto inicial de servicios: apuntar a costo cero dentro de las cuotas gratuitas. No hay contratación ni presupuesto de producción aprobado.
- Primera etapa jugable con amigos; no sólo una demostración con datos simulados.
- Fútbol argentino prioritario, sin renunciar al objetivo multiliga. Competencias exactas y cobertura inicial pendientes.
- Android/iPhone y comercialización son visión posterior; las cuentas de tiendas no son necesarias para el piloto web.
- Equipo, dedicación y fecha objetivo quedan abiertos por decisión del usuario.
- La documentación de `Contexto/` se usa como antecedente, pero las decisiones aprobadas en esta conversación prevalecen.
- La raíz actual es `C:/Users/GonziChan/Desktop/Proyecto_Prode`, tras el traslado indicado por el usuario. Se autorizó eliminar `Contexto/` sólo al completar toda la fundación, no al terminar Discovery. Este documento conserva las decisiones vigentes para no depender de esa carpeta.

### Costos de referencia, no presupuesto aprobado

Se investigaron planes gratuitos y costos de tiendas, datos e infraestructura para explicar la operación. La recomendación posterior del usuario fue comenzar sin servicios pagos. Los precios no son compromisos de compra y deben verificarse nuevamente al elegir proveedores. Ejemplos consultados: Google Play USD 25 de registro único; Apple Developer USD 99/año; API-Football con cuota gratuita y temporadas limitadas; PostgreSQL y correo con niveles gratuitos. El costo del dominio después del primer año no se determinó.

## 10. Riesgos, mantenimiento y validación

### Riesgos principales

| Riesgo o supuesto | Tratamiento previsto |
|---|---|
| La API gratuita no cubre la temporada argentina actual o sus cuotas no alcanzan. | Comprobar cobertura temprano y admitir operación manual centralizada. No prometer actualización en vivo ni plazos aún no definidos. |
| El servidor gratuito duerme o se agotan cuotas. | Distinguir las condiciones del piloto de una operación comercial; evaluar ejecución programada independiente. No depender de un reloj dentro de un proceso que pueda detenerse. |
| Un recordatorio falla o se duplica. | Probar permisos, programación y casos por usuario/partido/torneo. Compatibilidad y entrega deben validarse en celulares reales. |
| Una corrección altera puntos o genera duplicados. | Pruebas de puntuación y recálculo, trazabilidad y diseño idempotente como criterios técnicos a concretar. |
| Se ven pronósticos ajenos antes de tiempo o se edita fuera de plazo. | Comprobaciones del lado confiable y pruebas de permisos/cierre. |
| Temporadas de varias ligas terminan en fechas diferentes o el fixture cambia. | Definir conjunto de partidos, incorporación de calendario faltante y cierre final compatible con reglas congeladas. |
| La solución no resulta cómoda o los jugadores no vuelven. | Piloto real; observar carga de fecha, uso repetido, comprensión de puntos y comentarios del grupo. No se fijaron umbrales de retención. |
| La persona responsable no sabe operar un producto desplegado. | Guía y práctica de despliegue, diagnóstico, reversión y restauración antes de depender del sistema. |
| La identidad se acepta sin verificar o se confunde login con permisos. | Validación de sesión y autorización por operación en FastAPI; no confiar roles/correos del cliente. |
| Participante sin cuenta Google o que pierde acceso al proveedor. | Confirmar viabilidad del piloto y definir soporte; otros métodos quedan como evolución. |
| La visión B2B y suscripciones agrega complejidad demasiado temprano. | Mantener explícita esa evolución y discutir separación de empresas y planes en arquitectura, sin atribuir funciones empresariales no aprobadas al MVP. |

### Mantenimiento incorporado al MVP

El usuario identificó el mantenimiento como su principal preocupación y aprobó incluirlo en la fundación. Nunca creó una app móvil ni desplegó un producto real para vender.

El plan debe cubrir tres áreas: operación del juego (resultados y excepciones), cuidado técnico (errores, dependencias, pruebas y cambios de datos) y servicios/datos (cuotas, dominio y recuperación). Los servicios gestionados pueden reducir la administración de servidores, pero no eliminan estas tareas.

**Entregables acordados:** instrucciones para publicar, actualizar, comprobar errores, volver a una versión anterior y recuperar datos; recuperación de respaldo probada antes del piloto. Proveedores, retención y frecuencia de copias, alertas, responsables y rutina periódica deben concretarse en arquitectura/roadmap. No se afirma que ya existan copias o automatizaciones.

**Criterios de verificación propuestos para el piloto:** completar un flujo real crear/unirse/pronosticar/puntuar/ranking; comprobar aislamiento entre torneos y cierre temporal; demostrar un recálculo sin duplicación y una recuperación; probar recordatorios en dispositivos representativos. Estos criterios orientan la planificación y no constituyen pruebas ejecutadas ni métricas numéricas aprobadas.

## 11. Preguntas abiertas

| Prioridad | Decisión pendiente |
|---|---|
| Antes de implementar las reglas afectadas | Competencias argentinas iniciales, disponibilidad del fixture y temporada en la fuente seleccionada. |
| Antes de implementar las reglas afectadas | Cómo delimitar una temporada multiliga y cuándo termina el torneo; qué se congela si el calendario todavía no está completo. |
| Antes de implementar las reglas afectadas | Opciones exactas del criterio de eliminatorias, incluyendo alargue y tanda de penales, y su representación de marcador. |
| Antes de implementar las reglas afectadas | Hora y zona horaria autoritativas, cambios de inicio y edición tras reprogramación, ingreso tardío en el instante de cierre. |
| Antes del piloto | Anticipación y agrupación/deduplicación de recordatorios cuando falta el mismo partido en varios torneos; permisos y compatibilidad web móvil. |
| Arquitectura/KB | Proveedores/regiones web/API/PostgreSQL, ORM/migraciones, tareas, despliegue conjunto o separado, recuperación y cuotas. Supabase Auth y acceso sólo Google ya decididos. |
| Arquitectura/KB | Google/callbacks por entorno, validación/ciclo/revocación de sesión, identidad estable y perfil, soporte ante pérdida de acceso. |
| Arquitectura/KB | Ciclo de estados de torneo, acciones del creador tras el inicio y detalles de expulsión/salida; no heredar estados manuales de documentos viejos sin validarlos. |
| Arquitectura/KB | Visibilidad de correcciones, datos de otros jugadores, historial necesario y numeración de puestos compartidos. |
| Antes del piloto | Tamaño real del grupo, disponibilidad de cuenta Google, responsable de operación, dedicación, fecha y criterios medibles de validación. |
| Evolución comercial | Oferta para empresas, roles y separación de organizaciones, titular de suscripción, prestaciones, precios, moneda y proveedor de cobros. |
| Evolución comercial | Límites de ligas/participantes y relación con planes; no están fijados ahora. |
| Evolución | Momento y alcance de apps Android/iPhone, noticias y minijuegos. |

Estas preguntas no invalidan el Discovery aprobado. Se preservan para decidirlas con evidencia en las fases y cambios correspondientes.

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

## Fuentes y precedencia

La fuente primaria de decisiones es la conversación aprobada por el usuario el 17 de noviembre y ampliada por su solicitud el 18 de noviembre de 2026, con acceso sólo Google vía Supabase Auth. Este documento registra ese resultado; la KB y los cambios OpenSpec posteriores deberán desarrollarlo sin sustituir decisiones pendientes por supuestos silenciosos.

**Antecedentes locales:** `Contexto/README_Proyecto.md`, `Contexto/requirements.md`, `Contexto/openspec/changes/prode-mvp/` y código existente. Se revisaron como material histórico. Se descartaron como mandatos vigentes el objetivo académico, cinco ligas europeas obligatorias, límites Free 10/Premium 50, puntuación acumulativa, reuso global de pronósticos y promesas de tiempos de actualización. No se certificó completitud del código heredado.

**Investigación de referencias:**

- Prode En Línea: https://prodeenlinea.com/faq/ - ficha `discovery/sources/prode-en-linea.md`.
- Prode.io: https://prode.io/en/faq - ficha `discovery/sources/prode-io.md`.
- Kicktipp: https://www.kicktipp.com/ y https://www.kicktipp.com/info/service/help/2/213 - ficha `discovery/sources/kicktipp.md`.
- Superbru: https://www.superbru.com/worldcup_predictor/ y https://www.superbru.com/premium - ficha `discovery/sources/superbru.md`.

**Documentación técnica y operación consultada:**

- Vite, despliegue estático: https://vite.dev/guide/static-deploy
- FastAPI, despliegue y módulos: https://fastapi.tiangolo.com/deployment/concepts/ y https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Expo, web y diferencias de plataforma: https://docs.expo.dev/workflow/web/ y https://docs.expo.dev/router/advanced/platform-specific-modules/
- Next.js, exportación estática: https://nextjs.org/docs/app/guides/static-exports
- Supabase, arquitectura, permisos y planes: https://supabase.com/docs/guides/getting-started/architecture, https://supabase.com/docs/guides/database/postgres/row-level-security y https://supabase.com/pricing
- Render, límites gratuitos: https://render.com/docs/free
- API-Football, precios y cobertura: https://www.api-football.com/pricing y https://www.api-football.com/coverage
- Apple, notificaciones web: https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers
- Tiendas: https://developer.apple.com/help/account/membership/program-enrollment/ y https://support.google.com/googleplay/android-developer/answer/6112435?hl=es
- GitHub Student Pack y conexión del dominio: https://education.github.com/pack y https://www.namecheap.com/support/knowledgebase/article.aspx/9837/46/how-to-connect-a-domain-to-a-server-or-hosting/

**Fuentes de la ampliación:** las secciones 12 a 15 enlazan documentación oficial de despliegue, identidad, producción y aprendizaje consultada el 18 de noviembre. Las notas locales `discovery/despliegue-y-aprendizaje.md` y `discovery/sources/despliegue-simple-sqlite.md` conservan la investigación detallada. Los proveedores de alojamiento comparados no se consideran adoptados.

## Continuidad de la fundación

Discovery está aprobado. La Knowledge Base, política visual, roadmap, registro de skills e instrucciones del proyecto siguen pendientes. El paso de estado permanece en `discovery` hasta que el usuario confirme continuar a la fase siguiente. El PDF reflejará la revisión 2 de este Discovery, no una certificación de producto implementado ni fundación completa. La aprobación original y su ampliación quedan trazadas; el paso sigue en discovery hasta el checkpoint de avance.
