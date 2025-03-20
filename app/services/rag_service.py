import logging
import re
from typing import List, Dict, Any
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Qdrant

from app.core.config import settings
from app.services.prompt_service import get_rag_prompt

logger = logging.getLogger("rag-app")

def clean_response(text: str) -> str:
    """Limpia la respuesta y asegura formato correcto para viñetas"""
    # Primero, normaliza todos los saltos de línea
    text = text.replace('\r\n', '\n')
    
    # Asegura que cada viñeta tenga un salto de línea completo antes y después
    text = re.sub(r'([^\n])(\s*•\s)', r'\1\n\n\2', text)  # Añade salto antes de viñeta
    text = re.sub(r'(•[^•\n]*?)(\s*?)(?=\s*•|\s*$)', r'\1\n', text)  # Añade salto después
    
    # Elimina saltos de línea excesivos (más de 2 seguidos)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

async def get_rag_answer(query: str, vector_store: Qdrant) -> str:
    """Obtiene una respuesta usando RAG (Retrieval-Augmented Generation)"""
    try:
        # Crear plantilla personalizada
        prompt = get_rag_prompt()
        
        # Crear LLM
        llm = ChatOpenAI(
            model_name=settings.OPENAI_LLM_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Crear cadena de recuperación con prompt personalizado
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 8}),
            chain_type_kwargs={"prompt": prompt}
        )
        
        # Obtener respuesta
        response = qa_chain.run(query)
        
        # Limpiar y formatear la respuesta
        cleaned_response = clean_response(response)
        
        return cleaned_response
    
    except Exception as e:
        logger.error(f"Error obteniendo respuesta RAG: {e}", exc_info=True)
        raise

async def get_relevant_documents(query: str, vector_store: Qdrant) -> List[Dict[str, Any]]:
    """Obtiene documentos relevantes para una consulta (para diagnóstico)"""
    try:
        # Recuperar documentos relevantes
        docs = vector_store.similarity_search(query, k=3)
        
        # Preparar respuesta de diagnóstico
        results = []
        for i, doc in enumerate(docs):
            results.append({
                "rank": i+1,
                "source": doc.metadata.get("source", "Desconocida"),
                "page": doc.metadata.get("page", "N/A"),
                "content_preview": doc.page_content[:200] + "...",
                "content_length": len(doc.page_content)
            })
        
        return results
    
    except Exception as e:
        logger.error(f"Error obteniendo documentos relevantes: {e}", exc_info=True)
        raise