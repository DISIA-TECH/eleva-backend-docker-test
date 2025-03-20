import logging
from typing import Optional, Dict, List, Any
from langchain.vectorstores import Qdrant

from app.core.config import settings
from app.db.document_loader import load_and_split_documents
from app.services.embeddings import get_embeddings

# Singleton para el almacén vectorial
_vector_store = None
logger = logging.getLogger("rag-app")

async def initialize_vector_store() -> Qdrant:
    """Inicializa el almacén vectorial con documentos"""
    global _vector_store
    
    try:
        # Cargar y dividir documentos
        chunks = await load_and_split_documents()
        if not chunks:
            logger.warning("No se encontraron fragmentos de documentos para cargar")
            return None
            
        # Obtener servicio de embeddings
        embeddings = get_embeddings()
        
        # Crear almacén vectorial
        logger.info("Creando base de datos vectorial...")
        _vector_store = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            url=settings.VECTOR_DB_URL,
            api_key=settings.VECTOR_DB_API_KEY,
            collection_name=settings.VECTOR_DB_COLLECTION,
        )
        
        logger.info(f"Almacén vectorial creado exitosamente con {len(chunks)} documentos")
        
        # Probar recuperación
        if _vector_store:
            sample_query = "horarios del centro comercial"
            docs = _vector_store.similarity_search(sample_query, k=1)
            logger.info(f"Prueba de recuperación con consulta '{sample_query}' exitosa")
        
        return _vector_store
    
    except Exception as e:
        logger.error(f"Error inicializando el almacén vectorial: {e}", exc_info=True)
        raise

async def get_vector_store() -> Optional[Qdrant]:
    """Obtiene el almacén vectorial, inicializándolo si no existe"""
    global _vector_store
    if not _vector_store:
        return await initialize_vector_store()
    return _vector_store