import React, { useEffect, useState } from 'react';

function App() {
  const [backendOnline, setBackendOnline] = useState(false);

  useEffect(() => {
    fetch('/api/healthz')
      .then(response => {
        if (response.ok) {
          setBackendOnline(true);
        }
      })
      .catch(error => {
        console.error('Errore chiamando /api/healthz:', error);
      });
  }, []);

  return (
    <div>
      {backendOnline ? 'Backend online' : 'Backend offline'}
    </div>
  );
}

export default App;
