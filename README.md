# Chatbot Docker Test Backend

## Descripción

Este proyecto es un backend para un chatbot utilizando FastAPI. La aplicación se puede desplegar fácilmente utilizando Docker.

## Requisitos

- Docker
- Docker Compose (opcional, si decides extender el proyecto)

## Instrucciones para Ejecutar

### 1. Clona el Repositorio

Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tuusuario/nombre-del-repositorio.git
cd nombre-del-repositorio/chatbot-docker-test-backend
```

### 2. Crea el Archivo `.env`

Debido a que el archivo `.env` está ignorado por Git y Docker, deberás crear uno manualmente en el directorio raíz del proyecto. Este archivo debe contener las siguientes variables de entorno:

```bash
touch .env
```

Luego, edita el archivo `.env` con el siguiente contenido:

```env
OPENAI_API_KEY=tu_clave_api_openai
QDRANT_URL=tu_url_qdrant
QDRANT_API_KEY=tu_clave_api_qdrant
```

### 3. Construye la Imagen Docker

Construye la imagen Docker usando el `Dockerfile` incluido en el proyecto:

```bash
docker build -t nombre-de-la-imagen .
```

### 4. Ejecuta el Contenedor Docker

Ejecuta el contenedor utilizando el archivo `.env` que creaste:

```bash
docker run -d -p 8000:8000 --name nombre-del-contenedor --env-file .env nombre-de-la-imagen
```

### 5. Accede a la Aplicación

Una vez que el contenedor esté en ejecución, puedes acceder a la aplicación en tu navegador web:

- URL: [http://localhost:8000](http://localhost:8000)

También puedes acceder a la documentación de la API generada por FastAPI en:

- Documentación interactiva con Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentación alternativa con ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Notas

- Asegúrate de que Docker esté instalado y en funcionamiento en tu máquina.
- Si necesitas configurar variables de entorno adicionales, puedes agregarlas al archivo `.env`.

## Comandos Útiles

### Verificar el Estado del Contenedor

```bash
docker ps
```

### Ver Logs del Contenedor

```bash
docker logs nombre-del-contenedor
```

### Detener el Contenedor

```bash
docker stop nombre-del-contenedor
```

### Eliminar el Contenedor

```bash
docker rm nombre-del-contenedor
```

Con estos pasos, deberías poder clonar, construir y ejecutar esta aplicación backend utilizando Docker sin problemas.
