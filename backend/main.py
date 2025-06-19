from fastapi import FastAPI
import requests, threading, time

# Configurazione del server Jellyfin
JELLYFIN_URL = "http://10.0.0.100:8096"
API_KEY = "a0b5c4560e424a47bb97a8bf8df89d3e"

app = FastAPI()

# Variabile condivisa per memorizzare la lista corrente delle sessioni attive
active_sessions = []

def poll_jellyfin():
    """Funzione di polling che interroga Jellyfin ogni 15 secondi per aggiornare active_sessions."""
    while True:
        try:
            # Richiede le sessioni attive dal server Jellyfin tramite API
            response = requests.get(f"{JELLYFIN_URL}/Sessions", params={"api_key": API_KEY})
            sessions = response.json()  # Jellyfin restituisce la lista delle sessioni in JSON

            sessions_list = []
            for sess in sessions:
                user = sess.get("UserName", "")
                now_playing = sess.get("NowPlayingItem")
                if not now_playing:
                    # Salta sessioni che non stanno riproducendo contenuti
                    continue
                content = now_playing.get("Name", "")
                # Calcola il tempo di visione corrente (PositionTicks in hh:mm:ss)
                pos_ticks = sess.get("PlayState", {}).get("PositionTicks", 0)
                seconds = pos_ticks // 10000000  # conversione da tick (.NET, 100ns) a secondi
                h = seconds // 3600
                m = (seconds % 3600) // 60
                s = seconds % 60
                time_str = f"{h:02}:{m:02}:{s:02}"
                # Ottiene informazioni sul dispositivo e l'IP (senza porta)
                device = sess.get("DeviceName") or sess.get("Client") or ""
                ip = sess.get("RemoteEndPoint", "")
                if ip and ":" in ip:
                    ip = ip.split(":")[0]  # rimuove la porta dall'indirizzo IP
                # Aggiunge la sessione corrente alla lista di sessioni attive
                sessions_list.append({
                    "user": user,
                    "content": content,
                    "time": time_str,
                    "device": device,
                    "ip": ip
                })
            # Aggiorna la lista globale delle sessioni attive (in memoria)
            active_sessions[:] = sessions_list
        except Exception as e:
            print(f"Errore nel recupero delle sessioni Jellyfin: {e}")
        # Attende 15 secondi prima di effettuare una nuova richiesta
        time.sleep(15)

# Avvia il polling in un thread separato quando il server FastAPI viene avviato
@app.on_event("startup")
def startup_event():
    threading.Thread(target=poll_jellyfin, daemon=True).start()

@app.get("/sessions/active")
def get_active_sessions():
    """
    Endpoint per ottenere l'elenco corrente delle sessioni attive in formato JSON.
    """
    return active_sessions
