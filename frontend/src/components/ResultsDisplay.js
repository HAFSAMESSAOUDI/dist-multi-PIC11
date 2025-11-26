import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DownloadIcon from '@mui/icons-material/Download';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const ResultsDisplay = ({ results }) => {
  const [expanded, setExpanded] = useState('bilans');

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  const exportResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = 'simulation_results.json';

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  // Préparer les données pour les graphiques
  const compositionData = results.stages.map((stage, index) => {
    const dataPoint = { stage };
    results.compounds.forEach((compound, i) => {
      dataPoint[`${compound}_liquid`] = results.liquid_profiles[index][i];
      dataPoint[`${compound}_vapor`] = results.vapor_profiles[index][i];
    });
    return dataPoint;
  });

  const temperatureData = results.stages.map((stage, index) => ({
    stage,
    temperature: results.temperatures[index]
  }));

  const materialBalanceData = results.compounds.map((compound, index) => ({
    compound,
    feed: results.flow_feed * results.composition_feed[index],
    distillate: results.flow_distillate * results.composition_distillate[index],
    bottom: results.flow_bottom * results.composition_bottom[index]
  }));

  const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'];

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 600 }}>
          Résultats de la Simulation
        </Typography>
        <Button
          variant="outlined"
          startIcon={<DownloadIcon />}
          onClick={exportResults}
        >
          Exporter JSON
        </Button>
      </Box>

      {/* Résumé Global */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'primary.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">{results.N_real}</Typography>
              <Typography variant="body2">Plateaux réels</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'secondary.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">{results.R_operating.toFixed(2)}</Typography>
              <Typography variant="body2">Rapport de reflux</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'success.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">{results.feed_stage}</Typography>
              <Typography variant="body2">Plateau d'alimentation</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: 'warning.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">{(results.efficiency * 100).toFixed(0)}%</Typography>
              <Typography variant="body2">Efficacité</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Sections détaillées */}
      <Accordion expanded={expanded === 'bilans'} onChange={handleChange('bilans')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Bilans Matières</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                Débits
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Flux</TableCell>
                      <TableCell align="right">Débit (kmol/h)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>Alimentation</TableCell>
                      <TableCell align="right">{results.flow_feed.toFixed(2)}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Distillat</TableCell>
                      <TableCell align="right">{results.flow_distillate.toFixed(2)}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Résidu</TableCell>
                      <TableCell align="right">{results.flow_bottom.toFixed(2)}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                Compositions
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Composé</TableCell>
                      <TableCell align="right">Alim.</TableCell>
                      <TableCell align="right">Dist.</TableCell>
                      <TableCell align="right">Rés.</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.compounds.map((compound, index) => (
                      <TableRow key={compound}>
                        <TableCell>{compound}</TableCell>
                        <TableCell align="right">
                          {(results.composition_feed[index] * 100).toFixed(1)}%
                        </TableCell>
                        <TableCell align="right">
                          {(results.composition_distillate[index] * 100).toFixed(1)}%
                        </TableCell>
                        <TableCell align="right">
                          {(results.composition_bottom[index] * 100).toFixed(1)}%
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, mt: 2 }}>
                Graphique des débits
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={materialBalanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="compound" />
                  <YAxis label={{ value: 'Débit (kmol/h)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="feed" fill="#2196f3" name="Alimentation" />
                  <Bar dataKey="distillate" fill="#4caf50" name="Distillat" />
                  <Bar dataKey="bottom" fill="#f44336" name="Résidu" />
                </BarChart>
              </ResponsiveContainer>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'dimensionnement'} onChange={handleChange('dimensionnement')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Dimensionnement</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Méthode de Fenske
                  </Typography>
                  <Typography variant="h5" color="primary">
                    N_min = {results.N_min.toFixed(2)}
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    α_avg = {results.alpha_avg.toFixed(3)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Méthode d'Underwood
                  </Typography>
                  <Typography variant="h5" color="primary">
                    R_min = {results.R_min.toFixed(3)}
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    θ = {results.theta.toFixed(3)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Paramètre</TableCell>
                      <TableCell align="right">Valeur</TableCell>
                      <TableCell>Description</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>N_min</TableCell>
                      <TableCell align="right">{results.N_min.toFixed(2)}</TableCell>
                      <TableCell>Plateaux minimum (Fenske)</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>R_min</TableCell>
                      <TableCell align="right">{results.R_min.toFixed(3)}</TableCell>
                      <TableCell>Reflux minimum (Underwood)</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>R_opératoire</TableCell>
                      <TableCell align="right">{results.R_operating.toFixed(3)}</TableCell>
                      <TableCell>Reflux de fonctionnement</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>N_théorique</TableCell>
                      <TableCell align="right">{results.N_theoretical.toFixed(2)}</TableCell>
                      <TableCell>Plateaux théoriques (Gilliland)</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>N_réel</TableCell>
                      <TableCell align="right"><strong>{results.N_real}</strong></TableCell>
                      <TableCell>Plateaux réels</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Plateau alimentation</TableCell>
                      <TableCell align="right"><strong>{results.feed_stage}</strong></TableCell>
                      <TableCell>Position (Kirkbride)</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'profils'} onChange={handleChange('profils')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Profils de Composition</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                Phase Liquide
              </Typography>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={compositionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="stage"
                    label={{ value: 'Numéro de plateau', position: 'insideBottom', offset: -5 }}
                    reversed
                  />
                  <YAxis
                    label={{ value: 'Fraction molaire liquide', angle: -90, position: 'insideLeft' }}
                    domain={[0, 1]}
                  />
                  <Tooltip />
                  <Legend />
                  <ReferenceLine x={results.feed_stage} stroke="blue" strokeDasharray="3 3" label="Alimentation" />
                  {results.compounds.map((compound, index) => (
                    <Line
                      key={compound}
                      type="monotone"
                      dataKey={`${compound}_liquid`}
                      stroke={colors[index % colors.length]}
                      name={compound}
                      dot={{ r: 2 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600 }}>
                Phase Vapeur
              </Typography>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={compositionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="stage"
                    label={{ value: 'Numéro de plateau', position: 'insideBottom', offset: -5 }}
                    reversed
                  />
                  <YAxis
                    label={{ value: 'Fraction molaire vapeur', angle: -90, position: 'insideLeft' }}
                    domain={[0, 1]}
                  />
                  <Tooltip />
                  <Legend />
                  <ReferenceLine x={results.feed_stage} stroke="blue" strokeDasharray="3 3" label="Alimentation" />
                  {results.compounds.map((compound, index) => (
                    <Line
                      key={compound}
                      type="monotone"
                      dataKey={`${compound}_vapor`}
                      stroke={colors[index % colors.length]}
                      name={compound}
                      strokeDasharray="5 5"
                      dot={{ r: 2 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'temperature'} onChange={handleChange('temperature')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Profil de Température</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Température tête
                  </Typography>
                  <Typography variant="h5" color="primary">
                    {results.temperature_top.toFixed(1)} °C
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Température fond
                  </Typography>
                  <Typography variant="h5" color="error">
                    {results.temperature_bottom.toFixed(1)} °C
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <ResponsiveContainer width="100%" height={500}>
                <LineChart data={temperatureData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    type="number"
                    label={{ value: 'Température (°C)', position: 'insideBottom', offset: -5 }}
                  />
                  <YAxis
                    dataKey="stage"
                    type="number"
                    label={{ value: 'Numéro de plateau', angle: -90, position: 'insideLeft' }}
                    reversed
                  />
                  <Tooltip />
                  <ReferenceLine y={results.feed_stage} stroke="blue" strokeDasharray="3 3" label="Alimentation" />
                  <Line
                    type="monotone"
                    dataKey="temperature"
                    stroke="#ff5722"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    name="Température"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      <Accordion expanded={expanded === 'debits'} onChange={handleChange('debits')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Débits Internes</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <TableContainer component={Paper} variant="outlined">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Section</TableCell>
                  <TableCell>Paramètre</TableCell>
                  <TableCell align="right">Valeur (kmol/h)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell rowSpan={2}>Rectification</TableCell>
                  <TableCell>Liquide (L)</TableCell>
                  <TableCell align="right">{results.liquid_rectification.toFixed(2)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Vapeur (V)</TableCell>
                  <TableCell align="right">{results.vapor_rectification.toFixed(2)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell rowSpan={2}>Épuisement</TableCell>
                  <TableCell>Liquide (L')</TableCell>
                  <TableCell align="right">{results.liquid_stripping.toFixed(2)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Vapeur (V')</TableCell>
                  <TableCell align="right">{results.vapor_stripping.toFixed(2)}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default ResultsDisplay;
