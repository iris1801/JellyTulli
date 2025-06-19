# Dockerfile
# Usa un'immagine base Python 3.11 slim (o versione successiva)
FROM python:3.11-slim

# Imposta la working directory nel container
WORKDIR /app

# Installa le dipendenze necessarie (FastAPI, Uvicorn e Requests)
RUN pip install --no-cache-dir fastapi uvicorn requests

# Copia il codice dell'applicazione nella working directory
COPY . .

# Espone la porta 8000 per il servizio FastAPI
EXPOSE 8000

# Comando di avvio del server Uvicorn per eseguire l'app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
