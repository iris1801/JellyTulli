# Jellytulli

Jellytulli è uno strumento di monitoraggio per Jellyfin (simile a Tautulli) composto da un **backend** e un **frontend** containerizzati tramite Docker.

- **Backend**: Un'applicazione FastAPI Python con un endpoint di health check (`/healthz`) per verificare lo stato del servizio.
- **Frontend**: Un'applicazione React minima che effettua una richiesta all'endpoint `/api/healthz` del backend e mostra "Backend online" se il servizio risponde correttamente.

## Avvio del progetto con Docker Compose

Assicurati di aver installato Docker e Docker Compose sul tuo sistema. Per avviare i container del frontend e del backend, esegui il comando:

```bash
docker-compose up --build
