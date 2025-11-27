# 🧪 Simulateur de Distillation Multicomposants

**Application Streamlit Interactive Complète**

**Module:** Modélisation et Simulation des Procédés
**Prof.** BAKHER Zine Elabidine
**Filière:** Procédés et Ingénierie Chimique (PIC)
**Université:** UH1
**Année:** 2024-2025

---

## 📖 Description

Application web interactive de simulation de colonnes de distillation multicomposants, construite avec **Streamlit** et implémentant **100% des méthodes du PDF du cours**.

### 🎯 Deux Versions Disponibles

#### 1. **Version Simple** (`streamlit_app.py`)
- ✅ Méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
- ✅ Interface épurée
- ✅ Calculs rapides (<1s)
- 📚 **Idéale pour:** Apprentissage, design préliminaire

#### 2. **Version Complète** (`streamlit_app_enhanced.py`) ⭐ RECOMMANDÉE
- ✅ **TOUT** de la version simple
- ✅ Méthode MESH rigoureuse (Wang-Henke)
- ✅ Modèles d'activité (Wilson, NRTL, UNIQUAC)
- ✅ Optimisation économique (TAC)
- ✅ Études paramétriques
- ✅ Mode comparaison (MESH vs Simplifiées)
- 📚 **Idéale pour:** Projets, design final, validation

### ✨ Fonctionnalités Complètes

#### Implémentées selon le PDF:
- ✅ **Section 3-5:** Méthodes simplifiées (Équations 10-23)
- ✅ **Section 4:** Méthode MESH rigoureuse (Équations 24-39)
- ✅ **Section 10.1:** Modèles d'activité (Équation 40)
- ✅ **Section 10.3:** Optimisation économique (Équations 43-50)
- ✅ **Section 9:** Études paramétriques (reflux, pression)

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+

### Installation Complète

```bash
# Cloner le projet
git clone [repository-url]
cd dist-multi-PIC11

# Installer les dépendances complètes
pip install -r requirements_complete.txt
```

---

## ⚡ Lancement

### Version Complète ⭐ RECOMMANDÉE

**Windows:**
```bash
run_enhanced.bat
```

**Linux/Mac:**
```bash
chmod +x run_enhanced.sh
./run_enhanced.sh
```

**Direct:**
```bash
python -m streamlit run streamlit_app_enhanced.py
```

### Version Simple

**Windows:**
```bash
run_streamlit.bat
```

**Linux/Mac:**
```bash
./run_streamlit.sh
```

**Direct:**
```bash
python -m streamlit run streamlit_app.py
```

### Linux/Mac
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

### Commande directe
```bash
streamlit run streamlit_app.py
```

L'application s'ouvre automatiquement dans votre navigateur à **http://localhost:8501**

---

## 📁 Structure du Projet

```
dist-multi-PIC11/
│
├── streamlit_app.py                   # ✅ Application principale Streamlit
├── distillation_multicomposants.py   # Moteur de calcul
│
├── requirements_streamlit.txt         # Dépendances Python
│
├── run_streamlit.bat                  # Lancement Windows
├── run_streamlit.sh                   # Lancement Linux/Mac
│
└── README.md                          # Ce fichier
```

---

## ✨ Fonctionnalités

### 🔬 Méthodes Implémentées
- ✅ **Fenske**: Nombre minimum de plateaux (N_min)
- ✅ **Underwood**: Reflux minimum (R_min)
- ✅ **Gilliland**: Corrélation plateaux/reflux
- ✅ **Kirkbride**: Position plateau d'alimentation

### 🎨 Interface Streamlit

#### Barre latérale
- Sélection des composés (multi-select)
- Configuration des compositions (%)
- Paramètres opératoires (débit, pression, condition d'alimentation)
- Spécifications de séparation (récupérations, reflux, efficacité)
- Bouton de simulation

#### Zone principale
- **5 KPIs** : N_min, N_réel, R_min, R_op, Plateau d'alimentation
- **4 Onglets** :
  - 📊 **Vue d'ensemble** : Compositions distillat/résidu + 3 jauges de performance
  - 📈 **Distribution** : Graphique barres des composés
  - 📋 **Bilans matières** : Tableau détaillé
  - 🔬 **Résultats détaillés** : Toutes les méthodes + températures + énergie

### 🧬 Composés Disponibles
13 composés prédéfinis:
- **Aromatiques**: Benzène, Toluène, o-Xylène, Éthylbenzène, Cumène, Styrène
- **Alcools**: Méthanol, Éthanol, 1-Propanol, 1-Butanol
- **Alcanes**: Hexane, Heptane, Octane

---

## 📊 Exemple: Cas BTX

### Configuration dans Streamlit

1. **Composés sélectionnés:**
   - Benzène
   - Toluène
   - o-Xylène

2. **Compositions:**
   - Benzène: 33.3%
   - Toluène: 33.3%
   - o-Xylène: 33.4%

3. **Paramètres opératoires:**
   - Débit d'alimentation: 100 kmol/h
   - Pression: 101325 Pa (1 atm)
   - Condition: Liquide saturé (q=1)

4. **Spécifications:**
   - Récupération léger: 95%
   - Récupération lourd: 95%
   - Multiplicateur reflux: 1.3
   - Efficacité: 70%

### Résultats Attendus
```
✅ N min (Fenske) = 6.8 plateaux
✅ N réel = 19 plateaux
✅ R min (Underwood) = 1.85
✅ R opératoire = 2.41
✅ Plateau alimentation = 10
✅ T tête = 80.1°C
✅ T fond = 138.5°C
```

---

## 🔧 Technologies

### Backend Python
- **Streamlit** 1.28+ : Framework web
- **NumPy** : Calculs numériques
- **SciPy** : Résolution d'équations
- **Plotly** : Visualisations interactives
- **Pandas** : Manipulation de données

### Moteur de Calcul
- **distillation_multicomposants.py** : Classes ThermodynamicPackage et Compound
- Équations thermodynamiques (Antoine, K-values, etc.)
- Méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)

---

## 🎨 Personnalisation

### Ajouter un Composé

Éditez le dictionnaire `COMPOUNDS_LIBRARY` dans [streamlit_app.py](streamlit_app.py):

```python
COMPOUNDS_LIBRARY = {
    'nouveau_compose': {
        'name': 'Nouveau Composé',
        'formula': 'CxHy',
        'Tb': 100.0,  # Température d'ébullition (°C)
        'Tc': 500.0,  # Température critique (K)
        'Pc': 40.0    # Pression critique (bar)
    }
}
```

### Modifier le Style

Le CSS personnalisé se trouve au début de [streamlit_app.py](streamlit_app.py):

```python
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    /* Personnalisez ici */
</style>
""", unsafe_allow_html=True)
```

---

## 📚 Utilisation

### 1. Sélectionner les Composés
Dans la barre latérale, choisissez **au moins 2 composés** dans le menu déroulant.

### 2. Définir les Compositions
Ajustez les pourcentages pour chaque composé. Utilisez le bouton **"Normaliser"** pour ajuster automatiquement à 100%.

### 3. Configurer les Paramètres
- Débit d'alimentation (kmol/h)
- Pression (Pa)
- Condition d'alimentation (liquide saturé, vapeur, etc.)

### 4. Spécifier la Séparation
- Récupérations des composés léger et lourd (%)
- Multiplicateur de reflux (1.1 à 3.0)
- Efficacité des plateaux (50% à 95%)

### 5. Lancer la Simulation
Cliquez sur **"🚀 LANCER LA SIMULATION"** et consultez les résultats dans les 4 onglets.

---

## 🐛 Dépannage

### Erreur: Module non trouvé
```bash
pip install -r requirements_streamlit.txt
```

### Port déjà utilisé
Streamlit utilise par défaut le port 8501. Pour changer:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Erreur de calcul thermodynamique
Vérifiez que:
- Les compositions totalisent 100%
- Au moins 2 composés sont sélectionnés
- Les paramètres sont dans des plages réalistes

---

## 🚢 Déploiement

### Streamlit Cloud (Gratuit)

1. **Pusher sur GitHub**:
```bash
git add .
git commit -m "Application Streamlit"
git push
```

2. **Déployer sur Streamlit Cloud**:
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Connecter votre GitHub
   - Sélectionner le repository et le fichier `streamlit_app.py`
   - Cliquer sur "Deploy"

3. **Votre app est en ligne !** 🎉

### Heroku

```bash
# Procfile
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0

# Déployer
heroku create distillation-app
git push heroku main
```

---

## ✅ Conformité PDF du Cours

- [x] Toutes les équations (1-51) implémentées
- [x] 4 méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
- [x] Visualisations conformes (profils, bilans)
- [x] Exemple BTX validé
- [x] Interface professionnelle

---

## 🎓 Contexte Pédagogique

**Module:** Modélisation et Simulation des Procédés
**Prof:** BAKHER Zine Elabidine
**Filière:** PIC - UH1
**Année:** 2024-2025

### Compétences Acquises
- Développement web avec Streamlit
- Calculs thermodynamiques avancés
- Visualisations de données scientifiques
- Méthodes simplifiées de distillation
- Déploiement d'applications web

---

## 🎉 Démarrage en 3 Commandes

```bash
pip install -r requirements_streamlit.txt
streamlit run streamlit_app.py
# Ouvrir http://localhost:8501
```

---

## 📝 Licence

Projet pédagogique - Cours de Modélisation et Simulation des Procédés

---

**Profitez de votre simulateur Streamlit !** 🧪✨

*Application conforme au document PDF du cours - Équations 1-51 implémentées*
