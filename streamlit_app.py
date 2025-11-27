"""
Application Streamlit avec Composant React
Simulation de Distillation Multicomposants


"""

import streamlit as st
import numpy as np
import sys
import os
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(__file__))

from distillation_multicomposants import (
    ThermodynamicPackage,
    Compound
)

# Configuration de la page
st.set_page_config(
    page_title="Distillation Multicomposants",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un style moderne
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    h1, h2, h3 {
        color: #667eea !important;
    }
    .stMetric {
        background: rgba(102, 126, 234, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Bibliothèque de composés disponibles
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


def simulate_distillation(compounds, compositions, feed_rate, pressure,
                          light_key_recovery, heavy_key_recovery,
                          feed_thermal_condition, reflux_ratio_multiplier, efficiency):
    """
    Fonction de simulation de distillation
    """
    try:
        # Normaliser les compositions
        compositions = np.array(compositions) / np.sum(compositions)

        # Créer les composés
        compound_objects = [Compound(name) for name in compounds]

        # Créer le package thermodynamique
        thermo_package = ThermodynamicPackage(compound_objects)

        # Paramètres de la colonne
        LK_idx = 0
        HK_idx = 1 if len(compounds) > 1 else 0

        # Calculer les débits
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

        # Calcul des K-values
        T_avg = np.mean([comp.Tb for comp in compound_objects])
        K_values = thermo_package.K_values(T_avg, pressure)

        # Volatilités relatives
        alphas = K_values / K_values[HK_idx]
        alpha_avg = alphas[LK_idx]

        # MÉTHODE DE FENSKE
        x_LK_D = light_key_recovery * compositions[LK_idx] / (
            light_key_recovery * compositions[LK_idx] + (1 - heavy_key_recovery) * compositions[HK_idx]
        )
        x_HK_D = 1 - x_LK_D
        x_LK_B = (1 - light_key_recovery) * compositions[LK_idx] / (
            (1 - light_key_recovery) * compositions[LK_idx] + heavy_key_recovery * compositions[HK_idx]
        )
        x_HK_B = 1 - x_LK_B

        N_min = np.log((x_LK_D / x_HK_D) / (x_LK_B / x_HK_B)) / np.log(alpha_avg)

        # MÉTHODE D'UNDERWOOD
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

        # CORRÉLATION DE GILLILAND
        R = R_min * reflux_ratio_multiplier
        X = (R - R_min) / (R + 1)
        exponent = (1 + 54.4 * X) * (X - 1) / ((11 + 117.2 * X) * np.sqrt(X))
        Y = 1 - np.exp(exponent)
        N_theoretical = N_min + Y / (1 - Y)
        N_real = int(np.ceil(N_theoretical / efficiency))

        # ÉQUATION DE KIRKBRIDE
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
# INTERFACE STREAMLIT
# =============================================================================

# En-tête
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='color: white; margin: 0;'>🧪 Distillation Multicomposants</h1>
    <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;'>
        Simulation par méthodes simplifiées (Fenske, Underwood, Gilliland, Kirkbride)
    </p>
    <p style='color: rgba(255,255,255,0.7); margin: 5px 0 0 0; font-size: 14px;'>
        Prof. BAKHER Zine Elabidine - Filière PIC - UH1
    </p>
</div>
""", unsafe_allow_html=True)

# Barre latérale - Paramètres d'entrée
with st.sidebar:
    st.header("⚙️ Paramètres de Simulation")

    st.subheader("🧪 Composés")
    selected_compounds = st.multiselect(
        "Sélectionner les composés",
        options=list(COMPOUNDS_LIBRARY.keys()),
        default=['benzene', 'toluene', 'o-xylene'],
        format_func=lambda x: f"{COMPOUNDS_LIBRARY[x]['name']} ({COMPOUNDS_LIBRARY[x]['formula']})"
    )

    if len(selected_compounds) >= 2:
        st.subheader("📊 Compositions (%)")
        compositions = {}
        for comp in selected_compounds:
            compositions[comp] = st.number_input(
                f"{COMPOUNDS_LIBRARY[comp]['name']}",
                min_value=0.0,
                max_value=100.0,
                value=100.0 / len(selected_compounds),
                step=0.1,
                key=f"comp_{comp}"
            )

        total = sum(compositions.values())
        st.info(f"Total: {total:.1f}%")

        if st.button("🔄 Normaliser"):
            st.rerun()

        st.divider()

        st.subheader("🔧 Paramètres Opératoires")
        feed_rate = st.number_input("Débit d'alimentation (kmol/h)",
                                     min_value=1.0, value=100.0, step=1.0)
        pressure = st.number_input("Pression (Pa)",
                                    min_value=10000, value=101325, step=1000)
        feed_condition = st.selectbox(
            "Condition d'alimentation",
            options=['saturated_liquid', 'saturated_vapor', 'subcooled_liquid',
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

        st.subheader("🎯 Spécifications de Séparation")
        light_key_recovery = st.slider("Récupération composé léger (%)",
                                        80.0, 99.9, 95.0, 0.1)
        heavy_key_recovery = st.slider("Récupération composé lourd (%)",
                                        80.0, 99.9, 95.0, 0.1)
        reflux_multiplier = st.slider("Multiplicateur de reflux",
                                       1.1, 3.0, 1.3, 0.1)
        efficiency = st.slider("Efficacité des plateaux (%)",
                               50, 95, 70, 1)

        st.divider()

        simulate_button = st.button("🚀 LANCER LA SIMULATION", type="primary")
    else:
        st.warning("⚠️ Sélectionnez au moins 2 composés")
        simulate_button = False

# Zone principale - Résultats
if simulate_button and len(selected_compounds) >= 2:
    with st.spinner("🔄 Simulation en cours..."):
        # Normaliser les compositions
        comp_values = list(compositions.values())
        total = sum(comp_values)
        normalized_comps = [c / total for c in comp_values]

        # Lancer la simulation
        results = simulate_distillation(
            compounds=selected_compounds,
            compositions=normalized_comps,
            feed_rate=feed_rate,
            pressure=pressure,
            light_key_recovery=light_key_recovery / 100,
            heavy_key_recovery=heavy_key_recovery / 100,
            feed_thermal_condition=feed_condition,
            reflux_ratio_multiplier=reflux_multiplier,
            efficiency=efficiency / 100
        )

        if results['success']:
            st.success("✅ Simulation terminée avec succès!")

            r = results['results']

            # KPIs
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("N min (Fenske)", f"{r['fenske']['N_min']:.2f}", "plateaux")
            with col2:
                st.metric("N réel", f"{r['gilliland']['N_real']}", "plateaux")
            with col3:
                st.metric("R min", f"{r['underwood']['R_min']:.2f}")
            with col4:
                st.metric("R opératoire", f"{r['gilliland']['R_operating']:.2f}")
            with col5:
                st.metric("Plateau alim.", f"{r['kirkbride']['feed_stage']}",
                         f"/{r['gilliland']['N_real']}")

            # Onglets
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Vue d'ensemble",
                "📈 Distribution",
                "📋 Bilans matières",
                "🔬 Résultats détaillés"
            ])

            with tab1:
                col1, col2 = st.columns(2)

                with col1:
                    # Composition Distillat
                    dist_labels = [d['compound'] for d in r['distribution']]
                    dist_values = [d['distillate'] for d in r['distribution']]

                    fig = go.Figure(data=[go.Pie(
                        labels=dist_labels,
                        values=dist_values,
                        hole=0.4,
                        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'])
                    )])
                    fig.update_layout(
                        title="Composition du Distillat",
                        template="plotly_dark",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Composition Résidu
                    bottoms_values = [d['bottoms'] for d in r['distribution']]

                    fig = go.Figure(data=[go.Pie(
                        labels=dist_labels,
                        values=bottoms_values,
                        hole=0.4,
                        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'])
                    )])
                    fig.update_layout(
                        title="Composition du Résidu",
                        template="plotly_dark",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Jauges
                col1, col2, col3 = st.columns(3)

                with col1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=r['efficiency'] * 100,
                        title={'text': "Efficacité (%)"},
                        gauge={'axis': {'range': [0, 100]},
                               'bar': {'color': "#667eea"},
                               'steps': [
                                   {'range': [0, 60], 'color': "rgba(255,100,100,0.2)"},
                                   {'range': [60, 80], 'color': "rgba(255,200,100,0.2)"},
                                   {'range': [80, 100], 'color': "rgba(100,255,100,0.2)"}
                               ]}
                    ))
                    fig.update_layout(template="plotly_dark", height=300)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=r['gilliland']['R_operating'] / r['underwood']['R_min'],
                        title={'text': "R / R_min"},
                        gauge={'axis': {'range': [1, 3]},
                               'bar': {'color': "#764ba2"},
                               'steps': [
                                   {'range': [1, 1.5], 'color': "rgba(100,255,100,0.2)"},
                                   {'range': [1.5, 2], 'color': "rgba(255,200,100,0.2)"},
                                   {'range': [2, 3], 'color': "rgba(255,100,100,0.2)"}
                               ]}
                    ))
                    fig.update_layout(template="plotly_dark", height=300)
                    st.plotly_chart(fig, use_container_width=True)

                with col3:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=r['gilliland']['N_theoretical'] / r['fenske']['N_min'],
                        title={'text': "N / N_min"},
                        gauge={'axis': {'range': [1, 5]},
                               'bar': {'color': "#f093fb"},
                               'steps': [
                                   {'range': [1, 2], 'color': "rgba(100,255,100,0.2)"},
                                   {'range': [2, 3], 'color': "rgba(255,200,100,0.2)"},
                                   {'range': [3, 5], 'color': "rgba(255,100,100,0.2)"}
                               ]}
                    ))
                    fig.update_layout(template="plotly_dark", height=300)
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                # Distribution des composés
                dist_data = r['distribution']

                fig = go.Figure()
                for i, comp_data in enumerate(dist_data):
                    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
                    fig.add_trace(go.Bar(
                        x=['Alimentation', 'Distillat', 'Résidu'],
                        y=[comp_data['feed'], comp_data['distillate'], comp_data['bottoms']],
                        name=comp_data['compound'],
                        marker_color=colors[i % 5]
                    ))

                fig.update_layout(
                    title="Distribution des Composés",
                    xaxis_title="Flux",
                    yaxis_title="Débit (kmol/h)",
                    barmode='group',
                    template="plotly_dark",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab3:
                # Tableau de bilan matière
                st.subheader("Bilan Matière Détaillé")

                import pandas as pd
                df = pd.DataFrame(r['distribution'])
                df.columns = ['Composé', 'Alim. (kmol/h)', 'Distillat (kmol/h)',
                             'Résidu (kmol/h)', 'Récup. D (%)', 'Récup. B (%)']

                st.dataframe(df, use_container_width=True)

                st.info(f"**Total:** Alimentation = {r['flows']['feed']:.2f} kmol/h | "
                       f"Distillat = {r['flows']['distillate']:.2f} kmol/h | "
                       f"Résidu = {r['flows']['bottoms']:.2f} kmol/h")

            with tab4:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🔬 Méthode de Fenske")
                    st.write(f"- N_min = {r['fenske']['N_min']:.3f} plateaux")
                    st.write(f"- α_avg = {r['fenske']['alpha_avg']:.3f}")

                    st.subheader("🔬 Méthode d'Underwood")
                    st.write(f"- R_min = {r['underwood']['R_min']:.3f}")
                    st.write(f"- θ = {r['underwood']['theta']:.3f}")

                    st.subheader("🌡️ Températures")
                    st.write(f"- T_tête = {r['temperatures']['top']:.1f}°C")
                    st.write(f"- T_fond = {r['temperatures']['bottom']:.1f}°C")
                    st.write(f"- T_alim = {r['temperatures']['feed']:.1f}°C")

                with col2:
                    st.subheader("🔬 Corrélation de Gilliland")
                    st.write(f"- R_op = {r['gilliland']['R_operating']:.3f}")
                    st.write(f"- N_théorique = {r['gilliland']['N_theoretical']:.2f} plateaux")
                    st.write(f"- N_réel = {r['gilliland']['N_real']} plateaux")
                    st.write(f"- X = {r['gilliland']['X']:.4f}")
                    st.write(f"- Y = {r['gilliland']['Y']:.4f}")

                    st.subheader("🔬 Équation de Kirkbride")
                    st.write(f"- Plateau d'alimentation = {r['kirkbride']['feed_stage']}")
                    st.write(f"- N_rectification = {r['kirkbride']['N_rectification']} plateaux")
                    st.write(f"- N_épuisement = {r['kirkbride']['N_stripping']} plateaux")

                    st.subheader("⚡ Besoins Énergétiques")
                    st.write(f"- Q_condenseur = {r['energy']['Q_condenser']:.0f} kW")
                    st.write(f"- Q_rebouilleur = {r['energy']['Q_reboiler']:.0f} kW")

        else:
            st.error(f"❌ Erreur lors de la simulation: {results['error']}")

else:
    st.info("👈 Configurez les paramètres dans la barre latérale et lancez la simulation")
