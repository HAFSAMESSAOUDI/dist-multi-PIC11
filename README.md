# 🧪 Simulateur de Distillation Multicomposants

## Application Web Full-Stack (Flask + React)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2-61dafb.svg)](https://reactjs.org/)
[![Material-UI](https://img.shields.io/badge/MUI-5.15-007FFF.svg)](https://mui.com/)

---

## 📖 Description

Application web moderne pour la **simulation de colonnes de distillation multicomposants** développée pour le cours de **Modélisation et Simulation des Procédés**.

### Caractéristiques Principales

✅ **Interface Web Intuitive** - React + Material-UI
✅ **API REST** - Backend Flask performant
✅ **Calculs Rigoureux** - Méthodes de Fenske, Underwood, Gilliland, Kirkbride
✅ **Visualisations Interactives** - Graphiques Recharts
✅ **Bibliothèque Thermodynamique** - 13+ composés disponibles
✅ **Export de Résultats** - Format JSON

---

## 🎯 Fonctionnalités

### Configuration de Simulation
- Sélection multiple de composés (2 à 10)
- Définition des compositions avec normalisation automatique
- Paramètres opératoires (débit, pression)
- Spécifications de séparation (récupérations)
- Contrôles interactifs (sliders pour reflux, efficacité)

### Calculs et Méthodes
- **Fenske**: Nombre minimum de plateaux (reflux total)
- **Underwood**: Reflux minimum
- **Gilliland**: Corrélation pour plateaux réels
- **Kirkbride**: Position du plateau d'alimentation
- Estimation des profils de composition et température

### Résultats et Visualisation
- Bilans matières complets
- Profils de composition (liquide et vapeur)
- Profil de température dans la colonne
- Débits internes (rectification et épuisement)
- Graphiques interactifs et zoomables
- Export JSON des résultats

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Node.js 14+
- pip et npm

### Installation en 3 étapes

#### 1. Cloner le dépôt (si applicable)
```bash
git clone [URL]
cd dist-multi-PIC11-main
```

#### 2. Installer les dépendances Backend
```bash
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
```

#### 3. Installer les dépendances Frontend
```bash
cd frontend
npm install
```

---

## ▶️ Lancement

### Méthode 1: Script Automatique (Recommandé)

**Windows:**
```bash
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

### Méthode 2: Lancement Manuel

**Terminal 1 - Backend Flask:**
```bash
cd backend
python app.py
```
Backend accessible sur: http://localhost:5000

**Terminal 2 - Frontend React:**
```bash
cd frontend
npm start
```
Frontend accessible sur: http://localhost:3000

---

## 📱 Utilisation

1. **Ouvrir l'application**: http://localhost:3000

2. **Onglet Simulation**:
   - Choisir les composés
   - Définir les compositions
   - Ajuster les paramètres
   - Lancer la simulation

3. **Onglet Résultats**:
   - Consulter les bilans
   - Analyser les graphiques
   - Exporter les données

4. **Onglet Composés**:
   - Explorer la bibliothèque

---

## 📊 Exemple: Système BTX

**Configuration par défaut:**
```json
{
  "compounds": ["benzene", "toluene", "o-xylene"],
  "compositions": [0.33, 0.33, 0.34],
  "flow_rate": 100.0,
  "pressure": 101325,
  "recovery_lk": 0.95,
  "recovery_hk": 0.95,
  "reflux_factor": 1.3,
  "feed_quality": 1.0,
  "efficiency": 0.70
}
```

**Résultats typiques:**
- N_min ≈ 8-10 plateaux
- R_min ≈ 0.6-0.8
- N_réel ≈ 15-20 plateaux
- Plateau alimentation ≈ 8-10

---

## 🏗️ Architecture

```
Frontend (React)  ←→  Backend (Flask)  ←→  Modules Python
   Port 3000              Port 5000        (Calculs thermo)
```

**Détails complets:** Voir [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📁 Structure du Projet

```
dist-multi-PIC11-main/
│
├── backend/                         # Backend Flask
│   ├── app.py                      # API REST
│   └── requirements.txt
│
├── frontend/                        # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/             # Composants React
│   │   ├── services/               # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── distillation_multicomposants.py # Moteur de calcul
├── visualization.py                 # Visualisations
├── exemple_btx.py                  # Script exemple
│
├── start_app.bat                   # Lanceur Windows
├── start_app.sh                    # Lanceur Linux/Mac
├── test_backend.py                 # Tests API
│
├── README.md                       # Ce fichier
├── README_APPLICATION.md           # Documentation complète
├── QUICK_START.md                  # Guide rapide
└── ARCHITECTURE.md                 # Architecture détaillée
```

---

## 🧪 Tests

### Tester le Backend
```bash
# Lancer le backend d'abord
cd backend && python app.py

# Dans un autre terminal
python test_backend.py
```

### Tester l'API manuellement
```bash
# Health check
curl http://localhost:5000/api/health

# Liste des composés
curl http://localhost:5000/api/compounds
```

---

## 📚 Documentation

- **[README_APPLICATION.md](README_APPLICATION.md)** - Documentation complète
- **[QUICK_START.md](QUICK_START.md)** - Guide de démarrage rapide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture technique

---

## 🔧 Technologies Utilisées

### Backend
- **Flask 3.0** - Framework web Python
- **NumPy** - Calculs matriciels
- **SciPy** - Optimisation numérique
- **Pandas** - Manipulation de données
- **Matplotlib** - Visualisation
- **thermo** - Propriétés thermodynamiques
- **chemicals** - Base de données chimiques
- **CoolProp** - Propriétés des fluides

### Frontend
- **React 18.2** - Framework UI
- **Material-UI 5.15** - Composants UI modernes
- **Recharts 2.10** - Graphiques interactifs
- **Axios 1.6** - Client HTTP
- **React-Toastify** - Notifications

---

## 🎓 Cas d'Usage Pédagogique

Cette application est un excellent exemple de:
1. **Full-Stack Development** - Flask + React
2. **API REST** - Design et implémentation
3. **Calculs d'ingénierie** - Intégration Python
4. **UX moderne** - Material Design
5. **Visualisation de données** - Graphiques interactifs

---

## 🐛 Dépannage

### Backend ne démarre pas
```bash
# Vérifier Python
python --version

# Réinstaller dépendances
pip install -r backend/requirements.txt
```

### Frontend ne démarre pas
```bash
# Vérifier Node.js
node --version

# Nettoyer et réinstaller
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erreur de connexion
- Vérifier que les deux serveurs sont lancés
- Vérifier les ports 3000 et 5000
- Désactiver temporairement le pare-feu

---

## 📈 Roadmap

### Version actuelle (v1.0)
- ✅ Interface web complète
- ✅ Méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
- ✅ Visualisations interactives
- ✅ 13+ composés disponibles

### Futures versions
- [ ] Méthode MESH rigoureuse
- [ ] Optimisation multi-objectifs
- [ ] Base de données des simulations
- [ ] Authentification utilisateurs
- [ ] Export PDF des rapports
- [ ] Mode multi-colonnes
- [ ] Intégration AspenPlus

---

## 👥 Contribution

Projet développé pour le cours **Modélisation et Simulation des Procédés**.

**Professeur:** BAKHER Zine Elabidine
**Institution:** Université
**Cours:** PIC - Modélisation et Simulation des Procédés

---

## 📝 License

Projet à usage pédagogique - Cours de Modélisation et Simulation des Procédés

---

## 📞 Support

Pour toute question ou problème:
1. Consulter la [documentation complète](README_APPLICATION.md)
2. Vérifier le [guide de dépannage](README_APPLICATION.md#-dépannage)
3. Examiner l'[architecture](ARCHITECTURE.md)

---

## 🎉 Crédits

- **Méthodes de calcul**: Fenske, Underwood, Gilliland, Kirkbride
- **Bibliothèques thermo**: thermo, chemicals, CoolProp
- **UI Framework**: Material-UI
- **Graphiques**: Recharts

---

**Développé avec ❤️ pour l'apprentissage du génie des procédés**

---

## 🚀 Démarrage Ultra-Rapide

```bash
# 1. Installer dépendances
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
cd frontend && npm install && cd ..

# 2. Lancer l'application
# Windows: double-cliquer sur start_app.bat
# Linux/Mac: ./start_app.sh

# 3. Ouvrir: http://localhost:3000

# 4. Profiter de la simulation!
```

---

**Bonne simulation! 🧪✨**
