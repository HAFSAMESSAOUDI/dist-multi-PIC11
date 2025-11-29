# 📁 Structure du Projet

## Fichiers Essentiels

### Backend Python (Streamlit)

**Application principale:**
- `streamlit_app_enhanced.py` - Interface Streamlit principale

**Modules de calcul:**
- `distillation_multicomposants.py` - Méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
- `mesh_solver.py` - Résolution rigoureuse MESH
- `activity_models.py` - Modèles thermodynamiques (Wilson, NRTL, UNIQUAC)
- `economic_optimization.py` - Optimisation économique (TAC)
- `pdf_generator.py` - Génération de rapports PDF (compilation en ligne)

**Configuration:**
- `requirements.txt` - Dépendances Python
- `run_enhanced.bat` - Lancement Windows
- `run_enhanced.sh` - Lancement Linux/Mac

### Frontend React

**Dossier `frontend/`:**
- Interface utilisateur React (optionnelle)
- Alternative à l'interface Streamlit

## Lancement de l'Application

### Streamlit (Recommandé)

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app_enhanced.py
```

Ou utiliser les scripts:
```bash
# Windows
run_enhanced.bat

# Linux/Mac
./run_enhanced.sh
```

### React Frontend (Optionnel)

```bash
cd frontend
npm install
npm start
```

## Fonctionnalités

✅ Méthodes simplifiées de distillation
✅ Méthode MESH rigoureuse
✅ Optimisation économique (TAC)
✅ Génération automatique de PDF (compilation en ligne)
✅ Visualisations interactives
✅ Export Excel des résultats

## Technologies

- **Backend:** Python, Streamlit, NumPy, SciPy
- **Frontend:** React (optionnel)
- **PDF:** LaTeX-on-HTTP (compilation cloud)
- **Visualisation:** Plotly
