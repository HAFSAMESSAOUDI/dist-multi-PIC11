# Démarrage Rapide - Application de Distillation

## 🚀 Lancement en 30 Secondes

### Windows
```bash
run_enhanced.bat
```

### Linux/Mac
```bash
chmod +x run_enhanced.sh
./run_enhanced.sh
```

### Direct
```bash
python -m streamlit run streamlit_app_enhanced.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## 📋 Utilisation Simple

### Étape 1: Choisir les Composés
- Sélectionnez 2 composés ou plus dans la liste
- Entrez leurs compositions (en fractions molaires)
- Le total doit faire 1.0

### Étape 2: Paramètres de Simulation
- **Débit d'alimentation** (kmol/h): 100 par défaut
- **Pression** (bar): 1.013 par défaut
- **Taux de récupération**: 98% pour léger et lourd

### Étape 3: Choisir la Méthode
- **Méthodes Simplifiées**: Rapide, design préliminaire
- **MESH Rigoureux**: Précis, design final
- **Comparaison**: Voir les deux résultats côte à côte

### Étape 4: Lancer la Simulation
Cliquez sur "Lancer la Simulation" et attendez quelques secondes.

---

## 📊 Interpréter les Résultats

### Paramètres Clés

**N** - Nombre de plateaux théoriques
- Plus élevé = meilleure séparation mais plus coûteux
- Typiquement entre 10 et 50 plateaux

**R** - Ratio de reflux
- Plus élevé = meilleure séparation mais plus d'énergie
- Généralement 1.2 à 1.5 fois le reflux minimal

**TAC** - Total Annualized Cost (€/an)
- Coût total annualisé de la colonne
- Plus bas = design plus économique
- Compromis entre capital et exploitation

### Profils de Composition
- X-axis: Numéro du plateau (1 = rebouilleur, N = condenseur)
- Y-axis: Fraction molaire de chaque composé
- Léger: concentration élevée en haut
- Lourd: concentration élevée en bas

### Profils de Température
- Température croissante du haut vers le bas
- Discontinuité possible à l'alimentation

---

## 🎯 Exemples Rapides

### Exemple 1: Mélange Benzène-Toluène (BTX)
```
Composés: Benzène + Toluène
Compositions: 0.5 / 0.5
Débit: 100 kmol/h
Pression: 1.013 bar
Récupération: 98% / 98%
Méthode: Méthodes Simplifiées

Résultat attendu: N ≈ 8-10, R ≈ 2.5-3.0
```

### Exemple 2: Mélange Ternaire
```
Composés: Benzène + Toluène + Xylène
Compositions: 0.4 / 0.4 / 0.2
Débit: 150 kmol/h
Pression: 1.013 bar
Méthode: MESH Rigoureux
Modèle: Wilson

Résultat: Profils détaillés par plateau
```

---

## ⚠️ Résolution de Problèmes Courants

### "Application ne démarre pas"
```bash
# Vérifier Python
python --version  # Doit être 3.8+

# Installer les dépendances
pip install -r requirements.txt
```

### "Erreur lors de la simulation"
- Vérifier que la somme des compositions = 1.0
- Vérifier que les taux de récupération sont < 100%
- Essayer avec un reflux multiplier plus élevé (1.5 au lieu de 1.2)

### "Résultats incohérents"
- Vérifier l'ordre des composés (léger → lourd)
- Pour MESH: essayer un modèle d'activité différent
- Augmenter le nombre de plateaux si la séparation est insuffisante

---

## 📚 Documentation Complète

Pour plus de détails:
- [README.md](README.md) - Vue d'ensemble
- [README_COMPLET.md](README_COMPLET.md) - Guide exhaustif (700+ lignes)
- [STATUS.md](STATUS.md) - État du projet
- [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) - Détails techniques

---

## 🎓 Équations Implémentées

### Méthodes Simplifiées
- **Fenske** (Éq. 10-14): Nₘᵢₙ
- **Underwood** (Éq. 15-18): Rₘᵢₙ
- **Gilliland** (Éq. 19-21): N réel
- **Kirkbride** (Éq. 22-23): Position alimentation

### MESH Rigoureux
- **Équations 24-39**: M, E, S, H equations
- **Algorithme Wang-Henke**: Résolution matricielle

### Modèles Thermodynamiques
- **Idéal**: γᵢ = 1
- **Wilson** (Éq. 40a): Modèle d'activité
- **NRTL** (Éq. 40b): Non-Random Two Liquid
- **UNIQUAC** (Éq. 40c): Universal Quasi-Chemical

### Optimisation Économique
- **TAC** (Éq. 43-50): Total Annualized Cost

---

## 💡 Conseils d'Utilisation

### Pour un Design Préliminaire
1. Utiliser "Méthodes Simplifiées"
2. Obtenir N et R rapidement
3. Évaluer le TAC approximatif

### Pour un Design Final
1. Utiliser "MESH Rigoureux"
2. Choisir le modèle d'activité approprié
3. Vérifier les profils de composition
4. Optimiser le reflux pour minimiser le TAC

### Pour Comparer
1. Utiliser "Mode Comparaison"
2. Voir les écarts entre simplifiées et rigoureux
3. Décider si la méthode simplifiée est suffisante

---

## 🔗 Liens Utiles

**Documentation**
- Streamlit: https://docs.streamlit.io
- Thermo library: https://thermo.readthedocs.io

**Cours**
- PDF du cours (sections 3-10)
- Prof. BAKHER Zine Elabidine - PIC UH1

---

**Version:** 2.0 Enhanced
**Date:** 2025-11-27
**Statut:** ✅ Production Ready

Bon design ! 🎯
