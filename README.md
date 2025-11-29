# Application de Distillation Multicomposants

Application web interactive pour la simulation et l'optimisation de colonnes de distillation multicomposants.

**Technologies:** Python + Streamlit | React (Frontend optionnel)
**Version:** 3.1

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
- **Génération PDF Automatique:** Compilation LaTeX en ligne (sans installation)
- **13 Composés:** Aromatiques, Alcools, Alcanes
- **Visualisations Interactives:** Plotly
- **Export:** Excel, PDF

---

## 📚 Structure

```
├── streamlit_app_enhanced.py        # Interface Streamlit
├── distillation_multicomposants.py  # Méthodes simplifiées
├── mesh_solver.py                   # MESH rigoureux
├── activity_models.py               # Modèles thermodynamiques
├── economic_optimization.py         # Optimisation TAC
├── pdf_generator.py                 # Génération PDF (compilation en ligne)
├── frontend/                        # Interface React (optionnelle)
└── requirements.txt                 # Dépendances
```

Voir [STRUCTURE.md](STRUCTURE.md) pour plus de détails.

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
- [STRUCTURE.md](STRUCTURE.md) - Architecture du projet

---

## 🎯 Nouveautés Version 3.1

- ✅ **Génération PDF automatique** - Compilation LaTeX en ligne (LaTeX-on-HTTP)
- ✅ **Page de garde professionnelle** - Design épuré sans mentions académiques
- ✅ **Table des matières cliquable** - Navigation interactive dans le PDF
- ✅ **Aucune installation requise** - Pas besoin de MiKTeX ou Chocolatey
- ✅ **Conclusion détaillée** - Résumé complet avec liste des résultats

---

**Version:** 3.1
**Statut:** ✅ Production Ready
