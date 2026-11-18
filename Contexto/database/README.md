<!---
[DATABASE] README.md - Documentación de la capa de datos.
Ubicación: database/README.md
Responsabilidad: Capa DATABASE - Explica división database/ vs app/, uso con DBeaver y migraciones.
Usa: database/connection.py, database/models/, database/alembic/
No hace: No ejecuta lógica de negocio, solo guía el manejo de datos.
--->

# Database — Capa de Datos (PostgreSQL)

Este folder `database/` concentra **TODO lo relacionado con persistencia**. La app pura (`app/`) nunca crea tablas.

## División de responsabilidades

| Carpeta | Rol | Analogía | Responsable |
|---------|-----|----------|-------------|
| `database/` | **Datos** — Modelos, conexión, migraciones, DDL, seeds | **DBA / Arquitecto DB** | Define qué se guarda y cómo |
| `app/` | **Lógica** — API, services, workers, schemas | **Backend / Cocina** | Define qué se hace con los datos |

> El backend (`app/`) **nunca** ejecuta `Base.metadata.create_all()`. Toda estructura nace de SQL o de Alembic.

### ¿Por qué híbrido profesional?

- Separación perfecta: cambiar de ORM o de motor no toca `app/services/` ni `app/api/`.
- DBeaver ve un `init_db.sql` autocontenido, sin depender de Python.
- Alembic vive junto a los modelos, no en la raíz.

## Estructura

```
database/
├── connection.py       # Engine async + Base (movido de app/core/database.py)
├── models/             # Modelos SQLAlchemy (9 tablas) - antes app/models/
├── alembic/            # Migraciones (movido de alembic/)
├── alembic.ini         # Config Alembic (movido de raíz, script_location = database/alembic)
├── seeds/
│   ├── leagues.sql     # 5 ligas (INSERT)
│   └── demo_data.sql   # Datos demo opcionales
└── init/
    └── init_db.sql     # DDL completo para pegar en DBeaver
```

## Cómo crear la DB en DBeaver (pasos)

1. **Crear DB vacía:**
   ```sql
   CREATE DATABASE quiniela OWNER postgres;
   \c quiniela
   CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- para gen_random_uuid()
   ```

2. **Ejecutar DDL completo:**
   - Abrir `database/init/init_db.sql` en DBeaver (SQL Editor → Open file).
   - Seleccionar todo → Execute SQL Script (`Ctrl+Alt+X`). Verifica 9 tablas creadas en el navegador.

3. **Cargar semillas (ligas):**
   ```sql
   \i database/seeds/leagues.sql
   -- o copiar/pegar el contenido en DBeaver
   SELECT * FROM leagues; -- 5 filas
   ```

4. **(Opcional) Demo data:**
   ```sql
   \i database/seeds/demo_data.sql
   ```

5. **Verificar:**
   ```sql
   \dt -- lista tablas
   \d+ users
   SELECT tablename FROM pg_tables WHERE schemaname='public';
   ```

## Cómo correr migraciones (Alembic)

Desde la **raíz del proyecto** (`C:/Users/GonziChan/Desktop/Proyecto`):

```bash
# Aplicar todo hasta la última versión
alembic -c database/alembic.ini upgrade head

# Crear nueva revisión autogenerada tras modificar database/models/*.py
alembic -c database/alembic.ini revision --autogenerate -m "add new column"

# Ver historial
alembic -c database/alembic.ini history

# Downgrade
alembic -c database/alembic.ini downgrade -1
```

> `database/alembic/env.py` hace `sys.path.insert(0, PROJECT_ROOT)` y usa `from database.connection import Base` → `target_metadata = Base.metadata`. No requiere cambiar `PYTHONPATH`.

## Cómo ver datos con SELECT (ejemplos)

```sql
-- Usuarios y torneos
SELECT id, username, email, is_premium FROM users;
SELECT id, name, invite_code, status, league_id FROM tournaments;
SELECT * FROM leagues; -- 5 ligas

-- Leaderboard de un torneo
SELECT u.username, tp.total_points, tp.accuracy, tp.rank
FROM tournament_participants tp
JOIN users u ON u.id = tp.user_id
WHERE tp.tournament_id = 'uuid-del-torneo'
ORDER BY tp.total_points DESC, tp.accuracy DESC;

-- Predicciones pendientes de scorear
SELECT * FROM predictions WHERE points_earned IS NULL;
SELECT * FROM matches WHERE status='NS' AND start_time > now() ORDER BY start_time LIMIT 10;

-- Verificar integridad
SELECT tournament_id, COUNT(*) FROM tournament_participants GROUP BY tournament_id;
```

## Reglas de oro

- **Backend nunca hace `create_all`**: solo Alembic o `init_db.sql` crean esquema. Buscar `create_all` en `app/` debe dar 0 resultados.
- **Cambios de esquema**: editar `database/models/*.py` → `alembic -c database/alembic.ini revision --autogenerate`.
- **FKs y CHECKs en DB**: no solo en Pydantic. Ej: `max_participants IN (10,50,100)`, `invite_code ~ '^[A-Za-z0-9]{8}$'`.
- **pgcrypto**: necesario para `gen_random_uuid()` en todas las PK UUID.
