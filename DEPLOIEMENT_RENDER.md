# 🚀 Guide de Déploiement sur Render

## 📋 Prérequis

1. **Compte Render** : https://render.com (gratuit)
2. **Compte GitHub** : https://github.com (pour héberger le code)
3. **Git** installé sur votre machine

---

## 🎯 Étape 1 : Préparer le Code pour Git

### 1.1 Initialiser Git (si pas déjà fait)

```bash
git init
git add .
git commit -m "Initial commit - Distillation Simulator"
```

### 1.2 Créer un Repository sur GitHub

1. Allez sur https://github.com
2. Cliquez sur "New repository"
3. Nom : `distillation-simulator`
4. Public ou Private (votre choix)
5. Ne cochez RIEN (pas de README, .gitignore, etc.)
6. Cliquez "Create repository"

### 1.3 Pousser le Code vers GitHub

```bash
git remote add origin https://github.com/VOTRE_USERNAME/distillation-simulator.git
git branch -M main
git push -u origin main
```

---

## 🌐 Étape 2 : Déployer sur Render

### Option A : Déploiement Automatique avec render.yaml

1. **Allez sur** : https://render.com
2. **Connectez-vous** avec GitHub
3. **Cliquez sur** "New +"
4. **Sélectionnez** "Blueprint"
5. **Connectez votre repository** `distillation-simulator`
6. **Render détectera** automatiquement le fichier `render.yaml`
7. **Donnez un nom** au blueprint : `distillation-app`
8. **Cliquez sur** "Apply"

✅ Render va déployer automatiquement :
- Backend Flask sur : `https://distillation-backend.onrender.com`
- Frontend React sur : `https://distillation-frontend.onrender.com`

### Option B : Déploiement Manuel

#### Backend Flask

1. Sur Render Dashboard, cliquez "New +" → "Web Service"
2. Connectez votre repository GitHub
3. Configurez :
   - **Name** : `distillation-backend`
   - **Region** : Europe (Frankfurt)
   - **Branch** : `main`
   - **Root Directory** : `backend`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Plan** : Free
4. Cliquez "Create Web Service"

#### Frontend React

1. Sur Render Dashboard, cliquez "New +" → "Static Site"
2. Connectez votre repository GitHub
3. Configurez :
   - **Name** : `distillation-frontend`
   - **Branch** : `main`
   - **Root Directory** : `frontend`
   - **Build Command** : `npm install && npm run build`
   - **Publish Directory** : `build`
4. Ajoutez une variable d'environnement :
   - **Key** : `REACT_APP_API_URL`
   - **Value** : `https://distillation-backend.onrender.com/api`
5. Cliquez "Create Static Site"

---

## ⚙️ Étape 3 : Configuration Backend

### 3.1 Modifier app.py pour la Production

Le fichier `backend/app.py` doit utiliser l'host et le port de Render :

```python
if __name__ == '__main__':
    # Pour Render
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

Cette modification est **déjà faite** dans le code !

### 3.2 Variables d'Environnement Backend

Sur Render, dans les paramètres du backend, ajoutez :

- `FLASK_ENV` = `production`
- `PORT` = `10000` (Render l'assigne automatiquement)

---

## ⚙️ Étape 4 : Configuration Frontend

### 4.1 Mettre à Jour l'URL de l'API

Dans `frontend/.env` :

```
REACT_APP_API_URL=https://distillation-backend.onrender.com/api
```

### 4.2 Rebuild le Frontend

Après avoir déployé le backend et obtenu l'URL, mettez à jour le frontend :

1. Sur Render Dashboard → Frontend
2. Settings → Environment
3. Ajoutez `REACT_APP_API_URL` avec l'URL du backend
4. Manual Deploy → Deploy latest commit

---

## 🔧 Étape 5 : Configurer CORS

Le backend doit autoriser les requêtes du frontend. Dans `backend/app.py` :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",  # Développement
    "https://distillation-frontend.onrender.com"  # Production
])
```

Ceci est **déjà configuré** !

---

## ✅ Étape 6 : Vérification

### 6.1 Tester le Backend

Visitez : `https://distillation-backend.onrender.com/api/health`

Vous devriez voir :
```json
{
  "status": "ok",
  "message": "Backend de simulation de distillation est opérationnel"
}
```

### 6.2 Tester le Frontend

Visitez : `https://distillation-frontend.onrender.com`

L'interface devrait se charger !

### 6.3 Tester une Simulation

1. Allez sur le frontend
2. Laissez la configuration BTX
3. Cliquez "Lancer la Simulation"
4. Les résultats devraient s'afficher !

---

## 📊 URLs Finales

Après le déploiement :

- **Backend API** : `https://distillation-backend.onrender.com`
- **Frontend Web** : `https://distillation-frontend.onrender.com`
- **Swagger/Docs** : `https://distillation-backend.onrender.com/api/health`

---

## 🐛 Dépannage

### Problème 1 : Backend ne démarre pas

**Vérifiez les logs** :
- Render Dashboard → Backend → Logs

**Solutions** :
- Vérifiez que `requirements.txt` est correct
- Assurez-vous que `gunicorn` est dans les dépendances
- Vérifiez la version de Python (3.11)

### Problème 2 : Frontend ne se connecte pas au Backend

**Solution** :
- Vérifiez `REACT_APP_API_URL` dans les variables d'environnement
- Assurez-vous que CORS est configuré
- Vérifiez que le backend est bien en ligne

### Problème 3 : Erreur 502 Bad Gateway

**Solution** :
- Le backend est peut-être en sommeil (plan gratuit)
- Attendez 30-60 secondes qu'il se réveille
- Rafraîchissez la page

### Problème 4 : Build échoue

**Backend** :
```bash
# Vérifiez les dépendances
pip install -r backend/requirements.txt
```

**Frontend** :
```bash
cd frontend
npm install
npm run build
```

---

## 💡 Astuces Render

### Plan Gratuit

Le plan gratuit de Render :
- ✅ 750 heures/mois (suffisant pour 1 service)
- ✅ 512 MB RAM
- ⚠️ Le service s'endort après 15 min d'inactivité
- ⚠️ Temps de réveil : ~30 secondes

### Améliorer les Performances

1. **Upgrade au plan Starter** ($7/mois) :
   - Pas de mise en veille
   - 1 GB RAM
   - SSL automatique

2. **Optimiser le Code** :
   - Caching des résultats
   - Compression gzip
   - Minification frontend

---

## 🔄 Mises à Jour

Pour déployer une nouvelle version :

```bash
# Faire les modifications
git add .
git commit -m "Update: description des changements"
git push origin main
```

Render va **automatiquement** redéployer !

---

## 📱 Domaine Personnalisé (Optionnel)

### Avec Render

1. Dashboard → Frontend → Settings
2. Custom Domain
3. Ajoutez votre domaine (ex: `distillation.votredomaine.com`)
4. Configurez les DNS selon les instructions

### Avec Cloudflare (Gratuit)

1. Ajoutez votre site sur Cloudflare
2. Configurez un CNAME vers Render
3. Activez SSL/TLS Full

---

## 🎉 Félicitations !

Votre application est maintenant **déployée en production** !

Partagez le lien : `https://distillation-frontend.onrender.com`

---

## 📚 Ressources

- **Documentation Render** : https://render.com/docs
- **Support Render** : https://render.com/support
- **Status Render** : https://status.render.com

---

## 🔐 Sécurité

### Recommandations

1. ✅ Ne commitez JAMAIS de secrets/clés API
2. ✅ Utilisez les variables d'environnement
3. ✅ Activez HTTPS (automatique sur Render)
4. ✅ Limitez les taux de requêtes (rate limiting)

### Variables Sensibles

Si vous ajoutez des clés API plus tard :

```bash
# Render Dashboard → Environment Variables
API_KEY=votre_cle_secrete
DATABASE_URL=postgresql://...
```

---

**Bon déploiement ! 🚀**
