import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
    background: {
      default: '#0f0f23',
      paper: '#1a1a2e',
    },
  },
  typography: {
    fontFamily: '"Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif',
  },
});

function App() {
  const [compounds, setCompounds] = useState({});
  const [selectedCompounds, setSelectedCompounds] = useState(['benzene', 'toluene', 'o-xylene']);
  const [compositions, setCompositions] = useState({ benzene: 33.3, toluene: 33.3, 'o-xylene': 33.4 });
  const [feedRate, setFeedRate] = useState(100);
  const [pressure, setPressure] = useState(101325);
  const [lightKeyRecovery, setLightKeyRecovery] = useState(95);
  const [heavyKeyRecovery, setHeavyKeyRecovery] = useState(95);
  const [refluxMultiplier, setRefluxMultiplier] = useState(1.3);
  const [efficiency, setEfficiency] = useState(70);
  const [feedCondition, setFeedCondition] = useState('saturated_liquid');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Charger la bibliothèque de composés au démarrage
  useEffect(() => {
    const fetchCompounds = async () => {
      try {
        const response = await axios.get('/api/compounds');
        setCompounds(response.data);
      } catch (err) {
        console.error('Erreur lors du chargement des composés:', err);
        setError('Impossible de charger la bibliothèque de composés');
      }
    };
    fetchCompounds();
  }, []);

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);

    try {
      // Normaliser les compositions
      const compArray = selectedCompounds.map(comp => compositions[comp] || 0);
      const total = compArray.reduce((a, b) => a + b, 0);
      const normalizedComps = compArray.map(c => c / total);

      const requestData = {
        compounds: selectedCompounds,
        compositions: normalizedComps,
        feed_rate: feedRate,
        pressure: pressure,
        light_key_recovery: lightKeyRecovery / 100,
        heavy_key_recovery: heavyKeyRecovery / 100,
        feed_thermal_condition: feedCondition,
        reflux_ratio_multiplier: refluxMultiplier,
        efficiency: efficiency / 100
      };

      const response = await axios.post('/api/simulate', requestData);

      if (response.data.success) {
        setResults(response.data.results);
      } else {
        setError(response.data.error || 'Erreur lors de la simulation');
      }
    } catch (err) {
      console.error('Erreur de simulation:', err);
      setError(err.response?.data?.error || 'Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar
          compounds={compounds}
          selectedCompounds={selectedCompounds}
          setSelectedCompounds={setSelectedCompounds}
          compositions={compositions}
          setCompositions={setCompositions}
          feedRate={feedRate}
          setFeedRate={setFeedRate}
          pressure={pressure}
          setPressure={setPressure}
          lightKeyRecovery={lightKeyRecovery}
          setLightKeyRecovery={setLightKeyRecovery}
          heavyKeyRecovery={heavyKeyRecovery}
          setHeavyKeyRecovery={setHeavyKeyRecovery}
          refluxMultiplier={refluxMultiplier}
          setRefluxMultiplier={setRefluxMultiplier}
          efficiency={efficiency}
          setEfficiency={setEfficiency}
          feedCondition={feedCondition}
          setFeedCondition={setFeedCondition}
          onSimulate={handleSimulate}
          loading={loading}
        />
        <Dashboard
          results={results}
          loading={loading}
          error={error}
          selectedCompounds={selectedCompounds}
          compounds={compounds}
        />
      </Box>
    </ThemeProvider>
  );
}

export default App;
