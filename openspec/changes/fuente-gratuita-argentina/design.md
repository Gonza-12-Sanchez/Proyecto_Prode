# Design

## Context

El Discovery R5 y los pendientes MVP-01/02/03/05/15 contienen las reglas y pistas iniciales. OpenFootAPI es la primera candidata. El intento anterior terminó con un error DNS y luego un timeout, sin respuesta JSON para comprobar la cobertura. Los planes, temporadas y términos mencionados en Discovery son observaciones históricas que requieren revisión.

## Goals / Non-Goals

**Goals:** permitir que otra persona repita las consultas, verifique los cálculos y llegue al mismo dictamen con la evidencia disponible.

**Non-Goals:** desplegar servicios, construir el adaptador, crear cuentas o contratar un plan. La excepción administrativa de RN-16 queda fuera del ensayo y no acredita cobertura ni actualización en vivo.

## Decisions

1. **Fijar el alcance con fuentes oficiales.** Registrar fecha de evaluación, edición, identificadores de la competencia y las fases, y calendario oficial de referencia. Consultar toda la paginación habilitada y conciliar los partidos publicados de Apertura, Clausura y eliminatorias. Guardar evidencia mínima y autorizada de IDs de equipos y partidos, horario con zona horaria, cambio de horario, estados y cruces. Distinguir fixture futuro todavía sin publicar de partidos oficiales ausentes. Si el piloto cambia de edición, repetir las comprobaciones antes de adoptar la fuente.
2. **Comprobar el significado del resultado.** Comparar partidos argentinos reales con el resultado oficial, incluyendo casos definidos en tiempo reglamentario, por alargue y por penales si ocurrieron. En cada caso identificar el valor al final de los 90 minutos más descuento y el estado que confirma el cierre. Conservar un caso de dato omitido o ambiguo para precisar qué debe quedar pendiente en el futuro contrato. Si la edición carece aún de un caso necesario, una muestra histórica podrá orientar el mapeo, dejando la comprobación de la edición objetivo pendiente.
3. **Medir demora y dimensionar consultas.** Elegir antes del ensayo una ventana de partidos concurrentes, el intervalo de consulta y una referencia verificable para la hora del evento. Registrar en UTC el evento, la disponibilidad en origen si puede comprobarse, la primera respuesta que lo muestra y cuánto tardaría en verse con la frecuencia de publicación prevista. Documentar cantidades y tipos de eventos muestreados, retraso máximo observado y margen hasta cinco minutos. La primera detección por consulta da una cota de observación, no identifica por sí sola cuándo cambió el origen. Si todavía no existe pantalla, separar lo observado de la proyección del tramo local y dejar la verificación completa para el ensayo operativo. Estimar solicitudes por minuto, día y mes según endpoints, concurrencia, páginas, refresh, reintentos y margen; comparar con cada límite oficial del plan gratuito.
4. **Guardar evidencia verificable con límites de acceso.** Fechar documentos oficiales de planes, cobertura y términos. Registrar URL y parámetros sin credenciales, instante, código, campos relevantes y extractos sólo si está permitida su conservación. Revisar persistencia, caché, exhibición pública, atribución y alcance del uso comercial proyectado. Si una condición es ambigua, consignar la aclaración necesaria con su fuente. Probar mediante endpoints públicos o acceso autorizado existente, sin credenciales en el informe.
5. **Decidir por criterio.** Usar una tabla con cada requisito, estado y referencia. Recomendar avanzar condicionalmente a C-02 si se verifican los requisitos de la fuente y las mediciones dejan margen razonable para el tramo pendiente de pantalla. Dar no-go al plan que incumple un requisito demostrado y marcar inconcluso cuando la evidencia no permite decidir, por ejemplo por DNS, timeout, muestra insuficiente o derechos sin confirmar. Si ninguna alternativa califica, presentar opciones de costo o alcance a decisión del usuario. La recomendación del informe no equivale a adoptar una fuente en producción.

## Risks / Trade-offs

- Acceso o ventana de observación insuficientes → registrar el bloqueo, probar otra candidata documentada cuando exista acceso habilitado y mantener el resultado inconcluso donde corresponda.
- Cobertura comercial genérica o cuotas promocionales → contrastar con el acceso habilitado de la edición real y fechar los términos aplicables.
- Pocos eventos observados → informar alcance y variación de la muestra; la demora medida describe el ensayo y no garantiza rendimiento futuro.
