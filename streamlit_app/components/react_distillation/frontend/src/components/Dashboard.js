import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Thermostat as ThermostatIcon,
  Speed as SpeedIcon,
  Layers as LayersIcon,
  Science as ScienceIcon,
} from '@mui/icons-material';
import Plot from 'react-plotly.js';

const SIDEBAR_WIDTH = 360;

const Dashboard = ({ results, loading, error, selectedCompounds, compounds }) => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Carte KPI
  const KPICard = ({ title, value, unit, icon: Icon, color }) => (
    <Card
      sx={{
        background: `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`,
        border: `1px solid ${color}40`,
        borderRadius: 2,
        height: '100%',
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Icon sx={{ color, mr: 1, fontSize: 24 }} />
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)', fontWeight: 500 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" sx={{ color: '#fff', fontWeight: 700 }}>
          {value}
        </Typography>
        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
          {unit}
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        ml: `${SIDEBAR_WIDTH}px`,
        p: 3,
        bgcolor: '#0f0f23',
        minHeight: '100vh',
      }}
    >
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ color: '#fff', fontWeight: 700, mb: 0.5 }}>
          Tableau de Bord
        </Typography>
        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.5)' }}>
          Résultats de simulation de distillation multicomposants
        </Typography>
      </Box>

      {/* Loading State */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} sx={{ color: '#667eea', mb: 2 }} />
            <Typography variant="h6" sx={{ color: '#fff' }}>
              Simulation en cours...
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.5)', mt: 1 }}>
              Calcul des méthodes de Fenske, Underwood, Gilliland et Kirkbride
            </Typography>
          </Box>
        </Box>
      )}

      {/* Error State */}
      {error && !loading && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Results */}
      {results && !loading && (
        <>
          {/* KPIs */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={2.4}>
              <KPICard
                title="N min (Fenske)"
                value={results.shortcut_methods.fenske.N_min.toFixed(2)}
                unit="plateaux"
                icon={LayersIcon}
                color="#667eea"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <KPICard
                title="N réel"
                value={results.shortcut_methods.gilliland.N_real}
                unit="plateaux"
                icon={LayersIcon}
                color="#764ba2"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <KPICard
                title="R min"
                value={results.shortcut_methods.underwood.R_min.toFixed(2)}
                unit="-"
                icon={TrendingUpIcon}
                color="#f093fb"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <KPICard
                title="R opératoire"
                value={results.shortcut_methods.gilliland.R_operating.toFixed(2)}
                unit="-"
                icon={SpeedIcon}
                color="#4facfe"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={2.4}>
              <KPICard
                title="Plateau alim."
                value={results.shortcut_methods.kirkbride.feed_stage}
                unit={`/${results.column_design.total_stages}`}
                icon={ThermostatIcon}
                color="#43e97b"
              />
            </Grid>
          </Grid>

          {/* Tabs */}
          <Paper sx={{ bgcolor: 'rgba(255,255,255,0.05)', mb: 3 }}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              sx={{
                borderBottom: 1,
                borderColor: 'rgba(255,255,255,0.1)',
                '& .MuiTab-root': { color: 'rgba(255,255,255,0.5)' },
                '& .Mui-selected': { color: '#667eea !important' },
              }}
            >
              <Tab label="Vue d'ensemble" />
              <Tab label="Profils de composition" />
              <Tab label="Bilans matières" />
              <Tab label="Résultats détaillés" />
            </Tabs>

            {/* Tab 0: Vue d'ensemble */}
            {tabValue === 0 && (
              <Box sx={{ p: 3 }}>
                <Grid container spacing={3}>
                  {/* Graphique circulaire - Composition Distillat */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" sx={{ color: '#fff', mb: 2, fontWeight: 600 }}>
                      Composition du Distillat
                    </Typography>
                    <Plot
                      data={[
                        {
                          values: results.compositions.distillate.map(c => c.fraction),
                          labels: results.compositions.distillate.map(c => c.compound),
                          type: 'pie',
                          hole: 0.4,
                          marker: {
                            colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'],
                          },
                          textinfo: 'label+percent',
                          textfont: {
                            color: '#fff',
                            size: 12,
                          },
                          hoverinfo: 'label+percent+value',
                        },
                      ]}
                      layout={{
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        showlegend: true,
                        legend: {
                          font: { color: '#fff' },
                        },
                        margin: { t: 20, b: 20, l: 20, r: 20 },
                        height: 350,
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%' }}
                    />
                  </Grid>

                  {/* Graphique circulaire - Composition Résidu */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" sx={{ color: '#fff', mb: 2, fontWeight: 600 }}>
                      Composition du Résidu
                    </Typography>
                    <Plot
                      data={[
                        {
                          values: results.compositions.bottoms.map(c => c.fraction),
                          labels: results.compositions.bottoms.map(c => c.compound),
                          type: 'pie',
                          hole: 0.4,
                          marker: {
                            colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'],
                          },
                          textinfo: 'label+percent',
                          textfont: {
                            color: '#fff',
                            size: 12,
                          },
                          hoverinfo: 'label+percent+value',
                        },
                      ]}
                      layout={{
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        showlegend: true,
                        legend: {
                          font: { color: '#fff' },
                        },
                        margin: { t: 20, b: 20, l: 20, r: 20 },
                        height: 350,
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%' }}
                    />
                  </Grid>

                  {/* Jauges de performance */}
                  <Grid item xs={12} md={4}>
                    <Plot
                      data={[
                        {
                          type: 'indicator',
                          mode: 'gauge+number',
                          value: results.column_design.efficiency * 100,
                          title: { text: 'Efficacité', font: { color: '#fff' } },
                          gauge: {
                            axis: { range: [0, 100], tickcolor: '#fff' },
                            bar: { color: '#667eea' },
                            bgcolor: 'rgba(255,255,255,0.1)',
                            borderwidth: 2,
                            bordercolor: '#667eea',
                            steps: [
                              { range: [0, 60], color: 'rgba(255,100,100,0.2)' },
                              { range: [60, 80], color: 'rgba(255,200,100,0.2)' },
                              { range: [80, 100], color: 'rgba(100,255,100,0.2)' },
                            ],
                          },
                        },
                      ]}
                      layout={{
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: { color: '#fff' },
                        height: 250,
                        margin: { t: 50, b: 20, l: 20, r: 20 },
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%' }}
                    />
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Plot
                      data={[
                        {
                          type: 'indicator',
                          mode: 'gauge+number',
                          value: results.shortcut_methods.gilliland.R_operating / results.shortcut_methods.underwood.R_min,
                          title: { text: 'R / R_min', font: { color: '#fff' } },
                          gauge: {
                            axis: { range: [1, 3], tickcolor: '#fff' },
                            bar: { color: '#764ba2' },
                            bgcolor: 'rgba(255,255,255,0.1)',
                            borderwidth: 2,
                            bordercolor: '#764ba2',
                            steps: [
                              { range: [1, 1.5], color: 'rgba(100,255,100,0.2)' },
                              { range: [1.5, 2], color: 'rgba(255,200,100,0.2)' },
                              { range: [2, 3], color: 'rgba(255,100,100,0.2)' },
                            ],
                          },
                        },
                      ]}
                      layout={{
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: { color: '#fff' },
                        height: 250,
                        margin: { t: 50, b: 20, l: 20, r: 20 },
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%' }}
                    />
                  </Grid>

                  <Grid item xs={12} md={4}>
                    <Plot
                      data={[
                        {
                          type: 'indicator',
                          mode: 'gauge+number',
                          value: results.shortcut_methods.gilliland.N_theoretical / results.shortcut_methods.fenske.N_min,
                          title: { text: 'N / N_min', font: { color: '#fff' } },
                          gauge: {
                            axis: { range: [1, 5], tickcolor: '#fff' },
                            bar: { color: '#f093fb' },
                            bgcolor: 'rgba(255,255,255,0.1)',
                            borderwidth: 2,
                            bordercolor: '#f093fb',
                            steps: [
                              { range: [1, 2], color: 'rgba(100,255,100,0.2)' },
                              { range: [2, 3], color: 'rgba(255,200,100,0.2)' },
                              { range: [3, 5], color: 'rgba(255,100,100,0.2)' },
                            ],
                          },
                        },
                      ]}
                      layout={{
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: { color: '#fff' },
                        height: 250,
                        margin: { t: 50, b: 20, l: 20, r: 20 },
                      }}
                      config={{ displayModeBar: false }}
                      style={{ width: '100%' }}
                    />
                  </Grid>
                </Grid>
              </Box>
            )}

            {/* Tab 1: Profils de composition */}
            {tabValue === 1 && (
              <Box sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', mb: 2, fontWeight: 600 }}>
                  Distribution des Composés
                </Typography>
                <Plot
                  data={results.distribution.map((comp, idx) => ({
                    x: ['Alimentation', 'Distillat', 'Résidu'],
                    y: [comp.feed, comp.distillate, comp.bottoms],
                    type: 'bar',
                    name: comp.compound,
                    marker: {
                      color: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'][idx % 5],
                    },
                  }))}
                  layout={{
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    barmode: 'group',
                    font: { color: '#fff' },
                    xaxis: {
                      gridcolor: 'rgba(255,255,255,0.1)',
                      title: { text: 'Flux', font: { color: '#fff' } },
                    },
                    yaxis: {
                      gridcolor: 'rgba(255,255,255,0.1)',
                      title: { text: 'Débit (kmol/h)', font: { color: '#fff' } },
                    },
                    legend: {
                      font: { color: '#fff' },
                      bgcolor: 'rgba(0,0,0,0.5)',
                    },
                    height: 500,
                    margin: { t: 50, b: 80, l: 80, r: 50 },
                  }}
                  config={{ displayModeBar: true }}
                  style={{ width: '100%' }}
                />
              </Box>
            )}

            {/* Tab 2: Bilans matières */}
            {tabValue === 2 && (
              <Box sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', mb: 2, fontWeight: 600 }}>
                  Bilan Matière Détaillé
                </Typography>
                <TableContainer component={Paper} sx={{ bgcolor: 'rgba(255,255,255,0.05)' }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell sx={{ color: '#667eea', fontWeight: 600 }}>Composé</TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 600 }}>
                          Alim. (kmol/h)
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 600 }}>
                          Distillat (kmol/h)
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 600 }}>
                          Résidu (kmol/h)
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 600 }}>
                          Récup. D (%)
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 600 }}>
                          Récup. B (%)
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.distribution.map((row) => (
                        <TableRow key={row.compound}>
                          <TableCell sx={{ color: '#fff' }}>{row.compound}</TableCell>
                          <TableCell align="right" sx={{ color: '#fff' }}>
                            {row.feed.toFixed(2)}
                          </TableCell>
                          <TableCell align="right" sx={{ color: '#fff' }}>
                            {row.distillate.toFixed(2)}
                          </TableCell>
                          <TableCell align="right" sx={{ color: '#fff' }}>
                            {row.bottoms.toFixed(2)}
                          </TableCell>
                          <TableCell align="right" sx={{ color: '#43e97b' }}>
                            {row.recovery_D.toFixed(1)}
                          </TableCell>
                          <TableCell align="right" sx={{ color: '#f093fb' }}>
                            {row.recovery_B.toFixed(1)}
                          </TableCell>
                        </TableRow>
                      ))}
                      <TableRow sx={{ bgcolor: 'rgba(102, 126, 234, 0.1)' }}>
                        <TableCell sx={{ color: '#667eea', fontWeight: 700 }}>TOTAL</TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 700 }}>
                          {results.flows.feed.toFixed(2)}
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 700 }}>
                          {results.flows.distillate.toFixed(2)}
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#667eea', fontWeight: 700 }}>
                          {results.flows.bottoms.toFixed(2)}
                        </TableCell>
                        <TableCell align="right" sx={{ color: '#fff' }}>-</TableCell>
                        <TableCell align="right" sx={{ color: '#fff' }}>-</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            )}

            {/* Tab 3: Résultats détaillés */}
            {tabValue === 3 && (
              <Box sx={{ p: 3 }}>
                <Grid container spacing={3}>
                  {/* Méthodes simplifiées */}
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(102, 126, 234, 0.1)', border: '1px solid rgba(102, 126, 234, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#667eea', mb: 2, fontWeight: 600 }}>
                        Méthode de Fenske
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • N<sub>min</sub> = {results.shortcut_methods.fenske.N_min.toFixed(3)} plateaux
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • α<sub>avg</sub> = {results.shortcut_methods.fenske.alpha_avg.toFixed(3)}
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(118, 75, 162, 0.1)', border: '1px solid rgba(118, 75, 162, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#764ba2', mb: 2, fontWeight: 600 }}>
                        Méthode d'Underwood
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • R<sub>min</sub> = {results.shortcut_methods.underwood.R_min.toFixed(3)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • θ = {results.shortcut_methods.underwood.theta.toFixed(3)}
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(240, 147, 251, 0.1)', border: '1px solid rgba(240, 147, 251, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#f093fb', mb: 2, fontWeight: 600 }}>
                        Corrélation de Gilliland
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • R<sub>op</sub> = {results.shortcut_methods.gilliland.R_operating.toFixed(3)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • N<sub>théorique</sub> = {results.shortcut_methods.gilliland.N_theoretical.toFixed(2)} plateaux
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • N<sub>réel</sub> = {results.shortcut_methods.gilliland.N_real} plateaux
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • X = {results.shortcut_methods.gilliland.X.toFixed(4)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • Y = {results.shortcut_methods.gilliland.Y.toFixed(4)}
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(79, 172, 254, 0.1)', border: '1px solid rgba(79, 172, 254, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#4facfe', mb: 2, fontWeight: 600 }}>
                        Équation de Kirkbride
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • Plateau d'alimentation = {results.shortcut_methods.kirkbride.feed_stage}
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • N<sub>rectification</sub> = {results.shortcut_methods.kirkbride.N_rectification} plateaux
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • N<sub>épuisement</sub> = {results.shortcut_methods.kirkbride.N_stripping} plateaux
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>

                  {/* Températures et énergie */}
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(67, 233, 123, 0.1)', border: '1px solid rgba(67, 233, 123, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#43e97b', mb: 2, fontWeight: 600 }}>
                        Températures
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • T<sub>tête</sub> = {results.temperatures.top.toFixed(1)}°C
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • T<sub>fond</sub> = {results.temperatures.bottom.toFixed(1)}°C
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • T<sub>alim</sub> = {results.temperatures.feed.toFixed(1)}°C
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(255, 75, 75, 0.1)', border: '1px solid rgba(255, 75, 75, 0.3)' }}>
                      <Typography variant="h6" sx={{ color: '#ff4b4b', mb: 2, fontWeight: 600 }}>
                        Besoins Énergétiques
                      </Typography>
                      <Box sx={{ pl: 2 }}>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • Q<sub>condenseur</sub> = {results.energy.Q_condenser.toFixed(0)} kW
                        </Typography>
                        <Typography variant="body2" sx={{ color: '#fff', mb: 1 }}>
                          • Q<sub>rebouilleur</sub> = {results.energy.Q_reboiler.toFixed(0)} kW
                        </Typography>
                      </Box>
                    </Paper>
                  </Grid>
                </Grid>
              </Box>
            )}
          </Paper>
        </>
      )}

      {/* État initial */}
      {!results && !loading && !error && (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '60vh',
            textAlign: 'center',
          }}
        >
          <Box>
            <ScienceIcon sx={{ fontSize: 100, color: 'rgba(102, 126, 234, 0.3)', mb: 2 }} />
            <Typography variant="h5" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1 }}>
              Aucune simulation lancée
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.5)' }}>
              Configurez les paramètres dans la barre latérale et lancez la simulation
            </Typography>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default Dashboard;
