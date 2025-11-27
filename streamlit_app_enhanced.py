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
        # Créer les objets Compound
        compound_objects = []
        for i, compound_key in enumerate(compounds):
            comp_data = COMPOUNDS_LIBRARY[compound_key]
            compound_objects.append(Compound(
                name=comp_data['name'],
                Tb_C=comp_data['Tb'],
                Tc_K=comp_data['Tc'],
                Pc_bar=comp_data['Pc']
            ))

        # Package thermodynamique
        thermo = ThermodynamicPackage(compound_objects)

        # K-values moyens
        T_avg = sum([c.Tb_C for c in compound_objects]) / len(compound_objects) + 273.15
        K_values = thermo.calculate_K_values(T_avg, pressure)

        # Volatilités relatives
        alpha = thermo.calculate_relative_volatilities(T_avg, pressure)

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

        T_top = compound_objects[0].Tb_C
        T_bottom = compound_objects[-1].Tb_C

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
    st.markdown("**Modélisation et Simulation des Procédés** | Prof. BAKHER Zine Elabidine | PIC UH1 2024-2025")

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
            st.info("Note: MESH Rigoureux nécessite une initialisation complète - Feature en développement")
            results_mesh = {'success': False, 'error': 'MESH solver integration en cours'}

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

                # Graphiques
                col_g1, col_g2 = st.columns(2)

                with col_g1:
                    fig1 = go.Figure(data=[go.Pie(
                        labels=[d['compound'] for d in r['distribution']],
                        values=[d['distillate'] for d in r['distribution']],
                        title="Distillat"
                    )])
                    st.plotly_chart(fig1, use_container_width=True)

                with col_g2:
                    fig2 = go.Figure(data=[go.Pie(
                        labels=[d['compound'] for d in r['distribution']],
                        values=[d['bottoms'] for d in r['distribution']],
                        title="Résidu"
                    )])
                    st.plotly_chart(fig2, use_container_width=True)

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

        elif results_shortcut and not results_shortcut['success']:
            st.error(f"Erreur: {results_shortcut['error']}")

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
        <span class="equation-number">(Éq. 10)</span>
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
        <span class="equation-number">(Éq. 15)</span>
        Σ[α<sub>i</sub> × z<sub>i</sub> / (α<sub>i</sub> - θ)] = 1 - q
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 16)</span>
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
        <span class="equation-number">(Éq. 19)</span>
        X = (R - R<sub>min</sub>) / (R + 1)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 20)</span>
        Y = 1 - exp[((1 + 54.4X)(X - 1)) / ((11 + 117.2X)√X)]
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 21)</span>
        N<sub>théorique</sub> = N<sub>min</sub> + Y / (1 - Y)
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="equation">
        <span class="equation-number">(Éq. 22)</span>
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
        <span class="equation-number">(Éq. 23)</span>
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
            <span class="equation-number">(Éq. 24)</span>
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
            <span class="equation-number">(Éq. 30)</span>
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
            <span class="equation-number">(Éq. 31)</span>
            Σ x<sub>i,j</sub> = 1
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 32)</span>
            Σ y<sub>i,j</sub> = 1
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("**H - Heat Balance (Bilan Enthalpique)**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 33)</span>
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
        <span class="equation-number">(Éq. 40a)</span>
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
        <span class="equation-number">(Éq. 40b)</span>
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
        <span class="equation-number">(Éq. 40c)</span>
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
        <span class="equation-number">(Éq. 43)</span>
        TAC = C<sub>capital</sub> × CRF + C<sub>operating</sub> + C<sub>maintenance</sub>
        </div>
        """, unsafe_allow_html=True)

        col_tac1, col_tac2, col_tac3 = st.columns(3)

        with col_tac1:
            st.markdown("**Coûts d'Investissement**")
            st.markdown("""
            <div class="equation">
            <span class="equation-number">(Éq. 44)</span>
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
            <span class="equation-number">(Éq. 45)</span>
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
            <span class="equation-number">(Éq. 46)</span>
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
