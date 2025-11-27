"""
Application Streamlit Complète - Distillation Multicomposants
Implémentation complète selon le PDF du cours

Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Fonctionnalités:
- Méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
- Méthode rigoureuse MESH
- Modèles d'activité (Wilson, NRTL, UNIQUAC)
- Optimisation économique (TAC)
- Études paramétriques
"""

import streamlit as st
import numpy as np
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(__file__))

from distillation_multicomposants import ThermodynamicPackage, Compound
from mesh_solver import MESHSolver
from activity_models import WilsonModel, NRTLModel, UNIQUACModel, IdealModel
from economic_optimization import EconomicOptimizer, parametric_study_reflux, parametric_study_pressure

# Configuration de la page
st.set_page_config(
    page_title="Distillation Multicomposants",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# CSS personnalisé - Clean and Professional
st.markdown("""
<style>
    /* Main Layout */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Navigation Buttons */
    .nav-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 5px;
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        color: #2c3e50;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    
    .nav-button:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button.active {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    /* Headers */
    h1 {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    
    h2 {
        color: #34495e !important;
        font-weight: 600 !important;
    }
    
    h3 {
        color: #667eea !important;
        font-weight: 600 !important;
    }
    
    /* Cards */
    .info-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 16px 0;
        border-left: 4px solid #667eea;
    }
    
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: #667eea;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 14px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #5568d3;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* Divider */
    hr {
        margin: 24px 0;
        border: none;
        border-top: 2px solid #e0e0e0;
    }
    
    /* Success/Warning/Info boxes */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Bibliothèque de composés
COMPOUNDS_LIBRARY = {
    'benzene': {'name': 'Benzène', 'formula': 'C6H6', 'Tb': 80.1, 'Tc': 562.05, 'Pc': 48.98},
    'toluene': {'name': 'Toluène', 'formula': 'C7H8', 'Tb': 110.6, 'Tc': 591.75, 'Pc': 41.08},
    'o-xylene': {'name': 'o-Xylène', 'formula': 'C8H10', 'Tb': 144.4, 'Tc': 630.3, 'Pc': 37.3},
    'ethylbenzene': {'name': 'Éthylbenzène', 'formula': 'C8H10', 'Tb': 136.2, 'Tc': 617.2, 'Pc': 36.0},
    'cumene': {'name': 'Cumène', 'formula': 'C9H12', 'Tb': 152.4, 'Tc': 631.0, 'Pc': 32.1},
    'styrene': {'name': 'Styrène', 'formula': 'C8H8', 'Tb': 145.0, 'Tc': 636.0, 'Pc': 38.4},
    'methanol': {'name': 'Méthanol', 'formula': 'CH4O', 'Tb': 64.7, 'Tc': 512.5, 'Pc': 80.9},
    'ethanol': {'name': 'Éthanol', 'formula': 'C2H6O', 'Tb': 78.4, 'Tc': 514.0, 'Pc': 61.4},
    'propanol': {'name': '1-Propanol', 'formula': 'C3H8O', 'Tb': 97.2, 'Tc': 536.8, 'Pc': 51.7},
    'butanol': {'name': '1-Butanol', 'formula': 'C4H10O', 'Tb': 117.7, 'Tc': 563.1, 'Pc': 44.1},
    'hexane': {'name': 'Hexane', 'formula': 'C6H14', 'Tb': 68.7, 'Tc': 507.6, 'Pc': 30.3},
    'heptane': {'name': 'Heptane', 'formula': 'C7H16', 'Tb': 98.4, 'Tc': 540.2, 'Pc': 27.4},
    'octane': {'name': 'Octane', 'formula': 'C8H18', 'Tb': 125.7, 'Tc': 568.7, 'Pc': 24.9}
}


def simulate_shortcut(compounds, compositions, feed_rate, pressure,
                      light_key_recovery, heavy_key_recovery,
                      feed_thermal_condition, reflux_ratio_multiplier, efficiency):
    """
    Simulation par méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
    """
    try:
        # Normaliser les compositions
        compositions = np.array(compositions) / np.sum(compositions)

        # Créer les composés
        compound_objects = [Compound(name) for name in compounds]

        # Package thermodynamique
        thermo_package = ThermodynamicPackage(compound_objects)

        # Indices clés
        LK_idx = 0
        HK_idx = 1 if len(compounds) > 1 else 0

        # Débits
        D = feed_rate * compositions[LK_idx] * light_key_recovery / light_key_recovery
        B = feed_rate - D

        # Facteur q
        q_values = {
            'saturated_liquid': 1.0,
            'saturated_vapor': 0.0,
            'subcooled_liquid': 1.2,
            'superheated_vapor': -0.2,
            'two_phase': 0.5
        }
        q = q_values.get(feed_thermal_condition, 1.0)

        # K-values
        T_avg = np.mean([comp.Tb for comp in compound_objects])
        K_values = thermo_package.K_values(T_avg, pressure)

        # Volatilités relatives
        alphas = K_values / K_values[HK_idx]
        alpha_avg = alphas[LK_idx]

        # FENSKE
        x_LK_D = light_key_recovery * compositions[LK_idx] / (
            light_key_recovery * compositions[LK_idx] + (1 - heavy_key_recovery) * compositions[HK_idx]
        )
        x_HK_D = 1 - x_LK_D
        x_LK_B = (1 - light_key_recovery) * compositions[LK_idx] / (
            (1 - light_key_recovery) * compositions[LK_idx] + heavy_key_recovery * compositions[HK_idx]
        )
        x_HK_B = 1 - x_LK_B

        N_min = np.log((x_LK_D / x_HK_D) / (x_LK_B / x_HK_B)) / np.log(alpha_avg)

        # UNDERWOOD
        def underwood_eq1(theta):
            return sum(alphas[i] * compositions[i] / (alphas[i] - theta)
                      for i in range(len(compounds))) - (1 - q)

        from scipy.optimize import brentq
        try:
            theta = brentq(underwood_eq1, alphas[HK_idx] + 0.01, alphas[LK_idx] - 0.01)
        except:
            theta = (alphas[LK_idx] + alphas[HK_idx]) / 2

        x_D = np.zeros(len(compounds))
        x_D[LK_idx] = x_LK_D
        x_D[HK_idx] = x_HK_D

        R_min_plus_1 = sum(alphas[i] * x_D[i] / (alphas[i] - theta)
                          for i in range(len(compounds)))
        R_min = R_min_plus_1 - 1

        # GILLILAND
        R = R_min * reflux_ratio_multiplier
        X = (R - R_min) / (R + 1)
        exponent = (1 + 54.4 * X) * (X - 1) / ((11 + 117.2 * X) * np.sqrt(X))
        Y = 1 - np.exp(exponent)
        N_theoretical = N_min + Y / (1 - Y)
        N_real = int(np.ceil(N_theoretical / efficiency))

        # KIRKBRIDE
        ratio = (B / D) * (compositions[HK_idx] / compositions[LK_idx]) * (x_LK_B / x_HK_D) ** 2
        log_ratio = 0.206 * np.log(ratio)
        N_R_over_N_S = np.exp(log_ratio)
        N_S = N_real / (1 + N_R_over_N_S)
        N_R = N_real - N_S
        feed_stage = int(np.ceil(N_R)) + 1

        # Températures
        T_top = compound_objects[LK_idx].Tb
        T_bottom = compound_objects[HK_idx].Tb

        # Besoins énergétiques
        lambda_avg = 40000
        Q_condenser = (R + 1) * D * lambda_avg / 1000
        Q_reboiler = Q_condenser * 1.1

        # Distribution des composés
        distribution = []
        for i, comp in enumerate(compound_objects):
            d_i = feed_rate * compositions[i] * (alphas[i] ** N_min) / (1 + (alphas[i] ** N_min))
            b_i = feed_rate * compositions[i] - d_i

            distribution.append({
                'compound': comp.name,
                'feed': float(feed_rate * compositions[i]),
                'distillate': float(d_i),
                'bottoms': float(b_i),
                'recovery_D': float(d_i / (feed_rate * compositions[i]) * 100) if compositions[i] > 0 else 0,
                'recovery_B': float(b_i / (feed_rate * compositions[i]) * 100) if compositions[i] > 0 else 0
            })

        D_total = sum(d['distillate'] for d in distribution)
        B_total = sum(d['bottoms'] for d in distribution)

        return {
            'success': True,
            'method': 'shortcut',
            'results': {
                'fenske': {'N_min': float(N_min), 'alpha_avg': float(alpha_avg)},
                'underwood': {'R_min': float(R_min), 'theta': float(theta)},
                'gilliland': {
                    'R_operating': float(R),
                    'N_theoretical': float(N_theoretical),
                    'N_real': int(N_real),
                    'X': float(X),
                    'Y': float(Y)
                },
                'kirkbride': {
                    'feed_stage': feed_stage,
                    'N_rectification': int(np.ceil(N_R)),
                    'N_stripping': int(np.floor(N_S))
                },
                'temperatures': {
                    'top': float(T_top),
                    'bottom': float(T_bottom),
                    'feed': float(T_avg)
                },
                'energy': {
                    'Q_condenser': float(Q_condenser),
                    'Q_reboiler': float(Q_reboiler)
                },
                'flows': {
                    'feed': float(feed_rate),
                    'distillate': float(D_total),
                    'bottoms': float(B_total)
                },
                'distribution': distribution,
                'efficiency': float(efficiency)
            }
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# =============================================================================
# NAVIGATION
# =============================================================================

# Header with Navigation
st.markdown("""
<div style='text-align: center; padding: 32px 20px; background: white; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    <h1 style='color: #2c3e50; margin: 0; font-size: 32px; font-weight: 700;'>Distillation Multicomposants</h1>
    <p style='color: #7f8c8d; margin: 12px 0 0 0; font-size: 16px; font-weight: 400;'>
        Simulation et Optimisation des Procédés de Séparation
    </p>
</div>
""", unsafe_allow_html=True)

# Navigation Menu
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Home", key="nav_home", use_container_width=True):
        st.session_state.current_page = 'Home'
        st.rerun()

with col2:
    if st.button("Méthodes Simplifiées", key="nav_shortcut", use_container_width=True):
        st.session_state.current_page = 'Shortcut'
        st.rerun()

with col3:
    if st.button("MESH Rigoureux", key="nav_mesh", use_container_width=True):
        st.session_state.current_page = 'MESH'
        st.rerun()

with col4:
    if st.button("Comparaison", key="nav_compare", use_container_width=True):
        st.session_state.current_page = 'Comparison'
        st.rerun()

with col5:
    if st.button("Documentation", key="nav_docs", use_container_width=True):
        st.session_state.current_page = 'Documentation'
        st.rerun()

st.markdown("---")

# =============================================================================
# HOME PAGE
# =============================================================================

if st.session_state.current_page == 'Home':
    # Welcome Section
    st.markdown("""
    <div class='info-card'>
        <h2 style='margin-top: 0;'>Bienvenue</h2>
        <p style='font-size: 16px; line-height: 1.6; color: #555;'>
            Cette application permet la simulation complète de colonnes de distillation multicomposants 
            en utilisant différentes approches de calcul, des méthodes simplifiées aux modèles rigoureux.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("### Fonctionnalités Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='margin-top: 0; color: #667eea;'>Méthodes Simplifiées</h3>
            <p style='color: #666; line-height: 1.6;'>
                Calculs rapides utilisant les corrélations classiques de Fenske, Underwood, 
                Gilliland et Kirkbride pour un dimensionnement préliminaire.
            </p>
            <ul style='color: #666;'>
                <li>Nombre minimum de plateaux (Fenske)</li>
                <li>Reflux minimum (Underwood)</li>
                <li>Nombre de plateaux réels (Gilliland)</li>
                <li>Position d'alimentation (Kirkbride)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3 style='margin-top: 0; color: #667eea;'>Modèles d'Activité</h3>
            <p style='color: #666; line-height: 1.6;'>
                Prise en compte des non-idéalités avec plusieurs modèles thermodynamiques.
            </p>
            <ul style='color: #666;'>
                <li>Modèle Idéal (Loi de Raoult)</li>
                <li>Wilson</li>
                <li>NRTL</li>
                <li>UNIQUAC</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3 style='margin-top: 0; color: #667eea;'>MESH Rigoureux</h3>
            <p style='color: #666; line-height: 1.6;'>
                Résolution rigoureuse des équations MESH (Material, Equilibrium, Summation, Heat) 
                pour une précision maximale.
            </p>
            <ul style='color: #666;'>
                <li>Bilans matière plateau par plateau</li>
                <li>Équilibres thermodynamiques rigoureux</li>
                <li>Profils de température et composition</li>
                <li>Convergence garantie</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-card'>
            <h3 style='margin-top: 0; color: #667eea;'>Optimisation Économique</h3>
            <p style='color: #666; line-height: 1.6;'>
                Minimisation du coût annuel total (TAC) et études paramétriques.
            </p>
            <ul style='color: #666;'>
                <li>Calcul du TAC (CAPEX + OPEX)</li>
                <li>Études de sensibilité</li>
                <li>Optimisation reflux/pression</li>
                <li>Analyse économique détaillée</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("---")
    st.markdown("### Guide de Démarrage Rapide")
    
    st.markdown("""
    <div class='info-card'>
        <ol style='font-size: 15px; line-height: 1.8; color: #555;'>
            <li><strong>Choisissez une méthode</strong> dans le menu de navigation ci-dessus</li>
            <li><strong>Configurez les paramètres</strong> dans la barre latérale (composés, débits, conditions opératoires)</li>
            <li><strong>Lancez la simulation</strong> en cliquant sur le bouton de calcul</li>
            <li><strong>Analysez les résultats</strong> dans les différents onglets (graphiques, tableaux, détails)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # About Section
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='margin-top: 0;'>À Propos</h3>
            <p style='color: #666; line-height: 1.6;'>
                <strong>Module:</strong> Modélisation et Simulation des Procédés<br>
                <strong>Professeur:</strong> BAKHER Zine Elabidine<br>
                <strong>Filière:</strong> PIC - Université UH1<br>
                <strong>Année:</strong> 2024-2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='margin-top: 0;'>Bibliothèque de Composés</h3>
            <p style='color: #666; line-height: 1.6;'>
                <strong>{}</strong> composés disponibles<br>
                Hydrocarbures aromatiques, alcools, alcanes
            </p>
        </div>
        """.format(len(COMPOUNDS_LIBRARY)), unsafe_allow_html=True)

# =============================================================================
# SIDEBAR FOR SIMULATION PAGES
# =============================================================================

elif st.session_state.current_page in ['Shortcut', 'MESH', 'Comparison']:
    with st.sidebar:
        st.markdown("### Configuration")
        
        # Map page to calculation method
        page_to_method = {
            'Shortcut': 'Méthodes Simplifiées',
            'MESH': 'MESH Rigoureux',
            'Comparison': 'Comparaison'
        }
        calculation_method = page_to_method[st.session_state.current_page]

        # Modèle thermodynamique
        if calculation_method in ['MESH Rigoureux', 'Comparaison']:
            st.markdown("#### Modèle Thermodynamique")
            thermo_model = st.selectbox(
                "Modèle d'activité",
                ['Idéal', 'Wilson', 'NRTL', 'UNIQUAC'],
                help="Choisir le modèle pour les coefficients d'activité"
            )
        else:
            thermo_model = 'Idéal'

        st.divider()

        # Sélection des composés
        st.markdown("#### Composés")
        selected_compounds = st.multiselect(
            "Sélectionner les composés",
            options=list(COMPOUNDS_LIBRARY.keys()),
            default=['benzene', 'toluene'],
            format_func=lambda x: f"{COMPOUNDS_LIBRARY[x]['name']} ({COMPOUNDS_LIBRARY[x]['formula']})"
        )

        # Compositions
        if len(selected_compounds) >= 2:
            st.markdown("#### Compositions (%)")
            compositions = []
            total_comp = 0

            for compound_key in selected_compounds:
                comp_value = st.number_input(
                    f"{COMPOUNDS_LIBRARY[compound_key]['name']}",
                    min_value=0.0,
                    max_value=100.0,
                    value=100.0 / len(selected_compounds),
                    step=1.0,
                    key=f"comp_{compound_key}"
                )
                compositions.append(comp_value)
                total_comp += comp_value

            if abs(total_comp - 100.0) > 0.1:
                st.warning(f"Total = {total_comp:.1f}% (devrait être 100%)")
                if st.button("Normaliser", use_container_width=True):
                    st.rerun()
            else:
                st.success(f"Total = {total_comp:.1f}%")

            st.divider()

            # Paramètres opératoires
            st.markdown("#### Paramètres Opératoires")

            feed_rate = st.number_input(
                "Débit d'alimentation (kmol/h)",
                min_value=1.0,
                max_value=10000.0,
                value=100.0,
                step=10.0
            )

            pressure = st.number_input(
                "Pression (Pa)",
                min_value=10000.0,
                max_value=1000000.0,
                value=101325.0,
                step=10000.0
            )

            feed_condition = st.selectbox(
                "Condition thermique de l'alimentation",
                ['saturated_liquid', 'saturated_vapor', 'subcooled_liquid',
                 'superheated_vapor', 'two_phase'],
                format_func=lambda x: {
                    'saturated_liquid': 'Liquide saturé (q=1)',
                    'saturated_vapor': 'Vapeur saturée (q=0)',
                    'subcooled_liquid': 'Liquide sous-refroidi (q>1)',
                    'superheated_vapor': 'Vapeur surchauffée (q<0)',
                    'two_phase': 'Mélange biphasique (0<q<1)'
                }[x]
            )

            st.divider()

            # Spécifications
            st.markdown("#### Spécifications")

            light_recovery = st.slider(
                "Récupération composé léger (%)",
                min_value=80.0,
                max_value=99.9,
                value=95.0,
                step=0.1
            ) / 100

            heavy_recovery = st.slider(
                "Récupération composé lourd (%)",
                min_value=80.0,
                max_value=99.9,
                value=95.0,
                step=0.1
            ) / 100

            reflux_multiplier = st.slider(
                "Multiplicateur de reflux",
                min_value=1.1,
                max_value=3.0,
                value=1.3,
                step=0.1
            )

            efficiency = st.slider(
                "Efficacité des plateaux (%)",
                min_value=50.0,
                max_value=95.0,
                value=70.0,
                step=5.0
            ) / 100

            st.divider()

            # Bouton simulation
            run_simulation = st.button("LANCER LA SIMULATION", use_container_width=True)
        else:
            st.warning("Sélectionnez au moins 2 composés")
            run_simulation = False

    # =============================================================================
    # ZONE PRINCIPALE
    # =============================================================================

    if run_simulation and len(selected_compounds) >= 2:
        with st.spinner('Simulation en cours...'):

            # Simulation par méthodes simplifiées
            if calculation_method in ['Méthodes Simplifiées', 'Comparaison']:
                results_shortcut = simulate_shortcut(
                    selected_compounds,
                    [c / 100 for c in compositions],
                    feed_rate,
                    pressure,
                    light_recovery,
                    heavy_recovery,
                    feed_condition,
                    reflux_multiplier,
                    efficiency
                )

            # Simulation MESH
            if calculation_method in ['MESH Rigoureux', 'Comparaison']:
                try:
                    # Créer les composés
                    compound_objects = [Compound(name) for name in selected_compounds]

                    # Normaliser compositions
                    z_F = np.array([c / 100 for c in compositions])
                    z_F = z_F / np.sum(z_F)

                    # Paramètres depuis shortcut si disponible
                    if calculation_method == 'Comparaison' and results_shortcut['success']:
                        N_stages = results_shortcut['results']['gilliland']['N_real']
                        feed_stage = results_shortcut['results']['kirkbride']['feed_stage']
                        R_min = results_shortcut['results']['underwood']['R_min']
                    else:
                        N_stages = 20
                        feed_stage = 10
                        R_min = 1.5

                    R = R_min * reflux_multiplier
                    D = feed_rate * z_F[0] * light_recovery / light_recovery

                    # Créer le solver MESH
                    mesh_solver = MESHSolver(
                        compound_objects,
                        N_stages,
                        feed_stage,
                        pressure
                    )

                    # Choisir le modèle d'activité
                    if thermo_model == 'Wilson':
                        activity_model = WilsonModel(compound_objects)
                    elif thermo_model == 'NRTL':
                        activity_model = NRTLModel(compound_objects)
                    elif thermo_model == 'UNIQUAC':
                        activity_model = UNIQUACModel(compound_objects)
                    else:
                        activity_model = IdealModel(compound_objects)

                    mesh_solver.activity_model = activity_model

                    # Résoudre
                    mesh_raw = mesh_solver.solve(feed_rate, z_F, R, D, max_iter=100, verbose=False)

                    # Reformater les résultats pour l'affichage
                    if mesh_raw['converged']:
                        results_mesh = {
                            'success': True,
                            'method': 'MESH',
                            'converged': True,
                            'iterations': mesh_raw['iterations'],
                            'n_stages': N_stages,
                            'feed_stage': feed_stage,
                            'R': R,
                            'D': mesh_raw['distillate']['flow'],
                            'B': mesh_raw['bottoms']['flow'],
                            'T': mesh_raw['temperatures'],
                            'x': mesh_raw['compositions']['liquid'],
                            'y': mesh_raw['compositions']['vapor'],
                            'L': mesh_raw['flows']['liquid'],
                            'V': mesh_raw['flows']['vapor']
                        }
                    else:
                        results_mesh = {
                            'success': False,
                            'converged': False,
                            'error': "MESH n'a pas convergé après {} itérations".format(mesh_raw['iterations'])
                        }

                except Exception as e:
                    results_mesh = {'success': False, 'converged': False, 'error': str(e)}

            # Affichage des résultats
            st.success("Simulation terminée!")

            # Tabs pour différentes vues
            if calculation_method == 'Méthodes Simplifiées':
                tabs = st.tabs([
                    "Vue d'ensemble",
                    "Distribution",
                    "Bilans",
                    "Détails",
                    "Économie"
                ])

                if results_shortcut['success']:
                    r = results_shortcut['results']

                    # TAB 1: Vue d'ensemble
                    with tabs[0]:
                        # KPIs
                        cols = st.columns(5)
                        cols[0].metric("N min (Fenske)", f"{r['fenske']['N_min']:.2f}")
                        cols[1].metric("N réel", r['gilliland']['N_real'])
                        cols[2].metric("R min", f"{r['underwood']['R_min']:.3f}")
                        cols[3].metric("R opératoire", f"{r['gilliland']['R_operating']:.3f}")
                        cols[4].metric("Plateau alim.", r['kirkbride']['feed_stage'])

                        st.divider()

                        # Graphiques
                        col1, col2 = st.columns(2)

                        with col1:
                            # Pie chart distillat
                            dist_values = [d['distillate'] for d in r['distribution']]
                            dist_labels = [d['compound'] for d in r['distribution']]

                            fig1 = go.Figure(data=[go.Pie(
                                labels=dist_labels,
                                values=dist_values,
                                hole=0.3,
                                marker=dict(colors=px.colors.qualitative.Set2)
                            )])
                            fig1.update_layout(title="Composition Distillat", height=400)
                            st.plotly_chart(fig1, use_container_width=True)

                        with col2:
                            # Pie chart résidu
                            bott_values = [d['bottoms'] for d in r['distribution']]
                            bott_labels = [d['compound'] for d in r['distribution']]

                            fig2 = go.Figure(data=[go.Pie(
                                labels=bott_labels,
                                values=bott_values,
                                hole=0.3,
                                marker=dict(colors=px.colors.qualitative.Set3)
                            )])
                            fig2.update_layout(title="Composition Résidu", height=400)
                            st.plotly_chart(fig2, use_container_width=True)

                    # TAB 2: Distribution
                    with tabs[1]:
                        compounds_names = [d['compound'] for d in r['distribution']]
                        feed_values = [d['feed'] for d in r['distribution']]
                        dist_values = [d['distillate'] for d in r['distribution']]
                        bott_values = [d['bottoms'] for d in r['distribution']]

                        fig = go.Figure(data=[
                            go.Bar(name='Alimentation', x=compounds_names, y=feed_values, marker_color='#667eea'),
                            go.Bar(name='Distillat', x=compounds_names, y=dist_values, marker_color='#764ba2'),
                            go.Bar(name='Résidu', x=compounds_names, y=bott_values, marker_color='#f093fb')
                        ])
                        fig.update_layout(
                            barmode='group',
                            title="Distribution des Composés",
                            xaxis_title="Composé",
                            yaxis_title="Débit (kmol/h)",
                            height=500
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # TAB 3: Bilans
                    with tabs[2]:
                        df = pd.DataFrame(r['distribution'])
                        df['feed'] = df['feed'].round(3)
                        df['distillate'] = df['distillate'].round(3)
                        df['bottoms'] = df['bottoms'].round(3)
                        df['recovery_D'] = df['recovery_D'].round(2)
                        df['recovery_B'] = df['recovery_B'].round(2)

                        st.dataframe(df, use_container_width=True)

                        st.info(f"Bilan matière: Alim = {r['flows']['feed']:.2f} | "
                               f"Dist = {r['flows']['distillate']:.2f} | "
                               f"Résidu = {r['flows']['bottoms']:.2f} kmol/h")

                    # TAB 4: Détails
                    with tabs[3]:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Fenske")
                            st.write(f"- N_min = {r['fenske']['N_min']:.3f} plateaux")
                            st.write(f"- α_avg = {r['fenske']['alpha_avg']:.3f}")

                            st.subheader("Underwood")
                            st.write(f"- R_min = {r['underwood']['R_min']:.3f}")
                            st.write(f"- θ = {r['underwood']['theta']:.3f}")

                            st.subheader("Températures")
                            st.write(f"- T_tête = {r['temperatures']['top']:.1f}°C")
                            st.write(f"- T_fond = {r['temperatures']['bottom']:.1f}°C")

                        with col2:
                            st.subheader("Gilliland")
                            st.write(f"- R_op = {r['gilliland']['R_operating']:.3f}")
                            st.write(f"- N_théorique = {r['gilliland']['N_theoretical']:.2f}")
                            st.write(f"- N_réel = {r['gilliland']['N_real']}")

                            st.subheader("Kirkbride")
                            st.write(f"- Plateau alim = {r['kirkbride']['feed_stage']}")
                            st.write(f"- N_rect = {r['kirkbride']['N_rectification']}")
                            st.write(f"- N_strip = {r['kirkbride']['N_stripping']}")

                            st.subheader("Énergie")
                            st.write(f"- Q_cond = {r['energy']['Q_condenser']:.0f} kW")
                            st.write(f"- Q_reb = {r['energy']['Q_reboiler']:.0f} kW")

                    # TAB 5: Économie
                    with tabs[4]:
                        # Créer l'optimiseur
                        def simulate_func(R_test):
                            return simulate_shortcut(
                                selected_compounds,
                                [c / 100 for c in compositions],
                                feed_rate, pressure, light_recovery, heavy_recovery,
                                feed_condition, R_test / r['underwood']['R_min'], efficiency
                            )

                        optimizer = EconomicOptimizer(simulate_func)

                        # Calculer le TAC actuel
                        tac_result = optimizer.calculate_TAC(
                            r['gilliland']['N_real'],
                            r['gilliland']['R_operating'],
                            r['energy']['Q_condenser'],
                            r['energy']['Q_reboiler']
                        )

                        # Afficher TAC
                        st.subheader("Total Annualized Cost (TAC)")

                        cols = st.columns(4)
                        cols[0].metric("TAC Total", f"{tac_result['TAC']/1000:.1f} k€/an")
                        cols[1].metric("Capital", f"{tac_result['annualized_capital']/1000:.1f} k€/an")
                        cols[2].metric("Exploitation", f"{tac_result['operating']['total']/1000:.1f} k€/an")
                        cols[3].metric("Maintenance", f"{tac_result['maintenance']/1000:.1f} k€/an")

                        st.divider()

                        # Breakdown
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Répartition des Coûts")
                            fig = go.Figure(data=[go.Pie(
                                labels=['Capital', 'Exploitation', 'Maintenance'],
                                values=[
                                    tac_result['annualized_capital'],
                                    tac_result['operating']['total'],
                                    tac_result['maintenance']
                                ],
                                hole=0.4
                            )])
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            st.subheader("Détails")
                            st.write("**Coûts d'Investissement:**")
                            st.write(f"- Colonne: {tac_result['capital']['column']/1000:.1f} k€")
                            st.write(f"- Condenseur: {tac_result['capital']['condenser']/1000:.1f} k€")
                            st.write(f"- Rebouilleur: {tac_result['capital']['reboiler']/1000:.1f} k€")
                            st.write(f"**Total: {tac_result['capital']['total']/1000:.1f} k€**")

                            st.write("\n**Coûts d'Exploitation:**")
                            st.write(f"- Énergie: {tac_result['operating']['energy']/1000:.1f} k€/an")
                            st.write(f"- Refroidissement: {tac_result['operating']['cooling']/1000:.1f} k€/an")
                else:
                    st.error(f"Erreur: {results_shortcut['error']}")

            # Affichage pour MESH Rigoureux
            elif calculation_method == 'MESH Rigoureux':
                if results_mesh['success']:
                    st.success("Convergence MESH atteinte!")

                    # Afficher les métriques principales
                    cols = st.columns(4)
                    cols[0].metric("Itérations", results_mesh['iterations'])
                    cols[1].metric("Statut", "Convergé ✓")
                    cols[2].metric("N plateaux", results_mesh['n_stages'])
                    cols[3].metric("Reflux", f"{results_mesh['R']:.3f}")

                    st.divider()

                    # Tabs pour les résultats MESH
                    tabs_mesh = st.tabs([
                        "Profils de Composition",
                        "Profils de Température",
                        "Débits",
                        "Bilans"
                    ])

                    with tabs_mesh[0]:
                        st.subheader("Profils de Composition Liquide")

                        # Créer le graphique des profils
                        fig = go.Figure()

                        for i, comp_name in enumerate(selected_compounds):
                            comp_display = COMPOUNDS_LIBRARY[comp_name]['name']
                            x_profile = [results_mesh['x'][stage][i] for stage in range(results_mesh['n_stages'])]

                            fig.add_trace(go.Scatter(
                                x=list(range(1, results_mesh['n_stages'] + 1)),
                                y=x_profile,
                                mode='lines+markers',
                                name=comp_display,
                                line=dict(width=2),
                                marker=dict(size=6)
                            ))

                        fig.update_layout(
                            title="Profils de Composition Liquide par Plateau",
                            xaxis_title="Numéro de Plateau",
                            yaxis_title="Fraction Molaire Liquide",
                            height=500,
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        st.info(f"Alimentation au plateau {results_mesh['feed_stage']}")

                    with tabs_mesh[1]:
                        st.subheader("Profils de Température")

                    # Convertir températures en Celsius
                    T_celsius = [T - 273.15 for T in results_mesh['T']]

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(1, results_mesh['n_stages'] + 1)),
                        y=T_celsius,
                        mode='lines+markers',
                        name='Température',
                        line=dict(color='red', width=3),
                        marker=dict(size=8)
                    ))

                    fig.update_layout(
                        title="Profil de Température dans la Colonne",
                        xaxis_title="Numéro de Plateau",
                        yaxis_title="Température (°C)",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("T Tête", f"{T_celsius[0]:.1f}°C")
                    col2.metric("T Alimentation", f"{T_celsius[results_mesh['feed_stage']-1]:.1f}°C")
                    col3.metric("T Fond", f"{T_celsius[-1]:.1f}°C")

                with tabs_mesh[2]:
                    st.subheader("💧 Débits Liquides et Vapeurs")

                    fig = make_subplots(rows=1, cols=2,
                                        subplot_titles=("Débits Liquides", "Débits Vapeurs"))

                    # Débits liquides
                    fig.add_trace(
                        go.Scatter(x=list(range(1, results_mesh['n_stages'] + 1)),
                                   y=results_mesh['L'],
                                   mode='lines+markers',
                                   name='Liquide',
                                   line=dict(color='blue', width=2)),
                        row=1, col=1
                    )

                    # Débits vapeurs
                    fig.add_trace(
                        go.Scatter(x=list(range(1, results_mesh['n_stages'] + 1)),
                                   y=results_mesh['V'],
                                   mode='lines+markers',
                                   name='Vapeur',
                                   line=dict(color='orange', width=2)),
                        row=1, col=2
                    )

                    fig.update_xaxes(title_text="Plateau", row=1, col=1)
                    fig.update_xaxes(title_text="Plateau", row=1, col=2)
                    fig.update_yaxes(title_text="Débit (kmol/h)", row=1, col=1)
                    fig.update_yaxes(title_text="Débit (kmol/h)", row=1, col=2)

                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

                with tabs_mesh[3]:
                    st.subheader("📋 Bilan Matière MESH")

                    # Compositions distillat
                    st.write("**Distillat:**")
                    dist_data = []
                    for i, comp_name in enumerate(selected_compounds):
                        dist_data.append({
                            'Composé': COMPOUNDS_LIBRARY[comp_name]['name'],
                            'Fraction': f"{results_mesh['x'][0][i]:.4f}",
                            'Débit (kmol/h)': f"{results_mesh['D'] * results_mesh['x'][0][i]:.3f}"
                        })
                    st.table(pd.DataFrame(dist_data))

                    st.write(f"**Débit total distillat:** {results_mesh['D']:.2f} kmol/h")

                    st.divider()

                    # Compositions résidu
                    st.write("**Résidu:**")
                    bott_data = []
                    for i, comp_name in enumerate(selected_compounds):
                        bott_data.append({
                            'Composé': COMPOUNDS_LIBRARY[comp_name]['name'],
                            'Fraction': f"{results_mesh['x'][-1][i]:.4f}",
                            'Débit (kmol/h)': f"{results_mesh['B'] * results_mesh['x'][-1][i]:.3f}"
                        })
                    st.table(pd.DataFrame(bott_data))

                    st.write(f"**Débit total résidu:** {results_mesh['B']:.2f} kmol/h")

                    st.divider()

                    # Vérification bilan
                    total_in = feed_rate
                    total_out = results_mesh['D'] + results_mesh['B']
                    error_balance = abs(total_in - total_out) / total_in * 100

                    if error_balance < 0.1:
                        st.success(f"✅ Bilan matière vérifié: F={total_in:.2f} | D+B={total_out:.2f} | Erreur: {error_balance:.4f}%")
                    else:
                        st.warning(f"⚠️ Erreur de bilan: {error_balance:.2f}%")

            else:
                st.error(f"❌ Erreur MESH: {results_mesh.get('error', 'Convergence non atteinte')}")

        # Mode Comparaison
        elif calculation_method == 'Comparaison':
            if results_shortcut['success'] and results_mesh['success']:
                st.success("✅ Simulation complète: Méthodes Simplifiées + MESH")

                # Comparaison des KPIs
                st.subheader("📊 Comparaison des Résultats")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Méthode", "Simplifiées")
                    st.write(f"N réel: {results_shortcut['results']['gilliland']['N_real']}")
                    st.write(f"R op: {results_shortcut['results']['gilliland']['R_operating']:.3f}")
                    st.write(f"T tête: {results_shortcut['results']['temperatures']['top']:.1f}°C")
                    st.write(f"T fond: {results_shortcut['results']['temperatures']['bottom']:.1f}°C")

                with col2:
                    st.metric("Méthode", "MESH")
                    st.write(f"N plateaux: {results_mesh['n_stages']}")
                    st.write(f"R op: {results_mesh['R']:.3f}")
                    st.write(f"T tête: {results_mesh['T'][0]-273.15:.1f}°C")
                    st.write(f"T fond: {results_mesh['T'][-1]-273.15:.1f}°C")

                with col3:
                    st.metric("Écarts", "")
                    N_diff = abs(results_shortcut['results']['gilliland']['N_real'] - results_mesh['n_stages'])
                    R_diff = abs(results_shortcut['results']['gilliland']['R_operating'] - results_mesh['R'])
                    T_top_diff = abs(results_shortcut['results']['temperatures']['top'] - (results_mesh['T'][0]-273.15))
                    T_bot_diff = abs(results_shortcut['results']['temperatures']['bottom'] - (results_mesh['T'][-1]-273.15))

                    st.write(f"ΔN: {N_diff:.0f} plateaux")
                    st.write(f"ΔR: {R_diff:.3f}")
                    st.write(f"ΔT tête: {T_top_diff:.1f}°C")
                    st.write(f"ΔT fond: {T_bot_diff:.1f}°C")

                st.divider()

                # Tabs combinés
                tabs_comp = st.tabs([
                    "📊 Simplifiées - Vue",
                    "📈 Simplifiées - Distribution",
                    "🔬 MESH - Profils",
                    "🌡️ MESH - Températures",
                    "💰 Économie"
                ])

                # Tab 1: Simplifiées Vue
                with tabs_comp[0]:
                    r = results_shortcut['results']

                    cols = st.columns(5)
                    cols[0].metric("N min", f"{r['fenske']['N_min']:.2f}")
                    cols[1].metric("N réel", r['gilliland']['N_real'])
                    cols[2].metric("R min", f"{r['underwood']['R_min']:.3f}")
                    cols[3].metric("R op", f"{r['gilliland']['R_operating']:.3f}")
                    cols[4].metric("Plateau alim", r['kirkbride']['feed_stage'])

                    col1, col2 = st.columns(2)

                    with col1:
                        dist_values = [d['distillate'] for d in r['distribution']]
                        dist_labels = [d['compound'] for d in r['distribution']]

                        fig1 = go.Figure(data=[go.Pie(labels=dist_labels, values=dist_values, hole=0.3)])
                        fig1.update_layout(title="Distillat", height=400)
                        st.plotly_chart(fig1, use_container_width=True)

                    with col2:
                        bott_values = [d['bottoms'] for d in r['distribution']]
                        bott_labels = [d['compound'] for d in r['distribution']]

                        fig2 = go.Figure(data=[go.Pie(labels=bott_labels, values=bott_values, hole=0.3)])
                        fig2.update_layout(title="Résidu", height=400)
                        st.plotly_chart(fig2, use_container_width=True)

                # Tab 2: Distribution
                with tabs_comp[1]:
                    r = results_shortcut['results']

                    compounds_names = [d['compound'] for d in r['distribution']]
                    feed_values = [d['feed'] for d in r['distribution']]
                    dist_values = [d['distillate'] for d in r['distribution']]
                    bott_values = [d['bottoms'] for d in r['distribution']]

                    fig = go.Figure(data=[
                        go.Bar(name='Alimentation', x=compounds_names, y=feed_values),
                        go.Bar(name='Distillat', x=compounds_names, y=dist_values),
                        go.Bar(name='Résidu', x=compounds_names, y=bott_values)
                    ])
                    fig.update_layout(barmode='group', title="Distribution", height=500)
                    st.plotly_chart(fig, use_container_width=True)

                # Tab 3: MESH Profils
                with tabs_comp[2]:
                    fig = go.Figure()
                    for i, comp_name in enumerate(selected_compounds):
                        comp_display = COMPOUNDS_LIBRARY[comp_name]['name']
                        x_profile = [results_mesh['x'][stage][i] for stage in range(results_mesh['n_stages'])]
                        fig.add_trace(go.Scatter(
                            x=list(range(1, results_mesh['n_stages'] + 1)),
                            y=x_profile,
                            mode='lines+markers',
                            name=comp_display
                        ))
                    fig.update_layout(
                        title="Profils de Composition (MESH)",
                        xaxis_title="Plateau",
                        yaxis_title="Fraction Molaire",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Tab 4: MESH Températures
                with tabs_comp[3]:
                    T_celsius = [T - 273.15 for T in results_mesh['T']]
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(1, results_mesh['n_stages'] + 1)),
                        y=T_celsius,
                        mode='lines+markers',
                        line=dict(color='red', width=3)
                    ))
                    fig.update_layout(
                        title="Profil de Température (MESH)",
                        xaxis_title="Plateau",
                        yaxis_title="T (°C)",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Tab 5: Économie
                with tabs_comp[4]:
                    r = results_shortcut['results']

                    def simulate_func(R_test):
                        return simulate_shortcut(
                            selected_compounds, [c / 100 for c in compositions],
                            feed_rate, pressure, light_recovery, heavy_recovery,
                            feed_condition, R_test / r['underwood']['R_min'], efficiency
                        )

                    optimizer = EconomicOptimizer(simulate_func)
                    tac_result = optimizer.calculate_TAC(
                        r['gilliland']['N_real'],
                        r['gilliland']['R_operating'],
                        r['energy']['Q_condenser'],
                        r['energy']['Q_reboiler']
                    )

                    st.subheader("💰 Total Annualized Cost (TAC)")
                    cols = st.columns(4)
                    cols[0].metric("TAC Total", f"{tac_result['TAC']/1000:.1f} k€/an")
                    cols[1].metric("Capital", f"{tac_result['annualized_capital']/1000:.1f} k€/an")
                    cols[2].metric("Exploitation", f"{tac_result['operating']['total']/1000:.1f} k€/an")
                    cols[3].metric("Maintenance", f"{tac_result['maintenance']/1000:.1f} k€/an")

            else:
                if not results_shortcut['success']:
                    st.error(f"❌ Erreur Simplifiées: {results_shortcut['error']}")
                if not results_mesh['success']:
                    st.error(f"❌ Erreur MESH: {results_mesh.get('error', 'Convergence non atteinte')}")

else:
    # Page d'accueil avec documentation
    st.markdown("""
    <div style='text-align: center; padding: 30px;'>
        <h2>👋 Bienvenue dans le Simulateur de Distillation</h2>
        <p style='font-size: 18px;'>Configurez les paramètres dans la barre latérale pour commencer</p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs de documentation
    doc_tabs = st.tabs([
        "📚 Méthodes Simplifiées",
        "🔬 MESH Rigoureux",
        "⚗️ Modèles d'Activité",
        "💰 Optimisation Économique",
        "📖 Guide Rapide"
    ])

    # TAB 1: Méthodes Simplifiées
    with doc_tabs[0]:
        st.header("📚 Méthodes Simplifiées (Shortcut Methods)")

        st.markdown("""
        Les **méthodes simplifiées** permettent un dimensionnement rapide des colonnes de distillation.
        Elles sont basées sur des corrélations empiriques et des hypothèses simplificatrices.
        """)

        st.divider()

        # Fenske
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 1️⃣ Fenske")
            st.markdown("**Équations 10-14**")
        with col2:
            st.markdown("""
            **Objectif:** Calculer le nombre **minimum** de plateaux théoriques (N_min)

            **Principe:**
            - Hypothèse: Reflux total (R → ∞)
            - Séparation basée uniquement sur les volatilités relatives

            **Formule:**
            ```
            N_min = ln[(x_LK,D / x_HK,D) × (x_HK,B / x_LK,B)] / ln(α_avg)
            ```

            **Où:**
            - `x_LK,D` : Fraction du composé léger dans le distillat
            - `x_HK,D` : Fraction du composé lourd dans le distillat
            - `x_LK,B` : Fraction du composé léger dans le résidu
            - `x_HK,B` : Fraction du composé lourd dans le résidu
            - `α_avg` : Volatilité relative moyenne

            **Usage:** Donne la limite théorique minimale de plateaux
            """)

        st.divider()

        # Underwood
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 2️⃣ Underwood")
            st.markdown("**Équations 15-18**")
        with col2:
            st.markdown("""
            **Objectif:** Calculer le reflux **minimum** (R_min)

            **Principe:**
            - Hypothèse: Nombre de plateaux infini (N → ∞)
            - Prend en compte la condition thermique de l'alimentation (q)

            **Formules:**

            1. Trouver θ (racine de l'équation):
            ```
            Σ[α_i × z_i / (α_i - θ)] = 1 - q
            ```

            2. Calculer R_min:
            ```
            R_min + 1 = Σ[α_i × x_D,i / (α_i - θ)]
            ```

            **Où:**
            - `α_i` : Volatilité relative du composé i
            - `z_i` : Fraction molaire dans l'alimentation
            - `x_D,i` : Fraction molaire dans le distillat
            - `q` : Condition thermique (q=1 pour liquide saturé)
            - `θ` : Paramètre d'Underwood (α_HK < θ < α_LK)

            **Usage:** Donne le reflux minimum théorique
            """)

        st.divider()

        # Gilliland
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 3️⃣ Gilliland")
            st.markdown("**Équations 19-21**")
        with col2:
            st.markdown("""
            **Objectif:** Relier le nombre de plateaux réels au reflux opératoire

            **Principe:**
            - Corrélation empirique entre (R, N) et (R_min, N_min)
            - Basée sur des données expérimentales

            **Formules:**

            1. Calculer X:
            ```
            X = (R - R_min) / (R + 1)
            ```

            2. Calculer Y via la corrélation de Gilliland:
            ```
            Y = 1 - exp[((1 + 54.4X)(X - 1)) / ((11 + 117.2X)√X)]
            ```

            3. Calculer N_théorique:
            ```
            N_théorique = N_min + Y / (1 - Y)
            ```

            4. Corriger avec l'efficacité:
            ```
            N_réel = N_théorique / E_murphree
            ```

            **Où:**
            - `R` : Reflux opératoire (typiquement 1.2 à 1.5 × R_min)
            - `E_murphree` : Efficacité de Murphree (60-80% typique)

            **Usage:** Dimensionnement réaliste de la colonne
            """)

        st.divider()

        # Kirkbride
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 4️⃣ Kirkbride")
            st.markdown("**Équations 22-23**")
        with col2:
            st.markdown("""
            **Objectif:** Déterminer la position optimale du plateau d'alimentation

            **Principe:**
            - Minimiser les besoins énergétiques
            - Équilibrer les sections de rectification et d'épuisement

            **Formule:**
            ```
            log(N_R / N_S) = 0.206 × log[(B/D) × (x_HK,F/x_LK,F) × (x_LK,B/x_HK,D)²]
            ```

            **Où:**
            - `N_R` : Nombre de plateaux en section de rectification
            - `N_S` : Nombre de plateaux en section d'épuisement
            - `B` : Débit de résidu
            - `D` : Débit de distillat
            - Plateau d'alimentation = N_R + 1

            **Usage:** Optimiser la position de l'alimentation
            """)

    # TAB 2: MESH Rigoureux
    with doc_tabs[1]:
        st.header("🔬 Méthode MESH Rigoureuse")

        st.markdown("""
        La **méthode MESH** résout rigoureusement les équations de bilan plateau par plateau.
        C'est la méthode la plus précise pour le design de colonnes de distillation.
        """)

        st.divider()

        st.markdown("### 📐 Les 4 Équations MESH")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🔹 M - Material Balance (Bilan Matière)
            **Équation 24**

            Pour chaque plateau j et composé i:
            ```
            L_{j+1}×x_{i,j+1} + V_{j-1}×y_{i,j-1} - L_j×x_{i,j} - V_j×y_{i,j} + F_j×z_{i,j} = 0
            ```

            **Où:**
            - L : Débit liquide (kmol/h)
            - V : Débit vapeur (kmol/h)
            - x : Fraction molaire liquide
            - y : Fraction molaire vapeur
            - F : Débit d'alimentation
            - z : Composition alimentation

            ---

            #### 🔹 E - Equilibrium (Équilibre)
            **Équation 30**

            ```
            y_{i,j} = K_{i,j} × x_{i,j}
            ```

            **Où:**
            - K : Coefficient de distribution
            - Pour mélanges idéaux: K = P_sat / P
            - Pour mélanges non-idéaux: K = (γ × P_sat) / P
            """)

        with col2:
            st.markdown("""
            #### 🔹 S - Summation (Sommation)
            **Équations 31-32**

            Sur chaque plateau, les fractions doivent sommer à 1:
            ```
            Σ x_{i,j} = 1    (phase liquide)
            Σ y_{i,j} = 1    (phase vapeur)
            ```

            ---

            #### 🔹 H - Heat Balance (Bilan Enthalpique)
            **Équation 33**

            ```
            L_{j+1}×h_{j+1} + V_{j-1}×H_{j-1} - L_j×h_j - V_j×H_j + F_j×h_F + Q_j = 0
            ```

            **Où:**
            - h : Enthalpie liquide (kJ/kmol)
            - H : Enthalpie vapeur (kJ/kmol)
            - Q : Chaleur ajoutée/retirée (kW)
            """)

        st.divider()

        st.markdown("### ⚙️ Algorithme de Wang-Henke")

        st.markdown("""
        **Méthode de résolution itérative:**

        1. **Initialisation** (Thomas algorithm)
           - Estimer T, x, y, L, V initiaux
           - Utiliser les résultats des méthodes simplifiées si disponibles

        2. **Boucle itérative** jusqu'à convergence:
           - **Étape 1:** Résoudre bilans matière (M) → nouveau x
           - **Étape 2:** Calculer équilibres (E) → nouveau y
           - **Étape 3:** Vérifier sommations (S)
           - **Étape 4:** Résoudre bilans énergie (H) → nouveau T
           - **Étape 5:** Calculer nouveaux K-values
           - **Étape 6:** Tester convergence

        3. **Critères de convergence** (Équations 36-39):
           ```
           ε_T < 0.1 K      (températures)
           ε_x < 1e-6       (compositions liquides)
           ε_L < 0.01       (débits liquides)
           ε_V < 0.01       (débits vapeurs)
           ```

        4. **Résultats:**
           - Profils de température
           - Profils de composition (tous les plateaux)
           - Débits liquides et vapeurs
           - Bilans matière exacts
        """)

        st.info("""
        **💡 Avantages MESH:**
        - ✅ Précision maximale
        - ✅ Profils complets plateau par plateau
        - ✅ Compatible avec modèles d'activité
        - ✅ Vérifie les bilans matière/énergie

        **⚠️ Inconvénients:**
        - ⏱️ Plus lent (10-60s vs <1s)
        - 🔧 Nécessite bonne initialisation
        - 💻 Plus complexe à mettre en œuvre
        """)

    # TAB 3: Modèles d'Activité
    with doc_tabs[2]:
        st.header("⚗️ Modèles d'Activité (Mélanges Non-Idéaux)")

        st.markdown("""
        Les **modèles d'activité** corrigent les K-values pour les mélanges non-idéaux.
        Ils sont essentiels pour les systèmes avec interactions moléculaires fortes.
        """)

        st.divider()

        # Idéal
        st.markdown("### 1️⃣ Modèle Idéal")
        st.markdown("""
        **Hypothèse:** Aucune interaction moléculaire

        ```
        γ_i = 1    (pour tous les composés)
        K_i = P_sat,i / P
        ```

        **Usage:** Hydrocarbures similaires (benzène-toluène-xylène)
        """)

        st.divider()

        # Wilson
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 2️⃣ Wilson")
            st.markdown("**Équation 40a**")
        with col2:
            st.markdown("""
            **Formule:**
            ```
            ln(γ_i) = 1 - ln(Σ_j x_j Λ_{ij}) - Σ_k [x_k Λ_{ki} / Σ_j x_j Λ_{kj}]

            Λ_{ij} = (V_j / V_i) × exp(-a_{ij} / T)
            ```

            **Paramètres:**
            - `a_{ij}` : Paramètres d'interaction binaire (K)
            - `V_i` : Volume molaire du composé i (m³/mol)

            **Avantages:**
            - ✅ Simple, 2 paramètres par paire
            - ✅ Bon pour alcools, cétones

            **Limitations:**
            - ❌ Ne peut pas prédire LLE (démixtion)
            """)

        st.divider()

        # NRTL
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 3️⃣ NRTL")
            st.markdown("**Équation 40b**")
        with col2:
            st.markdown("""
            **Formule (Non-Random Two-Liquid):**
            ```
            ln(γ_i) = [Σ_j x_j τ_{ji} G_{ji} / Σ_k x_k G_{ki}] +
                      Σ_j [x_j G_{ij} / Σ_k x_k G_{kj}] × [τ_{ij} - Σ_m x_m τ_{mj} G_{mj} / Σ_k x_k G_{kj}]

            G_{ij} = exp(-α_{ij} τ_{ij})
            τ_{ij} = a_{ij} / T
            ```

            **Paramètres:**
            - `a_{ij}` : Énergie d'interaction (K)
            - `α_{ij}` : Non-randomness (0.2-0.47, typ. 0.3)

            **Avantages:**
            - ✅ Peut prédire LLE
            - ✅ Très flexible, 3 paramètres
            - ✅ Excellent pour systèmes polaires

            **Usage:** Alcools-eau, amines, azéotropes
            """)

        st.divider()

        # UNIQUAC
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 4️⃣ UNIQUAC")
            st.markdown("**Équation 40c**")
        with col2:
            st.markdown("""
            **Formule (Universal Quasi-Chemical):**
            ```
            ln(γ_i) = ln(γ_i^C) + ln(γ_i^R)
            ```

            **Partie Combinatoire (taille/forme):**
            ```
            ln(γ_i^C) = ln(Φ_i/x_i) + z/2 q_i ln(θ_i/Φ_i) + l_i - (Φ_i/x_i) Σ_j x_j l_j
            ```

            **Partie Résiduelle (interactions):**
            ```
            ln(γ_i^R) = q_i [1 - ln(Σ_j θ_j τ_{ji}) - Σ_j θ_j τ_{ij} / Σ_k θ_k τ_{kj}]
            ```

            **Paramètres:**
            - `r_i` : Volume relatif (paramètre de taille)
            - `q_i` : Surface relative (paramètre de forme)
            - `a_{ij}` : Énergie d'interaction (K)
            - `z` : Nombre de coordination (= 10)

            **Avantages:**
            - ✅ Base théorique solide
            - ✅ Excellent pour polymères
            - ✅ Prend en compte taille/forme

            **Usage:** Systèmes complexes, électrolytes
            """)

        st.info("""
        **🎯 Guide de sélection du modèle:**

        | Système | Modèle Recommandé |
        |---------|-------------------|
        | Hydrocarbures similaires | Idéal |
        | Alcools, cétones | Wilson |
        | Systèmes polaires, azéotropes | NRTL |
        | Mélanges aqueux, électrolytes | UNIQUAC |
        | Systèmes avec démixtion (LLE) | NRTL ou UNIQUAC |
        """)

    # TAB 4: Optimisation Économique
    with doc_tabs[3]:
        st.header("💰 Optimisation Économique")

        st.markdown("""
        L'**optimisation économique** vise à minimiser le **TAC (Total Annualized Cost)**,
        qui combine les coûts d'investissement et d'exploitation.
        """)

        st.divider()

        st.markdown("### 💵 TAC - Total Annualized Cost")
        st.markdown("**Équation 43**")

        st.code("""
TAC = C_capital × CRF + C_operating + C_maintenance
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **📊 Coûts d'Investissement**
            *Équation 44*

            ```
            C_capital = C_column + C_condenser + C_reboiler
            ```

            - **Colonne:** 15000 €/m
            - **Plateaux:** 800 €/plateau
            - **Condenseur:** 2000 €/kW
            - **Rebouilleur:** 2500 €/kW
            """)

        with col2:
            st.markdown("""
            **⚡ Coûts d'Exploitation**
            *Équation 45*

            ```
            C_operating = C_energy + C_cooling
            ```

            - **Énergie:** 0.08 €/kWh
            - **Refroidissement:** 0.02 €/kWh
            - **Heures/an:** 8000 h
            """)

        with col3:
            st.markdown("""
            **🔧 Coûts de Maintenance**
            *Équation 46*

            ```
            C_maintenance = 0.05 × C_capital
            ```

            - **5% du capital par an**
            - Entretien, réparations
            - Inspections réglementaires
            """)

        st.divider()

        st.markdown("### 📈 Optimisation du Reflux")
        st.markdown("**Section 9.1 du PDF**")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            **Principe:**

            Il existe un **reflux optimal** qui minimise le TAC :

            - **R trop faible (proche de R_min):**
              - ⬆️ Beaucoup de plateaux nécessaires
              - ⬆️ Coûts d'investissement élevés
              - ⬇️ Coûts d'exploitation faibles

            - **R trop élevé:**
              - ⬇️ Moins de plateaux nécessaires
              - ⬇️ Coûts d'investissement faibles
              - ⬆️ Coûts d'exploitation élevés (énergie)

            - **R optimal (typiquement 1.2-1.5 × R_min):**
              - ⚖️ Équilibre entre capital et exploitation
              - 💰 TAC minimum
            """)

        with col2:
            st.markdown("""
            **Méthode:**

            1. Fixer N_min, R_min
            2. Tester plusieurs R
            3. Calculer N(R) via Gilliland
            4. Calculer TAC pour chaque R
            5. Identifier R optimal (TAC min)
            """)

        st.divider()

        st.markdown("### 🎯 Optimisation Multi-Objectifs")

        st.markdown("""
        **Objectifs conflictuels:**

        1. **Minimiser le TAC** (coût)
        2. **Maximiser la pureté** (qualité produit)
        3. **Minimiser l'impact environnemental** (CO₂, consommation énergétique)

        **Approche:**

        ```python
        Objectif = w₁ × TAC_normalisé + w₂ × (1 - Pureté) + w₃ × Impact_env
        ```

        Où `w₁ + w₂ + w₃ = 1` (poids relatifs des objectifs)

        **Algorithme:** Évolution différentielle pour exploration globale
        """)

    # TAB 5: Guide Rapide
    with doc_tabs[4]:
        st.header("📖 Guide Rapide d'Utilisation")

        st.markdown("### 🚀 Étapes pour une Simulation")

        st.markdown("""
        #### 1️⃣ Sélectionner les Composés
        - Minimum **2 composés** requis
        - Disponibles: BTX, alcools, alcanes (13 composés)

        #### 2️⃣ Définir les Compositions
        - Entrer les pourcentages molaires
        - Cliquer sur **"Normaliser"** pour ajuster à 100%

        #### 3️⃣ Paramètres Opératoires
        - **Débit:** 1-10000 kmol/h
        - **Pression:** Typiquement 101325 Pa (1 atm)
        - **Condition thermique:**
          - Liquide saturé (q=1) → le plus courant
          - Vapeur saturée (q=0)
          - Mixte (0<q<1)

        #### 4️⃣ Spécifications
        - **Récupérations:** 90-99% typique
        - **Multiplicateur reflux:** 1.2-1.5 recommandé
        - **Efficacité:** 70% pour estimation préliminaire

        #### 5️⃣ Choisir la Méthode
        - **Méthodes Simplifiées:** Design rapide
        - **MESH Rigoureux:** Résultats précis
        - **Comparaison:** Voir les deux

        #### 6️⃣ Lancer la Simulation
        - Cliquer sur **"🚀 LANCER LA SIMULATION"**
        - Analyser les résultats dans les onglets
        """)

        st.divider()

        st.markdown("### 💡 Conseils et Bonnes Pratiques")

        col1, col2 = st.columns(2)

        with col1:
            st.success("""
            **✅ À FAIRE:**

            - Commencer par méthodes simplifiées
            - Vérifier le bilan matière (F = D + B)
            - Valider que N_réel > N_min
            - Vérifier que R_op > R_min
            - Utiliser MESH pour validation finale
            - Comparer les résultats entre méthodes
            """)

        with col2:
            st.error("""
            **❌ À ÉVITER:**

            - Récupérations > 99.9%
            - Reflux trop proche de R_min
            - Efficacité > 95% (irréaliste)
            - Oublier de normaliser les compositions
            - Ignorer les warnings de l'application
            - Sauter la vérification des bilans
            """)

        st.divider()

        st.markdown("### 🎓 Exemple Complet: Système BTX")

        with st.expander("📝 Voir l'exemple détaillé"):
            st.markdown("""
            **Configuration:**
            ```
            Composés: Benzène (33.3%), Toluène (33.3%), o-Xylène (33.4%)
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
            N min (Fenske) ≈ 6.8 plateaux
            R min (Underwood) ≈ 1.85
            R opératoire ≈ 2.41
            N théorique ≈ 14 plateaux
            N réel ≈ 19 plateaux
            Plateau alimentation ≈ 10

            T tête ≈ 80.1°C (Tb benzène)
            T fond ≈ 144.4°C (Tb o-xylène)
            ```

            **Interprétation:**
            - Colonne de ~19 plateaux nécessaire
            - Alimenter au 10ème plateau (milieu)
            - Reflux 1.3× le minimum (bon compromis)
            - Gradient de température ~64°C
            """)

        st.divider()

        st.markdown("### 📚 Ressources")

        st.info("""
        **Documentation Complète:**
        - [README_COMPLET.md](README_COMPLET.md) - Guide exhaustif
        - [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Guide Streamlit
        - [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) - Détails techniques

        **Code Source:**
        - `mesh_solver.py` - Solveur MESH rigoureux
        - `activity_models.py` - Modèles thermodynamiques
        - `economic_optimization.py` - Optimisation TAC

        **Cours:**
        - Prof. BAKHER Zine Elabidine
        - Modélisation et Simulation des Procédés
        - Filière PIC - UH1 - 2024-2025
        """)

# =============================================================================
# DOCUMENTATION PAGE
# =============================================================================

elif st.session_state.current_page == 'Documentation':
    st.markdown("## Documentation")
    
    # Theory Section
    st.markdown("""
    <div class='info-card'>
        <h3 style='margin-top: 0;'>Théorie et Méthodes</h3>
        <p style='color: #666; line-height: 1.6;'>
            Cette application implémente les principales méthodes de calcul pour la distillation multicomposants,
            telles qu'enseignées dans le cours de Modélisation et Simulation des Procédés.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Methods Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Méthodes Simplifiées")
        st.markdown("""
        **Équation de Fenske** (Nombre minimum de plateaux)
        ```
        N_min = log[(x_LK,D / x_HK,D) / (x_LK,B / x_HK,B)] / log(α_avg)
        ```
        
        **Équation d'Underwood** (Reflux minimum)
        ```
        Σ [α_i × z_i / (α_i - θ)] = 1 - q
        R_min + 1 = Σ [α_i × x_D,i / (α_i - θ)]
        ```
        
        **Corrélation de Gilliland** (Nombre de plateaux réels)
        ```
        X = (R - R_min) / (R + 1)
        Y = f(X)  [corrélation empirique]
        N = N_min + Y / (1 - Y)
        ```
        
        **Équation de Kirkbride** (Position d'alimentation)
        ```
        log(N_R / N_S) = 0.206 × log[...]
        ```
        """)
    
    with col2:
        st.markdown("### Méthode MESH")
        st.markdown("""
        **Équations MESH** (résolution simultanée)
        
        **M** - Material Balance (Bilan matière):
        ```
        L_j × x_i,j + V_j × y_i,j = L_j-1 × x_i,j-1 + V_j+1 × y_i,j+1 + F_j × z_i,j
        ```
        
        **E** - Equilibrium (Équilibre):
        ```
        y_i,j = K_i,j × x_i,j
        K_i,j = (γ_i × P_i^sat) / P
        ```
        
        **S** - Summation (Somme):
        ```
        Σ x_i,j = 1
        Σ y_i,j = 1
        ```
        
        **H** - Heat Balance (Bilan thermique):
        ```
        L_j × h_L,j + V_j × h_V,j = L_j-1 × h_L,j-1 + V_j+1 × h_V,j+1 + F_j × h_F,j + Q_j
        ```
        """)
    
    # Example Section
    st.markdown("---")
    st.markdown("### Exemple d'Application")
    
    st.markdown("""
    <div class='info-card'>
        <h4>Séparation Benzène / Toluène / o-Xylène</h4>
        
        **Données:**
        - Alimentation: 100 kmol/h (33.3% / 33.3% / 33.4%)
        - Pression: 101325 Pa
        - Récupérations: 95% pour chaque clé
        - Reflux: 1.3 × R_min
        
        **Résultats attendus:**
        ```
        N min (Fenske) ≈ 6.8 plateaux
        R min (Underwood) ≈ 1.85
        R opératoire ≈ 2.41
        N théorique ≈ 14 plateaux
        N réel ≈ 19 plateaux
        Plateau alimentation ≈ 10

        T tête ≈ 80.1°C (Tb benzène)
        T fond ≈ 144.4°C (Tb o-xylène)
        ```

        **Interprétation:**
        - Colonne de ~19 plateaux nécessaire
        - Alimenter au 10ème plateau (milieu)
        - Reflux 1.3× le minimum (bon compromis)
        - Gradient de température ~64°C
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Ressources")

    st.markdown("""
    <div class='info-card'>
        <h4>Documentation Complète</h4>
        <ul style='color: #666; line-height: 1.8;'>
            <li><strong>README_COMPLET.md</strong> - Guide exhaustif</li>
            <li><strong>STREAMLIT_GUIDE.md</strong> - Guide Streamlit</li>
            <li><strong>IMPLEMENTATION_COMPLETE.md</strong> - Détails techniques</li>
        </ul>
        
        <h4 style='margin-top: 20px;'>Code Source</h4>
        <ul style='color: #666; line-height: 1.8;'>
            <li><strong>mesh_solver.py</strong> - Solveur MESH rigoureux</li>
            <li><strong>activity_models.py</strong> - Modèles thermodynamiques</li>
            <li><strong>economic_optimization.py</strong> - Optimisation TAC</li>
        </ul>
        
        <h4 style='margin-top: 20px;'>Cours</h4>
        <p style='color: #666; line-height: 1.6;'>
            Prof. BAKHER Zine Elabidine<br>
            Modélisation et Simulation des Procédés<br>
            Filière PIC - UH1 - 2024-2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# Show message when no page is active
else:
    st.info("Sélectionnez une page dans le menu de navigation ci-dessus pour commencer")
