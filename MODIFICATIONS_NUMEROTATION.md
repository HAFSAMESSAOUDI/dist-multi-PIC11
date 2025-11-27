# Modifications de Numérotation des Équations

**Date:** 2025-11-27
**Version:** 2.2 - Numérotation Séquentielle

---

## 📋 Résumé des Modifications

### 1. Titre de l'Application
**Ancien:** "Modélisation et Simulation des Procédés | Prof. BAKHER Zine Elabidine | PIC UH1 2024-2025"
**Nouveau:** "La distillation - Procédés de Séparation"

### 2. Bouton de Téléchargement PDF
**Ajouté:** Bouton "📥 Télécharger PDF" sur la page d'accueil permettant de télécharger la documentation LaTeX complète

### 3. Numérotation des Équations
Les équations ont été renumérotées séquentiellement de **1 à 20** (au lieu de la numérotation dispersée précédente)

---

## 🔢 Tableau de Correspondance des Équations

| Nouvelle Numérotation | Ancienne Numérotation | Description | Méthode |
|---|---|---|---|
| **Éq. 1** | Éq. 10 | $N_{min}$ (Fenske) | Méthodes Simplifiées |
| **Éq. 2** | Éq. 15 | Underwood - Équation θ | Méthodes Simplifiées |
| **Éq. 3** | Éq. 16 | Underwood - $R_{min}$ | Méthodes Simplifiées |
| **Éq. 4** | Éq. 19 | Gilliland - Paramètre X | Méthodes Simplifiées |
| **Éq. 5** | Éq. 20 | Gilliland - Paramètre Y | Méthodes Simplifiées |
| **Éq. 6** | Éq. 21 | Gilliland - N théorique | Méthodes Simplifiées |
| **Éq. 7** | Éq. 22 | Efficacité - N réel | Méthodes Simplifiées |
| **Éq. 8** | Éq. 23 | Kirkbride - Position alimentation | Méthodes Simplifiées |
| **Éq. 9** | Éq. 24 | MESH - Bilan Matière (M) | MESH Rigoureux |
| **Éq. 10** | Éq. 30 | MESH - Équilibre (E) | MESH Rigoureux |
| **Éq. 11** | Éq. 31 | MESH - Sommation liquide (S) | MESH Rigoureux |
| **Éq. 12** | Éq. 32 | MESH - Sommation vapeur (S) | MESH Rigoureux |
| **Éq. 13** | Éq. 33 | MESH - Bilan Enthalpique (H) | MESH Rigoureux |
| **Éq. 14** | Éq. 40a | Modèle de Wilson | Modèles d'Activité |
| **Éq. 15** | Éq. 40b | Modèle NRTL | Modèles d'Activité |
| **Éq. 16** | Éq. 40c | Modèle UNIQUAC | Modèles d'Activité |
| **Éq. 17** | Éq. 43 | TAC - Coût Total Annualisé | Optimisation Économique |
| **Éq. 18** | Éq. 44 | Coût d'Investissement | Optimisation Économique |
| **Éq. 19** | Éq. 45 | Coût d'Exploitation | Optimisation Économique |
| **Éq. 20** | Éq. 46 | Coût de Maintenance | Optimisation Économique |

---

## 📝 Détail des Équations

### Section 1: Méthodes Simplifiées (Éq. 1-8)

#### Éq. 1 - Fenske
```
N_min = ln[(x_LK,D / x_HK,D) × (x_HK,B / x_LK,B)] / ln(α_avg)
```
**Objectif:** Nombre minimum de plateaux théoriques (reflux total)

#### Éq. 2 - Underwood (θ)
```
Σ[α_i × z_i / (α_i - θ)] = 1 - q
```
**Objectif:** Résolution du paramètre θ d'Underwood

#### Éq. 3 - Underwood (R_min)
```
R_min + 1 = Σ[α_i × x_D,i / (α_i - θ)]
```
**Objectif:** Calcul du reflux minimum

#### Éq. 4 - Gilliland (X)
```
X = (R - R_min) / (R + 1)
```
**Objectif:** Paramètre X de Gilliland

#### Éq. 5 - Gilliland (Y)
```
Y = 1 - exp[((1 + 54.4X)(X - 1)) / ((11 + 117.2X)√X)]
```
**Objectif:** Paramètre Y de Gilliland

#### Éq. 6 - Gilliland (N)
```
N_théorique = N_min + Y / (1 - Y)
```
**Objectif:** Nombre de plateaux théoriques

#### Éq. 7 - Efficacité
```
N_réel = N_théorique / E_Murphree
```
**Objectif:** Conversion en plateaux réels

#### Éq. 8 - Kirkbride
```
log(N_R / N_S) = 0.206 × log[(B/D) × (x_HK,F/x_LK,F) × (x_LK,B/x_HK,D)²]
```
**Objectif:** Position du plateau d'alimentation

---

### Section 2: MESH Rigoureux (Éq. 9-13)

#### Éq. 9 - MESH: Bilan Matière (M)
```
L_{j+1}x_{i,j+1} + V_{j-1}y_{i,j-1} - L_j x_{i,j} - V_j y_{i,j} + F_j z_{i,j} = 0
```
**Pour chaque plateau j et composé i**

#### Éq. 10 - MESH: Équilibre (E)
```
y_{i,j} = K_{i,j} × x_{i,j}
```
**Avec:** K_{i,j} = (γ_i P_sat,i) / P pour mélanges non-idéaux

#### Éq. 11 - MESH: Sommation Liquide (S)
```
Σ x_{i,j} = 1
```
**Conservation des fractions molaires liquides**

#### Éq. 12 - MESH: Sommation Vapeur (S)
```
Σ y_{i,j} = 1
```
**Conservation des fractions molaires vapeurs**

#### Éq. 13 - MESH: Bilan Enthalpique (H)
```
L_{j+1}h_{j+1} + V_{j-1}H_{j-1} - L_j h_j - V_j H_j + F_j h_F + Q_j = 0
```
**Bilan énergétique pour chaque plateau**

---

### Section 3: Modèles d'Activité (Éq. 14-16)

#### Éq. 14 - Modèle de Wilson
```
ln(γ_i) = 1 - ln(Σ_j x_j Λ_ij) - Σ_k [x_k Λ_ki / Σ_j x_j Λ_kj]
```
**Pour mélanges non-idéaux sans azéotrope**

#### Éq. 15 - Modèle NRTL
```
G_ij = exp(-α_ij τ_ij), τ_ij = a_ij / T
```
**Non-Random Two-Liquid (azéotropes possibles)**

#### Éq. 16 - Modèle UNIQUAC
```
ln(γ_i) = ln(γ_i^C) + ln(γ_i^R)
```
**Universal Quasi-Chemical (partie combinatoire + résiduelle)**

---

### Section 4: Optimisation Économique (Éq. 17-20)

#### Éq. 17 - TAC (Total Annualized Cost)
```
TAC = C_capital × CRF + C_operating + C_maintenance
```
**Coût total annualisé de la colonne**

#### Éq. 18 - Coût d'Investissement
```
C_capital = C_colonne + C_condenseur + C_rebouilleur
```
**Coûts d'investissement (CAPEX)**

#### Éq. 19 - Coût d'Exploitation
```
C_operating = C_énergie + C_refroidissement
```
**Coûts d'exploitation (OPEX)**

#### Éq. 20 - Coût de Maintenance
```
C_maintenance = 0.05 × C_capital
```
**Maintenance annuelle (5% du capital)**

---

## 🎯 Avantages de la Nouvelle Numérotation

### ✅ Clarté
- Numérotation **séquentielle et logique** de 1 à 20
- Plus facile à suivre pour les étudiants
- Cohérence avec le flux d'apprentissage

### ✅ Organisation
- **Section 1 (Éq. 1-8):** Méthodes Simplifiées
- **Section 2 (Éq. 9-13):** MESH Rigoureux
- **Section 3 (Éq. 14-16):** Modèles d'Activité
- **Section 4 (Éq. 17-20):** Optimisation Économique

### ✅ Pédagogie
- Progression naturelle: Simplifiées → MESH → Thermo → Économie
- Références faciles dans les rapports de TP
- Numérotation unique et non ambiguë

---

## 📱 Modifications de l'Interface

### Page d'Accueil
```python
# Avant
col1, col2, col3 = st.columns(3)

# Après
col1, col2, col3, col4 = st.columns(4)

# Ajout du bouton de téléchargement PDF dans col4
st.download_button(
    label="📥 Télécharger PDF",
    data=pdf_content,
    file_name="Documentation_Distillation.tex",
    mime="application/x-latex"
)
```

### Titre Principal
```python
# Avant
st.markdown("**Modélisation et Simulation des Procédés** | Prof. BAKHER Zine Elabidine | PIC UH1 2024-2025")

# Après
st.markdown("**La distillation - Procédés de Séparation**")
```

---

## 📊 Impact sur la Documentation

### Fichiers Modifiés
1. **streamlit_app_enhanced.py** (20 équations renumérotées)
2. **DOCUMENTATION_LATEX.tex** (déjà avec numérotation 1-47, compatible)

### Cohérence
- L'application Streamlit utilise maintenant Éq. 1-20
- Le document LaTeX utilise Éq. 1-47 (équations supplémentaires détaillées)
- Les 20 premières équations sont cohérentes entre les deux

---

## ✅ Tests de Validation

### ✓ Navigation
- [x] Page d'accueil affiche le nouveau titre
- [x] Bouton "Télécharger PDF" fonctionne
- [x] 4 colonnes de navigation correctement alignées

### ✓ Documentation
- [x] Onglet "Méthodes Simplifiées" → Éq. 1-8
- [x] Onglet "MESH Rigoureux" → Éq. 9-13
- [x] Onglet "Modèles d'Activité" → Éq. 14-16
- [x] Onglet "Optimisation Économique" → Éq. 17-20

### ✓ Cohérence
- [x] Toutes les équations référencées correctement
- [x] Numérotation séquentielle sans saut
- [x] Descriptions claires pour chaque équation

---

## 🚀 Utilisation

### Pour les Étudiants
1. **Apprendre:** Suivre les équations dans l'ordre (1 → 20)
2. **Référencer:** Citer "Éq. X" dans les rapports de TP
3. **Télécharger:** Bouton PDF pour documentation complète

### Pour les Enseignants
1. **Enseigner:** Progression logique des concepts
2. **Évaluer:** Références uniques pour les examens
3. **Documenter:** Export LaTeX pour supports de cours

---

**Version:** 2.2 - Numérotation Séquentielle
**Date:** 2025-11-27
**Statut:** ✅ **PRODUCTION READY**

---

*Application de Distillation Multicomposants*
*La distillation - Procédés de Séparation*
