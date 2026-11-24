# PRODE — Dudas, decisiones y pruebas del MVP

**Actualizado:** 24 de noviembre de 2026.
**Estado:** Discovery cerrado y resumen final aprobado el 19 de noviembre de 2026; validaciones técnicas pendientes en el roadmap.  
**Propósito:** retomar el trabajo en distintas sesiones sin perder dudas, propuestas ni decisiones.

Este registro acompaña al [Discovery canónico, revisión 5](discovery.md). Conserva los IDs, decisiones e historial de sesiones y funciona como índice de validaciones técnicas para el roadmap. Las alternativas históricas o propuestas no prevalecen sobre R5 ni amplían automáticamente el MVP. El PDF se genera desde ese Discovery; este registro no acredita implementación ni pruebas de proveedores.

**Decisión vigente del 24/11/2026:** la API es la fuente habitual. RN-16/RN-24 permiten una intervención excepcional y auditada por personal autorizado. Las políticas anteriores quedan como historial.

## 1. Cómo usar este documento

- Al empezar una sesión, elegir entre uno y tres IDs pendientes.
- Para cada punto, conversar opciones, reunir evidencia y registrar la decisión explícita.
- Marcar `Resuelto` cuando haya respuesta acordada y evidencia suficiente; conservar el ID y el motivo.
- Si aparece una idea nueva, anotarla como `Propuesta`, sin incorporarla automáticamente al MVP.
- Si una prueba cambia una decisión, registrar qué cambió y revisar sus efectos sobre otros puntos.
- El resumen de alcance fue confirmado y consolidado en R3. Resolver las pruebas técnicas mediante el roadmap; si cambian una decisión, actualizar primero el Discovery y después su PDF.

**Estados:** `Pendiente`, `En investigación`, `Propuesta`, `Resuelto`, `Diferido`. `Resuelto (definición)` registra una decisión de producto confirmada por el usuario; no acredita implementación ni pruebas.  
**Prioridad:** `Alta` bloquea la decisión o función afectada; `Media` se puede resolver durante su diseño/prueba; `Baja` corresponde a evolución. La prioridad no fija fechas ni obliga a resolver toda la lista antes de experimentar.

## 2. Base de conversación y decisiones previas

| Tema | Situación actual |
|---|---|
| Producto inicial | Web cómoda en celular, jugable con amigos/conocidos; objetivo de servicios gratuitos dentro de sus cuotas. |
| Liga inicial | Temporada argentina vigente al piloto, Apertura/Clausura con eliminatorias y partidos futuros desde la creación; Trofeo de Campeones excluido. Al primer partido se congelan reglas, temporada y criterio de fases, no una lista incompleta: incorporar cruces oficiales y reprogramaciones sin selección arbitraria del creador. Tras la final del Clausura, esperar la resolución de partidos incluidos pendientes, sin incorporar la siguiente edición. |
| Calendario | Público: fixture y marcadores sin login, por días con hoy, mañana y selector de fecha; no navegación principal por jornada deportiva. |
| Carga | Jornada completa con botón «Guardar pronósticos», confirmación y aviso al salir con cambios pendientes. Si un encuentro cerró antes de guardar, guardar los pronósticos válidos de partidos aún abiertos e informar guardados/rechazados; manda la hora del servidor. No se adopta autosave ni persistencia automática en navegador; recuperación ante fallos pendiente. |
| Seguimiento | Elegido por el usuario: marcadores durante los partidos, aceptando hasta cinco minutos de demora para intentar costo cero. Fuente y demora real de extremo a extremo por medir; no es una garantía de servicio. |
| Acceso | Calendario/fixture/marcadores públicos sin login. Crear o unirse a prodes privados y pronosticar requiere Google mediante Supabase Auth; FastAPI valida identidad, membresía y permisos para contenido/operaciones privadas. Administrar la sincronización requiere personal autorizado de PRODE, con permiso de intervención separado según RN-24. Sin contraseña propia. |
| Stack | Aprobado: React + TypeScript + Vite, Python + FastAPI y PostgreSQL. Proveedores de alojamiento y base pendientes. |
| Juego | Pronósticos independientes por torneo; marcador de 90 minutos más descuento, sin alargue/tanda, con 3 puntos por exacto o 1 por ganador/empate sin acumular. Ranking sólo con partidos finalizados y ese marcador confirmado: puntos descendentes, luego exactos descendentes; igualdad en ambos comparte puesto y el siguiente es consecutivo (1.º, 1.º, 2.º). Cierre/revelación al inicio. |
| Invitaciones | Regla previa: torneo privado; ingreso por enlace/código, incluso iniciado, sólo para partidos futuros y sin puntos retroactivos. |
| Resultados | La API es la fuente habitual. Un marcador final válido de los 90 minutos más descuento habilita puntos automáticos, también cuando se confirma según RN-16. Las correcciones recalculan sin duplicar. |
| Recordatorios | Web Push, con anticipación configurable por usuario y opción de desactivar; 30 minutos queda como valor inicial propuesto, no fijo común. Un aviso por participante/partido agrupa sólo sus torneos con pronóstico faltante al enviar; si completó todos, no se avisa. Sin correo en el MVP; entrega/compatibilidad y operación gratuitas por validar. |
| Alcance anterior | La revisión 2 contemplaba multiliga y selección flexible de jornadas/partidos. Falta reconciliar ese alcance con la simplificación reciente, tras confirmar el resumen. |

## 3. Resolver antes de comprometer la función afectada

| ID | Prioridad / estado | Pregunta y motivo | Qué permitiría cerrarlo |
|---|---|---|---|
| MVP-01 | Alta · Resuelto (definición) | Usar la temporada vigente al comenzar el piloto: Apertura y Clausura con eliminatorias, cierre en la final del Clausura y Trofeo de Campeones excluido. No se fija de antemano 2026 ni 2027. | Política de edición confirmada explícitamente el 19/11/2026. Al iniciar el piloto, verificar año concreto, formato y fixture reales y cobertura de la fuente; no son verificaciones ya ejecutadas ni cobertura garantizada. |
| MVP-02 | Alta · En investigación | ¿Qué fuente permite vivo de esa edición dentro de sus condiciones y cuotas? API-Football documenta Free 2022–2024 en 2026, no la temporada 2026 ([restricción oficial](https://www.api-football.com/news/post/how-to-get-all-data-from-a-league-with-api-football)); se corrige la incertidumbre anterior sobre acceso actual gratuito. | Acceso verificado a encuentros de la edición elegida, condiciones revisadas y prueba de consumo/cobertura. Verificar que entregue el marcador de 90 minutos separado de alargue/tanda para puntuar eliminatorias; no se presume ese campo. No se probó con token ni se eligió proveedor. |
| MVP-03 | Alta · Pendiente | Aceptada una demora de hasta cinco minutos para intentar costo cero. ¿Qué fuente y mecanismo cumplen esa tolerancia real y cómo se informa un fallo? | Medir demora desde el evento hasta la pantalla, incluyendo fuente, consulta y entrega. Consultar cada cinco minutos no garantiza cinco minutos de demora total; falta probar y acordar el estado desactualizado. |
| MVP-04 | Alta · Resuelto (definición) | Alcance fijo de la edición: Apertura/Clausura con eliminatorias, partidos futuros desde la creación y participación desde el ingreso sin retroactivos; Trofeo de Campeones excluido. Cierre deportivo en la final del Clausura; si quedan partidos incluidos pendientes, estado «finalizando» hasta su resolución oficial y sin ganador definitivo. No entran encuentros de la siguiente edición; cancelados definitivamente no puntúan. | Usuario confirmó completar el fixture oficial y esperar la resolución de pendientes. Al primer partido se congelan reglas, temporada y criterio de fases, no una lista incompleta: nuevos cruces oficiales/reprogramaciones conservan el alcance, sin agregar/quitar partidos selectivamente por el creador. Fixture y comportamiento aún por validar. |
| MVP-05 | Alta · Resuelto (definición) | El MVP siempre usa el marcador de 90 minutos más descuento, sin alargue ni tanda de penales. Exacto: 3 puntos; ganador/empate sin exacto: 1; sin acumular. | Usuario confirmó “Simplificar el MVP: siempre 90 minutos” el 19/11/2026. Reemplaza la elección configurable del creador en el MVP; esa regla queda como historial de la revisión 2 y su posible regreso es sólo propuesta posterior. Pruebas de implementación pendientes. |
| MVP-06 | Alta · Pendiente | ¿Cómo se distribuyen web, API, PostgreSQL y actualización de marcadores? ¿Qué pasa si un servicio duerme o agota cuota? Define operación viable. | Ensayo de publicación y actualización, persistencia comprobada y consumo medido; proveedores elegidos con condiciones revisadas. |
| MVP-07 | Alta · Pendiente | ¿Cómo se validan sesiones Google/Supabase y permisos de participante, creador y administrador? Un login correcto no concede acceso a todos los torneos. | Diseño de sesión/identidad y permisos revisado; casos de acceso permitido/denegado definidos antes de implementar auth. |
| MVP-08 | Alta · Pendiente | ¿Qué subconjunto conserva la revisión del MVP respecto de la revisión 2? Evita desarrollar multiliga/configuración flexible por arrastre. | Resumen actualizado confirmado por el usuario, con incluidos, diferidos y reglas conservadas. |

## 4. Diseñar y comprobar durante la construcción

Estos puntos orientan ensayos progresivos; cada función necesita su decisión antes de considerarse terminada.

| ID | Prioridad / estado | Pregunta y motivo | Evidencia o criterio de cierre |
|---|---|---|---|
| MVP-09 | Media · Pendiente (guardado parcial definido) | Jornada con botón explícito: si un partido cerró antes de guardar, guardar los pronósticos válidos de los que sigan abiertos según el servidor e informar cuáles guardó y cuáles rechazó. Confirmación y aviso al salir conservados. | Probar el caso parcial y permisos; resolver recuperación ante fallos y navegación. Conservar campos con la pantalla abierta y reintentar sigue como propuesta, sin aprobar persistencia automática del navegador. No generalizar a otros campos inválidos; no se acredita implementación. |
| MVP-10 | Alta · Pendiente (tratamiento del cierre definido) | Guardar pronósticos válidos abiertos según la hora del servidor y rechazar cerrados sin borrar guardados previos ni reabrir edición; cierre/revelación al inicio conservados, sin puntos extra. Reglas, temporada y criterio de fases congelados al primer partido; completar cruces oficiales y actualizar reprogramaciones no autoriza cambios selectivos del creador. | Definir zona horaria y detalles de actualización; probar permisos, guardado parcial y cierre/revelación ante reprogramaciones y cruces incorporados. Decisiones de producto confirmadas; implementación y validación pendientes. |
| MVP-11 | Alta · Resuelto (definición) | Ranking final con marcador válido de 90 minutos más descuento. Orden por puntos y exactos. Empate persistente comparte posición (1.º, 1.º, 2.º). | Validar tanto los cambios de API como las excepciones de RN-16, con recálculo y trazabilidad. |
| MVP-12 | Media · Pendiente | ¿Qué ocurre al abrir una invitación sin sesión, con código inválido o siendo ya miembro? | Recorrido probado desde enlace hasta ingreso, con destino conservado tras Google y sin duplicar membresía. |
| MVP-13 | Alta · Pendiente | ¿Cómo se representan estados, reprogramaciones y fallos de fuente/conexión sin presentar un dato viejo como actual? Calendario y prode deben coincidir. | Mismo partido/horario/resultado en ambas vistas; reglas de aplazamiento/suspensión y recuperación probadas; última actualización y reintento acordados. |
| MVP-14 | Alta · Pendiente (producto definido, validación técnica abierta) | Confirmados Web Push sin correo, anticipación por usuario y desactivación. Un único aviso por participante/partido enumera sólo sus torneos sin pronóstico guardado, validando pendientes al enviar; ninguno si completó todo. Los 30 minutos previos quedan como valor inicial propuesto. | Definir rango/control de minutos sin adoptar uno por defecto implícito; validar permisos, desactivación, compatibilidad iPhone/PWA, reprogramaciones, programación/cuotas, reintentos, entrega y deduplicación mediante pruebas. No se garantiza puntualidad ni viabilidad gratuita antes del ensayo. |
| MVP-15 | Alta · Resuelto (definición) | API habitual. Personal calificado con permiso específico puede cargar o corregir un marcador final excepcionalmente y con evidencia. | Diseñar en C-14 autorización, auditoría, precedencia y retiro explícito. C-01 sigue pendiente. |
| MVP-16 | Alta · Pendiente | ¿Podemos actualizar, detectar errores, volver a una versión anterior y recuperar los datos? | Ensayo documentado de publicación y restauración en destino separado antes del piloto, con límites de recuperación conocidos. |

## 5. Mejoras pequeñas que conviene evaluar

Son recomendaciones para probar; no agregan requisitos automáticamente. Algunas desarrollan funciones ya acordadas, como explicar puntos o compartir invitaciones.

| ID | Propuesta | Beneficio esperado | Costo o duda a validar | Estado |
|---|---|---|---|---|
| IDEA-01 | Mostrar cuántos partidos faltan pronosticar y un acceso a pendientes. | Facilita completar la carga sin revisar todo. | Aclarar si cuenta por día, jornada o torneo. | Propuesta |
| IDEA-02 | Botón «Guardar pronósticos», confirmación al guardar y aviso al salir con cambios pendientes. | Da confianza y control sobre los pronósticos guardados al cargar una jornada. | Modalidad explícita elegida; resolver y probar errores y navegación en MVP-09. | Adoptada (definición) |
| IDEA-03 | Mostrar resultado válido, pronóstico y motivo de los puntos juntos. | Permite entender el ranking sin hacer cuentas aparte. | Acordar presentación y explicación de puntos definitivos de partidos finalizados. | Propuesta |
| IDEA-04 | Mostrar última actualización del marcador, demora detectada y reintento. | Ayuda a reconocer una interrupción del seguimiento. | Definir cuándo se considera desactualizado; véase MVP-03/13. | Propuesta |
| IDEA-05 | Compartir invitación fácilmente y retomar el torneo después del login. | Reduce pasos para que entren amigos. | Probar enlaces y navegación reales en celular. | Propuesta |
| IDEA-06 | Calendario, fixture y marcadores públicos sin login; prodes privados con login Google. | Permite consultar fútbol libremente y reserva el juego del grupo a sus participantes. | Definición confirmada por el usuario; implementar/probar membresía y permisos sobre contenido privado, y administración sólo autorizada. Estar logueado no habilita todos los torneos. | Adoptada (definición) |

Mi recomendación de trabajo: priorizar estas ayudas de uso y confianza antes de agregar otro módulo. Una propuesta se incorpora sólo después de acordar qué problema resuelve y cómo la probaremos.

## 6. Ideas para después del primer circuito jugable

| ID | Idea | Motivo para evaluarla después | Estado |
|---|---|---|---|
| FUT-01 | Minijuegos inspirados en Potrero. | Requieren definir mecánica, contenido y objetivo propio; probar primero que el prode se usa. | Diferido |
| FUT-02 | Noticias de fútbol. | Agregan fuentes, selección y mantenimiento editorial. | Diferido |
| FUT-03 | Más ligas y torneos multiliga. | Requieren calendarios, coberturas y cierres compatibles. Simplificación inicial por confirmar en MVP-08. | Propuesta para después |
| FUT-04 | Estadísticas detalladas, alineaciones y eventos del partido. | Amplían datos y pantallas; primero validar marcador/estado y disponibilidad. | Propuesta para después |
| FUT-05 | Aplicaciones Android/iPhone. | La visión móvil se conserva; distribución y operación se revisan después del piloto web. | Diferido |
| FUT-06 | Empresas, suscripciones y cobros. | Visión comercial conservada; planes, aislamiento, permisos y precios necesitan Discovery propio. | Diferido |
| FUT-07 | Ranking provisional en vivo. | Permitiría seguir posiciones mientras se juegan partidos; reconsiderar después del piloto según el uso observado, sin fecha ni compromiso de implementación. | Diferido |

## 7. Propuesta de pruebas por partes

Esta secuencia permite aprender durante la construcción; no sustituye el roadmap ni habilita implementación por sí sola. Una interfaz simple puede probarse antes de tener todas las integraciones.

1. **Datos y calendario:** elegir competencia, ensayar acceso al fixture y ver un día real. Verificar cambios de horario y correspondencia entre día y jornada.
2. **Circuito del prode:** crear torneo, abrir invitación, entrar con Google, guardar pronósticos y recuperarlos. Probar desde otro celular.
3. **Reglas y confianza:** cerrar edición, revelar pronósticos, puntuar y procesar una corrección recibida de la API; revisar ranking con el grupo.
4. **Seguimiento en vivo:** observar partidos reales y medir actualización, cuota y recuperación ante fallos. Los datos de ensayo deben estar identificados y separados; no introducir resultados simulados en un torneo real.
5. **Preparación del piloto:** practicar administración, publicación y restauración; acordar recordatorios y resolver los riesgos que afecten al grupo.
6. **Piloto con amigos:** observar si completan pronósticos, entienden el ranking y vuelven en jornadas siguientes. Anotar problemas antes de sumar funciones.

Cada ensayo termina con evidencia y una decisión: conservar, ajustar, investigar o diferir explícitamente. No hace falta terminar todo el producto para probar una parte, pero una prueba local no acredita que el flujo completo esté listo.

## 8. Próximos tres temas sugeridos

1. Presentar el resumen final revisado del Discovery para confirmación explícita del usuario; no cerrarlo automáticamente.
2. Tras ese checkpoint, adaptar el roadmap directamente desde Discovery según lo solicitado, sin exigir una Knowledge Base de diez archivos. No se crea el roadmap en esta actualización.
3. Mantener como validaciones operativas MVP-02/03 (fuente/cobertura/demora), MVP-09 (fallos de guardado), MVP-14 (Web Push) y permisos/reintentos de MVP-15; no prometer costo cero ya verificado.

## 9. Registro por sesión

### 18/11/2026 — Apertura de este seguimiento

- **Tratados:** navegación y seguimiento de partidos; necesidad de revisar alcance en varias sesiones.
- **Decisiones explícitas:** usuario eligió calendario por días y marcadores en vivo; pidió este documento para continuar en distintos momentos.
- **Preferencia reciente:** comenzar con una sola liga, compartida por calendario y prode; competencia y duración pendientes.
- **Propuestas:** mejoras pequeñas de uso y secuencia de pruebas de las secciones 5 y 7.
- **Evidencia:** conversación; referencias públicas registradas en las fichas enlazadas abajo. La viabilidad de datos gratuitos en vivo no está demostrada.
- **Próximo:** elegir uno de los tres temas sugeridos; conservar el Discovery abierto.

### 19/11/2026 — Liga argentina y opciones de datos

- **Tratados:** MVP-01 y MVP-02.
- **Decisión explícita:** el usuario elige liga argentina para el piloto, compartida por calendario y prode. Primera División/Liga Profesional es la interpretación a confirmar; edición y fases siguen pendientes.
- **Hallazgo:** API-Football limita Free a temporadas Year-4 a Year-2: en 2026, 2022–2024 ([explicación oficial](https://www.api-football.com/news/post/how-to-get-all-data-from-a-league-with-api-football)). No sirve como acceso gratuito a 2026; no hubo prueba con token.
- **Candidato, no adoptado:** API-Football publica [cobertura argentina](https://www.api-football.com/coverage) y [Pro de USD 16/mes, 7.500 consultas/día](https://www.api-football.com/pricing), verificados el 19/11/2026. La cobertura general no demuestra acceso completo a la edición/fases elegidas.
- **Otras opciones investigadas:** [Sportmonks Argentina](https://www.sportmonks.com/football-api/primera-division-argentina/) desde EUR 29/mes para cinco ligas, con prueba temporal de 14 días que requiere tarjeta; no equivale a servicio gratuito permanente.
- **API-Ninjas:** su [API de fútbol](https://api-ninjas.com/api/football) ofrece fixture/finales de la temporada argentina actual en el acceso gratuito y reserva vivo al pago. Sus [condiciones de planes](https://api-ninjas.com/pricing) limitan Free a evaluación/demo, sin uso comercial ni caché/almacenamiento; la tabla tampoco permite almacenamiento en Developer. No recomendarla para nuestro backend persistente sin permiso adecuado.
- **football-data.org:** Argentina no integra la [cobertura gratuita](https://www.football-data.org/coverage). Ninguna de estas opciones queda adoptada.
- **Próximo:** confirmar edición/fases y ensayar cobertura real y frecuencia con credenciales guardadas como secretos; no compartir claves en el chat. Registrar datos faltantes, consumo y derechos de uso antes de decidir.
- **Estado:** Discovery abierto; MVP-01 pendiente y MVP-02 en investigación. El Discovery principal y el PDF no se actualizaron en esta sesión.

#### 19/11/2026 — Consultas compartidas y nuevas fuentes por ensayar

- **Flujo previsto:** el proveedor actualiza registros compartidos; calendario y torneos consultan nuestra base. Crear un torneo o guardar pronósticos no requiere solicitudes al proveedor. El almacenamiento de datos externos depende de la licencia aplicable.
- **OpenFootAPI, candidata nueva:** [Free](https://openfootapi.com/pricing) publica 5.000 consultas/mes y 60/minuto con fixture y marcadores; su [cobertura](https://openfootapi.com/coverage) lista Liga Profesional Argentina 2026 (`comp_liga_profesional_arg`).
- Su [documentación de esa competencia](https://openfootapi.com/docs?competition=comp_liga_profesional_arg) describe partidos con marcadores en vivo en Free; eventos y stream requieren pago. Los [términos](https://openfootapi.com/terms) permiten persistencia, sujeta a licencia y atribución por fuente indicadas en `meta.sources`.
- **Límite de evidencia:** el intento de abrir un endpoint público mediante la herramienta web resultó inaccesible; no se validó una respuesta JSON ni el vivo argentino. OpenFootAPI no está adoptada: requiere ensayo real de cobertura, demora, consumo y atribución.
- **SportsAPI, pista secundaria:** [precios](https://sportsapi.app/pricing) anuncia vivo gratuito con 1.000 consultas/día durante beta y luego 100/día, con historial de últimos siete días. Argentina y licencia aún no verificadas; no es una candidata confirmada.
- **Próximo:** contrastar documentación con respuestas reales antes de elegir fuente. Se conserva el requisito de marcadores en vivo; no se promete viabilidad gratuita.

#### 19/11/2026 — Año deportivo completo y tolerancia del vivo

- **Decisiones explícitas:** el usuario quiere todo el año deportivo de la liga argentina y todos los partidos futuros hasta el final de la edición. Acepta hasta cinco minutos de demora del marcador para intentar mantener costo cero.
- **Pendiente:** año/edición exactos y frontera de fases, incluidas eliminatorias y eventual Trofeo de Campeones, que debe aclararse como copa separada antes de agregarlo. MVP-01 y MVP-04 siguen pendientes; en MVP-03 queda medir el retraso real. No se promete una fuente sin demora ni se equipara consulta cada cinco minutos con demora total de cinco minutos.
- **Formato 2026, fuente oficial:** [AFA](https://www.afa.com.ar/primerabnacional/posts/se-realizo-el-sorteo-de-la-liga-profesional-2026-ya-se-conocen-los-grupos-del-torneo-apertura-y-torneo-clausura) describe dos zonas de 15, 16 encuentros por club en cada torneo, ocho clasificados por zona y fase final eliminatoria.
- **Cambio para 2027 anunciado el 29/10/2026:** [Liga Profesional](https://www.ligaprofesional.ar/notas/institucional/2026/10/29/alternativa-superadora-anual/) presenta campeonato anual de 30 fechas sin zonas; Apertura con fechas 1–15 y playoffs de los primeros 16; Clausura con fechas 16–30, puntos del semestre desde cero y playoffs. El campeón anual surge de sumar las fases regulares.
- **Consecuencia:** la tabla anual agrega puntos, no partidos adicionales. No aplicar indefinidamente el formato 2026: el fixture y sus fases dependen del año elegido.
- **Próximo:** confirmar edición y fronteras; después verificar cobertura completa y medir demora/consumo con la fuente candidata. No se actualizaron Discovery principal, PDF ni estado.

#### 19/11/2026 — Apertura y Clausura con eliminatorias confirmados

- **Respuesta explícita:** “Apertura y Clausura con eliminatorias”, ante la propuesta de cerrar en la final del Clausura y dejar Trofeo de Campeones como adicional.
- **Definición confirmada:** todos los encuentros futuros desde la creación del torneo de Apertura y Clausura, incluidas sus eliminatorias, hasta la final del Clausura. Trofeo de Campeones queda excluido del MVP de este prode. Cada participante pronostica desde su ingreso y sin puntos retroactivos.
- **Se conserva:** torneos privados, acceso Google mediante Supabase Auth y tolerancia de hasta cinco minutos de demora real del vivo, pendiente de medición.
- **Estados:** MVP-04 resuelto en definición de producto; MVP-01 conserva sólo año/edición exactos pendientes y su posterior validación de fixture. No se probó ni implementó el conjunto de partidos.
- **Próximo:** MVP-05, opciones de criterio de resultado que podrá elegir el creador para eliminatorias; después año/edición y fuente. No adoptar regla global ni opciones concretas hasta recibir respuesta.

#### 19/11/2026 — Criterio único de 90 minutos para el MVP

- **Respuesta explícita:** “Simplificar el MVP: siempre 90 minutos”. MVP-05 queda resuelto en definición: marcador al terminar 90 minutos más descuento; no cuenta alargue ni tanda. Se mantienen 3 puntos por exacto y 1 por ganador/empate sin acumular.
- **Cambio de alcance:** reemplaza en el MVP la elección configurable del creador registrada en la revisión 2. Una configuración posterior queda como propuesta, no requisito actual.
- **Ejemplos documentales:** 1-1 a los 90 minutos más descuento y 2-1 tras alargue → vale 1-1; 1-1 a los 90 minutos más descuento y tanda 5-4 → vale 1-1. No son pruebas ejecutadas ni resultados de un torneo real.
- **Pendiente MVP-11:** decidir ranking final/provisional y cuándo confirmar resultado y puntos definitivos. No se da por aprobado puntuar definitivamente al minuto 90 antes de finalizar el partido.
- **Próximo:** MVP-11, luego año/edición exactos (MVP-01) y fuente de datos (MVP-02). Discovery principal y PDF conservan su revisión previa hasta reconciliar el resumen.

#### 19/11/2026 — Ranking provisional fuera del MVP

- **Respuesta explícita:** “Por ahora saquémoslo del MVP, dejémoslo como una feature posible para más adelante”, sobre ranking provisional en vivo.
- **Definición confirmada:** el ranking del MVP suma sólo partidos finalizados, con el marcador válido de 90 minutos más descuento confirmado. Se conservan los marcadores en vivo y la tolerancia de hasta cinco minutos, pendiente de comprobar; mostrar marcadores no implica asignar puntos provisionales.
- **Registro:** FUT-07 queda diferido como posibilidad posterior. MVP-11 conserva pendientes la confirmación/corrección de resultados, numeración de empates y validación del recálculo; no se da el ítem completo por resuelto ni se acreditan pruebas.
- **Referencias parciales:** snippets de las páginas oficiales de [TippBlitz](https://tippblitz.de/ratgeber/alternative-zu-kicktipp) y [Kickfan](https://kickfan.de/?lang=de) anuncian puntos/ranking en vivo. La apertura directa falló y no se probaron interfaces; no se infiere esa función en otros productos.
- **Próximo:** año/edición (MVP-01), fuente de datos (MVP-02) y resto de decisiones de MVP-11. Discovery principal, PDF y estado permanecen sin cambios.

#### 19/11/2026 — Temporada vigente y puestos consecutivos

- **Decisiones explícitas:** usar la temporada vigente al comenzar el piloto y numerar empates con puestos consecutivos: 1.º, 1.º, 2.º, sin saltar al 3.º.
- **MVP-01:** política de edición resuelta en definición; año concreto, fixture/formato y cobertura deberán verificarse al iniciar el piloto. No se fija 2026/2027 ni se garantiza acceso a esa temporada.
- **MVP-11:** puntos descendentes, luego marcadores exactos descendentes; si ambos coinciden, comparten puesto. Ejemplo documental: Ana, 10 puntos y 2 exactos → 1.ª; Juan, 10 puntos y 2 exactos → 1.º; Carlos, 9 puntos → 2.º. No es una prueba ejecutada.
- **Pendiente:** orden visual entre Ana y Juan sin romper el empate deportivo; no se inventa una regla. También siguen abiertos confirmación/corrección de resultados, explicación de puntos y pruebas.
- **Próximo:** fuente/demora del vivo (MVP-02/03), confirmación de resultados (MVP-11) y carga de pronósticos (MVP-09). No se actualizan Discovery principal, PDF ni estado.

- **Prueba técnica 19/11/2026 (MVP-02):** GET a `https://openfootapi.com/v1/matches?competition=comp_liga_profesional_arg&season=2026`, con credencial pública de demostración documentada, sin registrar su valor aquí.
- **Resultado:** primer intento sin resolución DNS en el entorno restringido; reintento con red escalada autorizada agotó el tiempo de espera de 20 segundos, sin estado HTTP ni JSON. Prueba inconclusa: no demuestra caída de la API ni ausencia de cobertura.
- **Estado de fuente:** MVP-02 sigue sin confirmar; OpenFootAPI no está adoptada y no se promete acceso gratuito viable. El parámetro 2026 pertenece a esta prueba, no fija la edición del piloto.
- **Próxima conversación (MVP-11), aún sin decisión:** comparar puntuación automática cuando la fuente indique final y entregue marcador completo de 90 minutos, con corrección administrativa, frente a validación administrativa de cada resultado antes de puntuar.

#### 19/11/2026 — Puntuación automática con corrección administrativa

- **Respuesta explícita:** “Automático con posibilidad de corrección administrativa”. La fuente debe indicar final y proporcionar completo el marcador de 90 minutos más descuento; si falta información, el partido queda pendiente sin puntuar.
- **Regla conservada:** sólo administradores de PRODE pueden corregir resultados, con registro visible y recálculo sin duplicación. No hay ranking provisional ni puntos definitivos por alcanzar el minuto 90 mientras el encuentro sigue en alargue.
- **Estados:** MVP-11 resuelto en definición de producto; implementación, pruebas y presentación detallada de puntos se validan durante la construcción. MVP-15 conserva pendientes procedimiento de discrepancias, permisos y mecanismo técnico. No se acredita software probado.
- **Próximo:** MVP-09 (carga/guardado), IDEA-06 (calendario público) y MVP-02 (fuente). La pregunta anterior queda como historial; esta respuesta confirma la política actual.

#### 19/11/2026 — Guardado explícito y consulta sobre visibilidad

- **Respuesta explícita:** usuario elige el botón «Guardar pronósticos» en la opción que incluía confirmación de guardado y aviso al salir con cambios pendientes. Se conserva la carga de jornada completa; no se adopta autosave.
- **Estado:** IDEA-02 adoptada en definición y modalidad de MVP-09 resuelta; recuperación de errores, navegación y ensayo de uso siguen pendientes. No se acredita implementación.
- **Segunda respuesta:** el usuario pregunta qué sentido tiene exigir login para consultar el calendario; no eligió aún acceso público. IDEA-06 sigue como propuesta, pendiente de explicar calendario/marcadores frente a torneos/pronósticos privados; no cambia el login sólo con Google.
- **Próximo:** aclarar visibilidad antes de decidir y continuar el diseño/pruebas del guardado. Discovery principal, PDF y estado permanecen intactos.

#### 19/11/2026 — Calendario público y prodes privados confirmados

- **Respuesta explícita:** “calendario público y prodes privados con login”. IDEA-06 queda adoptada en definición: fixture y marcadores pueden consultarse sin iniciar sesión; crear/unirse/pronosticar requiere Google mediante Supabase Auth.
- **Límite de acceso:** contenido y operaciones privadas requieren membresía y permisos, no sólo estar logueado. La administración de resultados sigue reservada a personal autorizado de PRODE; implementación y pruebas pendientes.
- **Sin decisiones adicionales:** conservar el destino después del login sigue como propuesta de IDEA-05; esta respuesta no la adopta. Tampoco define almacenamiento local/de sesión ni guardado parcial de pronósticos.
- **Próximo:** fallos de guardado (MVP-09) y partido que comienza antes de guardar (MVP-10/09), sin anticipar políticas. No se modifican Discovery principal, PDF ni estado.

#### 19/11/2026 — Guardado parcial y recordatorios de 30 minutos

- **Respuestas explícitas:** guardar los pronósticos abiertos y señalar el partido cerrado al guardar la jornada; recordar 30 minutos antes de los partidos con pronóstico faltante según lo registrado.
- **Definición:** el servidor comprueba la hora y guarda los pronósticos válidos de partidos todavía abiertos; informa guardados y rechazados. Rechazar un cerrado no borra un pronóstico previamente guardado ni habilita edición, y no agrega puntos. Esta decisión no generaliza el tratamiento de otros datos inválidos.
- **Pendiente MVP-09/10:** permisos, detalles de horario y pruebas del guardado parcial. Conservar campos mientras siga abierta la pantalla y ofrecer reintento continúa como propuesta; no se aprueba autosave ni persistencia automática del navegador.
- **Pendiente MVP-14:** canal, permisos, programación/envío y deduplicación de avisos. No se promete puntualidad ni se afirma compatibilidad gratuita verificada.
- **Próximo:** canal/deduplicación de recordatorios y otros detalles operativos. No se modifican Discovery principal, PDF ni estado.

#### 19/11/2026 — Web Push configurable y avisos agrupados

- **Respuestas explícitas:** canal Web Push; anticipación ajustable por usuario; un aviso por partido agrupando torneos pendientes. La configuración individual amplía la elección previa de 30 minutos fijos: 30 minutos queda como valor inicial propuesto, no un horario común obligatorio.
- **Reglas conservadas:** el usuario puede desactivar avisos. Al enviar, validar sus pronósticos guardados y listar sólo sus torneos pendientes para ese partido; si completó todos, no enviar. No se agrega correo al MVP.
- **MVP-14:** canal, configuración individual y agrupación definidos en producto; quedan rango/control de minutos, permisos/desactivación, compatibilidad iPhone/PWA, reprogramaciones, programación/cuotas, reintentos, entrega y deduplicación por definir o validar según corresponda.
- **Límite:** no se adoptan rangos nuevos, crean servicios ni prometen envíos puntuales. Próximo: distinguir los detalles de producto pendientes de los ensayos técnicos; Discovery principal, PDF y estado permanecen intactos.

#### 19/11/2026 — Fixture oficial completo y resolución de pendientes

- **Decisiones explícitas:** alcance fijo de temporada/fases, completando el fixture oficial; esperar la resolución de encuentros incluidos que sigan pendientes tras la final del Clausura.
- **Alcance y cierre:** al comenzar el primer partido se congelan reglas, temporada y criterio de selección, no la lista incompleta de cruces. Se incorporan cruces oficiales y reprogramaciones; el creador no puede agregar/quitar partidos selectivamente. Tras el cierre deportivo, el torneo queda «finalizando» sin ganador definitivo hasta resolver los incluidos; no se incorporan partidos de la siguiente edición y los cancelados definitivamente no puntúan.
- **Pregunta abierta MVP-15:** el usuario pide explicar por qué intervendría un administrador si la API es la fuente de verdad. No decidió exclusividad de la API ni predominio manual, ni canceló correcciones previas; explicar fuente operativa frente a intervención excepcional y fallback manual antes de resolver la política.
- **Próximo:** esa aclaración de API/correcciones, sin crear nuevas potestades. Implementación y pruebas pendientes; Discovery principal, PDF y estado intactos.

#### 19/11/2026 — API como única fuente de resultados confirmada

- **Respuesta explícita:** “API como única fuente de resultados”. Reemplaza para el MVP el fallback manual y la corrección administrativa de marcadores de la revisión 2; esos acuerdos anteriores quedan sólo como historial.
- **Política acordada en esa fecha:** estado final y marcador completo de 90 minutos más descuento de la API habilitan puntos automáticos; correcciones posteriores del proveedor recalculan sin duplicación. Información incompleta/inconsistente o errores quedan pendientes para reintentar, sin introducir un resultado manual.
- **Límite administrativo:** revisar registros/estado y reintentar sincronización; no editar marcadores ni puntuar manualmente. Una intervención manual futura sería sólo evolución posible, fuera del MVP.
- **MVP-15:** resuelto en definición; errores, permisos, reintentos, rastro de cambios del proveedor y pruebas van al roadmap. MVP-02 sigue sin fuente adoptada o validada y la prueba de OpenFootAPI fue inconclusa.
- **Próximo checkpoint:** confirmar el resumen final del Discovery y después adaptar el roadmap desde ese insumo, sin la KB de diez archivos solicitada previamente por el flujo. Esta actualización no cambia Discovery principal, PDF, estado ni roadmap, y no realiza operaciones git.

#### 24/11/2026 — Intervención excepcional sobre resultados

- Se aclararon RN-07 y RN-11 con ejemplos.
- RN-16 y RN-24 habilitan la intervención excepcional de personal calificado con permiso específico y evidencia. RN-08 y RN-15 se alinearon con el recálculo automático y la trazabilidad.

### Plantilla para copiar en la próxima sesión

- **Fecha:**
- **IDs tratados:**
- **Opciones y sus pros/contras:**
- **Decisión explícita o duda pendiente:**
- **Evidencia / resultado de prueba:**
- **IDs actualizados y efectos en otras decisiones:**
- **Próximo paso:**

## 10. Referencias para retomar

- [Discovery vigente](discovery.md): reglas y decisiones actuales.
- [Guía de despliegue y aprendizaje](despliegue-y-aprendizaje.md): investigación de opciones, no garantía de costo cero ni selección de proveedor.
- [Ficha de Promiedos](sources/promiedos.md): calendario y seguimiento como referencia; preferencia del usuario por otra dirección visual.
- [Ficha de Potrero](sources/potrero.md): minijuegos y evolución de entretenimiento como referencia.

Las condiciones de servicios y fuentes se vuelven a verificar al elegirlos. Este documento no asigna fechas de entrega, presupuesto de producción ni nuevas funciones aprobadas.
