# 🧪 Guide d'Utilisation - Application Streamlit de Distillation Multicomposants

**Module:** Modélisation et Simulation des Procédés
**Prof.** BAKHER Zine Elabidine
**Filière:** PIC - UH1
**Année:** 2024-2025

---

## 🎯 Vue d'Ensemble

Cette application Streamlit permet de simuler des colonnes de distillation multicomposants en utilisant les méthodes simplifiées classiques :
- **Fenske** : Nombre minimum de plateaux
- **Underwood** : Reflux minimum
- **Gilliland** : Corrélation plateaux/reflux
- **Kirkbride** : Position du plateau d'alimentation

---

## 🚀 Démarrage Rapide

### 1. Installation des Dépendances

```bash
pip install -r requirements_streamlit.txt
```

### 2. Lancement de l'Application

**Windows:**
```bash
run_streamlit.bat
```

**Linux/Mac:**
```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

**Commande directe:**
```bash
streamlit run streamlit_app.py
```

### 3. Accès à l'Application

L'application s'ouvre automatiquement dans votre navigateur à l'adresse :
**http://localhost:8501**

---

## 📋 Interface Utilisateur

### Barre Latérale (Paramètres d'Entrée)

#### 1. Sélection des Composés
- **Menu déroulant multi-sélection** avec 13 composés disponibles
- Minimum **2 composés** requis pour la simulation
- Affichage : Nom (Formule chimique)

#### 2. Compositions (%)
- Saisie du pourcentage molaire pour chaque composé sélectionné
- Bouton **"Normaliser"** pour ajuster automatiquement à 100%
- Indicateur du total en temps réel

#### 3. Paramètres Opératoires
- **Débit d'alimentation** (kmol/h) : 1 à 10000
- **Pression** (Pa) : 10000 à 1000000
- **Condition d'alimentation** :
  - Liquide saturé (q = 1)
  - Vapeur saturée (q = 0)
  - Liquide sous-refroidi (q > 1)
  - Vapeur surchauffée (q < 0)
  - Mélange biphasique (0 < q < 1)

#### 4. Spécifications de Séparation
- **Récupération composé léger** : 80% à 99.9%
- **Récupération composé lourd** : 80% à 99.9%
- **Multiplicateur de reflux** : 1.1 à 3.0
- **Efficacité des plateaux** : 50% à 95%

#### 5. Bouton de Simulation
- Cliquer sur **"🚀 LANCER LA SIMULATION"**
- Désactivé si moins de 2 composés sont sélectionnés

---

### Zone Principale (Résultats)

#### KPIs (Indicateurs Clés)
5 métriques principales affichées en haut :
1. **N min (Fenske)** : Nombre minimum de plateaux théoriques
2. **N réel** : Nombre réel de plateaux (avec efficacité)
3. **R min** : Reflux minimum (Underwood)
4. **R opératoire** : Reflux opératoire (R_min × multiplicateur)
5. **Plateau alim.** : Position du plateau d'alimentation

#### Onglets de Résultats

##### 📊 **Onglet 1 : Vue d'ensemble**
- **2 graphiques circulaires** :
  - Composition du distillat
  - Composition du résidu
- **3 jauges de performance** :
  - Efficacité des plateaux (%)
  - Ratio R/R_min
  - Ratio N/N_min

##### 📈 **Onglet 2 : Distribution**
- **Graphique en barres groupées** :
  - Répartition des composés entre alimentation, distillat et résidu
  - Couleurs distinctes par composé
  - Interactif (Plotly)

##### 📋 **Onglet 3 : Bilans matières**
- **Tableau détaillé** :
  - Débit de chaque composé (kmol/h)
  - Récupérations au distillat et au résidu (%)
  - Ligne de total pour vérification du bilan

##### 🔬 **Onglet 4 : Résultats détaillés**
- **Méthode de Fenske** : N_min, α_avg
- **Méthode d'Underwood** : R_min, θ
- **Corrélation de Gilliland** : R_op, N_théorique, N_réel, X, Y
- **Équation de Kirkbride** : Plateau d'alimentation, N_rectification, N_épuisement
- **Températures** : T_tête, T_fond, T_alim (°C)
- **Besoins énergétiques** : Q_condenseur, Q_rebouilleur (kW)

---

## 🔬 Exemple Pratique : Système BTX

### Configuration
1. **Sélectionner les composés** :
   - Benzène
   - Toluène
   - o-Xylène

2. **Définir les compositions** :
   - Benzène : 33.3%
   - Toluène : 33.3%
   - o-Xylène : 33.4%
   - Cliquer sur "Normaliser" si besoin

3. **Paramètres opératoires** :
   - Débit : 100 kmol/h
   - Pression : 101325 Pa (1 atm)
   - Condition : Liquide saturé (q=1)

4. **Spécifications** :
   - Récupération léger : 95%
   - Récupération lourd : 95%
   - Multiplicateur reflux : 1.3
   - Efficacité : 70%

5. **Lancer la simulation**

### Résultats Attendus
```
N min (Fenske) ≈ 6.8 plateaux
N réel ≈ 19 plateaux
R min (Underwood) ≈ 1.85
R opératoire ≈ 2.41
Plateau alimentation ≈ 10
T tête ≈ 80.1°C
T fond ≈ 138.5°C
```

---

## 🎨 Personnalisation

### Ajouter un Nouveau Composé

Éditez le fichier [streamlit_app.py](streamlit_app.py) et ajoutez une entrée dans `COMPOUNDS_LIBRARY` :

```python
COMPOUNDS_LIBRARY = {
    # ... composés existants ...
    'nouveau_compose': {
        'name': 'Nouveau Composé',
        'formula': 'CxHy',
        'Tb': 100.0,   # Température d'ébullition (°C)
        'Tc': 500.0,   # Température critique (K)
        'Pc': 40.0     # Pression critique (bar)
    }
}
```

### Modifier le Style Visuel

Les styles CSS se trouvent au début de [streamlit_app.py](streamlit_app.py) :

```python
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    /* Ajoutez vos styles ici */
</style>
""", unsafe_allow_html=True)
```

---

## 🐛 Dépannage

### Erreur : Module introuvable

**Problème** : `ModuleNotFoundError: No module named 'streamlit'`

**Solution** :
```bash
pip install -r requirements_streamlit.txt
```

### Erreur : Port déjà utilisé

**Problème** : `Address already in use`

**Solution** :
```bash
# Utiliser un autre port
streamlit run streamlit_app.py --server.port 8502
```

### Erreur : Compositions ne totalisent pas 100%

**Problème** : Warning dans l'interface

**Solution** :
- Ajuster manuellement les compositions
- Ou cliquer sur le bouton **"Normaliser"**

### Erreur : Calcul thermodynamique échoue

**Problème** : `Error during simulation`

**Solutions** :
- Vérifier que les compositions sont > 0
- Vérifier que la pression est réaliste (> 10000 Pa)
- Vérifier que les récupérations sont < 100%

---

## 🚢 Déploiement en Production

### Streamlit Cloud (Recommandé - Gratuit)

1. **Préparer le repository GitHub** :
```bash
git add .
git commit -m "Application Streamlit prête"
git push origin main
```

2. **Déployer sur Streamlit Cloud** :
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Se connecter avec GitHub
   - Cliquer sur "New app"
   - Sélectionner :
     - Repository : votre repository
     - Branch : main
     - Main file path : `streamlit_app.py`
   - Cliquer sur "Deploy"

3. **Votre application est en ligne !**
   Elle sera accessible à une URL du type :
   `https://username-dist-multi-pic11-streamlit-app-abc123.streamlit.app`

### Heroku

1. **Créer un Procfile** :
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Déployer** :
```bash
heroku create mon-app-distillation
git push heroku main
```

---

## 📊 Méthodologie de Calcul

### Séquence de Calcul

1. **Normalisation** : Les compositions sont normalisées à 1.0
2. **K-values** : Calcul des coefficients de distribution à T_moy
3. **Volatilités relatives** : α_i = K_i / K_HK
4. **Fenske** : N_min = ln[(x_LK_D/x_HK_D)/(x_LK_B/x_HK_B)] / ln(α_avg)
5. **Underwood** :
   - Résolution de Σ[α_i·z_i/(α_i-θ)] = 1-q pour θ
   - R_min = Σ[α_i·x_D_i/(α_i-θ)] - 1
6. **Gilliland** : Corrélation graphique pour N en fonction de R
7. **Kirkbride** : Position du plateau d'alimentation

### Hypothèses

- Pression constante dans la colonne
- Efficacité uniforme sur tous les plateaux
- Pertes de chaleur négligeables
- Mélanges idéaux (volatilité relative constante)

---

## 📚 Références

- **Cours** : Modélisation et Simulation des Procédés - Prof. BAKHER
- **Méthodes** : Fenske, Underwood, Gilliland, Kirkbride
- **Framework** : Streamlit Documentation ([docs.streamlit.io](https://docs.streamlit.io))
- **Visualisations** : Plotly Python ([plotly.com/python](https://plotly.com/python))

---

## ✅ Checklist de Validation

Avant de présenter vos résultats, vérifiez :

- [ ] Les compositions totalisent 100%
- [ ] Au moins 2 composés sont sélectionnés
- [ ] Les récupérations sont < 100%
- [ ] Le bilan matière est équilibré (F = D + B)
- [ ] Les températures sont cohérentes (T_tête < T_fond)
- [ ] N_réel > N_min
- [ ] R_op > R_min
- [ ] Les graphiques s'affichent correctement

---

## 🎯 Prochaines Étapes

1. **Tester** différents systèmes de composés
2. **Analyser** l'effet des paramètres (reflux, efficacité)
3. **Comparer** avec des résultats de simulateurs commerciaux
4. **Étendre** : Ajouter d'autres méthodes (McCabe-Thiele, etc.)

---

## 📞 Support

Pour toute question ou problème :
1. Consulter ce guide
2. Vérifier les messages d'erreur dans l'application
3. Consulter la documentation Streamlit
4. Contacter le professeur

---

**Bon calcul !** 🧪✨

*Application développée dans le cadre du cours de Modélisation et Simulation des Procédés - PIC UH1*
