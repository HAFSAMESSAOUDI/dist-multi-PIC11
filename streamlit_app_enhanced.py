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
from pdf_generator import SimulationPDFGenerator

#  Fonction helper pour générer et afficher le bouton de téléchargement PDF
def display_pdf_download_button(simulation_data, method_name):
    """
    Affiche un bouton pour télécharger les résultats en PDF/LaTeX

    Parameters
    ----------
    simulation_data : dict
        Données de simulation
    method_name : str
        Nom de la méthode utilisée
    """
    st.divider()
    st.subheader("📥 Télécharger les Résultats")

    col_pdf1, col_pdf2 = st.columns(2)

    with col_pdf1:
        st.markdown("**Format LaTeX (.tex)**")
        st.caption("Fichier source LaTeX modifiable")

    with col_pdf2:
        try:
            pdf_gen = SimulationPDFGenerator()
            latex_content = pdf_gen.generate_latex_only(simulation_data, method_name)

            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rapport_distillation_{timestamp}.tex"

            st.download_button(
                label="📄 Télécharger LaTeX",
                data=latex_content.encode('utf-8'),
                file_name=filename,
                mime="application/x-latex",
                use_container_width=True,
                type="primary"
            )

            st.info("💡 Compilez ce fichier avec pdfLaTeX ou Overleaf pour obtenir un PDF professionnel")

        except Exception as e:
            st.error(f"Erreur lors de la génération du rapport: {e}")

# Configuration de la page
st.set_page_config(
    page_title="Distillation Multicomposants",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Design professionnel et épuré
st.markdown("""
<style>
    /* Style général */
    .main {
        background-color: #f8f9fa;
    }

    /* Boutons */
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    /* Titres */
    h1 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #334155;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #475569;
        font-weight: 600;
    }

    /* Métriques */
    .stMetric {
        background-color: white;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Cartes d'information */
    .info-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Navigation */
    .nav-button {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    .nav-button:hover {
        border-color: #2563eb;
        background-color: #eff6ff;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
    }

    /* Équations */
    .equation {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #2563eb;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }

    .equation-number {
        color: #2563eb;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    /* Dividers */
    hr {
        margin: 2rem 0;
        border-color: #e2e8f0;
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
    """Simulation avec les méthodes simplifiées"""
    try:
        # Créer les objets Compound (utiliser les noms pour la bibliothèque thermo)
        compound_objects = []
        compound_name_map = {
            'benzene': 'benzene',
            'toluene': 'toluene',
            'o-xylene': 'o-xylene',
            'ethylbenzene': 'ethylbenzene',
            'cumene': 'cumene',
            'styrene': 'styrene',
            'methanol': 'methanol',
            'ethanol': 'ethanol',
            'propanol': '1-propanol',
            'butanol': '1-butanol',
            'hexane': 'hexane',
            'heptane': 'heptane',
            'octane': 'octane'
        }

        for compound_key in compounds:
            thermo_name = compound_name_map.get(compound_key, compound_key)
            compound_objects.append(Compound(name=thermo_name))

        # Package thermodynamique
        thermo = ThermodynamicPackage(compound_objects)

        # K-values moyens
        T_avg = sum([c.Tb for c in compound_objects]) / len(compound_objects)
        K_values = thermo.K_values(T_avg, pressure)

        # Volatilités relatives
        alpha = thermo.relative_volatilities(T_avg, pressure)

        # Fenske - N_min
        LK_idx, HK_idx = 0, len(compound_objects) - 1
        x_LK_D = light_key_recovery / 100 * compositions[LK_idx]
        x_HK_D = (1 - heavy_key_recovery / 100) * compositions[HK_idx]
        x_LK_B = (1 - light_key_recovery / 100) * compositions[LK_idx]
        x_HK_B = heavy_key_recovery / 100 * compositions[HK_idx]

        alpha_avg = (alpha[LK_idx] * alpha[HK_idx]) ** 0.5
        N_min = np.log((x_LK_D / x_HK_D) * (x_HK_B / x_LK_B)) / np.log(alpha_avg)

        # Underwood - R_min
        q = feed_thermal_condition

        def underwood_eq1(theta):
            return sum([alpha[i] * compositions[i] / (alpha[i] - theta) for i in range(len(compositions))]) - (1 - q)

        from scipy.optimize import fsolve
        theta = fsolve(underwood_eq1, alpha[HK_idx] + 0.1)[0]

        D = feed_rate * sum([compositions[i] * light_key_recovery / 100 if i == LK_idx else compositions[i] * (1 - heavy_key_recovery / 100) for i in range(len(compositions))])
        x_D = [compositions[i] * light_key_recovery / 100 / D * feed_rate if i == LK_idx else compositions[i] * (1 - heavy_key_recovery / 100) / D * feed_rate for i in range(len(compositions))]

        R_min_plus_1 = sum([alpha[i] * x_D[i] / (alpha[i] - theta) for i in range(len(compositions))])
        R_min = R_min_plus_1 - 1

        # Gilliland
        R_operating = R_min * reflux_ratio_multiplier
        X = (R_operating - R_min) / (R_operating + 1)
        Y = 1 - np.exp(((1 + 54.4 * X) * (X - 1)) / ((11 + 117.2 * X) * X ** 0.5))
        N_theoretical = N_min + Y / (1 - Y) if Y < 1 else N_min * 2
        N_real = int(np.ceil(N_theoretical / efficiency))

        # Kirkbride
        B = feed_rate - D
        ratio = (B / D) * (compositions[HK_idx] / compositions[LK_idx]) * (x_LK_B / x_HK_D) ** 2
        log_ratio = np.log10(ratio)
        NR_over_NS = 10 ** (0.206 * log_ratio)
        N_R = int(np.ceil(N_real * NR_over_NS / (1 + NR_over_NS)))
        feed_stage = N_R + 1

        # Distribution et températures
        distribution = []
        for i, compound_key in enumerate(compounds):
            if i == LK_idx:
                d_i = feed_rate * compositions[i] * light_key_recovery / 100
            elif i == HK_idx:
                d_i = feed_rate * compositions[i] * (1 - heavy_key_recovery / 100)
            else:
                d_i = feed_rate * compositions[i] * 0.5

            b_i = feed_rate * compositions[i] - d_i

            distribution.append({
                'compound': COMPOUNDS_LIBRARY[compound_key]['name'],
                'feed': feed_rate * compositions[i],
                'distillate': d_i,
                'bottoms': b_i
            })

        T_top = compound_objects[0].Tb - 273.15  # Convertir K vers °C
        T_bottom = compound_objects[-1].Tb - 273.15  # Convertir K vers °C

        # Besoins énergétiques (estimation simplifiée)
        lambda_avg = 35000  # kJ/kmol (estimation)
        Q_condenser = R_operating * D * lambda_avg / 3600  # kW
        Q_reboiler = (R_operating + 1) * D * lambda_avg / 3600  # kW

        return {
            'success': True,
            'results': {
                'fenske': {'N_min': N_min},
                'underwood': {'R_min': R_min, 'theta': theta},
                'gilliland': {'N_theoretical': N_theoretical, 'N_real': N_real, 'R_operating': R_operating},
                'kirkbride': {'feed_stage': feed_stage, 'N_R': N_R, 'N_S': N_real - N_R},
                'distribution': distribution,
                'temperatures': {'top': T_top, 'bottom': T_bottom},
                'energy': {'Q_condenser': Q_condenser, 'Q_reboiler': Q_reboiler}
            }
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def simulate_mesh(compounds, compositions, feed_rate, pressure,
                  light_recovery, heavy_recovery, feed_condition,
                  reflux_multiplier, efficiency, thermo_model='Idéal'):
    """Simulation avec la méthode MESH rigoureuse"""
    try:
        # Créer les objets Compound
        compound_objects = []
        compound_name_map = {
            'benzene': 'benzene',
            'toluene': 'toluene',
            'o-xylene': 'o-xylene',
            'ethylbenzene': 'ethylbenzene',
            'cumene': 'cumene',
            'styrene': 'styrene',
            'methanol': 'methanol',
            'ethanol': 'ethanol',
            'propanol': '1-propanol',
            'butanol': '1-butanol',
            'hexane': 'hexane',
            'heptane': 'heptane',
            'octane': 'octane'
        }

        for compound_key in compounds:
            thermo_name = compound_name_map.get(compound_key, compound_key)
            compound_objects.append(Compound(name=thermo_name))

        # Obtenir N et R depuis les méthodes simplifiées pour initialisation
        shortcut_results = simulate_shortcut(
            compounds, compositions, feed_rate, pressure,
            light_recovery, heavy_recovery, feed_condition,
            reflux_multiplier, efficiency
        )

        if not shortcut_results['success']:
            return {'success': False, 'error': 'Échec de l\'initialisation avec méthodes simplifiées'}

        r = shortcut_results['results']
        N_stages = r['gilliland']['N_real']
        feed_stage = r['kirkbride']['feed_stage']
        R = r['gilliland']['R_operating']

        # Estimer D depuis les récupérations
        D = feed_rate * sum([compositions[i] * light_recovery / 100 if i == 0
                            else compositions[i] * (1 - heavy_recovery / 100)
                            for i in range(len(compositions))])

        # Créer le solveur MESH
        mesh_solver = MESHSolver(
            compounds=compound_objects,
            n_stages=N_stages,
            feed_stage=feed_stage,
            pressure=pressure
        )

        # Sélectionner le modèle d'activité
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
        z_F = np.array(compositions)
        mesh_raw = mesh_solver.solve(feed_rate, z_F, R, D, max_iter=100, verbose=False)

        # Reformater les résultats
        if mesh_raw['converged']:
            return {
                'success': True,
                'converged': True,
                'iterations': mesh_raw['iterations'],
                'n_stages': N_stages,
                'feed_stage': feed_stage,
                'R': R,
                'D': mesh_raw['distillate']['flow'],
                'B': mesh_raw['bottoms']['flow'],
                'x_D': mesh_raw['distillate']['composition'],
                'x_B': mesh_raw['bottoms']['composition'],
                'T': mesh_raw['temperatures'],
                'x': mesh_raw['compositions']['liquid'],
                'y': mesh_raw['compositions']['vapor'],
                'L': mesh_raw['flows']['liquid'],
                'V': mesh_raw['flows']['vapor'],
                'Q_condenser': abs(mesh_raw['duties']['condenser']) / 1000,  # kW
                'Q_reboiler': abs(mesh_raw['duties']['reboiler']) / 1000,  # kW
            }
        else:
            return {
                'success': False,
                'converged': False,
                'error': f"MESH n'a pas convergé après {mesh_raw['iterations']} itérations"
            }

    except Exception as e:
        import traceback
        return {'success': False, 'error': f"Erreur MESH: {str(e)}\n{traceback.format_exc()}"}


# =============================================================================
# GESTION DE L'ÉTAT DE NAVIGATION
# =============================================================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# =============================================================================
# EN-TÊTE PRINCIPAL
# =============================================================================

col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.title("Simulateur de Distillation Multicomposants")
    st.markdown("**La distillation - Procédés de Séparation**")

with col_header2:
    if st.session_state.current_page != 'home':
        if st.button("← Retour à l'accueil", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()

st.divider()

# =============================================================================
# PAGE D'ACCUEIL
# =============================================================================

if st.session_state.current_page == 'home':

    # Boutons de navigation principaux
    st.subheader("Bienvenue")
    st.write("Sélectionnez un module pour commencer:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Lancer une Simulation", use_container_width=True, type="primary"):
            st.session_state.current_page = 'simulation'
            st.rerun()
        st.caption("Effectuer des calculs de dimensionnement de colonne")

    with col2:
        if st.button("Documentation Théorique", use_container_width=True):
            st.session_state.current_page = 'documentation'
            st.rerun()
        st.caption("Consulter les équations et méthodes de calcul")

    with col3:
        if st.button("Guide d'Utilisation", use_container_width=True):
            st.session_state.current_page = 'guide'
            st.rerun()
        st.caption("Apprendre à utiliser l'application")


    st.divider()

    # Présentation
    st.subheader("À propos de ce simulateur")

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("""
        <div class="info-card">
        <h4>Méthodes Disponibles</h4>
        <ul>
            <li><b>Méthodes Simplifiées:</b> Fenske, Underwood, Gilliland, Kirkbride</li>
            <li><b>MESH Rigoureux:</b> Algorithme Wang-Henke avec bilans plateau par plateau</li>
            <li><b>Modèles Thermodynamiques:</b> Idéal, Wilson, NRTL, UNIQUAC</li>
            <li><b>Optimisation Économique:</b> Calcul du TAC (Total Annualized Cost)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown("""
        <div class="info-card">
        <h4>Composés Disponibles</h4>
        <ul>
            <li><b>Aromatiques:</b> Benzène, Toluène, Xylène, Éthylbenzène, Cumène, Styrène</li>
            <li><b>Alcools:</b> Méthanol, Éthanol, 1-Propanol, 1-Butanol</li>
            <li><b>Alcanes:</b> Hexane, Heptane, Octane</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Exemples de Cas d'Usage")

    tab1, tab2, tab3 = st.tabs(["Système BTX", "Alcools", "Alcanes"])

    with tab1:
        st.markdown("""
        **Séparation Benzène-Toluène-Xylène (BTX)**

        Configuration recommandée:
        - Composés: Benzène (33.3%), Toluène (33.3%), o-Xylène (33.4%)
        - Débit: 100 kmol/h
        - Pression: 101325 Pa (1 atm)
        - Récupérations: 95% / 95%
        - Multiplicateur de reflux: 1.3

        Résultats attendus: ~19 plateaux réels, Reflux opératoire ~2.4
        """)

    with tab2:
        st.markdown("""
        **Séparation d'Alcools**

        Configuration recommandée:
        - Composés: Méthanol, Éthanol, 1-Propanol
        - Utiliser modèle d'activité Wilson ou NRTL
        - Récupérations: 90-95%

        Note: Les alcools forment des mélanges non-idéaux
        """)

    with tab3:
        st.markdown("""
        **Séparation d'Alcanes**

        Configuration recommandée:
        - Composés: Hexane, Heptane, Octane
        - Modèle Idéal acceptable
        - Récupérations: 95% / 95%

        Note: Comportement proche de l'idéalité
        """)

# =============================================================================
# PAGE DE SIMULATION
# =============================================================================

elif st.session_state.current_page == 'simulation':

    # Sidebar pour la configuration
    with st.sidebar:
        st.header("Configuration de la Simulation")

        # Méthode de calcul
        st.subheader("Méthode de Calcul")
        calculation_method = st.selectbox(
            "Choisir la méthode",
            ['Méthodes Simplifiées', 'MESH Rigoureux', 'Comparaison']
        )

        # Modèle thermodynamique
        if calculation_method in ['MESH Rigoureux', 'Comparaison']:
            st.subheader("Modèle Thermodynamique")
            thermo_model = st.selectbox(
                "Modèle d'activité",
                ['Idéal', 'Wilson', 'NRTL', 'UNIQUAC']
            )
        else:
            thermo_model = 'Idéal'

        st.divider()

        # Sélection des composés
        st.subheader("Composés")
        selected_compounds = st.multiselect(
            "Sélectionner les composés",
            options=list(COMPOUNDS_LIBRARY.keys()),
            default=['benzene', 'toluene'],
            format_func=lambda x: f"{COMPOUNDS_LIBRARY[x]['name']} ({COMPOUNDS_LIBRARY[x]['formula']})"
        )

        # Compositions
        if len(selected_compounds) >= 2:
            st.subheader("Compositions Molaires (%)")
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
                if st.button("Normaliser les compositions"):
                    st.rerun()
            else:
                st.success(f"Total = {total_comp:.1f}%")

            st.divider()

            # Paramètres opératoires
            st.subheader("Paramètres Opératoires")

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

            feed_condition = st.slider(
                "Condition thermique (q)",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.1,
                help="q=0: vapeur saturée, q=1: liquide saturé"
            )

            st.divider()

            # Spécifications
            st.subheader("Spécifications de Séparation")

            light_recovery = st.slider(
                "Récupération du léger (%)",
                min_value=50.0,
                max_value=99.9,
                value=95.0,
                step=0.5
            )

            heavy_recovery = st.slider(
                "Récupération du lourd (%)",
                min_value=50.0,
                max_value=99.9,
                value=95.0,
                step=0.5
            )

            reflux_multiplier = st.slider(
                "Multiplicateur de reflux",
                min_value=1.1,
                max_value=3.0,
                value=1.3,
                step=0.1,
                help="R_op = R_min × multiplicateur"
            )

            efficiency = st.slider(
                "Efficacité de Murphree",
                min_value=0.5,
                max_value=0.95,
                value=0.70,
                step=0.05
            )

            st.divider()

            # Bouton de simulation
            run_simulation = st.button("Lancer la Simulation", type="primary", use_container_width=True)

        else:
            st.warning("Sélectionnez au moins 2 composés")
            run_simulation = False

    # Zone principale de résultats
    if run_simulation and len(selected_compounds) >= 2:

        # Normaliser les compositions
        compositions = [c / sum(compositions) for c in compositions]

        st.subheader("Résultats de la Simulation")

        # Simuler selon la méthode choisie
        results_shortcut = None
        results_mesh = None

        if calculation_method in ['Méthodes Simplifiées', 'Comparaison']:
            with st.spinner("Calcul avec les méthodes simplifiées..."):
                results_shortcut = simulate_shortcut(
                    selected_compounds, compositions, feed_rate, pressure,
                    light_recovery, heavy_recovery, feed_condition,
                    reflux_multiplier, efficiency
                )

        if calculation_method in ['MESH Rigoureux', 'Comparaison']:
            with st.spinner("Calcul rigoureux MESH en cours (peut prendre 10-30 secondes)..."):
                results_mesh = simulate_mesh(
                    selected_compounds, compositions, feed_rate, pressure,
                    light_recovery, heavy_recovery, feed_condition,
                    reflux_multiplier, efficiency, thermo_model
                )

        # Afficher les résultats
        if calculation_method == 'Méthodes Simplifiées' and results_shortcut and results_shortcut['success']:
            r = results_shortcut['results']

            # Métriques principales
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("N min (Fenske)", f"{r['fenske']['N_min']:.2f}")
            col2.metric("N réel", r['gilliland']['N_real'])
            col3.metric("R min", f"{r['underwood']['R_min']:.3f}")
            col4.metric("R opératoire", f"{r['gilliland']['R_operating']:.3f}")
            col5.metric("Plateau alim.", r['kirkbride']['feed_stage'])

            st.divider()

            # Tabs pour les détails
            tab1, tab2, tab3, tab4 = st.tabs(["Distribution", "Températures", "Énergie", "TAC"])

            with tab1:
                st.subheader("Distribution des Produits")
                df_dist = pd.DataFrame(r['distribution'])
                st.dataframe(df_dist, use_container_width=True)

                # Graphique 1: Bilans matières (débits)
                st.subheader("Bilans Matières de la Colonne de Distillation")

                # Calculer les débits
                feed_flow = feed_rate
                dist_flow = sum([d['distillate'] for d in r['distribution']])
                bott_flow = sum([d['bottoms'] for d in r['distribution']])

                # Graphique des débits
                fig_flow = go.Figure()
                fig_flow.add_trace(go.Bar(
                    x=['Alimentation', 'Distillat', 'Résidu'],
                    y=[feed_flow, dist_flow, bott_flow],
                    marker_color=['#3b82f6', '#10b981', '#ef4444'],
                    text=[f"{feed_flow:.1f}<br>kmol/h", f"{dist_flow:.1f}<br>kmol/h", f"{bott_flow:.1f}<br>kmol/h"],
                    textposition='outside'
                ))
                fig_flow.update_layout(
                    title="Débits des flux",
                    xaxis_title="",
                    yaxis_title="Débit (kmol/h)",
                    height=400,
                    showlegend=False
                )

                # Graphique des compositions
                fig_comp = go.Figure()
                compounds_names = [d['compound'] for d in r['distribution']]
                feed_comps = compositions
                dist_comps = [d['distillate']/dist_flow if dist_flow > 0 else 0 for d in r['distribution']]
                bott_comps = [d['bottoms']/bott_flow if bott_flow > 0 else 0 for d in r['distribution']]

                x_pos = np.arange(len(compounds_names))
                width = 0.25

                fig_comp.add_trace(go.Bar(
                    name='Alimentation',
                    x=x_pos - width,
                    y=feed_comps,
                    marker_color='#3b82f6',
                    width=width
                ))
                fig_comp.add_trace(go.Bar(
                    name='Distillat',
                    x=x_pos,
                    y=dist_comps,
                    marker_color='#10b981',
                    width=width
                ))
                fig_comp.add_trace(go.Bar(
                    name='Résidu',
                    x=x_pos + width,
                    y=bott_comps,
                    marker_color='#ef4444',
                    width=width
                ))

                fig_comp.update_layout(
                    title="Compositions des flux",
                    xaxis=dict(
                        tickmode='array',
                        tickvals=x_pos,
                        ticktext=compounds_names
                    ),
                    yaxis_title="Fraction molaire",
                    height=400,
                    barmode='group',
                    legend=dict(x=0.7, y=0.95)
                )

                col_bilan1, col_bilan2 = st.columns(2)
                with col_bilan1:
                    st.plotly_chart(fig_flow, use_container_width=True)
                with col_bilan2:
                    st.plotly_chart(fig_comp, use_container_width=True)

            with tab2:
                st.subheader("Profil de Température")
                col_t1, col_t2, col_t3 = st.columns(3)
                col_t1.metric("Température Tête", f"{r['temperatures']['top']:.1f} °C")
                col_t2.metric("Température Fond", f"{r['temperatures']['bottom']:.1f} °C")
                col_t3.metric("ΔT", f"{r['temperatures']['bottom'] - r['temperatures']['top']:.1f} °C")

            with tab3:
                st.subheader("Besoins Énergétiques")
                col_e1, col_e2 = st.columns(2)
                col_e1.metric("Condenseur", f"{r['energy']['Q_condenser']:.1f} kW")
                col_e2.metric("Rebouilleur", f"{r['energy']['Q_reboiler']:.1f} kW")

            with tab4:
                st.subheader("Coût Annualisé Total (TAC)")

                def simulate_func_dummy(R_test):
                    return results_shortcut

                optimizer = EconomicOptimizer(simulate_func_dummy)
                tac_result = optimizer.calculate_TAC(
                    r['gilliland']['N_real'],
                    r['gilliland']['R_operating'],
                    r['energy']['Q_condenser'],
                    r['energy']['Q_reboiler']
                )

                col_tac1, col_tac2, col_tac3, col_tac4 = st.columns(4)
                col_tac1.metric("TAC Total", f"{tac_result['TAC']/1000:.1f} k€/an")
                col_tac2.metric("Capital Annualisé", f"{tac_result['annualized_capital']/1000:.1f} k€/an")
                col_tac3.metric("Exploitation", f"{tac_result['operating']['total']/1000:.1f} k€/an")
                col_tac4.metric("Maintenance", f"{tac_result['maintenance']/1000:.1f} k€/an")

                st.divider()

                # Graphique de l'effet du reflux
                st.subheader("Effet du rapport de reflux sur le nombre de plateaux")

                # Générer des données pour le graphique Gilliland
                R_min = r['underwood']['R_min']
                N_min = r['fenske']['N_min']

                # Ratios de reflux à tester (de 1.05 à 3.0 fois R_min)
                R_ratios = np.linspace(1.05, 3.0, 50)
                N_values = []

                for ratio in R_ratios:
                    R_test = R_min * ratio
                    X = (R_test - R_min) / (R_test + 1)
                    exponent = (1 + 54.4 * X) * (X - 1) / ((11 + 117.2 * X) * np.sqrt(X))
                    Y = 1 - np.exp(exponent)
                    N_theoretical = N_min + Y / (1 - Y)
                    N_real = N_theoretical / efficiency
                    N_values.append(N_real)

                # Créer le graphique
                fig_reflux = go.Figure()

                # Courbe N vs R/R_min
                fig_reflux.add_trace(go.Scatter(
                    x=R_ratios,
                    y=N_values,
                    mode='lines',
                    name='Courbe N vs R/R_min',
                    line=dict(color='#2563eb', width=3)
                ))

                # Ligne N_min
                fig_reflux.add_hline(
                    y=N_min,
                    line_dash="dash",
                    line_color="#ef4444",
                    annotation_text=f"N_min = {N_min:.1f}",
                    annotation_position="right"
                )

                # Ligne R = 1.3×R_min (valeur typique)
                fig_reflux.add_vline(
                    x=1.3,
                    line_dash="dash",
                    line_color="#10b981",
                    annotation_text="R = 1.3×R_min (typique)",
                    annotation_position="top"
                )

                # Point optimum économique (approximatif autour de 1.1-1.2)
                optimum_ratio = 1.1
                optimum_idx = np.argmin(np.abs(R_ratios - optimum_ratio))
                fig_reflux.add_trace(go.Scatter(
                    x=[R_ratios[optimum_idx]],
                    y=[N_values[optimum_idx]],
                    mode='markers',
                    name=f'Optimum économique (R/R_min ≈ {optimum_ratio:.2f})',
                    marker=dict(size=15, color='#ef4444', symbol='circle')
                ))

                # Point de fonctionnement actuel
                current_ratio = r['gilliland']['R_operating'] / R_min
                current_N = r['gilliland']['N_real']
                fig_reflux.add_trace(go.Scatter(
                    x=[current_ratio],
                    y=[current_N],
                    mode='markers',
                    name=f'Point actuel (R/R_min = {current_ratio:.2f})',
                    marker=dict(size=12, color='#8b5cf6', symbol='diamond')
                ))

                fig_reflux.update_layout(
                    title="Effet du rapport de reflux sur le nombre de plateaux<br>(Système BTX)",
                    xaxis_title="R / R_min",
                    yaxis_title="Nombre de plateaux réels",
                    height=500,
                    hovermode='x unified',
                    legend=dict(x=0.6, y=0.95, bgcolor='rgba(255,255,255,0.8)')
                )

                st.plotly_chart(fig_reflux, use_container_width=True)

                st.info(f"📊 N_min = {N_min:.1f} | R_min = {R_min:.3f} | Point optimal économique ≈ 1.1×R_min | Point typique = 1.3×R_min")

                # Bouton de téléchargement des résultats en PDF
                simulation_data = {
                    'parameters': {
                        'compounds': [{'name': c, 'fraction': z} for c, z in zip(selected_compounds, compositions)],
                        'feed_flow': feed_rate,
                        'pressure': pressure,
                        'recovery_light': light_recovery,
                        'recovery_heavy': heavy_recovery,
                        'q': feed_condition,
                        'reflux_mult': reflux_multiplier,
                        'efficiency': efficiency
                    },
                    'results': results_shortcut['results']
                }
                display_pdf_download_button(simulation_data, "Méthodes Simplifiées")

        elif results_shortcut and not results_shortcut['success']:
            st.error(f"Erreur: {results_shortcut['error']}")

        # Affichage pour MESH Rigoureux
        elif calculation_method == 'MESH Rigoureux' and results_mesh:
            if results_mesh['success']:
                st.success(f"Convergence MESH atteinte en {results_mesh['iterations']} itérations!")

                # Métriques principales
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("N plateaux", results_mesh['n_stages'])
                col2.metric("Plateau alim.", results_mesh['feed_stage'])
                col3.metric("Reflux", f"{results_mesh['R']:.3f}")
                col4.metric("Itérations", results_mesh['iterations'])

                st.divider()

                # Tabs pour les résultats
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Profils Composition",
                    "Profils Température",
                    "Débits",
                    "Bilans Matière",
                    "Énergie & TAC"
                ])

                with tab1:
                    st.subheader("Profils de Composition dans la Colonne")

                    # Créer subplots pour liquide et vapeur côte à côte
                    fig_profiles = make_subplots(
                        rows=1, cols=2,
                        subplot_titles=("Phase Liquide", "Phase Vapeur"),
                        horizontal_spacing=0.12
                    )

                    # Couleurs pour chaque composé
                    colors = ['#fbbf24', '#a3e635', '#22d3ee', '#f97316', '#c084fc', '#fb923c']

                    # Profils de composition liquide (x)
                    for i, comp_key in enumerate(selected_compounds):
                        comp_name = COMPOUNDS_LIBRARY[comp_key]['name']
                        x_profile = [results_mesh['x'][stage][i] for stage in range(results_mesh['n_stages'])]
                        stages = list(range(1, results_mesh['n_stages'] + 1))

                        fig_profiles.add_trace(go.Scatter(
                            x=x_profile,
                            y=stages,
                            mode='lines+markers',
                            name=comp_name,
                            line=dict(width=2, color=colors[i % len(colors)]),
                            marker=dict(size=6),
                            showlegend=True
                        ), row=1, col=1)

                    # Profils de composition vapeur (y)
                    for i, comp_key in enumerate(selected_compounds):
                        comp_name = COMPOUNDS_LIBRARY[comp_key]['name']
                        y_profile = [results_mesh['y'][stage][i] for stage in range(results_mesh['n_stages'])]
                        stages = list(range(1, results_mesh['n_stages'] + 1))

                        fig_profiles.add_trace(go.Scatter(
                            x=y_profile,
                            y=stages,
                            mode='lines+markers',
                            name=comp_name,
                            line=dict(width=2, color=colors[i % len(colors)]),
                            marker=dict(size=6),
                            showlegend=False
                        ), row=1, col=2)

                    # Ajouter ligne horizontale pour le plateau d'alimentation
                    fig_profiles.add_hline(
                        y=results_mesh['feed_stage'],
                        line_dash="dash",
                        line_color="#2563eb",
                        line_width=2,
                        annotation_text=f"Plateau alimentation ({results_mesh['feed_stage']})",
                        annotation_position="right",
                        row=1, col=1
                    )
                    fig_profiles.add_hline(
                        y=results_mesh['feed_stage'],
                        line_dash="dash",
                        line_color="#2563eb",
                        line_width=2,
                        row=1, col=2
                    )

                    # Mise en forme
                    fig_profiles.update_xaxes(title_text="Fraction molaire liquide (x)", row=1, col=1, range=[0, 1])
                    fig_profiles.update_xaxes(title_text="Fraction molaire vapeur (y)", row=1, col=2, range=[0, 1])
                    fig_profiles.update_yaxes(title_text="Numéro de plateau", row=1, col=1, autorange="reversed")
                    fig_profiles.update_yaxes(title_text="Numéro de plateau", row=1, col=2, autorange="reversed")

                    fig_profiles.update_layout(
                        title="Profils de Composition dans la Colonne",
                        height=600,
                        hovermode='y unified',
                        legend=dict(x=1.05, y=0.5, xanchor='left', yanchor='middle')
                    )

                    st.plotly_chart(fig_profiles, use_container_width=True)

                    # Information additionnelle
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.info(f"🔵 Alimentation au plateau {results_mesh['feed_stage']}")
                    with col_info2:
                        st.success(f"✓ {results_mesh['n_stages']} plateaux théoriques")

                with tab2:
                    st.subheader("Profil de Température dans la Colonne")
                    T_celsius = [T - 273.15 for T in results_mesh['T']]
                    stages = list(range(1, results_mesh['n_stages'] + 1))

                    fig_temp = go.Figure()
                    fig_temp.add_trace(go.Scatter(
                        y=stages,
                        x=T_celsius,
                        mode='lines+markers',
                        name='Température',
                        line=dict(color='#f97316', width=3),
                        marker=dict(size=8, color='#f97316'),
                        fill=None
                    ))

                    # Ajouter ligne pour le plateau d'alimentation
                    fig_temp.add_hline(
                        y=results_mesh['feed_stage'],
                        line_dash="dash",
                        line_color="#2563eb",
                        line_width=2,
                        annotation_text=f"Plateau alimentation ({results_mesh['feed_stage']})",
                        annotation_position="right"
                    )

                    # Annoter les températures limites
                    fig_temp.add_annotation(
                        x=T_celsius[0],
                        y=1,
                        text=f"{T_celsius[0]:.1f}°C",
                        showarrow=True,
                        arrowhead=2,
                        ax=-40,
                        ay=-30,
                        font=dict(size=12, color="#dc2626", weight="bold")
                    )

                    fig_temp.add_annotation(
                        x=T_celsius[-1],
                        y=results_mesh['n_stages'],
                        text=f"{T_celsius[-1]:.1f}°C",
                        showarrow=True,
                        arrowhead=2,
                        ax=40,
                        ay=30,
                        font=dict(size=12, color="#dc2626", weight="bold")
                    )

                    fig_temp.update_layout(
                        title="Profil de Température dans la Colonne",
                        xaxis_title="Température (°C)",
                        yaxis_title="Numéro de plateau",
                        height=600,
                        yaxis=dict(autorange="reversed"),
                        hovermode='y'
                    )

                    st.plotly_chart(fig_temp, use_container_width=True)

                    col_t1, col_t2, col_t3 = st.columns(3)
                    col_t1.metric("T Tête", f"{T_celsius[0]:.1f} °C")
                    col_t2.metric("T Alimentation", f"{T_celsius[results_mesh['feed_stage']-1]:.1f} °C")
                    col_t3.metric("T Fond", f"{T_celsius[-1]:.1f} °C")

                with tab3:
                    st.subheader("Profils de Débits Liquides et Vapeurs")
                    fig = make_subplots(
                        rows=1, cols=2,
                        subplot_titles=("Débits Liquides (L)", "Débits Vapeurs (V)")
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=list(range(1, results_mesh['n_stages'] + 1)),
                            y=results_mesh['L'],
                            mode='lines+markers',
                            name='Liquide',
                            line=dict(color='#2563eb', width=2)
                        ),
                        row=1, col=1
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=list(range(1, results_mesh['n_stages'] + 1)),
                            y=results_mesh['V'],
                            mode='lines+markers',
                            name='Vapeur',
                            line=dict(color='#f97316', width=2)
                        ),
                        row=1, col=2
                    )
                    fig.update_xaxes(title_text="Plateau", row=1, col=1)
                    fig.update_xaxes(title_text="Plateau", row=1, col=2)
                    fig.update_yaxes(title_text="Débit (kmol/h)", row=1, col=1)
                    fig.update_yaxes(title_text="Débit (kmol/h)", row=1, col=2)
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

                with tab4:
                    st.subheader("Bilan Matière MESH")

                    # Graphiques de bilans matière similaires à ceux des méthodes simplifiées
                    # Calculer les débits
                    dist_flow = results_mesh['D']
                    bott_flow = results_mesh['B']

                    # Graphique 1: Bilans des débits
                    fig_flow_mesh = go.Figure()
                    fig_flow_mesh.add_trace(go.Bar(
                        x=['Alimentation', 'Distillat', 'Résidu'],
                        y=[feed_rate, dist_flow, bott_flow],
                        marker_color=['#3b82f6', '#10b981', '#ef4444'],
                        text=[f"{feed_rate:.1f}<br>kmol/h", f"{dist_flow:.1f}<br>kmol/h", f"{bott_flow:.1f}<br>kmol/h"],
                        textposition='outside'
                    ))
                    fig_flow_mesh.update_layout(
                        title="Débits des flux",
                        xaxis_title="",
                        yaxis_title="Débit (kmol/h)",
                        height=400,
                        showlegend=False
                    )

                    # Graphique 2: Compositions des flux
                    fig_comp_mesh = go.Figure()
                    compounds_names = [COMPOUNDS_LIBRARY[comp_key]['name'] for comp_key in selected_compounds]
                    feed_comps = compositions
                    dist_comps = results_mesh['x_D']
                    bott_comps = results_mesh['x_B']

                    x_pos = np.arange(len(compounds_names))
                    width = 0.25

                    fig_comp_mesh.add_trace(go.Bar(
                        name='Alimentation',
                        x=x_pos - width,
                        y=feed_comps,
                        marker_color='#3b82f6',
                        width=width
                    ))
                    fig_comp_mesh.add_trace(go.Bar(
                        name='Distillat',
                        x=x_pos,
                        y=dist_comps,
                        marker_color='#10b981',
                        width=width
                    ))
                    fig_comp_mesh.add_trace(go.Bar(
                        name='Résidu',
                        x=x_pos + width,
                        y=bott_comps,
                        marker_color='#ef4444',
                        width=width
                    ))

                    fig_comp_mesh.update_layout(
                        title="Compositions des flux",
                        xaxis=dict(
                            tickmode='array',
                            tickvals=x_pos,
                            ticktext=compounds_names
                        ),
                        yaxis_title="Fraction molaire",
                        height=400,
                        barmode='group',
                        legend=dict(x=0.7, y=0.95)
                    )

                    col_graph1, col_graph2 = st.columns(2)
                    with col_graph1:
                        st.plotly_chart(fig_flow_mesh, use_container_width=True)
                    with col_graph2:
                        st.plotly_chart(fig_comp_mesh, use_container_width=True)

                    st.divider()

                    # Tableaux détaillés
                    col_bilan1, col_bilan2 = st.columns(2)

                    with col_bilan1:
                        st.markdown("**Distillat:**")
                        dist_data = []
                        for i, comp_key in enumerate(selected_compounds):
                            dist_data.append({
                                'Composé': COMPOUNDS_LIBRARY[comp_key]['name'],
                                'Fraction': f"{results_mesh['x_D'][i]:.4f}",
                                'Débit (kmol/h)': f"{results_mesh['D'] * results_mesh['x_D'][i]:.3f}"
                            })
                        st.table(pd.DataFrame(dist_data))
                        st.metric("Débit total distillat", f"{results_mesh['D']:.2f} kmol/h")

                    with col_bilan2:
                        st.markdown("**Résidu:**")
                        bott_data = []
                        for i, comp_key in enumerate(selected_compounds):
                            bott_data.append({
                                'Composé': COMPOUNDS_LIBRARY[comp_key]['name'],
                                'Fraction': f"{results_mesh['x_B'][i]:.4f}",
                                'Débit (kmol/h)': f"{results_mesh['B'] * results_mesh['x_B'][i]:.3f}"
                            })
                        st.table(pd.DataFrame(bott_data))
                        st.metric("Débit total résidu", f"{results_mesh['B']:.2f} kmol/h")

                    st.divider()

                    # Vérification bilan
                    total_in = feed_rate
                    total_out = results_mesh['D'] + results_mesh['B']
                    error_balance = abs(total_in - total_out) / total_in * 100

                    if error_balance < 0.1:
                        st.success(f"✓ Bilan matière vérifié: F={total_in:.2f} | D+B={total_out:.2f} | Erreur: {error_balance:.4f}%")
                    else:
                        st.warning(f"⚠ Erreur de bilan: {error_balance:.2f}%")

                with tab5:
                    st.subheader("Besoins Énergétiques")
                    col_e1, col_e2 = st.columns(2)
                    col_e1.metric("Condenseur", f"{results_mesh['Q_condenser']:.1f} kW")
                    col_e2.metric("Rebouilleur", f"{results_mesh['Q_reboiler']:.1f} kW")

                    st.divider()
                    st.subheader("Coût Annualisé Total (TAC)")

                    def simulate_func_dummy(R_test):
                        return results_mesh

                    optimizer = EconomicOptimizer(simulate_func_dummy)
                    tac_result = optimizer.calculate_TAC(
                        results_mesh['n_stages'],
                        results_mesh['R'],
                        results_mesh['Q_condenser'],
                        results_mesh['Q_reboiler']
                    )

                    col_tac1, col_tac2, col_tac3, col_tac4 = st.columns(4)
                    col_tac1.metric("TAC Total", f"{tac_result['TAC']/1000:.1f} k€/an")
                    col_tac2.metric("Capital Annualisé", f"{tac_result['annualized_capital']/1000:.1f} k€/an")
                    col_tac3.metric("Exploitation", f"{tac_result['operating']['total']/1000:.1f} k€/an")
                    col_tac4.metric("Maintenance", f"{tac_result['maintenance']/1000:.1f} k€/an")

                # Bouton de téléchargement des résultats en PDF
                mesh_simulation_data = {
                    'parameters': {
                        'compounds': [{'name': c, 'fraction': z} for c, z in zip(selected_compounds, compositions)],
                        'feed_flow': feed_rate,
                        'pressure': pressure,
                        'recovery_light': light_recovery,
                        'recovery_heavy': heavy_recovery,
                        'q': feed_condition,
                        'reflux_mult': reflux_multiplier,
                        'efficiency': efficiency
                    },
                    'results': {
                        'flows': {'distillate': results_mesh['D'], 'bottoms': results_mesh['B']},
                        'temperatures': {
                            'top': results_mesh['T'][0] - 273.15,
                            'bottom': results_mesh['T'][-1] - 273.15,
                            'feed': results_mesh['T'][results_mesh['feed_stage']] - 273.15
                        },
                        'energy': {
                            'Q_condenser': results_mesh['Q_condenser'],
                            'Q_reboiler': results_mesh['Q_reboiler']
                        },
                        'economic': tac_result,
                        'column_design': {
                            'total_stages': results_mesh['n_stages']
                        },
                        'convergence': {
                            'iterations': results_mesh['iterations'],
                            'error': results_mesh.get('error', 0)
                        }
                    }
                }
                display_pdf_download_button(mesh_simulation_data, "MESH Rigoureux")

            else:
                st.error(f"Erreur MESH: {results_mesh.get('error', 'Convergence non atteinte')}")

        # Mode Comparaison
        elif calculation_method == 'Comparaison':
            if results_shortcut and results_shortcut['success'] and results_mesh and results_mesh['success']:
                st.success("Simulation complète: Méthodes Simplifiées + MESH Rigoureux")

                # Comparaison des KPIs
                st.subheader("Comparaison des Résultats")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Méthodes Simplifiées**")
                    r = results_shortcut['results']
                    st.write(f"N réel: {r['gilliland']['N_real']}")
                    st.write(f"R opératoire: {r['gilliland']['R_operating']:.3f}")
                    st.write(f"T tête: {r['temperatures']['top']:.1f}°C")
                    st.write(f"T fond: {r['temperatures']['bottom']:.1f}°C")

                with col2:
                    st.markdown("**MESH Rigoureux**")
                    st.write(f"N plateaux: {results_mesh['n_stages']}")
                    st.write(f"R opératoire: {results_mesh['R']:.3f}")
                    st.write(f"T tête: {results_mesh['T'][0]-273.15:.1f}°C")
                    st.write(f"T fond: {results_mesh['T'][-1]-273.15:.1f}°C")

                with col3:
                    st.markdown("**Écarts**")
                    N_diff = abs(r['gilliland']['N_real'] - results_mesh['n_stages'])
                    R_diff = abs(r['gilliland']['R_operating'] - results_mesh['R'])
                    T_top_diff = abs(r['temperatures']['top'] - (results_mesh['T'][0]-273.15))
                    T_bot_diff = abs(r['temperatures']['bottom'] - (results_mesh['T'][-1]-273.15))

                    st.write(f"ΔN: {N_diff:.0f} plateaux")
                    st.write(f"ΔR: {R_diff:.3f}")
                    st.write(f"ΔT tête: {T_top_diff:.1f}°C")
                    st.write(f"ΔT fond: {T_bot_diff:.1f}°C")

                st.info("Utilisez les onglets ci-dessus pour voir les résultats détaillés de chaque méthode")

            else:
                if results_shortcut and not results_shortcut['success']:
                    st.error(f"Erreur Simplifiées: {results_shortcut['error']}")
                if results_mesh and not results_mesh['success']:
                    st.error(f"Erreur MESH: {results_mesh.get('error', 'Convergence non atteinte')}")

    else:
        st.info("Configurez les paramètres dans la barre latérale et cliquez sur 'Lancer la Simulation'")

# =============================================================================
# PAGE DE DOCUMENTATION
# =============================================================================

elif st.session_state.current_page == 'documentation':

    st.subheader("Documentation Théorique")

    doc_tabs = st.tabs([
        "Méthodes Simplifiées",
        "MESH Rigoureux",
        "Modèles d'Activité",
        "Optimisation Économique"
    ])

    # TAB 1: Méthodes Simplifiées
    with doc_tabs[0]:
        st.markdown("### Méthodes Simplifiées (Shortcut Methods)")

        st.markdown("""
        Les méthodes simplifiées permettent un dimensionnement rapide des colonnes de distillation.
        Elles sont basées sur des corrélations empiriques.
        """)

        st.markdown("---")

        # Fenske
        st.markdown("#### 1. Méthode de Fenske")
        st.markdown("**Objectif:** Calculer le nombre minimum de plateaux théoriques (N_min)")

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 1)</span>
        N<sub>min</sub> = ln[(x<sub>LK,D</sub> / x<sub>HK,D</sub>) × (x<sub>HK,B</sub> / x<sub>LK,B</sub>)] / ln(α<sub>avg</sub>)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Où:**
        - x<sub>LK,D</sub> : Fraction du composé léger dans le distillat
        - x<sub>HK,D</sub> : Fraction du composé lourd dans le distillat
        - x<sub>LK,B</sub> : Fraction du composé léger dans le résidu
        - x<sub>HK,B</sub> : Fraction du composé lourd dans le résidu
        - α<sub>avg</sub> : Volatilité relative moyenne

        **Hypothèse:** Reflux total (R → ∞)
        """)

        st.markdown("---")

        # Underwood
        st.markdown("#### 2. Méthode d'Underwood")
        st.markdown("**Objectif:** Calculer le reflux minimum (R_min)")

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 2)</span>
        Σ[α<sub>i</sub> × z<sub>i</sub> / (α<sub>i</sub> - θ)] = 1 - q
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 3)</span>
        R<sub>min</sub> + 1 = Σ[α<sub>i</sub> × x<sub>D,i</sub> / (α<sub>i</sub> - θ)]
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Où:**
        - α<sub>i</sub> : Volatilité relative du composé i
        - z<sub>i</sub> : Fraction molaire dans l'alimentation
        - x<sub>D,i</sub> : Fraction molaire dans le distillat
        - q : Condition thermique (q=1 pour liquide saturé, q=0 pour vapeur saturée)
        - θ : Paramètre d'Underwood (α<sub>HK</sub> < θ < α<sub>LK</sub>)

        **Hypothèse:** Nombre de plateaux infini (N → ∞)
        """)

        st.markdown("---")

        # Gilliland
        st.markdown("#### 3. Corrélation de Gilliland")
        st.markdown("**Objectif:** Relier N réel au reflux opératoire")

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 4)</span>
        X = (R - R<sub>min</sub>) / (R + 1)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 5)</span>
        Y = 1 - exp[((1 + 54.4X)(X - 1)) / ((11 + 117.2X)√X)]
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 6)</span>
        N<sub>théorique</sub> = N<sub>min</sub> + Y / (1 - Y)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 7)</span>
        N<sub>réel</sub> = N<sub>théorique</sub> / E<sub>Murphree</sub>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Où:**
        - R : Reflux opératoire (typiquement 1.2 à 1.5 × R<sub>min</sub>)
        - E<sub>Murphree</sub> : Efficacité de Murphree (60-80% typique)
        """)

        st.markdown("---")

        # Kirkbride
        st.markdown("#### 4. Équation de Kirkbride")
        st.markdown("**Objectif:** Déterminer la position du plateau d'alimentation")

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 8)</span>
        log(N<sub>R</sub> / N<sub>S</sub>) = 0.206 × log[(B/D) × (x<sub>HK,F</sub>/x<sub>LK,F</sub>) × (x<sub>LK,B</sub>/x<sub>HK,D</sub>)²]
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Où:**
        - N<sub>R</sub> : Nombre de plateaux en section de rectification (au-dessus de l'alimentation)
        - N<sub>S</sub> : Nombre de plateaux en section d'épuisement (en-dessous de l'alimentation)
        - B : Débit de résidu
        - D : Débit de distillat
        - Plateau d'alimentation = N<sub>R</sub> + 1
        """)

    # TAB 2: MESH
    with doc_tabs[1]:
        st.markdown("### Méthode MESH Rigoureuse")

        st.markdown("""
        La méthode MESH résout rigoureusement les équations de bilan plateau par plateau.
        C'est la méthode la plus précise pour le design de colonnes de distillation.
        """)

        st.markdown("---")

        st.markdown("#### Les 4 Équations MESH")

        col_mesh1, col_mesh2 = st.columns(2)

        with col_mesh1:
            st.markdown("**M - Material Balance (Bilan Matière)**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 9)</span>
            L<sub>j+1</sub>x<sub>i,j+1</sub> + V<sub>j-1</sub>y<sub>i,j-1</sub> - L<sub>j</sub>x<sub>i,j</sub> - V<sub>j</sub>y<sub>i,j</sub> + F<sub>j</sub>z<sub>i,j</sub> = 0
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            Pour chaque plateau j et composé i
            """)

            st.markdown("---")

            st.markdown("**E - Equilibrium (Équilibre)**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 10)</span>
            y<sub>i,j</sub> = K<sub>i,j</sub> × x<sub>i,j</sub>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            Avec K<sub>i,j</sub> = (γ<sub>i</sub> P<sub>sat,i</sub>) / P pour mélanges non-idéaux
            """)

        with col_mesh2:
            st.markdown("**S - Summation (Sommation)**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 11)</span>
            Σ x<sub>i,j</sub> = 1
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 12)</span>
            Σ y<sub>i,j</sub> = 1
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("**H - Heat Balance (Bilan Enthalpique)**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 13)</span>
            L<sub>j+1</sub>h<sub>j+1</sub> + V<sub>j-1</sub>H<sub>j-1</sub> - L<sub>j</sub>h<sub>j</sub> - V<sub>j</sub>H<sub>j</sub> + F<sub>j</sub>h<sub>F</sub> + Q<sub>j</sub> = 0
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("#### Algorithme de Wang-Henke")

        st.markdown("""
        1. **Initialisation:** Estimer T, x, y, L, V initiaux
        2. **Boucle itérative:**
           - Résoudre bilans matière (M) → nouveau x
           - Calculer équilibres (E) → nouveau y
           - Vérifier sommations (S)
           - Résoudre bilans énergie (H) → nouveau T
           - Calculer nouveaux K-values
           - Tester convergence
        3. **Critères de convergence:**
           - ε<sub>T</sub> < 0.1 K (températures)
           - ε<sub>x</sub> < 10⁻⁶ (compositions liquides)
        """)

    # TAB 3: Modèles d'activité
    with doc_tabs[2]:
        st.markdown("### Modèles d'Activité (Mélanges Non-Idéaux)")

        st.markdown("""
        Les modèles d'activité corrigent les K-values pour les mélanges non-idéaux.
        """)

        st.markdown("---")

        st.markdown("#### 1. Modèle Idéal")
        st.markdown("""
        <div class="equation">
        γ<sub>i</sub> = 1 pour tous les composés
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Usage:** Hydrocarbures similaires (benzène-toluène-xylène)")

        st.markdown("---")

        st.markdown("#### 2. Modèle de Wilson")
        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 14)</span>
        ln(γ<sub>i</sub>) = 1 - ln(Σ<sub>j</sub> x<sub>j</sub> Λ<sub>ij</sub>) - Σ<sub>k</sub> [x<sub>k</sub> Λ<sub>ki</sub> / Σ<sub>j</sub> x<sub>j</sub> Λ<sub>kj</sub>]
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        Avec Λ<sub>ij</sub> = (V<sub>j</sub> / V<sub>i</sub>) × exp(-a<sub>ij</sub> / T)

        **Avantages:** Simple, bon pour alcools et cétones
        **Limitation:** Ne peut pas prédire LLE (démixtion)
        """)

        st.markdown("---")

        st.markdown("#### 3. Modèle NRTL")
        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 15)</span>
        G<sub>ij</sub> = exp(-α<sub>ij</sub> τ<sub>ij</sub>), τ<sub>ij</sub> = a<sub>ij</sub> / T
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Avantages:** Peut prédire LLE, très flexible
        **Usage:** Systèmes polaires, azéotropes, alcools-eau
        """)

        st.markdown("---")

        st.markdown("#### 4. Modèle UNIQUAC")
        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 16)</span>
        ln(γ<sub>i</sub>) = ln(γ<sub>i</sub><sup>C</sup>) + ln(γ<sub>i</sub><sup>R</sup>)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        Partie Combinatoire (taille/forme) + Partie Résiduelle (interactions)

        **Avantages:** Base théorique solide, excellent pour polymères
        **Usage:** Systèmes complexes, électrolytes
        """)

    # TAB 4: Optimisation
    with doc_tabs[3]:
        st.markdown("### Optimisation Économique")

        st.markdown("""
        L'optimisation économique vise à minimiser le TAC (Total Annualized Cost).
        """)

        st.markdown("---")

        st.markdown("#### TAC - Total Annualized Cost")

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 17)</span>
        TAC = C<sub>capital</sub> × CRF + C<sub>operating</sub> + C<sub>maintenance</sub>
        </div>
        """, unsafe_allow_html=True)

        col_tac1, col_tac2, col_tac3 = st.columns(3)

        with col_tac1:
            st.markdown("**Coûts d'Investissement**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 18)</span>
            C<sub>capital</sub> = C<sub>colonne</sub> + C<sub>condenseur</sub> + C<sub>rebouilleur</sub>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            - Colonne: 15000 €/m
            - Plateaux: 800 €/plateau
            - Condenseur: 2000 €/kW
            - Rebouilleur: 2500 €/kW
            """)

        with col_tac2:
            st.markdown("**Coûts d'Exploitation**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 19)</span>
            C<sub>operating</sub> = C<sub>énergie</sub> + C<sub>refroidissement</sub>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            - Énergie: 0.08 €/kWh
            - Refroidissement: 0.02 €/kWh
            - Heures/an: 8000 h
            """)

        with col_tac3:
            st.markdown("**Coûts de Maintenance**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 20)</span>
            C<sub>maintenance</sub> = 0.05 × C<sub>capital</sub>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            - 5% du capital par an
            - Entretien, réparations
            - Inspections réglementaires
            """)

        st.markdown("---")

        st.markdown("#### Optimisation du Reflux")

        st.markdown("""
        Il existe un **reflux optimal** qui minimise le TAC:

        - **R trop faible:** Beaucoup de plateaux nécessaires → Coûts d'investissement élevés
        - **R trop élevé:** Coûts d'exploitation élevés (énergie)
        - **R optimal:** Équilibre entre capital et exploitation (typiquement 1.2-1.5 × R<sub>min</sub>)
        """)

# =============================================================================
# PAGE GUIDE
# =============================================================================

elif st.session_state.current_page == 'guide':

    st.subheader("Guide d'Utilisation")

    st.markdown("### Étapes pour une Simulation")

    st.markdown("""
    1. **Retourner à l'accueil** et cliquer sur "Lancer une Simulation"

    2. **Sélectionner les composés** (minimum 2 composés requis)
       - Disponibles: BTX, alcools, alcanes (13 composés au total)

    3. **Définir les compositions**
       - Entrer les pourcentages molaires
       - Cliquer sur "Normaliser" si le total ≠ 100%

    4. **Paramètres opératoires**
       - Débit: 1-10000 kmol/h
       - Pression: Typiquement 101325 Pa (1 atm)
       - Condition thermique: q=1 pour liquide saturé (le plus courant)

    5. **Spécifications de séparation**
       - Récupérations: 90-99% typique
       - Multiplicateur reflux: 1.2-1.5 recommandé
       - Efficacité: 70% pour estimation préliminaire

    6. **Choisir la méthode**
       - Méthodes Simplifiées: Design rapide
       - MESH Rigoureux: Résultats précis
       - Comparaison: Voir les deux

    7. **Lancer la simulation**
       - Analyser les résultats dans les onglets
    """)

    st.divider()

    st.markdown("### Conseils et Bonnes Pratiques")

    col_tips1, col_tips2 = st.columns(2)

    with col_tips1:
        st.success("""
        **À FAIRE:**

        - Commencer par méthodes simplifiées
        - Vérifier le bilan matière (F = D + B)
        - Valider que N_réel > N_min
        - Vérifier que R_op > R_min
        - Utiliser MESH pour validation finale
        - Comparer les résultats entre méthodes
        """)

    with col_tips2:
        st.error("""
        **À ÉVITER:**

        - Récupérations > 99.9%
        - Reflux trop proche de R_min
        - Efficacité > 95% (irréaliste)
        - Oublier de normaliser les compositions
        - Ignorer les warnings
        - Sauter la vérification des bilans
        """)
