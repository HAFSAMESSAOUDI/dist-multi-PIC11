import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  InputAdornment,
  Chip,
  Avatar
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ScienceIcon from '@mui/icons-material/Science';

const CompoundsList = ({ compounds }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCompounds = compounds.filter(compound =>
    compound.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    compound.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    compound.formula.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Composés Disponibles
      </Typography>

      <TextField
        fullWidth
        variant="outlined"
        placeholder="Rechercher un composé..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        {filteredCompounds.length} composé(s) trouvé(s)
      </Typography>

      <Grid container spacing={2}>
        {filteredCompounds.map((compound) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={compound.id}>
            <Card
              sx={{
                height: '100%',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <ScienceIcon />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" component="div">
                      {compound.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {compound.id}
                    </Typography>
                  </Box>
                </Box>

                <Chip
                  label={compound.formula}
                  size="small"
                  color="primary"
                  variant="outlined"
                  sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}
                />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredCompounds.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6" color="text.secondary">
            Aucun composé trouvé
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Essayez avec un autre terme de recherche
          </Typography>
        </Box>
      )}

      <Box sx={{ mt: 4, p: 2, bgcolor: 'info.lighter', borderRadius: 2 }}>
        <Typography variant="body2" color="text.secondary">
          <strong>Note:</strong> Ces composés sont chargés depuis la bibliothèque thermodynamique.
          Vous pouvez en sélectionner plusieurs pour créer votre mélange à séparer.
        </Typography>
      </Box>
    </Box>
  );
};

export default CompoundsList;
