"""
[WORKERS] mocks/__init__.py - Paquete de datos mock (fallback sin API).
Ubicación: app/mocks/__init__.py
Responsabilidad: Capa WORKERS - Expone fixtures/results/leagues JSON para MockAdapter cuando MOCK_MODE=true. No toca DB.
Usa: app.mocks.fixtures.json, app.mocks.results.json
No hace: No sincroniza ni persiste, solo provee datos estáticos para demo $0.
"""

"""Mocks package."""
