# ⚡ Déploiement Rapide sur Render (5 minutes)

## 🚀 Étapes Ultra-Rapides

### 1️⃣ Préparer GitHub (2 min)

```bash
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "App distillation multicomposants"

# Créer repo sur GitHub et pusher
# (Remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/distillation-app.git
git branch -M main
git push -u origin main
```

### 2️⃣ Déployer sur Render (3 min)

1. **Allez sur** : https://render.com
2. **Connectez GitHub**
3. **New** → **Blueprint**
4. **Sélectionnez votre repo** `distillation-app`
5. **Apply** (Render détecte le `render.yaml`)

✅ **C'EST TOUT !** Attendez 5-10 minutes pour le build.

---

## 🌐 URLs après Déploiement

- **Backend** : `https://distillation-backend.onrender.com`
- **Frontend** : `https://distillation-frontend.onrender.com`

---

## 🎯 Test Rapide

Visitez : `https://distillation-backend.onrender.com/api/health`

Si vous voyez `{"status": "ok"}` → ✅ Ça marche !

---

## 📝 Checklist

- [ ] Git initialisé
- [ ] Code pushé sur GitHub
- [ ] Compte Render créé
- [ ] Blueprint déployé
- [ ] Backend accessible
- [ ] Frontend accessible
- [ ] Simulation teste fonctionne

---

## ⚠️ Important

**Premier démarrage** : 5-10 minutes de build
**Plan gratuit** : Le service s'endort après 15 min d'inactivité

**Pour rester éveillé** : Utilisez un service comme **UptimeRobot** pour ping toutes les 14 minutes.

---

**Déploiement terminé ! 🎉**
