from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Query(BaseModel):
    """Modelo para las consultas del usuario"""
    query: str

class ChatResponse(BaseModel):
    """Modelo para la respuesta de chat"""
    response: str

class DocumentInfo(BaseModel):
    """Información sobre un documento recuperado"""
    rank: int
    source: str
    page: str
    content_preview: str
    content_length: int

class DiagnosticResponse(BaseModel):
    """Modelo para la respuesta de diagnóstico"""
    query: str
    retrieved_documents: List[DocumentInfo]
    total_documents: int

class HealthResponse(BaseModel):
    """Modelo para la respuesta de verificación de salud"""
    status: str
    documents_loaded: bool