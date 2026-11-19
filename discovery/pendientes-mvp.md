# PRODE — Dudas, decisiones y pruebas del MVP

**Actualizado:** 19 de noviembre de 2026.  
**Estado:** Discovery abierto; alcance del MVP en discusión.  
**Propósito:** retomar el trabajo en distintas sesiones sin perder dudas, propuestas ni decisiones.

Este registro acompaña al [Discovery, revisión 2](discovery.md). Las preferencias recientes de la conversación se registran acá mientras se acuerda un resumen revisado. El Discovery y su PDF todavía describen la revisión 2; este archivo no es el alcance final, un roadmap aprobado ni una autorización para implementar todo lo listado.

## 1. Cómo usar este documento

- Al empezar una sesión, elegir entre uno y tres IDs pendientes.
- Para cada punto, conversar opciones, reunir evidencia y registrar la decisión explícita.
- Marcar `Resuelto` cuando haya respuesta acordada y evidencia suficiente; conservar el ID y el motivo.
- Si aparece una idea nueva, anotarla como `Propuesta`, sin incorporarla automáticamente al MVP.
- Si una prueba cambia una decisión, registrar qué cambió y revisar sus efectos sobre otros puntos.
- Al confirmar el resumen de alcance, reconciliar el Discovery y después su PDF.

**Estados:** `Pendiente`, `En investigación`, `Propuesta`, `Resuelto`, `Diferido`.  
**Prioridad:** `Alta` bloquea la decisión o función afectada; `Media` se puede resolver durante su diseño/prueba; `Baja` corresponde a evolución. La prioridad no fija fechas ni obliga a resolver toda la lista antes de experimentar.

## 2. Base de conversación y decisiones previas

| Tema | Situación actual |
|---|---|
| Producto inicial | Web cómoda en celular, jugable con amigos/conocidos; objetivo de servicios gratuitos dentro de sus cuotas. |
| Liga inicial | El usuario eligió la liga argentina para el piloto y la misma liga para calendario y prode. Se interpreta Primera División/Liga Profesional; falta confirmar competencia exacta, edición y fases. |
| Calendario | Elegido por el usuario: por días, con hoy, mañana y selector de fecha; no navegación principal por jornada deportiva. |
| Seguimiento | Elegido por el usuario: también marcadores durante los partidos. Fuente, frecuencia y viabilidad gratuita por validar. |
| Acceso | Aprobado: sólo Google mediante Supabase Auth. FastAPI valida identidad y autoriza operaciones; sin contraseña propia de PRODE. |
| Stack | Aprobado: React + TypeScript + Vite, Python + FastAPI y PostgreSQL. Proveedores de alojamiento y base pendientes. |
| Juego | Reglas previas: pronósticos independientes por torneo, 3 por exacto y 1 por ganador/empate sin acumular; cierre y revelación al inicio; desempate por exactos y luego posición compartida. |
| Invitaciones | Regla previa: torneo privado; ingreso por enlace/código, incluso iniciado, sólo para partidos futuros y sin puntos retroactivos. |
| Resultados | Administración centralizada en PRODE, correcciones trazables y recálculo. La carga manual de finales no equivale a un servicio de marcadores en vivo. |
| Recordatorios | Estaban aprobados antes de cada partido sin pronóstico. La propuesta de probar primero el circuito básico no los elimina: falta acordar su lugar en el MVP. |
| Alcance anterior | La revisión 2 contemplaba multiliga y selección flexible de jornadas/partidos. Falta reconciliar ese alcance con la simplificación reciente, tras confirmar el resumen. |

## 3. Resolver antes de comprometer la función afectada

| ID | Prioridad / estado | Pregunta y motivo | Qué permitiría cerrarlo |
|---|---|---|---|
| MVP-01 | Alta · Pendiente | Elegida la liga argentina para calendario y prode; ¿confirmamos Primera División/Liga Profesional y qué edición/fases (Apertura, Clausura u otras)? Define fixture y datos necesarios. | Competencia exacta, edición y fases confirmadas y estructura real revisada; la preferencia por Argentina no cierra este punto. |
| MVP-02 | Alta · En investigación | ¿Qué fuente permite vivo de esa edición dentro de sus condiciones y cuotas? API-Football documenta Free 2022–2024 en 2026, no la temporada 2026 ([restricción oficial](https://www.api-football.com/news/post/how-to-get-all-data-from-a-league-with-api-football)); se corrige la incertidumbre anterior sobre acceso actual gratuito. | Acceso verificado a encuentros de la edición elegida, condiciones revisadas y prueba de consumo/cobertura. No se probó con token ni se eligió proveedor. |
| MVP-03 | Alta · Pendiente | ¿Qué demora de actualización resulta aceptable y qué ocurre si la fuente falla? “En vivo” necesita una expectativa concreta. | Frecuencia y tolerancia acordadas, medición de una prueba y presentación acordada de dato desactualizado. |
| MVP-04 | Alta · Pendiente | ¿Cuánto dura un torneo privado: edición completa, resto de la edición o jornadas habilitadas? ¿Todos usan el mismo conjunto? Define cierre y ganador. | Una modalidad inicial acordada, con inicio, conjunto de partidos y final inequívocos. |
| MVP-05 | Alta · Pendiente | Si hay eliminatorias, ¿qué resultado puntúa y qué opciones ofrece el creador? La elección del criterio ya se había aprobado; las opciones siguen abiertas. | Opciones acordadas para 90 minutos, alargue y penales, con ejemplos. Si no aplica al piloto, diferimiento explícito. |
| MVP-06 | Alta · Pendiente | ¿Cómo se distribuyen web, API, PostgreSQL y actualización de marcadores? ¿Qué pasa si un servicio duerme o agota cuota? Define operación viable. | Ensayo de publicación y actualización, persistencia comprobada y consumo medido; proveedores elegidos con condiciones revisadas. |
| MVP-07 | Alta · Pendiente | ¿Cómo se validan sesiones Google/Supabase y permisos de participante, creador y administrador? Un login correcto no concede acceso a todos los torneos. | Diseño de sesión/identidad y permisos revisado; casos de acceso permitido/denegado definidos antes de implementar auth. |
| MVP-08 | Alta · Pendiente | ¿Qué subconjunto conserva la revisión del MVP respecto de la revisión 2? Evita desarrollar multiliga/configuración flexible por arrastre. | Resumen actualizado confirmado por el usuario, con incluidos, diferidos y reglas conservadas. |

## 4. Diseñar y comprobar durante la construcción

Estos puntos orientan ensayos progresivos; cada función necesita su decisión antes de considerarse terminada.

| ID | Prioridad / estado | Pregunta y motivo | Evidencia o criterio de cierre |
|---|---|---|---|
| MVP-09 | Media · Pendiente | ¿Se pronostica por jornada o desde la lista diaria? Calendario y jornada no son equivalentes. ¿Cómo se evita perder cambios al navegar? | Persona completa varios partidos desde celular, reconoce cuáles guardó y recupera sus valores al volver. |
| MVP-10 | Alta · Pendiente | ¿Cómo se bloquea al inicio y se evita revelar pronósticos ajenos antes? Incluye hora del servidor, zona horaria y cambios de horario. | Casos de antes/después del cierre y permisos probados; política de horario acordada. |
| MVP-11 | Alta · Pendiente | ¿Cómo se explican los puntos y se recalcula sin duplicar? ¿Hay ranking provisional durante el juego o sólo final? ¿Cómo se numeran empates? | Ejemplos acordados de puntuación, empate y corrección; resultados verificables y distinción clara entre provisional y definitivo. |
| MVP-12 | Media · Pendiente | ¿Qué ocurre al abrir una invitación sin sesión, con código inválido o siendo ya miembro? | Recorrido probado desde enlace hasta ingreso, con destino conservado tras Google y sin duplicar membresía. |
| MVP-13 | Alta · Pendiente | ¿Cómo se representan estados, reprogramaciones y fallos de fuente/conexión sin presentar un dato viejo como actual? Calendario y prode deben coincidir. | Mismo partido/horario/resultado en ambas vistas; reglas de aplazamiento/suspensión y recuperación probadas; última actualización y reintento acordados. |
| MVP-14 | Alta · Pendiente | ¿Cuándo incorporamos recordatorios y por qué canal? ¿Qué anticipación, permisos y deduplicación necesitan? | Alcance confirmado explícitamente; entrega y desactivación probadas en celulares, incluyendo pendientes resueltos y partidos compartidos entre torneos. |
| MVP-15 | Alta · Pendiente | ¿Quién opera fixture/resultados y cómo se resuelve una discrepancia con la fuente? | Procedimiento probado de carga/corrección por administrador, registro visible y recálculo consistente. |
| MVP-16 | Alta · Pendiente | ¿Podemos actualizar, detectar errores, volver a una versión anterior y recuperar los datos? | Ensayo documentado de publicación y restauración en destino separado antes del piloto, con límites de recuperación conocidos. |

## 5. Mejoras pequeñas que conviene evaluar

Son recomendaciones para probar; no agregan requisitos automáticamente. Algunas desarrollan funciones ya acordadas, como explicar puntos o compartir invitaciones.

| ID | Propuesta | Beneficio esperado | Costo o duda a validar | Estado |
|---|---|---|---|---|
| IDEA-01 | Mostrar cuántos partidos faltan pronosticar y un acceso a pendientes. | Facilita completar la carga sin revisar todo. | Aclarar si cuenta por día, jornada o torneo. | Propuesta |
| IDEA-02 | Confirmar guardado por partido y señalar cambios sin guardar. | Da confianza en que el pronóstico quedó registrado. | Elegir guardado explícito o automático y resolver errores. | Propuesta |
| IDEA-03 | Mostrar resultado válido, pronóstico y motivo de los puntos juntos. | Permite entender el ranking sin hacer cuentas aparte. | Acordar presentación y distinción de puntos provisionales, si existen. | Propuesta |
| IDEA-04 | Mostrar última actualización del marcador, demora detectada y reintento. | Ayuda a reconocer una interrupción del seguimiento. | Definir cuándo se considera desactualizado; véase MVP-03/13. | Propuesta |
| IDEA-05 | Compartir invitación fácilmente y retomar el torneo después del login. | Reduce pasos para que entren amigos. | Probar enlaces y navegación reales en celular. | Propuesta |
| IDEA-06 | Permitir consultar el calendario sin login. | Reduce pasos para descubrir la app. | Definir pantallas públicas/privadas y proteger pronósticos y torneos. | Propuesta |

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

## 7. Propuesta de pruebas por partes

Esta secuencia permite aprender durante la construcción; no sustituye el roadmap ni habilita implementación por sí sola. Una interfaz simple puede probarse antes de tener todas las integraciones.

1. **Datos y calendario:** elegir competencia, ensayar acceso al fixture y ver un día real. Verificar cambios de horario y correspondencia entre día y jornada.
2. **Circuito del prode:** crear torneo, abrir invitación, entrar con Google, guardar pronósticos y recuperarlos. Probar desde otro celular.
3. **Reglas y confianza:** cerrar edición, revelar pronósticos, puntuar y corregir un resultado; revisar ranking con el grupo.
4. **Seguimiento en vivo:** observar partidos reales y medir actualización, cuota y recuperación ante fallos. Los datos de ensayo deben estar identificados y separados; no introducir resultados simulados en un torneo real.
5. **Preparación del piloto:** practicar administración, publicación y restauración; acordar recordatorios y resolver los riesgos que afecten al grupo.
6. **Piloto con amigos:** observar si completan pronósticos, entienden el ranking y vuelven en jornadas siguientes. Anotar problemas antes de sumar funciones.

Cada ensayo termina con evidencia y una decisión: conservar, ajustar, investigar o diferir explícitamente. No hace falta terminar todo el producto para probar una parte, pero una prueba local no acredita que el flujo completo esté listo.

## 8. Próximos tres temas sugeridos

1. **MVP-01 + MVP-04:** competencia/edición y duración inicial del torneo.
2. **MVP-02 + MVP-03:** prueba de datos en vivo, demora aceptable y viabilidad dentro de costo cero.
3. **MVP-08 + MVP-14:** resumen del alcance pequeño y ubicación de recordatorios respecto del piloto.

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

### Plantilla para copiar en la próxima sesión

- **Fecha:**
- **IDs tratados:**
- **Opciones y sus pros/contras:**
- **Decisión explícita o duda pendiente:**
- **Evidencia / resultado de prueba:**
- **IDs actualizados y efectos en otras decisiones:**
- **Próximo paso:**

## 10. Referencias para retomar

- [Discovery aprobado, revisión 2](discovery.md): reglas y decisiones anteriores; debe reconciliarse con el nuevo resumen confirmado.
- [Guía de despliegue y aprendizaje](despliegue-y-aprendizaje.md): investigación de opciones, no garantía de costo cero ni selección de proveedor.
- [Ficha de Promiedos](sources/promiedos.md): calendario y seguimiento como referencia; preferencia del usuario por otra dirección visual.
- [Ficha de Potrero](sources/potrero.md): minijuegos y evolución de entretenimiento como referencia.

Las condiciones de servicios y fuentes se vuelven a verificar al elegirlos. Este documento no asigna fechas de entrega, presupuesto de producción ni nuevas funciones aprobadas.
