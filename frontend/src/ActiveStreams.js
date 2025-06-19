import React, { useState, useEffect } from 'react';

function ActiveStreams() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    // Funzione per recuperare l'elenco degli stream attivi dal backend
    const fetchSessions = async () => {
      try {
        const res = await fetch('/api/sessions/active');
        if (!res.ok) {
          throw new Error('Risposta non valida dal server');
        }
        const data = await res.json();
        setSessions(data);
      } catch (err) {
        console.error('Errore nel caricamento delle sessioni attive:', err);
      }
    };

    // Chiamata iniziale e intervallo di polling ogni 15 secondi
    fetchSessions();
    const intervalId = setInterval(fetchSessions, 15000);
    return () => clearInterval(intervalId);  // pulizia intervallo al momento dell'unmount
  }, []);

  return (
    <div>
      <h2>Stream Attivi</h2>
      <table border="1" cellPadding="6" cellSpacing="0">
        <thead>
          <tr>
            <th>Utente</th>
            <th>Contenuto</th>
            <th>Tempo di visione</th>
            <th>Device</th>
            <th>IP</th>
          </tr>
        </thead>
        <tbody>
          {sessions.length === 0 ? (
            /* Mostra una riga di messaggio se non ci sono stream attivi */
            <tr>
              <td colSpan="5">Nessuno streaming attivo</td>
            </tr>
          ) : (
            /* Mostra ogni sessione attiva in una riga della tabella */
            sessions.map((sess, index) => (
              <tr key={index}>
                <td>{sess.user}</td>
                <td>{sess.content}</td>
                <td>{sess.time}</td>
                <td>{sess.device}</td>
                <td>{sess.ip}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ActiveStreams;
