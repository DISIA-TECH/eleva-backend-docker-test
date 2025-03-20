import logging
from typing import List
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.core.config import settings

logger = logging.getLogger("rag-app")

async def load_and_split_documents() -> List[Document]:
    """Carga documentos de un directorio y los divide en fragmentos"""
    try:
        # Cargar documentos desde el directorio
        logger.info(f"Cargando documentos desde el directorio {settings.DOCUMENT_DIR}")
        loader = DirectoryLoader(settings.DOCUMENT_DIR, glob=settings.DOCUMENT_GLOB)
        documents = loader.load()

        logger.info(f"Cargados {len(documents)} documentos")
        
        # Registrar información sobre documentos cargados
        for i, doc in enumerate(documents[:5]):  # Registrar solo los primeros 5 documentos
            logger.info(f"Documento #{i+1}: Fuente={doc.metadata.get('source', 'Desconocida')}, Tamaño={len(doc.page_content)} caracteres")
        
        if len(documents) > 5:
            logger.info(f"... y {len(documents) - 5} documentos más")
        
        # Dividir documentos en fragmentos
        logger.info("Dividiendo documentos en fragmentos")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)

        # Registrar información de fragmentos
        chunk_sizes = [len(chunk.page_content) for chunk in chunks]
        avg_size = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
        min_size = min(chunk_sizes) if chunk_sizes else 0
        max_size = max(chunk_sizes) if chunk_sizes else 0

        logger.info(f"Creados {len(chunks)} fragmentos con:")
        logger.info(f"  - Tamaño de fragmento: {settings.CHUNK_SIZE}, superposición: {settings.CHUNK_OVERLAP}")
        logger.info(f"  - Tamaño promedio: {avg_size:.2f} caracteres, mín: {min_size}, máx: {max_size}")
        
        return chunks
    
    except Exception as e:
        logger.error(f"Error cargando documentos: {e}", exc_info=True)
        raise