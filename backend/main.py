# main.py
# Importa le librerie necessarie
from fastapi import FastAPI, APIRouter
import requests
import threading
import time
import os

# Configurazione: URL del server Jellyfin e chiave API (le variabili d'ambiente possono sovrascrivere i valori di default)
JELLYFIN_URL = os.environ.get("JELLYFIN_URL", "http://jellyfin:8096")  # URL base del server Jellyfin (default per Docker network)
JELLYFIN_API_KEY = os.environ.get("JELLYFIN_API_KEY")  # Chiave API Jellyfin (se necessaria per l'autenticazione)

# Variabile globale per memorizzare le sessioni attive correnti (con contenuti in riproduzione)
active_sessions = []

def poll_jellyfin():
    """
    Funzione di polling per recuperare periodicamente le sessioni attive dal server Jellyfin.
    Esegue richieste HTTP GET all'endpoint /Sessions del server Jellyfin ogni 15 secondi,
    filtra le sessioni con contenuto attualmente in riproduzione e aggiorna la variabile globale active_sessions.
    """
    global active_sessions
    # Prepara gli header per l'autenticazione (usa la chiave API se fornita)
    headers = {}
    if JELLYFIN_API_KEY:
        headers["X-Emby-Token"] = JELLYFIN_API_KEY  # Header di autenticazione per Jellyfin

    # Loop infinito per il polling periodico
    while True:
        try:
            # Esegue la richiesta GET al server Jellyfin per ottenere le sessioni correnti
            response = requests.get(f"{JELLYFIN_URL}/Sessions", headers=headers)
            if response.status_code == 200:
                sessions = response.json()  # Ottiene la lista delle sessioni in formato JSON
                # Filtra solo le sessioni che hanno un contenuto in riproduzione (NowPlayingItem presente e non in pausa)
                active = []
                for session in sessions:
                    # Verifica se c'è un elemento in riproduzione nella sessione
                    now_playing = session.get("NowPlayingItem")
                    if now_playing:
                        # Verifica lo stato di riproduzione: aggiunge la sessione solo se non è in pausa
                        play_state = session.get("PlayState", {})
                        if not play_state.get("IsPaused", False):
                            active.append(session)
                # Aggiorna la variabile globale con la lista filtrata di sessioni attive
                active_sessions = active
        except Exception as e:
            # In caso di errore nella richiesta o nel parsing, stampa l'errore e prosegue
            print(f"Errore nel polling di Jellyfin: {e}")
        # Attende 15 secondi prima di effettuare la prossima richiesta
        time.sleep(15)

# Crea l'app FastAPI e il router con prefisso /api
app = FastAPI()
router = APIRouter(prefix="/api")

@router.get("/sessions/active")
def get_active_sessions():
    """
    Endpoint GET /api/sessions/active
    Restituisce le sessioni attive attualmente memorizzate (solo quelle con contenuti in riproduzione).
    Il formato della risposta è un dizionario con chiave "active_sessions" contenente la lista delle sessioni attive.
    """
    return {"active_sessions": active_sessions}

# Registra il router nell'app FastAPI
app.include_router(router)

# All'avvio dell'applicazione, avvia il thread di polling per aggiornare le sessioni attive
@app.on_event("startup")
def start_polling_thread():
    # Crea e avvia un thread daemon che esegue la funzione poll_jellyfin in background
    polling_thread = threading.Thread(target=poll_jellyfin, daemon=True)
    polling_thread.start()
