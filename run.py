"""
[APP] run.py - Runner para Windows (SelectorEventLoop fix para psycopg + asyncpg).
Ubicación: run.py (raíz)
Responsabilidad: Establecer WindowsSelectorEventLoopPolicy ANTES de que uvicorn cree el loop.
Usa: app.main:app
No hace: No define lógica, solo arranca el servidor de forma compatible con Windows.
"""
import asyncio
import sys

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # Crear un SelectorEventLoop explícito para psycopg
        try:
            loop = asyncio.SelectorEventLoop()
            asyncio.set_event_loop(loop)
        except Exception:
            pass
    except Exception:
        pass

import uvicorn

if __name__ == "__main__":
    # loop="none" evita que uvicorn cree Proactor, respeta SelectorEventLoop ya creado
    uvicorn.run("app.main:app", host="127.0.0.1", port=8002, reload=False, loop="none", log_level="debug")
