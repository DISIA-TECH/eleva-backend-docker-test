import logging
import sys
import nltk
import pathlib

def setup_logging():
    """Configura el logging para la aplicación"""
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger("rag-app")
    
    # Descargar recursos NLTK si no existen
    nltk_data_path = nltk.data.path[0]
    resources = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger_eng',
        'averaged_perceptron_tagger',
        'stopwords',
        'wordnet',
        'omw-1.4'
    ]

    for resource in resources:
        resource_path = pathlib.Path(nltk_data_path) / resource
        if not resource_path.exists():
            logger.info(f"Descargando recurso NLTK: {resource}")
            nltk.download(resource)
        else:
            logger.info(f"El recurso NLTK ya existe: {resource}")
    
    return logger