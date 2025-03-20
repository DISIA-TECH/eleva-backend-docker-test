from fastapi import APIRouter, HTTPException, Depends
import logging

from app.api.models import Query, ChatResponse, DiagnosticResponse, HealthResponse
from app.services.rag_service import get_rag_answer, get_relevant_documents
from app.db.vector_store import get_vector_store

# Crear router
router = APIRouter()
logger = logging.getLogger("rag-app")

@router.post("/chat", response_model=ChatResponse)
async def chat(query: Query):
    """Endpoint para chatear con el sistema RAG"""
    vector_store = await get_vector_store()
    if not vector_store:
        raise HTTPException(status_code=500, detail="Almacén vectorial no inicializado")
    
    try:
        response = await get_rag_answer(query.query, vector_store)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error procesando chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error procesando solicitud: {str(e)}")

@router.post("/diagnose", response_model=DiagnosticResponse)
async def diagnose_query(query: Query):
    """Endpoint para diagnosticar una consulta mostrando los documentos recuperados"""
    vector_store = await get_vector_store()
    if not vector_store:
        raise HTTPException(status_code=500, detail="Almacén vectorial no inicializado")
    
    try:
        results = await get_relevant_documents(query.query, vector_store)
        return {
            "query": query.query,
            "retrieved_documents": results,
            "total_documents": len(results)
        }
    except Exception as e:
        logger.error(f"Error diagnosticando consulta: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error procesando solicitud: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint para verificar si el sistema está funcionando correctamente"""
    vector_store = await get_vector_store()
    return {
        "status": "healthy" if vector_store else "not_ready",
        "documents_loaded": bool(vector_store)
    }