# CHANGES — Secuencia de Implementación

> Índice canónico de los changes del MVP **PRODE**.
> Cada item delimita una unidad de trabajo; duración y arquitectura se concretan al proponerlo, sin estimaciones de horas.
> **Leer este archivo antes de empezar un item.**

---

## Cómo usar este documento

1. Identificar el item y comprobar que sus dependencias están verificadas. C-01 es el primer item elegible; las pruebas de factibilidad preceden la construcción extensa.
2. Leer las referencias de Discovery indicadas en «Leer antes». Fuente: `discovery/discovery.md`, revisión 3 aprobada el 19/11/2026, y su registro `discovery/pendientes-mvp.md`. Por autorización explícita se genera este roadmap desde Discovery, sin crear ni exigir una KB duplicada de diez archivos.
3. Acordar alcance y verificación en el change OpenSpec correspondiente: consultar `openspec list --json`, luego status/instructions del change que exista. Este índice no crea changes. Modelos y rutas indicados abajo son propuestas operacionales para diseñar por change, no un esquema/API ya aprobado. Cerrar decisiones técnicas allí, sin duplicar una KB.
4. Implementar sólo tras las aprobaciones aplicables y verificar con evidencia. CRITICO: análisis y aprobación humana explícita antes de código; ALTO: propuesta revisada antes de escritura. MEDIO: checkpoints para decisiones; BAJO: autonomía con comprobaciones. El roadmap aprobado no autoriza automáticamente esas implementaciones. Aplicar TDD estricto a código: baseline, RED, GREEN, triangulación y refactor, registrando evidencia. Antes de la primera UI, resolver la política visual y los gates de C-06; hoy no hay opt-out.
5. Marcar `[x]` sólo tras verificar el resultado y registrar evidencia en el change; mantener dependencias y este índice coherentes. Conservar `Contexto/` como antecedente. No considerar cerradas fuente gratuita, demora real, hosting ni Push por estar planificados.

**Límites comunes:** web móvil con React/TypeScript/Vite, FastAPI y PostgreSQL; sólo Google vía Supabase Auth. Calendario público por día; prodes privados. Edición argentina vigente al piloto, Apertura/Clausura con eliminatorias, sin Trofeo de Campeones. Sin multiliga, noticias, minijuegos, estadísticas avanzadas, ranking provisional, apps nativas, B2B, suscripciones ni cobros. Las pruebas usan datos separados e identificados, nunca reemplazan el vivo del piloto. No hay resultado manual ni permisos administrativos para editarlo.

---

## Árbol de dependencias

Las ramas repetidas remiten al mismo item; «+» exige todas las dependencias indicadas. La lista Dependencias de cada item es la referencia operativa.

```text
C-01 fuente-gratuita-argentina
└── C-02 ensayo-operacion-gratuita
    └── C-03 base-tecnica
        ├── C-04 modelos-core
        │   ├── C-05 identidad-google
        │   │   └── C-08 prodes-invitaciones [+ C-07]
        │   │       └── C-09 pronosticos-por-jornada
        │   │           ├── C-10 puntuacion-ranking [+ C-07]
        │   │           │   ├── C-12 interfaz-prodes [+ C-06, C-09]
        │   │           │   └── C-14 supervision-sincronizacion [+ C-05, C-07]
        │   │           └── C-13 recordatorios-web-push [+ C-05, C-06]
        │   └── C-07 sincronizacion-fixture-resultados
        │       ├── C-08 (referencia)
        │       └── C-11 calendario-publico [+ C-06]
        └── C-06 politica-y-diseno-visual
            ├── C-11 (referencia)
            └── C-12 (referencia)

C-11 + C-12 + C-13 + C-14
└── C-15 verificacion-circuito-integrado
    └── C-16 preparacion-y-piloto
```

### Paralelismo por fase

```text
GATE 0: ninguna
  → C-01 fuente-gratuita-argentina                  [Agente A]
GATE 1: C-01 ✓, factibilidad de fuente acreditada
  → C-02 ensayo-operacion-gratuita                  [Agente B]
GATE 2: C-02 ✓, operación mínima acreditada
  → C-03 base-tecnica                              [Agente A]
GATE 3: C-03 ✓ — primer fork
  → C-04 modelos-core                              [Agente A]
  → C-06 politica-y-diseno-visual                   [Agente C]
GATE 4: C-04 ✓
  → C-05 identidad-google                          [Agente A]
  → C-07 sincronizacion-fixture-resultados          [Agente B]
GATE 5: C-05 + C-07 ✓
  → C-08 prodes-invitaciones                        [Agente A]
  → C-11 calendario-publico                        [Agente C — si C-06 ✓]
GATE 6: C-08 ✓
  → C-09 pronosticos-por-jornada                    [Agente A]
GATE 7: C-09 ✓
  → C-10 puntuacion-ranking                        [Agente A — si C-07 ✓]
  → C-13 recordatorios-web-push                     [Agente B — si C-05 + C-06 ✓]
GATE 8: C-10 ✓
  → C-12 interfaz-prodes                           [Agente C — si C-06 + C-09 ✓]
  → C-14 supervision-sincronizacion                [Agente B — si C-05 + C-07 ✓]
GATE 9: C-11 + C-12 + C-13 + C-14 ✓
  → C-15 verificacion-circuito-integrado            [Agente A]
GATE 10: C-15 ✓
  → C-16 preparacion-y-piloto                       [Agente A]
```

Los gates de factibilidad y revisión humana no son bloqueos de fase arbitrarios: sus resultados condicionan la viabilidad o la autorización del trabajo afectado. Si C-01 falla, volver al usuario para revisar presupuesto/alcance; no sustituir el vivo por históricos, carga manual o mocks.

### Camino crítico (11 changes — cadena de dependencia más larga)

```text
C-01 → C-02 → C-03 → C-04 → C-05 → C-08 → C-09 → C-10 → C-12 → C-15 → C-16
```

C-07 puede ocupar el lugar de C-05, y C-14 el de C-12: existen cadenas de igual longitud. Sin duraciones medidas, éste es el camino crítico por profundidad del grafo, no una predicción de fechas. Todos los items incluidos son requisitos del MVP; el camino no omite las otras ramas necesarias.

### Plan óptimo con 3 agentes

Pasos topológicos sin horas; cada paso espera la evidencia del anterior. Aprobaciones pueden cambiar su duración. Reservar archivos de contrato compartidos y evitar ediciones concurrentes sobre migraciones/estado.

| Paso | Agente A (Backend Core) | Agente B (Backend Aux) | Agente C (Frontend) |
|---|---|---|---|
| 1 | C-01 fuente | — | — |
| 2 | — | C-02 ensayo operativo | — |
| 3 | C-03 base | — | — |
| 4 | C-04 core | — | C-06 política/diseño |
| 5 | C-05 identidad | C-07 sincronización | — |
| 6 | C-08 prodes | — | C-11 calendario |
| 7 | C-09 pronósticos | — | — |
| 8 | C-10 ranking | C-13 Push | — |
| 9 | — | C-14 supervisión | C-12 prodes UI |
| 10 | C-15 integración | — | — |
| 11 | C-16 piloto | — | — |

---
## FASE 0 — Factibilidad antes de construir

### [C-01] `fuente-gratuita-argentina`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Producir informe reproducible de proveedor gratuito: edición argentina vigente al piloto, Apertura/Clausura y playoffs, identificadores de equipos/partidos, fixture actualizado y estados. Revisar licencia, persistencia y exhibición pública; conservar enlaces oficiales, fecha y evidencia de respuesta, sin credenciales.
  - Verificar en partidos reales marcador de 90 minutos más descuento separado de alargue/penales y estado final fiable; medir demora total evento→fuente→consulta→pantalla, objetivo aceptado hasta cinco minutos, y presupuesto de peticiones/cuotas en días de máxima concurrencia.
  - Tratar OpenFootAPI sólo como candidata: ensayo anterior falló por DNS en sandbox y timeout de 20 s con red escalada, sin JSON verificable. No hay proveedor adoptado. No confundir frecuencia de polling con demora total.
  - Entregar decisión go/no-go y casos para contrato de integración. Si cobertura, licencia, marcador, demora o cuota no cumplen, volver al usuario por presupuesto/alcance; no habilitar carga manual ni sustituir el vivo por históricos/mocks. Sin cuentas o compras por este item.
- **Dependencias**: ninguna
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-01/02/03/05/15)

---

### [C-02] `ensayo-operacion-gratuita`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Documentar ensayo pequeño y aislado web→FastAPI→PostgreSQL, actualización/publicación y persistencia después de reinicio; Render estático/API y Supabase PostgreSQL son candidatos, no proveedores seleccionados. Supabase Auth Google ya está aprobado independientemente del hosting/DB.
  - Comparar suspensión, arranque en frío, región, límites, conectividad y tareas programadas; medir coste/cuotas con C-01 y ensayar envío Web Push en dispositivos previstos, incluida condición iPhone/PWA. Comprobar recordatorio sin página abierta, permisos y reprogramación; no prometer puntualidad.
  - Ejecutar respaldo y restauración de datos de ensayo en destino separado; registrar tiempos/retención propuesta y pasos de recuperación. Entregar evidencia, riesgos y arquitectura mínima propuesta antes de gran construcción.
  - Revisar plan antes de cambios de configuración/datos. No crear cuentas, contratar ni usar datos reales sin autorización correspondiente. Si no es viable gratis, presentar al usuario el bloqueo y alternativas de alcance/presupuesto.
- **Dependencias**: C-01
- **Governance**: ALTO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-06); §4. Diseñar y comprobar durante la construcción (MVP-14/16)

---

## FASE 1 — Cimientos y contratos

### [C-03] `base-tecnica`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Proponer en OpenSpec la estructura React/TypeScript/Vite + FastAPI/PostgreSQL, herramientas de paquetes, ORM/migraciones y pruebas que aún no están elegidas; adoptar sólo tras revisar su diseño.
  - Generar base técnica mínima, configuración por entorno sin secretos versionados, health check propuesto GET /api/health, conexión de ensayo y pipeline de checks/build. Sin diseño de pantallas de producto antes de C-06.
  - Configurar ejecución reproducible de pruebas y documentación local; probar health/conexión y fallo de configuración sin exponer secretos. No inventar numeración de migración antes de elegir convención.
- **Dependencias**: C-02
- **Governance**: BAJO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-06)

---

### [C-04] `modelos-core`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar y revisar contratos/modelos provisionales User, Competition, Team, Edition, Phase y Match, con IDs del proveedor único, tiempos canónicos, estado y marcador 90 separado de alargue/tanda. Preparar migraciones sólo después de aprobación humana.
  - Representar edición anual vigente, Apertura/Clausura y eliminatorias; excluir Trofeo de Campeones y siguiente edición. Definir relaciones y claves/constraints antes de entidades que los referencian; no añadir CRUD administrativo de resultados.
  - Proponer catálogo de estados para aplazado antes de comenzar, suspendido tras comienzo, cancelado definitivo, final con datos completos e incompletos; preservar identidad ante reprogramación y cruces oficiales añadidos.
  - Tests de integridad/duplicación de IDs y transiciones límite; contratos suficientes para auth e integración posteriores. Registrar modelo y convención de migraciones en el diseño del change.
- **Dependencias**: C-03
- **Governance**: CRITICO
- **Leer antes**:
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-01/04/05); §4. Diseñar y comprobar durante la construcción (MVP-10/11/13)

---

### [C-05] `identidad-google`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Presentar diseño y obtener aprobación antes de implementar Google como único acceso mediante Supabase Auth: callbacks por entorno, identidad estable verificada, validación/renovación/revocación de sesión en FastAPI y perfil mínimo User.
  - Proponer GET /api/me y ciclo de logout; permisos de participante, creador y administrador técnico con mínimo privilegio. Diseñar dependencias de autorización reutilizables; membresía se conecta en C-08.
  - Definir política de sesión y soporte ante pérdida de acceso sin contraseña PRODE ni nuevos canales. Pruebas de token inválido/expirado, identidad ajena, sesión ausente y permisos denegados; ninguna operación privada confía sólo en el frontend.
- **Dependencias**: C-04
- **Governance**: CRITICO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §2. Usuarios y roles
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-07); §4. Diseñar y comprobar durante la construcción (MVP-12/15)

---

### [C-06] `politica-y-diseno-visual`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Invocar design-system antes de primera implementación visual y resolver una vez política system-and-mockups, system-only u off; no hay renuncia vigente. Auditar antecedentes/referencias sin asumirlos diseño aprobado y preservar estado previo.
  - Según política elegida, generar y mostrar fundación local/tokens/componentes, capturas móvil/escritorio y obtener aprobación; crear mockups requeridos de calendario, Google/invitación, prode/carga, ranking, preferencias Push y estados de error. Si la política exige aprobación, no avanzar UI antes de obtenerla.
  - Registrar revisión, fuentes, decisiones y gates en diseños de changes UI; propuesta de dirección propia, no copiar Promiedos por ser referencia. Incluir accesibilidad, carga, vacío, desactualizado, guardado parcial, fallo y permisos Push.
  - Verificar renders 390×844 y 1440×900 cuando haya navegador, o declarar revisión manual. Este item resuelve diseño; no implementa pantallas acopladas a endpoints aún inexistentes.
- **Dependencias**: C-03
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §3. Casos de uso
  - `discovery/discovery.md` §5. Funcionalidades necesarias para la primera versión
  - `discovery/pendientes-mvp.md` §5. Mejoras pequeñas que conviene evaluar

---

## FASE 2 — Dominio e integración de la fuente

### [C-07] `sincronizacion-fixture-resultados`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar adaptador del proveedor aceptado en C-01 y modelos provisionales SyncJob, ProviderSnapshot/Change y Match; registrar rastro de cambios sin exponer tokens. Solicitar aprobación para código de integración/auditoría antes de implementarlo.
  - Implementar importación idempotente de fixture, cruces y reprogramaciones, conciliación de IDs/horarios y resultados; limitar peticiones/reintentos según cuota, sin múltiples proveedores operativos ni vía manual de marcadores.
  - Proponer GET /api/public/matches?date= y GET /api/public/matches/{id}: datos públicos, estado, última actualización y señal de fuente demorada/fallida según umbral diseñado. Nunca presentar un dato viejo como vivo garantizado.
  - Emitir contrato interno de cambio de partido para cierre, puntuación y recordatorios; final + marcador90 completo habilita consumo, faltantes/inconsistencias quedan pendientes. Tests de duplicación, corrección, cuota, timeout, playoffs y cambio de horario.
- **Dependencias**: C-04
- **Governance**: CRITICO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-02/03); §4. Diseñar y comprobar durante la construcción (MVP-11/13/15)

---

### [C-08] `prodes-invitaciones`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar modelos provisionales Prode, Invitation y Membership; proponer POST /api/prodes, GET /api/prodes/mine, GET /api/prodes/{id} y POST /api/invitations/{code}/join, con autorización backend y aislamiento por membresía.
  - Fijar alcance a edición vigente con Apertura/Clausura/playoffs: partidos futuros desde creación y desde ingreso de cada participante, sin puntos retroactivos. Congelar reglas/edición/criterio de fases al primer partido sin congelar un fixture incompleto.
  - Incorporar cruces oficiales y reprogramaciones dentro del criterio congelado; impedir cambios selectivos del creador. Diseñar estados activo/finalizando/finalizado: esperar resolución de incluidos pendientes tras final del Clausura, cancelados definitivos sin puntos, nunca siguiente edición.
  - Probar enlace sin sesión preservado tras Google, código inválido, ingreso repetido idempotente y acceso de no miembro; probar límites de ingreso/creación al horario de inicio y finalización con pendientes.
- **Dependencias**: C-05, C-07
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §3. Casos de uso
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/pendientes-mvp.md` §3. Resolver antes de comprometer la función afectada (MVP-01/04); §4. Diseñar y comprobar durante la construcción (MVP-12)

---

### [C-09] `pronosticos-por-jornada`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar Prediction independiente por usuario/prode/partido; proponer GET /api/prodes/{id}/predictions y PUT /api/prodes/{id}/predictions/batch con respuesta por encuentro. Jornada agrupa la carga; no cambia el calendario público diario.
  - Aplicar hora de servidor para edición y revelación al inicio. Guardar válidos todavía abiertos y rechazar cerrados conservando cualquier pronóstico anterior guardado; no generalizar sin diseño el tratamiento de otros campos inválidos.
  - Ocultar pronósticos ajenos antes del inicio y revelarlos después sólo a miembros autorizados; tratar reprogramación previa sin reapertura automática de suspendido ya iniciado.
  - Tests de dos usuarios/prodes independientes, acceso ajeno, cierre durante envío parcial, reintento sin duplicados y conservación del dato rechazado; especificar errores recuperables que la UI usará.
- **Dependencias**: C-08
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/discovery.md` §3. Casos de uso
  - `discovery/pendientes-mvp.md` §4. Diseñar y comprobar durante la construcción (MVP-09/10/12)

---

### [C-10] `puntuacion-ranking`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar PointAward/RankingEntry o equivalentes y GET /api/prodes/{id}/ranking más detalle de puntos por partido; puntuar automáticamente sólo estado final del proveedor y marcador90 completo, aunque el encuentro haya requerido alargue/tanda.
  - Implementar 3 puntos por exacto o 1 por ganador/empate sin acumular; sin puntos provisionales. Recalcular idempotentemente ante corrección de API y cancelar puntuación que deje de tener resultado válido según contrato, preservando explicación/rastro de origen.
  - Ordenar por puntos descendentes, luego exactos descendentes; igualdad comparte puesto y siguiente consecutivo 1,1,2 sin tercer desempate deportivo. Mantener sin ganador definitivo un prode finalizando con partidos incluidos pendientes.
  - Tests de exacto/ganador/empate/error, eliminatoria empatada a 90 y decidida luego, resultado incompleto, correction/replay sin doble cómputo, empates densos y finalización diferida.
- **Dependencias**: C-09, C-07
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/discovery.md` §5. Funcionalidades necesarias para la primera versión
  - `discovery/pendientes-mvp.md` §4. Diseñar y comprobar durante la construcción (MVP-11/15)

---

## FASE 3 — Experiencia web y avisos

### [C-11] `calendario-publico`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Implementar vista pública por día con hoy, mañana y selector de fecha consumiendo GET /api/public/matches; mostrar fixture/estados/marcadores sin exigir Google y navegación cómoda en celular.
  - Aplicar política visual/revisión aprobada de C-06 y mockup correspondiente si se requiere; representar carga, vacío, error, horario cambiado, última actualización y demora, sin convertir jornada deportiva en navegación principal.
  - Probar filtros/fecha local frente a tiempo canónico, estados de datos faltantes, consulta sin sesión y consistencia con mismo partido en prode; capturar móvil/escritorio y revisar consola/red.
- **Dependencias**: C-06, C-07
- **Governance**: BAJO
- **Leer antes**:
  - `discovery/discovery.md` §5. Funcionalidades necesarias para la primera versión
  - `discovery/discovery.md` §3. Casos de uso
  - `discovery/pendientes-mvp.md` §5. Mejoras pequeñas que conviene evaluar

---

### [C-12] `interfaz-prodes`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Implementar recorridos Google→invitación→membresía y crear/listar/abrir prodes privados, cargando sólo endpoints autorizados de C-08/09/10. Mostrar estado finalizando y ranking definitivo con explicación de puntos y empates.
  - Implementar carga de jornada con botón «Guardar pronósticos», confirmación y aviso al salir con cambios; respuesta parcial distingue guardados/rechazados por cierre conservando valores previos.
  - Ante fallo de red conservar campos mientras la vista siga abierta y ofrecer reintento; no prometer recuperación tras cerrar/recargar, autosave ni persistencia offline. Probar navegación con pendientes, cierre en vuelo y errores de sesión/permisos.
  - Respetar diseño/mockups aprobados según C-06 y verificar móvil/escritorio, teclado y estados sin datos; comprobar que pronósticos ajenos no aparecen antes del cierre.
- **Dependencias**: C-06, C-09, C-10
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §3. Casos de uso
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/pendientes-mvp.md` §4. Diseñar y comprobar durante la construcción (MVP-09/10/11/12/13)

---

### [C-13] `recordatorios-web-push`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Revisar diseño de PushSubscription, NotificationPreference y ReminderDelivery antes de escribir: anticipación por usuario configurable, 30 minutos como valor inicial, desactivar y baja de suscripciones. Definir rango/control en el change sin inventarlo como decisión aprobada.
  - Proponer endpoints de preferencias/suscripciones y tareas según ensayo C-02. Emitir un único aviso por participante/partido agrupando sólo sus prodes con pronóstico faltante al momento de enviar; si completó todos, no emitir.
  - Aplicar revalidación al envío, idempotencia/deduplicación ante reintentos, múltiples dispositivos, reprogramación y desactivación; no usar correo como fallback. Proteger endpoints y secretos Push.
  - Verificar permisos, denegación, compatibilidad real incluida iPhone/PWA, entrega con página cerrada y cuotas; UI de permiso/preferencias debe respetar C-06 ya aprobado en la secuencia. Medir limitaciones y no prometer puntualidad.
- **Dependencias**: C-05, C-06, C-09
- **Governance**: ALTO
- **Leer antes**:
  - `discovery/discovery.md` §8. Integraciones y orientación técnica
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/pendientes-mvp.md` §4. Diseñar y comprobar durante la construcción (MVP-14)

---

## FASE 4 — Supervisión y validación del piloto

### [C-14] `supervision-sincronizacion`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Diseñar y aprobar acceso técnico restringido a SyncJob/ProviderChange y estado de recálculo; proponer GET /api/admin/sync-jobs y POST /api/admin/sync-jobs/{id}/retry con límites e idempotencia. Registrar actividad sensible bajo revisión humana.
  - Entregar herramienta operativa mínima para ver fallos/última sincronización y reintentar; no incluir edición/corrección manual de marcadores, validación manual para puntuar ni privilegios deportivos del creador.
  - Verificar permiso administrativo separado de Google/membresía, reintentos concurrentes y ausencia de tokens/datos personales innecesarios en logs. Si se añade pantalla, aplicar C-06 antes de implementarla; el diseño técnico concreta CLI o UI mínima.
- **Dependencias**: C-05, C-07, C-10
- **Governance**: CRITICO
- **Leer antes**:
  - `discovery/discovery.md` §2. Usuarios y roles
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/pendientes-mvp.md` §4. Diseñar y comprobar durante la construcción (MVP-11/15)

---

### [C-15] `verificacion-circuito-integrado`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Automatizar/ejecutar circuito calendario público→Google→crear/unirse→pronosticar→cierre/revelación→final API→ranking→corrección API con dos usuarios y prodes independientes; usar entornos/datos de ensayo separados.
  - Probar permisos negativos, guardado parcial, red caída/reintento, fixture reprogramado y cruces nuevos, finalizando sin siguiente edición, Push agrupado/desactivado y retry técnico sin mutar marcadores manualmente.
  - Observar encuentros reales de fuente aceptada para medir extremo a extremo el vivo y consumo en condiciones del piloto; verificar consistencia entre calendario/prode y señalización de atraso/fallo. Mocks son válidos en tests aislados, no evidencia de cobertura/vivo.
  - Comparar cada pantalla/estado con diseño aprobado a 390×844 y 1440×900, consola y red; registrar comprobado/no comprobado, diferencias y evidencia. Sin navegador declarar revisión manual. Corregir bloqueantes antes de completar.
- **Dependencias**: C-11, C-12, C-13, C-14
- **Governance**: MEDIO
- **Leer antes**:
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/discovery.md` §7. Reglas de negocio aprobadas
  - `discovery/pendientes-mvp.md` §7. Propuesta de pruebas por partes

---

### [C-16] `preparacion-y-piloto`
- **Estado**: `[ ]` pendiente
- **Scope**: diseño y entregables acotados al item.
  - Revisar plan operativo y ejecutar ensayo de publicar/actualizar, detectar error, revertir versión y restaurar datos en destino separado; documentar responsable, frecuencia/retención, límites de recuperación, alertas y cuotas sin presuponerlos acordados.
  - Preparar guías prácticas de mantenimiento y aprendizaje para stack/proveedores efectivamente elegidos; confirmar entorno, DNS/HTTPS/callbacks y backup antes de autorizar exposición real. No crear cuentas, comprar ni publicar como efecto automático del roadmap.
  - Acordar con usuario tamaño, participantes, fecha/edición vigente y criterios de piloto; comprobar fixture/cobertura actual y consumo. Lanzar sólo con autorizaciones operativas y de seguridad correspondientes.
  - Observar carga en celular, comprensión de puntos/ranking, recepción de avisos y regreso en próximas jornadas; registrar hallazgos y priorizar ajustes sin sumar multiliga, móvil, noticias/minijuegos o cobros al MVP.
- **Dependencias**: C-15
- **Governance**: ALTO
- **Leer antes**:
  - `discovery/discovery.md` §10. Riesgos, mantenimiento y validación
  - `discovery/discovery.md` §11. Preguntas abiertas y validaciones del roadmap
  - `discovery/pendientes-mvp.md` §7. Propuesta de pruebas por partes; §4. Diseñar y comprobar durante la construcción (MVP-16)

---

