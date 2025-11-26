import React, { useState } from 'react';
import {
  Box,
  Grid,
  TextField,
  Button,
  Typography,
  Card,
  CardContent,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  IconButton,
  Tooltip,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

const SimulationForm = ({ onSubmit, loading, availableCompounds }) => {
  const [formData, setFormData] = useState({
    compounds: ['benzene', 'toluene', 'o-xylene'],
    compositions: [0.33, 0.33, 0.34],
    flow_rate: 100.0,
    pressure: 101325,
    recovery_lk: 0.95,
    recovery_hk: 0.95,
    reflux_factor: 1.3,
    feed_quality: 1.0,
    efficiency: 0.70
  });

  const [errors, setErrors] = useState({});

  const handleCompoundChange = (index, value) => {
    const newCompounds = [...formData.compounds];
    newCompounds[index] = value;
    setFormData({ ...formData, compounds: newCompounds });
  };

  const handleCompositionChange = (index, value) => {
    const newCompositions = [...formData.compositions];
    newCompositions[index] = parseFloat(value) || 0;
    setFormData({ ...formData, compositions: newCompositions });
  };

  const addCompound = () => {
    if (formData.compounds.length < 10) {
      setFormData({
        ...formData,
        compounds: [...formData.compounds, 'benzene'],
        compositions: [...formData.compositions, 0.0]
      });
    }
  };

  const removeCompound = (index) => {
    if (formData.compounds.length > 2) {
      const newCompounds = formData.compounds.filter((_, i) => i !== index);
      const newCompositions = formData.compositions.filter((_, i) => i !== index);
      setFormData({
        ...formData,
        compounds: newCompounds,
        compositions: newCompositions
      });
    }
  };

  const normalizeCompositions = () => {
    const sum = formData.compositions.reduce((a, b) => a + b, 0);
    if (sum > 0 && Math.abs(sum - 1.0) > 0.01) {
      const normalized = formData.compositions.map(c => c / sum);
      setFormData({ ...formData, compositions: normalized });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Vérifier la somme des compositions
    const sum = formData.compositions.reduce((a, b) => a + b, 0);
    if (Math.abs(sum - 1.0) > 0.01) {
      newErrors.compositions = `La somme des compositions doit être 1.0 (actuellement ${sum.toFixed(3)})`;
    }

    // Vérifier les valeurs négatives
    if (formData.compositions.some(c => c < 0)) {
      newErrors.compositions = 'Les compositions ne peuvent pas être négatives';
    }

    if (formData.flow_rate <= 0) {
      newErrors.flow_rate = 'Le débit doit être positif';
    }

    if (formData.pressure <= 0) {
      newErrors.pressure = 'La pression doit être positive';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleReset = () => {
    setFormData({
      compounds: ['benzene', 'toluene', 'o-xylene'],
      compositions: [0.33, 0.33, 0.34],
      flow_rate: 100.0,
      pressure: 101325,
      recovery_lk: 0.95,
      recovery_hk: 0.95,
      reflux_factor: 1.3,
      feed_quality: 1.0,
      efficiency: 0.70
    });
    setErrors({});
  };

  const compositionSum = formData.compositions.reduce((a, b) => a + b, 0);

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Configuration de la Simulation
      </Typography>

      {/* Composés et Compositions */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" color="primary">
              Composés et Compositions
            </Typography>
            <Tooltip title="Ajouter un composé">
              <IconButton
                color="primary"
                onClick={addCompound}
                disabled={formData.compounds.length >= 10}
              >
                <AddIcon />
              </IconButton>
            </Tooltip>
          </Box>

          {formData.compounds.map((compound, index) => (
            <Grid container spacing={2} key={index} sx={{ mb: 2, alignItems: 'center' }}>
              <Grid item xs={12} sm={5}>
                <FormControl fullWidth size="small">
                  <InputLabel>Composé {index + 1}</InputLabel>
                  <Select
                    value={compound}
                    label={`Composé ${index + 1}`}
                    onChange={(e) => handleCompoundChange(index, e.target.value)}
                  >
                    {availableCompounds.map((c) => (
                      <MenuItem key={c.id} value={c.id}>
                        {c.name} ({c.formula})
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={10} sm={6}>
                <TextField
                  fullWidth
                  size="small"
                  type="number"
                  label="Fraction molaire"
                  value={formData.compositions[index]}
                  onChange={(e) => handleCompositionChange(index, e.target.value)}
                  inputProps={{ min: 0, max: 1, step: 0.01 }}
                />
              </Grid>
              <Grid item xs={2} sm={1}>
                <Tooltip title="Supprimer">
                  <span>
                    <IconButton
                      color="error"
                      onClick={() => removeCompound(index)}
                      disabled={formData.compounds.length <= 2}
                      size="small"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </span>
                </Tooltip>
              </Grid>
            </Grid>
          ))}

          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Chip
              label={`Somme: ${compositionSum.toFixed(3)}`}
              color={Math.abs(compositionSum - 1.0) < 0.01 ? 'success' : 'warning'}
              size="small"
            />
            <Button
              variant="outlined"
              size="small"
              onClick={normalizeCompositions}
              disabled={compositionSum === 0}
            >
              Normaliser
            </Button>
          </Box>

          {errors.compositions && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {errors.compositions}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Conditions Opératoires */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" color="primary" gutterBottom>
            Conditions Opératoires
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Débit d'alimentation (kmol/h)"
                type="number"
                value={formData.flow_rate}
                onChange={(e) => setFormData({ ...formData, flow_rate: parseFloat(e.target.value) })}
                error={!!errors.flow_rate}
                helperText={errors.flow_rate}
                inputProps={{ min: 0, step: 1 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Pression (Pa)"
                type="number"
                value={formData.pressure}
                onChange={(e) => setFormData({ ...formData, pressure: parseFloat(e.target.value) })}
                error={!!errors.pressure}
                helperText={errors.pressure || `${(formData.pressure / 1000).toFixed(1)} kPa`}
                inputProps={{ min: 0, step: 1000 }}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Spécifications de Séparation */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" color="primary" gutterBottom>
            Spécifications de Séparation
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography gutterBottom>
                Récupération du clé léger dans le distillat: {(formData.recovery_lk * 100).toFixed(0)}%
              </Typography>
              <Slider
                value={formData.recovery_lk}
                onChange={(e, newValue) => setFormData({ ...formData, recovery_lk: newValue })}
                min={0.5}
                max={0.999}
                step={0.01}
                marks={[
                  { value: 0.5, label: '50%' },
                  { value: 0.95, label: '95%' },
                  { value: 0.999, label: '99.9%' }
                ]}
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => `${(value * 100).toFixed(1)}%`}
              />
            </Grid>

            <Grid item xs={12}>
              <Typography gutterBottom>
                Récupération du clé lourd dans le résidu: {(formData.recovery_hk * 100).toFixed(0)}%
              </Typography>
              <Slider
                value={formData.recovery_hk}
                onChange={(e, newValue) => setFormData({ ...formData, recovery_hk: newValue })}
                min={0.5}
                max={0.999}
                step={0.01}
                marks={[
                  { value: 0.5, label: '50%' },
                  { value: 0.95, label: '95%' },
                  { value: 0.999, label: '99.9%' }
                ]}
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => `${(value * 100).toFixed(1)}%`}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Paramètres de Conception */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" color="primary" gutterBottom>
            Paramètres de Conception
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography gutterBottom>
                Facteur de reflux: {formData.reflux_factor.toFixed(2)} × R_min
              </Typography>
              <Slider
                value={formData.reflux_factor}
                onChange={(e, newValue) => setFormData({ ...formData, reflux_factor: newValue })}
                min={1.05}
                max={3.0}
                step={0.05}
                marks={[
                  { value: 1.05, label: '1.05' },
                  { value: 1.3, label: '1.3' },
                  { value: 2.0, label: '2.0' },
                  { value: 3.0, label: '3.0' }
                ]}
                valueLabelDisplay="auto"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography gutterBottom>
                Efficacité des plateaux: {(formData.efficiency * 100).toFixed(0)}%
              </Typography>
              <Slider
                value={formData.efficiency}
                onChange={(e, newValue) => setFormData({ ...formData, efficiency: newValue })}
                min={0.4}
                max={1.0}
                step={0.05}
                marks={[
                  { value: 0.4, label: '40%' },
                  { value: 0.7, label: '70%' },
                  { value: 1.0, label: '100%' }
                ]}
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => `${(value * 100).toFixed(0)}%`}
              />
            </Grid>

            <Grid item xs={12}>
              <Typography gutterBottom>
                Qualité de l'alimentation (q): {formData.feed_quality.toFixed(2)}
              </Typography>
              <Slider
                value={formData.feed_quality}
                onChange={(e, newValue) => setFormData({ ...formData, feed_quality: newValue })}
                min={0.0}
                max={1.0}
                step={0.1}
                marks={[
                  { value: 0.0, label: 'Vapeur saturée' },
                  { value: 0.5, label: 'Mélange' },
                  { value: 1.0, label: 'Liquide saturé' }
                ]}
                valueLabelDisplay="auto"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Boutons d'action */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
        <Button
          variant="outlined"
          startIcon={<RestartAltIcon />}
          onClick={handleReset}
          disabled={loading}
        >
          Réinitialiser
        </Button>
        <Button
          type="submit"
          variant="contained"
          size="large"
          startIcon={loading ? <CircularProgress size={20} /> : <PlayArrowIcon />}
          disabled={loading}
          sx={{ minWidth: 200 }}
        >
          {loading ? 'Simulation en cours...' : 'Lancer la Simulation'}
        </Button>
      </Box>
    </Box>
  );
};

export default SimulationForm;
