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
    """Inicializa el almacén vectorial con documentos o se conecta si ya existe"""
    global _vector_store
    
    try:
        # Obtener servicio de embeddings
        embeddings = get_embeddings()
        
        # Intentar conectarse primero a la colección existente
        from qdrant_client import QdrantClient
        
        client = QdrantClient(
            url=settings.VECTOR_DB_URL,
            api_key=settings.VECTOR_DB_API_KEY
        )
        
        # Verificar si la colección existe y tiene puntos
        collection_exists = False
        has_points = False
        
        try:
            collection_info = client.get_collection(settings.VECTOR_DB_COLLECTION)
            collection_exists = True
            
            # Verificar si la colección tiene puntos
            if hasattr(collection_info, 'points_count') and collection_info.points_count > 0:
                has_points = True
                logger.info(f"Colección '{settings.VECTOR_DB_COLLECTION}' encontrada con {collection_info.points_count} puntos")
            else:
                # Alternativa: verificar un punto de muestra
                sample_search = client.search(
                    collection_name=settings.VECTOR_DB_COLLECTION,
                    query_vector=[0.0] * 1536,  # Vector de ceros como consulta
                    limit=1
                )
                has_points = len(sample_search) > 0
                logger.info(f"Colección '{settings.VECTOR_DB_COLLECTION}' encontrada, tiene puntos: {has_points}")
                
        except Exception as e:
            logger.info(f"No se encontró la colección: {e}")
            
        # Si la colección existe y tiene puntos, solo conectarse
        if collection_exists and has_points:
            logger.info(f"Conectando a colección existente '{settings.VECTOR_DB_COLLECTION}'")
            # Crear instancia de Qdrant sin cargar nuevos documentos
            _vector_store = Qdrant(
                client=client,
                collection_name=settings.VECTOR_DB_COLLECTION,
                embeddings=embeddings
            )
            
            # Probar recuperación
            sample_query = "horarios del centro comercial"
            docs = _vector_store.similarity_search(sample_query, k=1)
            logger.info(f"Prueba de recuperación con consulta '{sample_query}' exitosa")
            
            return _vector_store
            
        # Si llegamos aquí, necesitamos crear/poblar la colección
        if collection_exists:
            logger.info("La colección existe pero está vacía. Cargando documentos...")
        else:
            logger.info("No se encontró la colección. Creando y cargando documentos...")
        
        # Cargar y dividir documentos
        chunks = await load_and_split_documents()
        if not chunks:
            logger.warning("No se encontraron fragmentos de documentos para cargar")
            return None
            
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