"""
[DATABASE] __init__.py - Paquete raíz de la capa de datos.
Ubicación: database/__init__.py
Responsabilidad: Capa DATABASE - Marca database como paquete y expone Base/engine para que DBeaver/Alembic y app lo importen.
Usa: database.connection.Base
No hace: No define tablas ni ejecuta migraciones.
"""

"""Database package - PostgreSQL via SQLAlchemy async."""
