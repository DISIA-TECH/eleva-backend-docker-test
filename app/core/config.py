import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    # Configuración de API
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "La Roca Village RAG API"
    
    # Configuración de OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    OPENAI_LLM_MODEL: str = "gpt-4o"
    
    # Configuración de la base de datos vectorial
    VECTOR_DB_LOCATION: str = ":memory:"  # Usar persistencia en producción
    VECTOR_DB_COLLECTION: str = "docs"

    VECTOR_DB_URL: str = os.getenv("QDRANT_URL", "")
    VECTOR_DB_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    
    # Configuración del procesamiento de documentos
    DOCUMENT_DIR: str = "./documents"
    DOCUMENT_GLOB: str = "**/*.pdf"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 250
    
    # Configuración CORS
    CORS_ORIGINS: list = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia singleton de configuración
settings = Settings()

# Validar configuración crítica
if not settings.OPENAI_API_KEY:
    raise ValueError("No se encontró la clave API de OpenAI en las variables de entorno")