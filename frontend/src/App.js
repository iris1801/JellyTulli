import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ActiveStreams from './ActiveStreams';

function App() {
  const [backendStatus, setBackendStatus] = useState('...');

  // Effettua una richiesta all'endpoint di health check del backend all'avvio
  useEffect(() => {
    fetch('/api/healthz')
      .then(res => {
        if (res.ok) {
          setBackendStatus('Backend online');
        } else {
          setBackendStatus('Backend offline');
        }
      })
      .catch(err => {
        console.error('Errore nel verificare il backend:', err);
        setBackendStatus('Backend offline');
      });
  }, []);

  return (
    <Router>
      {/* Navigazione tra Home e Stream Attivi */}
      <nav style={{ marginBottom: '1rem' }}>
        <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
        <Link to="/streams">Stream Attivi</Link>
      </nav>

      <Routes>
        {/* Home: mostra lo stato del backend */}
        <Route path="/" element={
          <div>
            <h1>Jellytulli</h1>
            <p>{backendStatus}</p>
          </div>
        } />
        {/* Pagina "Stream Attivi" */}
        <Route path="/streams" element={<ActiveStreams />} />
      </Routes>
    </Router>
  );
}

export default App;
