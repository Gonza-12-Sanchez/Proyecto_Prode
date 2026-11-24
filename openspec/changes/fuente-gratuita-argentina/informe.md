# C-01 · Validación de la fuente deportiva argentina

**Ensayo:** 24/11/2026. **Dictamen:** no-go para usar en el piloto el flujo argentino gratuito observado de OpenFootAPI. La demo devuelve resultados reales, pero omitió un partido futuro ya programado y su fuente declarada restringe el uso de los datos gratuitos. El plan Starter sigue sin prueba autenticada y sin permiso específico confirmado para PRODE. Ninguna de las alternativas gratuitas revisadas acredita los requisitos del piloto.

## Alcance oficial

- Temporada de referencia 2026. Apertura y Clausura tienen 16 fechas de 15 partidos y 15 eliminatorias por torneo, **510 partidos** según el formato. El conteo no acredita que todos estén publicados ni que la API los entregue. [Reglamento AFA, arts. 8 y 14](https://assets1.afa.com.ar/2026/BOLETINES/Boletin-Resoluciones-6818---Complementario-01---Reglamento-Torneos-LPF-Primera-2026.pdf) · [Fixture oficial](https://www.ligaprofesional.ar/notas/primera/2025/12/11/fixtures-de-la-temporada-2026/).
- Al momento del ensayo, la LPF programaba Boca–Independiente Rivadavia para el **25/11 a las 21:00 ART**, equivalente a **26/11 a las 00:00 UTC**. Era un solo partido pendiente de octavos. No se identificó una ventana publicada y confirmada de partidos concurrentes para medir goles y finales. [Agenda de octavos](https://www.ligaprofesional.ar/notas/primera/2026/11/11/agenda-de-los-octavos-de-final-2/).
- Si el piloto empieza en 2027, volver a validar fixture y formato de esa edición. La LPF anunció cambios en la fase regular. [Formato anunciado](https://www.ligaprofesional.ar/notas/institucional/2026/10/29/alternativa-superadora-anual).

## Consultas reproducibles a OpenFootAPI

GET a https://openfootapi.com con Accept: application/json y la demo pública Bearer descrita por el proveedor. Usar la clave directamente desde su documentación al reproducir. Se registraron conteos y observaciones puntuales para evaluación, sin cuerpos completos ni credenciales. Los resultados corresponden al plan demo y pueden cambiar. [Documentación](https://openfootapi.com/docs) · [OpenAPI](https://openfootapi.com/openapi.json).

| Hora UTC | Ruta o parámetros | Resultado |
|---|---|---|
| 14:51:46 | /v1/health | HTTP 200. El servicio respondió. |
| 14:51:46 | /v1/matches, competition=comp_liga_profesional_arg, season=2026 | Timeout a 12 s. Sin HTTP en ese intento. |
| 14:51:59 | Mismo filtro de competición, date=2026-11-22 | HTTP 200, 2 registros finalizados. |
| 14:52:46–47 | Mismo filtro, date=2026-05-09 y 2026-05-10 | HTTP 200, 2 y 5 registros. Comparación de marcadores debajo. |
| 14:52:48 | Mismo filtro, date=2026-11-20 | HTTP 200, 1 registro finalizado. |
| 14:52:56 y 14:53:23 | Mismo filtro, date=2026-11-25 y 2026-11-26 | HTTP 200, 0 registros en ambas consultas. Falta el partido oficial ya anunciado, incluso con fecha UTC. |
| 14:52:57 | /v1/competitions | HTTP 200. ARG1 declara Football-Data.co.uk como origen y Free-Open-Data como etiqueta. |
| 14:53:24–25 | Mismo filtro, date=2026-11-23 y luego season=2026 con limit=5 | HTTP 200 en ambas. La consulta de temporada devolvió 5 registros y anunció otro cursor. El contrato reserva la paginación con cursor para Developer. Quedó pendiente conciliar toda la temporada con un acceso habilitado para el plan candidato. |

La prueba directa inicial desde el sandbox falló por DNS. Las consultas HTTP de la tabla se hicieron con red autorizada. Los resultados muestreados incluyen ID de partido y equipos, hora UTC, estado y marcador. Los de mayo y noviembre muestran un rótulo genérico de ronda, Liga Profesional. La muestra no permite separar todas las fases por ese campo. IDs de ejemplo para repetir el contraste: `match_fd_arg1_2026_22012026_aldosivi_defensa_y_justicia`, `match_fd_arg1_2026_09052026_boca_juniors_huracan` y `match_fd_arg1_2026_10052026_river_plate_san_lorenzo`.

| Partido | Referencia oficial | Demo |
|---|---|---|
| Aldosivi–Defensa y Justicia, 22/01 | [0–0 en tiempo reglamentario](https://www.ligaprofesional.ar/notas/primera/2026/01/22/programacion-de-la-fecha-1-4/) | 0–0, finished / FT |
| Boca–Huracán, 09/05 | 1–1 a los 90 y 2–3 tras alargue. [LPF](https://www.ligaprofesional.ar/?p=82885) · [TV Pública](https://www.tvpublica.com.ar/post/boca-no-tuvo-respuesta-ante-huracan-y-quedo-eliminado-del-apertura) | 1–1, finished / FT |
| River–San Lorenzo, 10/05 | 1–1 a los 90, 2–2 tras alargue y 4–3 en penales. [Ficha oficial](https://www.ligaprofesional.ar/ficha-partido?competition=384&match=2634430&season=2026) | 1–1, finished / FT |

Los tres coinciden con el marcador reglamentario. El contrato muestra un solo score.home/away. Falta confirmar que represente siempre los 90 minutos más descuento para toda la edición y que finished corresponda al cierre del partido cuando hay alargue o tanda. Las respuestas de noviembre y enero compartían el mismo updatedAt. Ese campo no permite fechar cuándo apareció un gol o final.

## Condiciones de uso y alternativas

- OpenFootAPI anuncia para Starter 5.000 solicitudes al mes y 60 por minuto. La demo tiene 30 por minuto por dirección y es para pruebas. Cachear y retener datos está permitido por OpenFoot en términos generales, sujeto a las condiciones de la fuente. Se exige trasladar la atribución. La etiqueta Free-Open-Data no documenta un permiso para publicar resultados en PRODE. La fuente argentina declarada destina sus archivos gratis a uso personal o investigación y dirige otros usos a un servicio por suscripción. La página de OpenFoot menciona uso comercial en Pro. Para reconsiderar el plan hace falta un permiso específico de almacenamiento, exhibición pública y uso previsto en la aplicación, o una fuente alternativa con licencia apta. [Planes](https://openfootapi.com/pricing) · [Términos, §7](https://openfootapi.com/terms) · [Política de la fuente](https://football-data.co.uk/contact.php).
- API-Football Free queda descartado para la temporada 2026. La ventana gratuita publicada comprende 2022–2024, con 100 solicitudes al día y 10 por minuto. Pro se publica a USD 19/mes. Antes de evaluar su adopción, comprobar fixture actual, marcador reglamentario, demora y derechos. [Temporadas](https://www.api-football.com/news/post/how-to-get-all-data-from-a-league-with-api-football) · [Cuotas](https://www.api-football.com/news/post/how-to-optimize-api-sports-calls-and-quota-usage) · [Planes](https://www.api-football.com/pricing) · [Términos](https://www.api-football.com/terms).
- Sportmonks Free excluye Argentina. El plan pago anuncia el ID 636 y arranca en EUR 29/mes con facturación mensual. Su documentación distingue el acumulado reglamentario, alargue y tanda por períodos. Comprobarlo en partidos argentinos y obtener claridad sobre persistencia y publicación. [Cobertura](https://www.sportmonks.com/football-api/coverage/) · [Planes](https://www.sportmonks.com/football-api/plans-pricing/) · [Marcadores](https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/includes/scores) · [Términos](https://www.sportmonks.com/terms-of-service/).
- football-data.org Free no incluye Argentina entre sus doce competiciones y ofrece resultados demorados. [Cobertura](https://www.football-data.org/coverage) · [Planes](https://www.football-data.org/pricing).

## Demora y presupuesto de solicitudes

La demora de eventos en vivo queda **sin medir**. El tiempo de respuesta HTTP sólo describe el transporte. El partido del 25/11 permite observación individual, siempre que exista cobertura habilitada. La prueba decisiva requiere dos o más partidos simultáneos. Para cada gol y final se anotarán partido, hora UTC del evento según una referencia verificable, última consulta sin cambio, primera con cambio y publicación en pantalla. C-02 medirá el tramo sincronización→pantalla. Los eventos sin referencia temporal quedarán fuera del máximo observado y se contarán aparte.

Escenario de dimensionamiento, no medición: 8 horas de operación en un día de pico, 20 días al mes, 1 consulta agregada por intervalo, 2 consultas auxiliares por día para fixture o conciliación y 20 % de margen para reintentos. Fórmula diaria: techo((480 / intervalo en minutos × páginas por ciclo + 2) × 1,20).

| Caso | Base por minuto | Total por día pico | Total en 20 días |
|---|---:|---:|---:|
| 1 página, cada 5 min | 0,2 | 118 | 2.360 |
| 1 página, cada 2 min | 0,5 | 291 | 5.820 |
| 3 páginas, cada 5 min | 0,6 promedio, hasta 3 juntas por ciclo | 348 | 6.960 |

Con lotes de 5 y una fecha de 15 partidos se necesitan 3 páginas si el endpoint retorna toda la fecha. El margen diario no acredita el límite por minuto si hay ráfagas o varias jornadas sincronizadas. El caso de 5 minutos con una página entra en la cuota mensual, pero el intervalo por sí solo consume hasta casi todo el objetivo de latencia y deja poco margen al origen y a la pantalla. Repetir el cálculo con el endpoint y la ventana reales.

## Decisión y casos para C-07 / C-02

| Criterio | Estado |
|---|---|
| Liga argentina 2026 y resultados finales de muestra | Verificado en demo para los casos de la tabla. |
| Fixture vigente completo y fases | Falla puntual observada para un partido futuro. Conciliación completa y casos de reprogramación pendientes. |
| Marcador 90 y final fiables | Coincidencias en tres casos. Semántica general y transición durante alargue o tanda pendientes. |
| Cuota, demora total y derechos | Cuota modelada. Demora sin medir. Permiso de uso inapropiado o sin acreditar para la fuente gratuita observada. |

Para C-07, conservar como casos de verificación: final 0–0, final con 90 minutos distinto de alargue/tanda, marcador incompleto que debe quedar pendiente y reprogramación que actualiza el partido sin duplicarlo. Los dos últimos son criterios pendientes de corroborar con ejemplos reales del proveedor elegido. Para C-02, medir el tramo desde la primera detección hasta que se ve el cambio en pantalla y contrastarlo con el margen restante. La intervención excepcional de RN-16 cubre incidentes puntuales.

Para desbloquear la elección, probar una fuente licenciada si se autoriza evaluar un plan pago, o acordar un cambio de alcance si costo cero sigue siendo la condición principal. Con un acceso Starter ya habilitado y una aclaración del proveedor sobre origen, licencia y cobertura, se puede repetir el ensayo. La validación de C-01 permanece abierta.


## Ensayo exploratorio de otras ligas (24/11/2026)

Pruebas de lectura para comparar opciones de costo cero. La temporada argentina sigue siendo el alcance de C-01. Estas pruebas no cierran su tarea de latencia ni eligen la liga del piloto.

| Proveedor y consulta | Evidencia observada |
|---|---|
| OpenLigaDB, GET /getmatchdata/bl1/2026 | HTTP 200 sin clave, 306 registros: 90 finalizados y 216 con horario futuro al momento de la consulta. Werder Bremen–Hamburgo (83243) devolvió 4–0 con After90Minutes, incluido el gol del descuento según la crónica oficial. |
| OpenLigaDB, GET /getmatchdata/bl1/2026/11 | HTTP 200 sin clave, 9 partidos. Los horarios y cruces de la jornada coincidieron con el fixture oficial. Cuatro partidos empiezan el sábado 28/11 a las 11:30 ART (14:30 UTC). |
| football-data.org, GET /v4/competitions | HTTP 200 sin token. El catálogo público incluye los códigos PL y BL1. |
| football-data.org, GET /v4/competitions/PL/matches?season=2026 y su equivalente BL1 | HTTP 403 en ambas peticiones sin token. Queda pendiente probar el fixture y los resultados con una clave gratuita habilitada. El 403 no mide cobertura del plan. |

Referencias: [OpenLigaDB](https://api.openligadb.de/index.html), [fixture y horarios oficiales](https://products.bundesliga.com/fixtures), [crónica oficial de Bremen–Hamburgo](https://www.bundesliga.com/de/bundesliga/news/sv-werder-bremen-hamburger-sv-spieltag-10-spielbericht-highlights-40102), [cobertura](https://www.football-data.org/coverage) y [plan gratis de football-data.org](https://www.football-data.org/pricing).

OpenLigaDB solicita consultar cambios por jornada y descargar los partidos al detectar un cambio. Para una comparación justa de latencia, observar esos cuatro partidos de Bundesliga en ambas APIs, con la misma referencia temporal y el plan gratuito de football-data.org autenticado. Registrar último sondeo sin cambio, primero con cambio y hora del evento. Quedan sin medir la demora en vivo y la llegada al navegador. football-data.org describe su plan gratis como demorado.


### Frecuencia acordada y protocolo de comparación

Se evaluarán OpenLigaDB y football-data.org Free con una cadencia inicial de un minuto durante los partidos, ajustable después de medir la demora de origen. Durante la prueba se consulta la Bundesliga en ambos servicios para comparar los mismos encuentros. Sigue pendiente la decisión sobre la liga y el proveedor que se usarán en el piloto.

1. Antes del partido, contrastar los identificadores y horarios de la jornada 11 en OpenLigaDB y football-data.org, si este último tiene un token gratuito habilitado. Usar los IDs de cada fuente por separado y reconciliar por equipos y hora UTC.
2. Durante los partidos, sondear cada minuto. En OpenLigaDB usar GET /getlastchangedate/bl1/2026/11 y descargar GET /getmatchdata/bl1/2026/11 al detectar cambios, respetando sus condiciones de uso. En football-data.org pedir juntos los partidos de Bundesliga del día con su lista de competencia y las fechas UTC correspondientes. El token se carga localmente como FOOTBALL_DATA_TOKEN y se envía como X-Auth-Token. Registrar fecha UTC, estado HTTP y cuota disponible cuando el proveedor la informe.
3. Para cada gol y final, anotar la hora de una referencia verificable, la última consulta sin el cambio y la primera que lo refleja en cada fuente. Si la referencia carece de hora verificable, registrar el evento sin asignarle una demora. Comparar la primera detección con cinco minutos y dejar el tramo hasta pantalla separado para el ensayo operativo.
4. Para una sola liga, una lista por minuto durante dos horas usa 120 consultas base en football-data.org. Consultas de fixture y revisiones puntuales se hacen aparte. Centralizar el sondeo para calendario y prodes. Ante HTTP 429, esperar la renovación de la cuota antes de reintentar. Fuera de la ventana de partidos, refrescar el fixture con menor frecuencia.

Ventana prevista: cuatro partidos de Bundesliga el 28/11/2026 a las 11:30 ART, sujeta a la programación oficial. Al preparar el ensayo no se detectó un token de football-data.org configurado en el entorno. La prueba pública de OpenLigaDB está disponible. El usuario ejecutó la prueba autenticada de Premier League desde PowerShell. La captura de salida confirma que GET /v4/competitions/PL/matches devolvió 380 partidos. La evidencia acredita acceso al listado, sin verificar cada partido ni su demora. Una segunda captura del usuario confirma que el listado autenticado de Bundesliga (GET /v4/competitions/BL1/matches) devolvió 306 partidos, el mismo total observado en OpenLigaDB. Se verificó acceso a ambos listados, pero el conteo no comprueba igualdad de registros ni latencia. Queda pendiente la medición en vivo con ambas fuentes.

Referencias: [uso de OpenLigaDB](https://www.openligadb.de/en/terms-of-use), [partidos por competición](https://docs.football-data.org/general/v4/competition.html), [cabeceras de autenticación y cuota](https://docs.football-data.org/general/v4/lookup_tables.html).
