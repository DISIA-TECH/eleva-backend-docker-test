from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.router import router
from app.core.logging import setup_logging
from app.db.vector_store import get_vector_store

# Configurar logging
logger = setup_logging()

app = FastAPI(title="RAG API for La Roca Village")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Dirección de la app React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router con todas las rutas
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_db_client():
    """Inicializa la base de datos vectorial al iniciar la aplicación"""
    try:
        logger.info("Inicializando conexión al almacén vectorial...")
        vector_store = await get_vector_store()
        if vector_store:
            logger.info("Almacén vectorial inicializado correctamente")
        else:
            logger.warning("No se pudo inicializar el almacén vectorial")
    except Exception as e:
        logger.error(f"Error durante el inicio de la aplicación: {e}", exc_info=True)
        raise

@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {"message": "La Roca Village RAG API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)