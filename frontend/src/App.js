import React, { useState, useEffect } from 'react';
import {
  Container,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Box,
  ThemeProvider,
  createTheme,
  Paper,
  Grid,
  Tab,
  Tabs
} from '@mui/material';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ScienceIcon from '@mui/icons-material/Science';

import SimulationForm from './components/SimulationForm';
import ResultsDisplay from './components/ResultsDisplay';
import CompoundsList from './components/CompoundsList';
import api from './services/api';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [simulationResults, setSimulationResults] = useState(null);
  const [availableCompounds, setAvailableCompounds] = useState([]);

  useEffect(() => {
    checkBackendHealth();
    fetchAvailableCompounds();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await api.get('/health');
      toast.success('Connexion au backend établie', { autoClose: 2000 });
    } catch (error) {
      toast.error('Impossible de se connecter au backend. Assurez-vous que Flask est lancé.');
    }
  };

  const fetchAvailableCompounds = async () => {
    try {
      const response = await api.get('/compounds');
      setAvailableCompounds(response.data.compounds);
    } catch (error) {
      toast.error('Erreur lors du chargement des composés');
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleSimulation = async (simulationData) => {
    setLoading(true);
    try {
      const response = await api.post('/simulate', simulationData);

      if (response.data.success) {
        setSimulationResults(response.data.results);
        toast.success('Simulation terminée avec succès!');
        setTabValue(1); // Basculer vers l'onglet résultats
      } else {
        toast.error(`Erreur: ${response.data.error}`);
      }
    } catch (error) {
      console.error('Erreur simulation:', error);
      toast.error(`Erreur de simulation: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        {/* Header */}
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <ScienceIcon sx={{ mr: 2, fontSize: 40 }} />
            <Box>
              <Typography variant="h5" component="h1" sx={{ fontWeight: 700 }}>
                Simulateur de Distillation Multicomposants
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                Modélisation et Simulation des Procédés - Prof. BAKHER Zine Elabidine
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flex: 1 }}>
          <Paper elevation={3} sx={{ borderRadius: 2 }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              centered
              sx={{ borderBottom: 1, borderColor: 'divider' }}
            >
              <Tab label="Simulation" />
              <Tab label="Résultats" disabled={!simulationResults} />
              <Tab label="Composés disponibles" />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <SimulationForm
                onSubmit={handleSimulation}
                loading={loading}
                availableCompounds={availableCompounds}
              />
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              {simulationResults && (
                <ResultsDisplay results={simulationResults} />
              )}
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <CompoundsList compounds={availableCompounds} />
            </TabPanel>
          </Paper>
        </Container>

        {/* Footer */}
        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
            backgroundColor: 'primary.main',
            color: 'white',
            textAlign: 'center',
          }}
        >
          <Typography variant="body2">
            © 2024 - Université - Cours de Modélisation et Simulation des Procédés
          </Typography>
        </Box>
      </Box>

      <ToastContainer position="bottom-right" />
    </ThemeProvider>
  );
}

export default App;
