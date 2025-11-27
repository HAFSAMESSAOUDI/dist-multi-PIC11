# Application de Distillation Multicomposants

Application web interactive pour la simulation et l'optimisation de colonnes de distillation multicomposants.

**Module:** Modélisation et Simulation des Procédés
**Professeur:** BAKHER Zine Elabidine
**Filière:** Procédés Industriels et Chimiques (PIC)
**Université:** Hassan 1er
**Version:** 2.2

---

## 🚀 Démarrage Rapide

### Installation

```bash
pip install -r requirements.txt
```

### Lancement

**Windows:**
```bash
run_enhanced.bat
```

**Linux/Mac:**
```bash
chmod +x run_enhanced.sh
./run_enhanced.sh
```

L'application s'ouvre automatiquement à http://localhost:8501

---

## ✨ Fonctionnalités

- **Méthodes Simplifiées:** Fenske, Underwood, Gilliland, Kirkbride
- **MESH Rigoureux:** Algorithme Wang-Henke
- **Modèles Thermodynamiques:** Idéal, Wilson, NRTL, UNIQUAC
- **Optimisation Économique:** TAC (Total Annualized Cost)
- **13 Composés:** Aromatiques, Alcools, Alcanes
- **Visualisations Interactives:** Plotly

---

## 📚 Structure

```
├── streamlit_app_enhanced.py        # Interface Streamlit
├── distillation_multicomposants.py  # Méthodes simplifiées
├── mesh_solver.py                   # MESH rigoureux
├── activity_models.py               # Modèles thermodynamiques
├── economic_optimization.py         # Optimisation TAC
└── requirements.txt                 # Dépendances
```

---

## 🎓 Utilisation

1. **Sélectionner** 2-6 composés
2. **Définir** compositions (somme = 1.0)
3. **Configurer** paramètres (F, P, récupérations, R/R_min)
4. **Choisir** méthode (Simplifiées / MESH / Comparaison)
5. **Lancer** simulation

---

## 📊 Exemples

### BTX (Système Idéal)
- Benzène 33.3%, Toluène 33.3%, o-Xylène 33.4%
- F=100 kmol/h, P=1.013 bar
- Résultats: N_min≈4.6, R_min≈2.5, N_real≈10

### Éthanol-Eau (Azéotrope)
- Éthanol 10%, Eau 90%
- Modèle NRTL obligatoire
- Limitation: 95.6% éthanol max

---

## 🎯 Équations (20)

- **Éq. 1-8:** Méthodes Simplifiées
- **Éq. 9-13:** MESH (M, E, S, H)
- **Éq. 14-16:** Modèles d'Activité
- **Éq. 17-20:** Optimisation TAC

---

## 💡 Recommandations

| Système | Modèle |
|---------|--------|
| Hydrocarbures | Idéal |
| Alcools | Wilson |
| Azéotropes | **NRTL** |

---

## 📝 Documentation

- Documentation théorique intégrée dans l'app
- [QUICKSTART.md](QUICKSTART.md) - Guide rapide

---

**Version:** 2.2
**Statut:** ✅ Production Ready
