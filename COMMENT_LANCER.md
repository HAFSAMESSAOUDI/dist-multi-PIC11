# 🚀 COMMENT LANCER L'APPLICATION

## ✅ Méthode Recommandée : Script Automatique

### Windows (PLUS SIMPLE)

1. **Double-cliquez sur le fichier** : `start_app.bat`
2. Deux fenêtres de terminal vont s'ouvrir :
   - Une pour le **Backend Flask** (port 5000)
   - Une pour le **Frontend React** (port 3000)
3. Le navigateur s'ouvrira automatiquement sur **http://localhost:3000**

**C'est tout !** ✨

---

## 📝 Méthode Manuel (Si le script ne fonctionne pas)

### Étape 1: Lancer le Backend Flask

Ouvrez un **premier terminal** (CMD ou PowerShell) :

```bash
cd backend
python app.py
```

Vous devriez voir :
```
============================================================
  SERVEUR BACKEND FLASK - SIMULATEUR DE DISTILLATION
============================================================

  URL: http://localhost:5000
  API Health: http://localhost:5000/api/health

  Endpoints disponibles:
    - GET  /api/health
    - GET  /api/compounds
    - POST /api/simulate
    ...

============================================================

 * Running on http://127.0.0.1:5000
```

✅ **Laissez ce terminal ouvert** (ne le fermez pas)

---

### Étape 2: Lancer le Frontend React

Ouvrez un **deuxième terminal** (nouvelle fenêtre) :

```bash
cd frontend
npm start
```

Vous verrez :
```
Compiled successfully!

You can now view distillation-simulator-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

Le navigateur s'ouvrira automatiquement sur **http://localhost:3000**

✅ **Laissez ce terminal ouvert aussi**

---

## 🌐 Accéder à l'Application

Une fois les deux serveurs lancés, ouvrez votre navigateur et allez à :

👉 **http://localhost:3000**

Vous verrez l'interface du **Simulateur de Distillation Multicomposants** !

---

## 🎯 Première Utilisation

1. **Onglet "Simulation"** est ouvert par défaut
2. La configuration BTX est déjà remplie :
   - Benzène : 33%
   - Toluène : 33%
   - Xylène : 34%
3. Cliquez sur **"Lancer la Simulation"** (bouton bleu)
4. Attendez 2-3 secondes
5. Les résultats s'affichent dans l'**onglet "Résultats"**

---

## ❌ Arrêter l'Application

### Si lancé avec le script
- Fermez les deux fenêtres de terminal qui se sont ouvertes

### Si lancé manuellement
Dans chaque terminal, appuyez sur :
- **Ctrl + C** (Windows/Linux)
- **Cmd + C** (Mac)

---

## 🔧 Problèmes Courants

### Problème 1: "npm n'est pas reconnu"
**Solution:**
- Installez Node.js depuis : https://nodejs.org/
- Choisissez la version LTS (recommandée)
- Redémarrez votre terminal après installation

### Problème 2: "Port 5000 déjà utilisé"
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [numéro_du_PID] /F

# Ou changez le port dans backend/app.py ligne 479
app.run(debug=True, host='0.0.0.0', port=5001)  # Changez 5000 en 5001
```

### Problème 3: "Port 3000 déjà utilisé"
**Solution:**
Le terminal vous demandera : "Would you like to run the app on another port instead?"
- Tapez **Y** et appuyez sur Entrée
- L'app se lancera sur le port 3001

### Problème 4: "Module not found"
**Solution pour Backend:**
```bash
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
```

**Solution pour Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problème 5: Page blanche dans le navigateur
**Solution:**
1. Vérifiez que le backend est lancé (terminal 1)
2. Ouvrez la console du navigateur (F12)
3. Vérifiez les erreurs
4. Essayez de rafraîchir avec **Ctrl + F5**

---

## 📱 Tester que tout fonctionne

### Test Backend
Ouvrez votre navigateur et allez à :
👉 **http://localhost:5000/api/health**

Vous devriez voir :
```json
{
  "status": "ok",
  "message": "Backend de simulation de distillation est opérationnel"
}
```

### Test Frontend
Ouvrez votre navigateur et allez à :
👉 **http://localhost:3000**

Vous devriez voir l'interface avec le titre :
**"Simulateur de Distillation Multicomposants"**

---

## 🎨 Captures d'écran de l'Interface

### Page Simulation
- Formulaire avec sélection de composés
- Sliders pour ajuster les paramètres
- Bouton "Lancer la Simulation"

### Page Résultats
- Cartes récapitulatives (N_real, R, etc.)
- Accordéons avec :
  * Bilans matières (tableaux + graphiques)
  * Dimensionnement (Fenske, Underwood, etc.)
  * Profils de composition (graphiques)
  * Profil de température
  * Débits internes

### Page Composés
- Liste de 13 composés
- Barre de recherche
- Cartes avec formules chimiques

---

## ⚡ Raccourcis Utiles

### Dans le Terminal
- **Ctrl + C** : Arrêter le serveur
- **↑** (flèche haut) : Commande précédente
- **Ctrl + L** : Effacer le terminal

### Dans le Navigateur
- **F12** : Ouvrir la console développeur
- **Ctrl + F5** : Rafraîchir sans cache
- **Ctrl + Shift + I** : Ouvrir les outils de développement

---

## 📊 Exemple de Simulation Rapide

1. Laissez la configuration par défaut (BTX)
2. Cliquez sur "Lancer la Simulation"
3. Attendez 2-3 secondes
4. Consultez les résultats :
   - **N_min** ≈ 8-10 plateaux
   - **R_min** ≈ 0.6-0.8
   - **N_réel** ≈ 15-20 plateaux
   - **Plateau alimentation** ≈ 8-10

---

## 🎓 Commandes à Copier-Coller

### Lancement complet (méthode manuelle)

**Terminal 1 :**
```bash
cd backend
python app.py
```

**Terminal 2 (nouvelle fenêtre) :**
```bash
cd frontend
npm start
```

### Installation des dépendances (si besoin)

**Backend :**
```bash
pip install Flask flask-cors numpy scipy pandas matplotlib thermo chemicals CoolProp
```

**Frontend :**
```bash
cd frontend
npm install
```

---

## ✅ Checklist de Lancement

- [ ] Backend lancé (terminal 1, port 5000)
- [ ] Frontend lancé (terminal 2, port 3000)
- [ ] http://localhost:5000/api/health répond OK
- [ ] http://localhost:3000 affiche l'interface
- [ ] Simulation de test réussie

**Si toutes les cases sont cochées, votre application fonctionne ! 🎉**

---

## 📞 Besoin d'Aide ?

1. Vérifiez la console du navigateur (F12)
2. Vérifiez les terminaux pour les erreurs
3. Consultez [README.md](README.md) pour plus de détails
4. Essayez [INSTALLATION_COMPLETE.md](INSTALLATION_COMPLETE.md)

---

**Bonne simulation ! 🧪✨**
