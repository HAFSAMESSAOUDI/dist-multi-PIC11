# Application Web de Simulation de Distillation Multicomposants

## 🎯 Description

Application web complète pour la simulation de colonnes de distillation multicomposants avec:
- **Backend Flask** : API REST pour les calculs thermodynamiques
- **Frontend React** : Interface utilisateur moderne et interactive
- **Visualisations** : Graphiques dynamiques des profils de composition et température

---

## 📋 Prérequis

### Backend (Python)
- Python 3.8+
- pip

### Frontend (React)
- Node.js 14+
- npm ou yarn

---

## 🚀 Installation

### 1. Backend Flask

```bash
# Se placer dans le dossier backend
cd backend

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Frontend React

```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances
npm install
```

---

## ▶️ Lancement de l'Application

### Méthode 1: Lancement manuel

#### Terminal 1 - Backend Flask
```bash
cd backend
python app.py
```
Le backend sera accessible sur: `http://localhost:5000`

#### Terminal 2 - Frontend React
```bash
cd frontend
npm start
```
Le frontend sera accessible sur: `http://localhost:3000`

### Méthode 2: Script de lancement automatique

#### Windows
```bash
# Lancer les deux serveurs en même temps
start_app.bat
```

#### Linux/Mac
```bash
# Donner les permissions d'exécution
chmod +x start_app.sh

# Lancer les deux serveurs
./start_app.sh
```

---

## 🎨 Fonctionnalités

### 1. Configuration de la Simulation
- Sélection de composés depuis une bibliothèque thermodynamique
- Définition des compositions molaires avec normalisation automatique
- Paramètres opératoires (débit, pression)
- Spécifications de séparation (récupérations)
- Paramètres de conception (reflux, efficacité)

### 2. Méthodes de Calcul
- **Fenske**: Nombre minimum de plateaux (reflux total)
- **Underwood**: Reflux minimum
- **Gilliland**: Nombre de plateaux à reflux opératoire
- **Kirkbride**: Position du plateau d'alimentation

### 3. Résultats
- Bilans matières détaillés
- Paramètres de dimensionnement
- Profils de composition (liquide et vapeur)
- Profil de température
- Débits internes
- Export des résultats en JSON

### 4. Visualisations
- Graphiques de composition interactifs
- Profil de température dans la colonne
- Diagrammes des bilans matières
- Graphiques avec Recharts (intégrés) et possibilité d'export

---

## 📁 Structure du Projet

```
dist-multi-PIC11-main/
│
├── backend/                    # Backend Flask
│   ├── app.py                 # API REST principale
│   └── requirements.txt       # Dépendances Python
│
├── frontend/                  # Frontend React
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── SimulationForm.js      # Formulaire de simulation
│   │   │   ├── ResultsDisplay.js      # Affichage des résultats
│   │   │   └── CompoundsList.js       # Liste des composés
│   │   ├── services/
│   │   │   └── api.js                 # Client API
│   │   ├── App.js                     # Composant principal
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
│
├── distillation_multicomposants.py   # Module de calcul
├── visualization.py                   # Module de visualisation
├── exemple_btx.py                     # Exemple d'utilisation
└── README_APPLICATION.md              # Ce fichier
```

---

## 🔌 API Endpoints

### GET /api/health
Vérification de l'état du serveur

### GET /api/compounds
Liste des composés disponibles

### POST /api/compound-properties
Propriétés d'un composé spécifique
```json
{
  "compound_id": "benzene"
}
```

### POST /api/simulate
Lancement d'une simulation
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

### POST /api/generate-plot
Génération d'un graphique (base64)
```json
{
  "plot_type": "composition_profiles",
  "data": {...}
}
```

### POST /api/reflux-study
Étude paramétrique du reflux

---

## 🧪 Exemple d'Utilisation

1. Ouvrir l'application dans le navigateur: `http://localhost:3000`

2. **Onglet Simulation**:
   - Sélectionner 3 composés (ex: Benzène, Toluène, Xylène)
   - Entrer les compositions (ex: 0.33, 0.33, 0.34)
   - Définir le débit (ex: 100 kmol/h)
   - Ajuster les paramètres de séparation
   - Cliquer sur "Lancer la Simulation"

3. **Onglet Résultats**:
   - Consulter les bilans matières
   - Visualiser les profils de composition
   - Analyser le profil de température
   - Exporter les résultats

4. **Onglet Composés**:
   - Explorer la bibliothèque de composés disponibles

---

## 🛠️ Développement

### Backend Flask - Mode Debug
```bash
cd backend
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```

### Frontend React - Mode Développement
```bash
cd frontend
npm start
```
Le serveur de développement React supporte le hot-reload.

### Build Production
```bash
cd frontend
npm run build
```
Génère les fichiers optimisés dans `frontend/build/`

---

## 📊 Composés Disponibles

L'application inclut une bibliothèque de composés:
- **Aromatiques**: Benzène, Toluène, Xylène, Éthylbenzène
- **Alcools**: Méthanol, Éthanol, Propanol, Butanol
- **Hydrocarbures**: Hexane, Heptane, Octane
- **Autres**: Eau, Acétone

---

## 🐛 Dépannage

### Le backend ne démarre pas
- Vérifier que Python 3.8+ est installé: `python --version`
- Vérifier les dépendances: `pip install -r backend/requirements.txt`
- Vérifier que le port 5000 est libre

### Le frontend ne démarre pas
- Vérifier que Node.js est installé: `node --version`
- Supprimer `node_modules` et réinstaller: `rm -rf node_modules && npm install`
- Vérifier que le port 3000 est libre

### Erreur de connexion au backend
- Vérifier que le backend est lancé sur le port 5000
- Vérifier l'URL dans `frontend/src/services/api.js`
- Désactiver temporairement le pare-feu

### Erreurs de calcul
- Vérifier que la somme des compositions = 1.0
- Vérifier que tous les paramètres sont positifs
- Consulter la console du navigateur pour plus de détails

---

## 📚 Références

### Méthodes de Calcul
- **Fenske**: Calcul du nombre minimum de plateaux
- **Underwood**: Calcul du reflux minimum
- **Gilliland**: Corrélation pour le nombre de plateaux réels
- **Kirkbride**: Détermination du plateau d'alimentation

### Bibliothèques Utilisées
- **Backend**: Flask, NumPy, SciPy, thermo, chemicals, CoolProp
- **Frontend**: React, Material-UI, Recharts, Axios

---

## 👨‍🏫 Auteur

**Prof. BAKHER Zine Elabidine**
Cours: Modélisation et Simulation des Procédés - PIC
Université

---

## 📝 License

Ce projet est développé à des fins pédagogiques pour le cours de Modélisation et Simulation des Procédés.

---

## 🎓 Notes pour les Étudiants

Cette application web illustre l'intégration de:
1. **Calculs d'ingénierie** (Python)
2. **API REST** (Flask)
3. **Interface moderne** (React)
4. **Visualisation de données** (Recharts)

C'est un excellent exemple de développement full-stack appliqué au génie des procédés.

---

## 🔄 Mises à Jour Futures

Fonctionnalités prévues:
- [ ] Méthode MESH rigoureuse (résolution étage par étage)
- [ ] Optimisation automatique des paramètres
- [ ] Comparaison de plusieurs configurations
- [ ] Export des graphiques en PDF
- [ ] Base de données pour sauvegarder les simulations
- [ ] Mode multi-utilisateurs
- [ ] API pour intégration avec d'autres outils

---

**Bon usage de l'application! 🚀**
