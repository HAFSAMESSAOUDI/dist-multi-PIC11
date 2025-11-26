# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### Étape 1: Installer les dépendances Python (Backend)
```bash
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
```

### Étape 2: Installer Node.js et les dépendances React (Frontend)

**Si Node.js n'est pas installé:**
Téléchargez depuis: https://nodejs.org/ (version LTS recommandée)

**Installer les dépendances:**
```bash
cd frontend
npm install
```

---

## ▶️ Lancement Rapide

### Option 1: Script Automatique (Windows)
Double-cliquez sur: **`start_app.bat`**

### Option 2: Lancement Manuel

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

---

## 🎯 Utilisation

1. Ouvrez votre navigateur: **http://localhost:3000**

2. **Configurez la simulation:**
   - Choisissez 2-10 composés
   - Entrez les compositions (somme = 1.0)
   - Ajustez les paramètres

3. **Lancez la simulation:**
   - Cliquez sur "Lancer la Simulation"
   - Patientez quelques secondes

4. **Consultez les résultats:**
   - Onglet "Résultats" s'ouvre automatiquement
   - Explorez les différentes sections

---

## 📊 Exemple Rapide

**Configuration par défaut (système BTX):**
- Composés: Benzène, Toluène, Xylène
- Compositions: 33.3% chacun
- Débit: 100 kmol/h
- Pression: 1 atm

Cliquez simplement sur "Lancer la Simulation" !

---

## ❌ Problèmes Courants

### Backend ne démarre pas
```bash
# Vérifier Python
python --version

# Réinstaller les dépendances
pip install -r backend/requirements.txt
```

### Frontend ne démarre pas
```bash
# Vérifier Node.js
node --version

# Réinstaller les dépendances
cd frontend
rm -rf node_modules
npm install
```

### Port déjà utilisé
- Backend (5000): Fermez les applications sur ce port
- Frontend (3000): Fermez les navigateurs/serveurs existants

---

## 📱 URLs de l'Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

---

## 🎓 Prêt à Simuler!

L'application est maintenant prête. Bonne simulation! 🧪

Pour plus de détails, consultez [README_APPLICATION.md](README_APPLICATION.md)
