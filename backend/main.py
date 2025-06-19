import threading
import time
import requests
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Jellyfin URL fisso (il tuo server esterno)
JELLYFIN_URL = "http://10.0.0.100:8096"
API_KEY = "a0b5c4560e424a47bb97a8bf8df89d3e"

# Lista condivisa per contenere le sessioni attive
active_sessions = []

# FastAPI app + router
app = FastAPI()
router = APIRouter(prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funzione che esegue il polling delle sessioni Jellyfin ogni 15 secondi
def poll_jellyfin():
    global active_sessions
    while True:
        try:
            headers = {"X-Emby-Token": API_KEY}
            response = requests.get(f"{JELLYFIN_URL}/Sessions", headers=headers, timeout=10)
            response.raise_for_status()
            sessions = response.json()

            # Filtra e trasforma le sessioni attive
            active_sessions = []
            for session in sessions:
                state = session.get("PlayState", {})
                if state.get("IsPaused") is False and session.get("NowPlayingItem"):
                    active_sessions.append({
                        "user": session.get("UserName"),
                        "content": session["NowPlayingItem"].get("Name"),
                        "time": time.strftime('%H:%M:%S', time.gmtime(int(session.get("PlayState", {}).get("PositionTicks", 0)) // 10_000_000)),
                        "device": session.get("DeviceName") or session.get("Client"),
                        "ip": session.get("RemoteEndPoint", "").split(":")[0],
                    })

        except requests.exceptions.RequestException as e:
            print(f"Errore di connessione al server Jellyfin: {e}")
        except Exception as e:
            print(f"Errore generico durante il polling di Jellyfin: {e}")
        time.sleep(15)

# Endpoint API per recuperare le sessioni attive
@router.get("/sessions/active")
def get_active_sessions():
    return active_sessions

# Endpoint per healthcheck
@router.get("/healthz")
def healthz():
    return {"status": "ok"}

# Registrazione delle rotte e avvio del thread di polling
app.include_router(router)

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=poll_jellyfin, daemon=True)
    thread.start()
