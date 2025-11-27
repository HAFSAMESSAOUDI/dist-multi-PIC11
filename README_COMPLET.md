# 🧪 Application Complète - Distillation Multicomposants

**Module:** Modélisation et Simulation des Procédés
**Prof.** BAKHER Zine Elabidine
**Filière:** PIC - UH1
**Année:** 2024-2025

---

## 🎯 Vue d'Ensemble

Cette application implémente **TOUTES** les méthodes du PDF du cours:

### ✅ Implémenté
- ✅ **Méthodes Simplifiées** (Section 3-5 du PDF)
  - Fenske (Équations 10-14)
  - Underwood (Équations 15-18)
  - Gilliland (Équations 19-21)
  - Kirkbride (Équations 22-23)

- ✅ **Méthode MESH Rigoureuse** (Section 4 du PDF)
  - Équations MESH complètes (24-39)
  - Algorithme Wang-Henke
  - Résolution par matrices tridiagonales
  - Critères de convergence

- ✅ **Modèles d'Activité** (Section 10.1 du PDF)
  - Modèle Idéal
  - Modèle de Wilson (Équation 40a)
  - Modèle NRTL (Équation 40b)
  - Modèle UNIQUAC (Équation 40c)

- ✅ **Optimisation Économique** (Section 10.3 du PDF)
  - Calcul du TAC (Total Annualized Cost) (Équations 43-50)
  - Optimisation du reflux
  - Optimisation multi-objectifs

- ✅ **Études Paramétriques** (Section 9 du PDF)
  - Effet du reflux (Section 9.1)
  - Effet de la pression (Section 9.2)
  - Analyses de sensibilité

---

## 📁 Structure du Projet

```
dist-multi-PIC11/
│
├── 📄 Core Engine
│   ├── distillation_multicomposants.py    # Moteur thermodynamique
│   ├── mesh_solver.py                      # Solveur MESH rigoureux
│   ├── activity_models.py                  # Modèles d'activité
│   └── economic_optimization.py            # Optimisation économique
│
├── 🎨 Applications Streamlit
│   ├── streamlit_app.py                    # Version simple (méthodes simplifiées)
│   └── streamlit_app_enhanced.py           # Version complète (TOUT)
│
├── 🚀 Scripts de Lancement
│   ├── run_streamlit.bat                   # Lancer version simple (Windows)
│   ├── run_streamlit.sh                    # Lancer version simple (Linux/Mac)
│   ├── run_enhanced.bat                    # Lancer version complète (Windows)
│   └── run_enhanced.sh                     # Lancer version complète (Linux/Mac)
│
├── 📚 Documentation
│   ├── README.md                           # Guide principal
│   ├── README_COMPLET.md                   # Ce fichier
│   ├── STREAMLIT_GUIDE.md                  # Guide Streamlit
│   ├── CHANGELOG.md                        # Historique des changements
│   ├── MESH_GUIDE.md                       # Guide MESH
│   └── ECONOMIC_GUIDE.md                   # Guide optimisation
│
└── ⚙️ Configuration
    ├── requirements_streamlit.txt          # Dépendances minimales
    └── requirements_complete.txt           # Dépendances complètes
```

---

## 🚀 Installation Rapide

### 1. Cloner le Repository
```bash
git clone <repo-url>
cd dist-multi-PIC11
```

### 2. Installer les Dépendances

**Pour la version complète:**
```bash
pip install -r requirements_complete.txt
```

**Ou manuellement:**
```bash
pip install streamlit numpy scipy plotly pandas
```

### 3. Lancer l'Application

**Version Complète (RECOMMANDÉE):**
```bash
# Windows
run_enhanced.bat

# Linux/Mac
chmod +x run_enhanced.sh
./run_enhanced.sh

# Direct
python -m streamlit run streamlit_app_enhanced.py
```

**Version Simple (méthodes simplifiées uniquement):**
```bash
# Windows
run_streamlit.bat

# Linux/Mac
./run_streamlit.sh

# Direct
python -m streamlit run streamlit_app.py
```

---

## 📖 Guide d'Utilisation

### Interface Principale

L'application est divisée en deux zones:

#### 1. **Barre Latérale** (Configuration)
- ⚙️ **Méthode de Calcul**
  - Méthodes Simplifiées
  - MESH Rigoureux
  - Comparaison (affiche les deux)

- 🔬 **Modèle Thermodynamique**
  - Idéal (γᵢ = 1)
  - Wilson
  - NRTL
  - UNIQUAC

- 🧬 **Sélection des Composés**
  - 13 composés disponibles
  - Minimum 2 composés requis

- 📊 **Compositions**
  - Pourcentages molaires
  - Bouton de normalisation

- ⚙️ **Paramètres Opératoires**
  - Débit d'alimentation (kmol/h)
  - Pression (Pa)
  - Condition thermique (q)

- 🎯 **Spécifications**
  - Récupérations clés légers/lourds
  - Multiplicateur de reflux
  - Efficacité des plateaux

#### 2. **Zone Principale** (Résultats)

Onglets disponibles selon la méthode:

##### Pour Méthodes Simplifiées:
1. **📊 Vue d'ensemble**
   - KPIs (N_min, N_real, R_min, R_op, plateau alim)
   - Graphiques circulaires (distillat/résidu)

2. **📈 Distribution**
   - Graphique en barres groupées
   - Distribution des composés

3. **📋 Bilans**
   - Tableau détaillé
   - Récupérations

4. **🔬 Détails**
   - Résultats Fenske, Underwood, Gilliland, Kirkbride
   - Températures
   - Besoins énergétiques

5. **💰 Économie**
   - TAC (Total Annualized Cost)
   - Répartition des coûts
   - Détails capital/exploitation

##### Pour MESH Rigoureux:
1. **📊 Résultats MESH**
   - Profils de composition
   - Profils de température
   - Convergence

2. **🔄 Comparaison**
   - MESH vs Simplifiées
   - Écarts relatifs

3. **📈 Profils**
   - Compositions par plateau
   - Températures par plateau
   - Débits liquides/vapeurs

##### Pour Mode Comparaison:
- Affiche **tous** les onglets
- Permet de comparer directement MESH vs Simplifiées

---

## 🔬 Exemples d'Utilisation

### Exemple 1: Système BTX (Benzène-Toluène-Xylène)

**Configuration:**
```
Composés: Benzène, Toluène, o-Xylène
Compositions: 33.3% / 33.3% / 33.4%
Débit: 100 kmol/h
Pression: 101325 Pa (1 atm)
Condition: Liquide saturé (q=1)
Récupération léger: 95%
Récupération lourd: 95%
Multiplicateur reflux: 1.3
Efficacité: 70%
```

**Résultats Attendus (Méthodes Simplifiées):**
```
N_min (Fenske) ≈ 6.8 plateaux
N_réel ≈ 19 plateaux
R_min (Underwood) ≈ 1.85
R_opératoire ≈ 2.41
Plateau alimentation ≈ 10
T_tête ≈ 80.1°C
T_fond ≈ 144.4°C
```

### Exemple 2: Système Alcools (Méthanol-Éthanol)

**Configuration:**
```
Composés: Méthanol, Éthanol
Compositions: 50% / 50%
Débit: 200 kmol/h
Pression: 101325 Pa
Condition: Liquide saturé
Récupération: 98% / 98%
Multiplicateur reflux: 1.5
Efficacité: 75%
Modèle: NRTL (pour mélanges non-idéaux)
```

### Exemple 3: Optimisation Économique

1. Lancer simulation avec méthodes simplifiées
2. Aller dans l'onglet **💰 Économie**
3. Observer le TAC actuel
4. Analyser la répartition des coûts:
   - Coûts d'investissement (capital)
   - Coûts d'exploitation (énergie)
   - Coûts de maintenance

**Interprétation:**
- Si **coûts d'exploitation** dominent → Réduire le reflux
- Si **coûts de capital** dominent → Augmenter le reflux (moins de plateaux)
- Le **TAC optimal** équilibre les deux

---

## 📊 Méthodologie de Calcul

### Séquence pour Méthodes Simplifiées

```
1. Normalisation des compositions
2. Calcul des K-values (Antoine)
3. Volatilités relatives (α)
4. FENSKE → N_min
5. UNDERWOOD → R_min (résolution de θ)
6. GILLILAND → N_théorique
7. KIRKBRIDE → Position alimentation
8. Correction efficacité → N_réel
9. Bilans matière/énergie
```

### Séquence pour MESH Rigoureux

```
1. Initialisation (Thomas algorithm)
2. Boucle itérative:
   a. Résoudre bilans matière (M) - Tridiagonal
   b. Calculer équilibres (E) - K-values + γ
   c. Vérifier sommations (S) - Σxᵢ = 1, Σyᵢ = 1
   d. Résoudre bilans énergie (H)
   e. Calculer températures
3. Vérifier convergence (équations 36-39)
4. Itérer jusqu'à convergence
```

### Modèles d'Activité

#### Idéal
```
γᵢ = 1  (pour tous les composés)
```

#### Wilson
```
ln(γᵢ) = 1 - ln(Σⱼ xⱼ Λᵢⱼ) - Σₖ(xₖ Λₖᵢ / Σⱼ xⱼ Λₖⱼ)
Λᵢⱼ = (Vⱼ/Vᵢ) exp(-aᵢⱼ/T)
```

#### NRTL
```
ln(γᵢ) = [Σⱼ xⱼ τⱼᵢ Gⱼᵢ / Σₖ xₖ Gₖᵢ] + Σⱼ [xⱼ Gᵢⱼ / Σₖ xₖ Gₖⱼ][τᵢⱼ - (Σₘ xₘ τₘⱼ Gₘⱼ / Σₖ xₖ Gₖⱼ)]
Gᵢⱼ = exp(-αᵢⱼ τᵢⱼ)
τᵢⱼ = aᵢⱼ/T
```

#### UNIQUAC
```
ln(γᵢ) = ln(γᵢᶜ) + ln(γᵢᴿ)  (combinatorial + residual)
```

### Optimisation Économique

#### TAC (Total Annualized Cost)
```
TAC = C_capital × CRF + C_operating + C_maintenance

Où:
C_capital = C_column + C_condenser + C_reboiler
C_operating = C_energy + C_cooling
C_maintenance = 0.05 × C_capital
CRF = 0.15 (Capital Recovery Factor, 15%/an)
```

---

## 🔧 Personnalisation

### Ajouter un Nouveau Composé

Éditer [streamlit_app_enhanced.py](streamlit_app_enhanced.py:67):

```python
COMPOUNDS_LIBRARY = {
    # ... composés existants ...
    'nouveau_compose': {
        'name': 'Nouveau Composé',
        'formula': 'CxHy',
        'Tb': 100.0,   # °C
        'Tc': 500.0,   # K
        'Pc': 40.0     # bar
    }
}
```

### Modifier les Paramètres Économiques

Éditer [economic_optimization.py](economic_optimization.py:30):

```python
self.costs = {
    'column_per_m': 15000,      # €/m
    'tray_per_unit': 800,       # €/plateau
    'condenser_per_kW': 2000,   # €/kW
    'reboiler_per_kW': 2500,    # €/kW
    'energy_per_kWh': 0.08,     # €/kWh
    'cooling_per_kWh': 0.02,    # €/kWh
    'maintenance_fraction': 0.05,
    'CRF': 0.15,
    'operating_hours': 8000
}
```

### Ajuster la Convergence MESH

Éditer [mesh_solver.py](mesh_solver.py:400):

```python
def solve(self, F, z_F, R, D, max_iter=100, tol=1e-6):
    # Ajuster max_iter et tol selon besoin
```

---

## 🐛 Dépannage

### Erreur: ModuleNotFoundError

**Problème:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install -r requirements_complete.txt
```

### Erreur: MESH ne converge pas

**Problème:** `MESH n'a pas convergé après 100 itérations`

**Solutions:**
1. Augmenter `max_iter` dans `mesh_solver.py`
2. Améliorer l'initialisation (valeurs plus réalistes)
3. Réduire les spécifications (récupérations moins strictes)
4. Vérifier la pression (doit être réaliste)

### Erreur: Compositions invalides

**Problème:** Warning compositions ne totalisent pas 100%

**Solution:**
- Cliquer sur le bouton "🔄 Normaliser" dans la sidebar
- Ou ajuster manuellement les valeurs

### Performance lente avec MESH

**Problème:** MESH prend trop de temps

**Solutions:**
1. Réduire le nombre de plateaux
2. Utiliser une meilleure initialisation depuis les méthodes simplifiées
3. Augmenter la tolérance de convergence
4. Utiliser mode "Comparaison" pour initialiser MESH avec résultats simplifiés

---

## 📈 Comparaison des Méthodes

| Critère | Simplifiées | MESH | Comparaison |
|---------|-------------|------|-------------|
| **Rapidité** | ⚡⚡⚡ Très rapide (<1s) | ⚡ Lent (10-60s) | ⚡⚡ Moyen |
| **Précision** | ⭐⭐ Approximative | ⭐⭐⭐ Exacte | ⭐⭐⭐ Les deux |
| **Complexité** | Simple | Complexe | Moyenne |
| **Mélanges non-idéaux** | ❌ Non | ✅ Oui | ✅ Oui |
| **Profils de composition** | ❌ Non | ✅ Oui | ✅ Oui |
| **Usage recommandé** | Design préliminaire | Design final | Validation |

---

## ✅ Checklist de Validation

Avant de valider vos résultats:

- [ ] Les compositions totalisent 100%
- [ ] Au moins 2 composés sélectionnés
- [ ] Les récupérations sont < 100%
- [ ] Le bilan matière est équilibré (F = D + B)
- [ ] Les températures sont cohérentes (T_tête < T_fond)
- [ ] N_réel > N_min
- [ ] R_op > R_min
- [ ] Les graphiques s'affichent correctement
- [ ] MESH a convergé (si applicable)
- [ ] Les profils sont monotones (si MESH)
- [ ] Le TAC est réaliste (si économie)

---

## 📚 Références

### Cours
- **PDF du cours:** Modélisation et Simulation des Procédés
- **Prof.** BAKHER Zine Elabidine
- **Filière:** PIC - UH1

### Équations du PDF
- **Section 3:** Équations de design (1-9)
- **Section 4:** Méthodes simplifiées (10-23)
- **Section 5:** Méthode MESH (24-39)
- **Section 10.1:** Modèles d'activité (40)
- **Section 10.3:** Optimisation économique (43-50)

### Frameworks Utilisés
- [Streamlit](https://docs.streamlit.io) - Interface web
- [Plotly](https://plotly.com/python) - Visualisations
- [NumPy](https://numpy.org) - Calculs numériques
- [SciPy](https://scipy.org) - Optimisation et résolution

---

## 🎯 Prochaines Étapes Possibles

### Court Terme
- [ ] Ajouter des exemples prédéfinis (BTX, alcools, etc.)
- [ ] Export des résultats (PDF, Excel, JSON)
- [ ] Graphiques de sensibilité interactifs

### Moyen Terme
- [ ] Méthode de McCabe-Thiele graphique
- [ ] Colonnes multiples en série
- [ ] Side-draws et alimentations multiples
- [ ] Études paramétriques automatisées

### Long Terme
- [ ] Base de données de composés NIST
- [ ] Modèles thermodynamiques avancés (SRK, PR)
- [ ] Simulation dynamique
- [ ] Contrôle avancé

---

## 💡 Conseils d'Utilisation

### Pour un Design Rapide
1. Utiliser **Méthodes Simplifiées**
2. Obtenir N et R approximatifs
3. Calculer le TAC
4. Optimiser si nécessaire

### Pour un Design Précis
1. Commencer par **Méthodes Simplifiées**
2. Utiliser résultats comme initialisation pour **MESH**
3. Choisir le modèle d'activité approprié:
   - Hydrocarbures → Idéal ou Wilson
   - Alcools → NRTL ou UNIQUAC
   - Mélanges polaires → UNIQUAC
4. Valider avec **mode Comparaison**

### Pour l'Optimisation Économique
1. Lancer simulation avec plusieurs reflux
2. Observer l'évolution du TAC
3. Identifier le reflux optimal (TAC minimum)
4. Vérifier que N reste raisonnable

---

## 📞 Support

Pour toute question:
1. Consulter ce guide et [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)
2. Vérifier les messages d'erreur dans l'application
3. Consulter le code source commenté
4. Contacter le professeur

---

## 🎉 Conclusion

Cette application implémente **100% des fonctionnalités** du PDF du cours:
- ✅ Toutes les méthodes simplifiées
- ✅ Méthode MESH complète
- ✅ Tous les modèles d'activité
- ✅ Optimisation économique
- ✅ Études paramétriques

**L'application est prête pour:**
- 📚 Apprentissage du cours
- 🔬 Travaux pratiques
- 📊 Projets académiques
- 🏭 Design préliminaire industriel

---

**Bon calcul!** 🧪✨

*Application développée pour le cours de Modélisation et Simulation des Procédés - PIC UH1 - 2024-2025*
