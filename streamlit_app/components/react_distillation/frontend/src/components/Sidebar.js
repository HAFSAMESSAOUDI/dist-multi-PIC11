import React from 'react';
import {
  Box,
  Drawer,
  Typography,
  Select,
  MenuItem,
  Slider,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Chip,
  OutlinedInput,
  Divider,
  Paper,
  CircularProgress,
} from '@mui/material';
import {
  Science as ScienceIcon,
  PlayArrow as PlayIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const SIDEBAR_WIDTH = 360;

const Sidebar = ({
  compounds,
  selectedCompounds,
  setSelectedCompounds,
  compositions,
  setCompositions,
  feedRate,
  setFeedRate,
  pressure,
  setPressure,
  lightKeyRecovery,
  setLightKeyRecovery,
  heavyKeyRecovery,
  setHeavyKeyRecovery,
  refluxMultiplier,
  setRefluxMultiplier,
  efficiency,
  setEfficiency,
  feedCondition,
  setFeedCondition,
  onSimulate,
  loading
}) => {
  const handleCompoundChange = (event) => {
    const value = event.target.value;
    setSelectedCompounds(value);

    // Initialiser les compositions pour les nouveaux composés
    const newComps = { ...compositions };
    value.forEach(comp => {
      if (!(comp in newComps)) {
        newComps[comp] = 33.3;
      }
    });
    setCompositions(newComps);
  };

  const handleCompositionChange = (compound, value) => {
    setCompositions({
      ...compositions,
      [compound]: parseFloat(value) || 0
    });
  };

  const normalizeCompositions = () => {
    const total = selectedCompounds.reduce((sum, comp) => sum + (compositions[comp] || 0), 0);
    if (total > 0) {
      const normalized = {};
      selectedCompounds.forEach(comp => {
        normalized[comp] = ((compositions[comp] || 0) / total * 100).toFixed(2);
      });
      setCompositions(normalized);
    }
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: SIDEBAR_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: SIDEBAR_WIDTH,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #1a1a2e 0%, #16213e 100%)',
          borderRight: '2px solid rgba(102, 126, 234, 0.3)',
          overflowY: 'auto',
        },
      }}
    >
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <ScienceIcon sx={{ fontSize: 48, color: '#667eea', mb: 1 }} />
          <Typography variant="h5" sx={{ fontWeight: 700, color: '#fff', mb: 0.5 }}>
            Distillation
          </Typography>
          <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
            Multicomposants
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block', mt: 1 }}>
            Prof. BAKHER Zine Elabidine
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
            PIC - UH1
          </Typography>
        </Box>

        <Divider sx={{ mb: 3, borderColor: 'rgba(102, 126, 234, 0.2)' }} />

        {/* Sélection des composés */}
        <Paper sx={{ p: 2, mb: 2, bgcolor: 'rgba(255,255,255,0.05)' }}>
          <Typography variant="subtitle2" sx={{ mb: 1, color: '#667eea', fontWeight: 600 }}>
            <SettingsIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
            Composés
          </Typography>
          <FormControl fullWidth size="small">
            <InputLabel>Sélectionner les composés</InputLabel>
            <Select
              multiple
              value={selectedCompounds}
              onChange={handleCompoundChange}
              input={<OutlinedInput label="Sélectionner les composés" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip
                      key={value}
                      label={compounds[value]?.name || value}
                      size="small"
                      sx={{
                        bgcolor: '#667eea',
                        color: '#fff',
                        fontWeight: 500
                      }}
                    />
                  ))}
                </Box>
              )}
            >
              {Object.keys(compounds).map((key) => (
                <MenuItem key={key} value={key}>
                  {compounds[key].name} ({compounds[key].formula})
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Paper>

        {/* Compositions */}
        {selectedCompounds.length > 0 && (
          <Paper sx={{ p: 2, mb: 2, bgcolor: 'rgba(255,255,255,0.05)' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography variant="subtitle2" sx={{ color: '#667eea', fontWeight: 600 }}>
                Compositions (%)
              </Typography>
              <Button
                size="small"
                onClick={normalizeCompositions}
                sx={{ textTransform: 'none', fontSize: 11 }}
              >
                Normaliser
              </Button>
            </Box>
            {selectedCompounds.map(comp => (
              <TextField
                key={comp}
                fullWidth
                size="small"
                type="number"
                label={compounds[comp]?.name}
                value={compositions[comp] || 0}
                onChange={(e) => handleCompositionChange(comp, e.target.value)}
                sx={{ mb: 1 }}
                InputProps={{
                  endAdornment: '%'
                }}
              />
            ))}
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
              Total: {selectedCompounds.reduce((sum, comp) => sum + (parseFloat(compositions[comp]) || 0), 0).toFixed(1)}%
            </Typography>
          </Paper>
        )}

        {/* Paramètres opératoires */}
        <Paper sx={{ p: 2, mb: 2, bgcolor: 'rgba(255,255,255,0.05)' }}>
          <Typography variant="subtitle2" sx={{ mb: 2, color: '#667eea', fontWeight: 600 }}>
            Paramètres Opératoires
          </Typography>

          <TextField
            fullWidth
            size="small"
            type="number"
            label="Débit d'alimentation"
            value={feedRate}
            onChange={(e) => setFeedRate(parseFloat(e.target.value))}
            sx={{ mb: 2 }}
            InputProps={{
              endAdornment: 'kmol/h'
            }}
          />

          <TextField
            fullWidth
            size="small"
            type="number"
            label="Pression"
            value={pressure}
            onChange={(e) => setPressure(parseFloat(e.target.value))}
            sx={{ mb: 2 }}
            InputProps={{
              endAdornment: 'Pa'
            }}
          />

          <FormControl fullWidth size="small" sx={{ mb: 2 }}>
            <InputLabel>Condition d'alimentation</InputLabel>
            <Select
              value={feedCondition}
              onChange={(e) => setFeedCondition(e.target.value)}
              label="Condition d'alimentation"
            >
              <MenuItem value="saturated_liquid">Liquide saturé (q=1)</MenuItem>
              <MenuItem value="saturated_vapor">Vapeur saturée (q=0)</MenuItem>
              <MenuItem value="subcooled_liquid">Liquide sous-refroidi (q&gt;1)</MenuItem>
              <MenuItem value="superheated_vapor">Vapeur surchauffée (q&lt;0)</MenuItem>
              <MenuItem value="two_phase">Mélange biphasique (0&lt;q&lt;1)</MenuItem>
            </Select>
          </FormControl>
        </Paper>

        {/* Spécifications de séparation */}
        <Paper sx={{ p: 2, mb: 2, bgcolor: 'rgba(255,255,255,0.05)' }}>
          <Typography variant="subtitle2" sx={{ mb: 2, color: '#667eea', fontWeight: 600 }}>
            Spécifications de Séparation
          </Typography>

          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              Récupération composé léger: {lightKeyRecovery}%
            </Typography>
            <Slider
              value={lightKeyRecovery}
              onChange={(e, val) => setLightKeyRecovery(val)}
              min={80}
              max={99.9}
              step={0.1}
              valueLabelDisplay="auto"
              sx={{
                color: '#667eea',
                '& .MuiSlider-thumb': {
                  bgcolor: '#667eea'
                }
              }}
            />
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              Récupération composé lourd: {heavyKeyRecovery}%
            </Typography>
            <Slider
              value={heavyKeyRecovery}
              onChange={(e, val) => setHeavyKeyRecovery(val)}
              min={80}
              max={99.9}
              step={0.1}
              valueLabelDisplay="auto"
              sx={{
                color: '#764ba2',
                '& .MuiSlider-thumb': {
                  bgcolor: '#764ba2'
                }
              }}
            />
          </Box>

          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              Multiplicateur de reflux: {refluxMultiplier.toFixed(2)}
            </Typography>
            <Slider
              value={refluxMultiplier}
              onChange={(e, val) => setRefluxMultiplier(val)}
              min={1.1}
              max={3.0}
              step={0.1}
              valueLabelDisplay="auto"
              sx={{
                color: '#667eea',
                '& .MuiSlider-thumb': {
                  bgcolor: '#667eea'
                }
              }}
            />
          </Box>

          <Box>
            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
              Efficacité des plateaux: {efficiency}%
            </Typography>
            <Slider
              value={efficiency}
              onChange={(e, val) => setEfficiency(val)}
              min={50}
              max={95}
              step={1}
              valueLabelDisplay="auto"
              sx={{
                color: '#764ba2',
                '& .MuiSlider-thumb': {
                  bgcolor: '#764ba2'
                }
              }}
            />
          </Box>
        </Paper>

        {/* Bouton de simulation */}
        <Button
          fullWidth
          variant="contained"
          size="large"
          onClick={onSimulate}
          disabled={loading || selectedCompounds.length < 2}
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <PlayIcon />}
          sx={{
            py: 1.5,
            background: loading
              ? 'rgba(255,255,255,0.1)'
              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
            },
            fontWeight: 600,
            fontSize: 16,
            boxShadow: '0 4px 20px rgba(102, 126, 234, 0.4)',
          }}
        >
          {loading ? 'Simulation en cours...' : 'LANCER LA SIMULATION'}
        </Button>

        {selectedCompounds.length < 2 && (
          <Typography
            variant="caption"
            sx={{ display: 'block', textAlign: 'center', mt: 1, color: 'rgba(255,100,100,0.8)' }}
          >
            ⚠️ Sélectionnez au moins 2 composés
          </Typography>
        )}
      </Box>
    </Drawer>
  );
};

export default Sidebar;
