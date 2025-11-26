# 🏗️ Architecture de l'Application

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATEUR WEB                            │
│                   (http://localhost:3000)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/AJAX
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  FRONTEND REACT                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  App.js (Composant Principal)                        │   │
│  │  ├─ SimulationForm.js  (Formulaire de saisie)       │   │
│  │  ├─ ResultsDisplay.js  (Affichage des résultats)    │   │
│  │  └─ CompoundsList.js   (Liste des composés)         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services API (api.js)                               │   │
│  │  - Appels REST vers le backend                       │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API (JSON)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   BACKEND FLASK                              │
│                  (http://localhost:5000)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints (app.py)                              │   │
│  │  ├─ GET  /api/health                                 │   │
│  │  ├─ GET  /api/compounds                              │   │
│  │  ├─ POST /api/compound-properties                    │   │
│  │  ├─ POST /api/simulate                               │   │
│  │  ├─ POST /api/generate-plot                          │   │
│  │  └─ POST /api/reflux-study                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         │ Python Imports                     │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Modules de Calcul                                   │   │
│  │  ├─ distillation_multicomposants.py                 │   │
│  │  │   ├─ Compound (propriétés thermodynamiques)      │   │
│  │  │   ├─ ThermodynamicPackage (équilibres)           │   │
│  │  │   └─ ShortcutDistillation (dimensionnement)      │   │
│  │  └─ visualization.py (graphiques)                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         │ Python Libraries                   │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Bibliothèques Externes                              │   │
│  │  ├─ NumPy, SciPy (calculs scientifiques)            │   │
│  │  ├─ Pandas (données)                                 │   │
│  │  ├─ Matplotlib (visualisation)                       │   │
│  │  ├─ thermo, chemicals (thermodynamique)             │   │
│  │  └─ CoolProp (propriétés fluides)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Composants Principaux

### 1. Frontend React (Port 3000)

**Technologies:**
- React 18.2
- Material-UI (MUI) 5.15 - Interface moderne
- Recharts 2.10 - Graphiques interactifs
- Axios 1.6 - Client HTTP
- React-Toastify - Notifications

**Composants:**

#### `App.js`
- Composant racine
- Gestion des onglets
- État global de l'application
- Intégration des sous-composants

#### `SimulationForm.js`
- Formulaire de configuration
- Validation des entrées
- Normalisation des compositions
- Contrôles interactifs (sliders)

#### `ResultsDisplay.js`
- Affichage des résultats
- Graphiques Recharts
- Tables de données
- Accordéons pour organisation
- Export JSON

#### `CompoundsList.js`
- Liste des composés disponibles
- Recherche/filtrage
- Affichage des propriétés

**Services:**

#### `api.js`
- Configuration Axios
- Gestion des erreurs
- Timeout (60s)
- Base URL configurable

---

### 2. Backend Flask (Port 5000)

**Technologies:**
- Flask 3.0 - Framework web
- Flask-CORS - Support CORS
- NumPy, SciPy - Calculs scientifiques
- Matplotlib - Génération de graphiques
- thermo, chemicals - Thermodynamique

**Endpoints API:**

```
GET  /api/health
     → Vérification serveur

GET  /api/compounds
     → Liste des composés disponibles

POST /api/compound-properties
     Body: { "compound_id": "benzene" }
     → Propriétés thermodynamiques

POST /api/simulate
     Body: { configuration complète }
     → Simulation complète avec résultats

POST /api/generate-plot
     Body: { "plot_type": "...", "data": {...} }
     → Génération graphique (base64)

POST /api/reflux-study
     Body: { configuration }
     → Étude paramétrique du reflux
```

**Modules de Calcul:**

#### `Compound`
- Chargement depuis base thermo
- Propriétés critiques (Tc, Pc, ω)
- Pressions de vapeur
- Coefficients K
- Enthalpies

#### `ThermodynamicPackage`
- Calculs d'équilibre
- Températures de bulle/rosée
- Volatilités relatives
- Enthalpies de mélanges

#### `ShortcutDistillation`
- Méthode de Fenske (N_min)
- Méthode d'Underwood (R_min)
- Corrélation de Gilliland (N)
- Équation de Kirkbride (feed stage)
- Bilans matières

---

## 🔄 Flux de Données

### Simulation Complète

```
1. Utilisateur remplit le formulaire
   └─> SimulationForm.js

2. Validation locale (React)
   ├─ Somme compositions = 1.0
   ├─ Valeurs positives
   └─ Contraintes min/max

3. Envoi requête POST /api/simulate
   └─> api.js (Axios)

4. Backend reçoit la requête
   └─> app.py

5. Création des objets
   ├─> Compound (pour chaque composé)
   ├─> ThermodynamicPackage
   └─> ShortcutDistillation

6. Calculs séquentiels
   ├─ Bilans matières
   ├─ Fenske (N_min)
   ├─ Underwood (R_min)
   ├─ Gilliland (N)
   ├─ Kirkbride (feed stage)
   └─ Estimation profils

7. Formatage réponse JSON
   └─> Retour au frontend

8. Affichage des résultats
   └─> ResultsDisplay.js
       ├─ Graphiques Recharts
       ├─ Tables Material-UI
       └─ Accordéons pour organisation
```

---

## 🎨 Stack Technologique

### Frontend
```javascript
React 18.2          // Framework UI
Material-UI 5.15    // Composants UI
Recharts 2.10       // Graphiques
Axios 1.6           // HTTP Client
React-Toastify      // Notifications
```

### Backend
```python
Flask 3.0           # Framework web
NumPy 1.20+         # Calculs matriciels
SciPy 1.7+          # Optimisation
Pandas 1.3+         # Données
Matplotlib 3.4+     # Visualisation
thermo 0.2.20+      # Thermodynamique
chemicals 1.1.4+    # Propriétés chimiques
CoolProp 6.4.1+     # Fluides
```

---

## 🔐 Sécurité et Bonnes Pratiques

### Frontend
- Validation côté client
- Sanitization des entrées
- Gestion des erreurs
- Timeout sur requêtes (60s)
- Messages d'erreur clairs

### Backend
- CORS configuré (Flask-CORS)
- Validation des données d'entrée
- Gestion des exceptions
- Logs d'erreur détaillés
- Limite de taille des requêtes (16 MB)

---

## 📊 Performance

### Frontend
- React optimisé (hooks, memo)
- Lazy loading des composants
- Recharts efficient rendering
- Mise en cache navigateur

### Backend
- Calculs vectorisés (NumPy)
- Pas de base de données (stateless)
- Timeout configuré
- Backend non-interactif (Matplotlib Agg)

---

## 🚀 Déploiement

### Développement
```bash
# Backend
cd backend && python app.py

# Frontend
cd frontend && npm start
```

### Production
```bash
# Backend avec Gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend build
cd frontend
npm run build
# Servir avec nginx ou autre
```

---

## 📝 Configuration

### Variables d'Environnement

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:5000/api
PORT=3000
```

**Backend (optionnel)**
```
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## 🔧 Extensions Futures

### Backend
- [ ] Cache Redis pour résultats
- [ ] Base de données (PostgreSQL)
- [ ] Authentification JWT
- [ ] Rate limiting
- [ ] Websockets pour progression

### Frontend
- [ ] PWA (Progressive Web App)
- [ ] Mode hors-ligne
- [ ] Comparaison de simulations
- [ ] Historique des simulations
- [ ] Export PDF des rapports

### Calculs
- [ ] Méthode MESH rigoureuse
- [ ] Optimisation multi-objectifs
- [ ] Analyse de sensibilité
- [ ] Simulation dynamique
- [ ] Intégration AspenPlus

---

**Architecture conçue pour:**
- ✅ Scalabilité
- ✅ Maintenabilité
- ✅ Extensibilité
- ✅ Performance
- ✅ UX moderne
