import logging
from langchain.embeddings.openai import OpenAIEmbeddings

from app.core.config import settings

logger = logging.getLogger("rag-app")

# Singleton para el servicio de embeddings
_embeddings = None

def get_embeddings() -> OpenAIEmbeddings:
    """Obtiene el servicio de embeddings, inicializándolo si no existe"""
    global _embeddings
    
    if not _embeddings:
        logger.info(f"Inicializando servicio de embeddings con modelo {settings.OPENAI_EMBEDDING_MODEL}")
        _embeddings = OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Probar embeddings con un texto de muestra
        try:
            sample_text = "Texto de prueba para verificar el servicio de embeddings"
            sample_embedding = _embeddings.embed_query(sample_text)
            logger.info(f"Prueba de embedding exitosa: dimensión={len(sample_embedding)}")
        except Exception as e:
            logger.error(f"Prueba de embedding fallida: {e}")
            raise
    
    return _embeddings