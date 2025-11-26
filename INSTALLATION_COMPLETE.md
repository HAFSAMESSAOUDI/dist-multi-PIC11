# 📦 Guide d'Installation Complète

## ✅ Checklist d'Installation

### Phase 1: Vérifications Préalables

- [ ] Python 3.8+ installé
  ```bash
  python --version
  ```

- [ ] pip installé
  ```bash
  pip --version
  ```

- [ ] Node.js 14+ installé
  ```bash
  node --version
  ```

- [ ] npm installé
  ```bash
  npm --version
  ```

---

### Phase 2: Installation Backend (Python)

#### 2.1 Bibliothèques de Base
```bash
pip install Flask flask-cors
```
✅ Flask (serveur web) et flask-cors (support CORS)

#### 2.2 Bibliothèques Scientifiques
```bash
pip install numpy scipy pandas matplotlib seaborn
```
✅ Calculs numériques et visualisation

#### 2.3 Bibliothèques Thermodynamiques
```bash
pip install thermo chemicals CoolProp
```
✅ Propriétés thermodynamiques des composés

#### 2.4 Autres Dépendances
```bash
pip install gunicorn python-dotenv
```
✅ Serveur production et configuration

#### 2.5 Installation Complète en Une Ligne
```bash
pip install Flask flask-cors numpy scipy pandas matplotlib seaborn thermo chemicals CoolProp gunicorn python-dotenv
```

#### 2.6 Vérification Backend
```bash
cd backend
python -c "from app import app; print('Backend OK')"
cd ..
```

---

### Phase 3: Installation Frontend (React)

#### 3.1 Navigation vers le dossier
```bash
cd frontend
```

#### 3.2 Installation des dépendances npm
```bash
npm install
```

Cela installera automatiquement:
- react et react-dom
- @mui/material (Material-UI)
- recharts (graphiques)
- axios (HTTP client)
- react-toastify (notifications)
- Et toutes les dépendances

#### 3.3 Retour au dossier principal
```bash
cd ..
```

#### 3.4 Vérification Frontend
```bash
cd frontend
npm list react
cd ..
```

---

### Phase 4: Test de l'Installation

#### 4.1 Test Backend
```bash
# Terminal 1: Lancer le backend
cd backend
python app.py
```

Attendez de voir:
```
* Running on http://0.0.0.0:5000
```

#### 4.2 Test API (dans un autre terminal)
```bash
# Sous Windows
curl http://localhost:5000/api/health

# Ou avec Python
python -c "import requests; print(requests.get('http://localhost:5000/api/health').json())"
```

Résultat attendu:
```json
{
  "status": "ok",
  "message": "Backend de simulation de distillation est opérationnel"
}
```

#### 4.3 Test Frontend
```bash
# Terminal 2: Lancer le frontend
cd frontend
npm start
```

Le navigateur devrait s'ouvrir automatiquement sur http://localhost:3000

---

### Phase 5: Validation Complète

#### 5.1 Exécuter les tests backend
```bash
# Backend doit être lancé
python test_backend.py
```

Résultat attendu:
```
Tests réussis: 4/4
✓ Tous les tests sont passés avec succès!
```

#### 5.2 Test de simulation
1. Ouvrir http://localhost:3000
2. Laisser la configuration par défaut (BTX)
3. Cliquer sur "Lancer la Simulation"
4. Vérifier que les résultats s'affichent

---

## 🔧 Installation par Système d'Exploitation

### Windows

#### Méthode 1: PowerShell
```powershell
# Backend
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Frontend
cd frontend
npm install
cd ..
```

#### Méthode 2: Git Bash
```bash
# Même commandes que Linux
```

### Linux (Ubuntu/Debian)

```bash
# Mise à jour du système
sudo apt update

# Python et pip (si nécessaire)
sudo apt install python3 python3-pip

# Node.js et npm (si nécessaire)
sudo apt install nodejs npm

# Backend
pip3 install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Frontend
cd frontend
npm install
cd ..
```

### macOS

```bash
# Homebrew (si nécessaire)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python (si nécessaire)
brew install python3

# Node.js (si nécessaire)
brew install node

# Backend
pip3 install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Frontend
cd frontend
npm install
cd ..
```

---

## 📊 Tailles d'Installation

### Backend Python
- Flask + dépendances: ~50 MB
- NumPy + SciPy: ~150 MB
- Pandas + Matplotlib: ~100 MB
- thermo + chemicals + CoolProp: ~200 MB
- **Total Backend: ~500 MB**

### Frontend React
- node_modules: ~300-400 MB
- **Total Frontend: ~350 MB**

### Total Projet
- **~850 MB - 1 GB**

---

## ⏱️ Temps d'Installation

### Avec connexion rapide (100 Mbps+)
- Backend: 5-10 minutes
- Frontend: 3-5 minutes
- **Total: 10-15 minutes**

### Avec connexion moyenne (10-50 Mbps)
- Backend: 10-20 minutes
- Frontend: 5-10 minutes
- **Total: 20-30 minutes**

---

## 🐛 Problèmes Courants et Solutions

### Problème 1: pip n'est pas reconnu
**Solution:**
```bash
# Windows
python -m pip install [package]

# Linux/Mac
python3 -m pip install [package]
```

### Problème 2: npm install échoue
**Solution:**
```bash
# Nettoyer le cache
npm cache clean --force

# Supprimer node_modules
rm -rf node_modules package-lock.json

# Réinstaller
npm install
```

### Problème 3: Erreur "module not found"
**Solution:**
```bash
# Backend
pip install --upgrade [nom_module]

# Frontend
cd frontend
npm install [nom_package]
```

### Problème 4: Permission denied (Linux/Mac)
**Solution:**
```bash
# Backend (éviter sudo)
pip install --user [packages]

# Frontend
sudo chown -R $USER ~/.npm
npm install
```

### Problème 5: Versions incompatibles
**Solution:**
```bash
# Backend - créer un environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Puis installer les packages
pip install [packages]
```

---

## 📦 Installation Hors Ligne

### Préparation (avec connexion)
```bash
# Backend
pip download -d backend_packages Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Frontend
cd frontend
npm pack
cd ..
```

### Installation (sans connexion)
```bash
# Backend
pip install --no-index --find-links=backend_packages Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Frontend
cd frontend
npm install ./[package-name].tgz
```

---

## 🎯 Environnement Virtuel (Recommandé)

### Création
```bash
# Créer l'environnement
python -m venv env_distillation

# Activer
# Windows
env_distillation\Scripts\activate

# Linux/Mac
source env_distillation/bin/activate
```

### Installation dans l'environnement
```bash
# Backend
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp

# Le reste reste identique
```

### Désactivation
```bash
deactivate
```

---

## ✅ Validation Finale

### Checklist Post-Installation

- [ ] Backend installé (pip list | grep Flask)
- [ ] Frontend installé (ls frontend/node_modules)
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] API accessible (http://localhost:5000/api/health)
- [ ] Interface accessible (http://localhost:3000)
- [ ] Test de simulation réussi
- [ ] Graphiques s'affichent correctement

---

## 📚 Commandes de Référence Rapide

```bash
# Installation complète
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
cd frontend && npm install && cd ..

# Lancement
# Terminal 1
cd backend && python app.py

# Terminal 2
cd frontend && npm start

# Test
python test_backend.py

# Clean
cd frontend && rm -rf node_modules && cd ..
```

---

## 🎉 Installation Terminée!

Si toutes les étapes sont complétées avec succès:

✅ Votre application est prête!
✅ Vous pouvez lancer la simulation
✅ Consultez le README.md pour l'utilisation

**Prochaine étape:** Lancer l'application avec `start_app.bat` (Windows) ou `./start_app.sh` (Linux/Mac)

---

**Bon développement! 🚀**
