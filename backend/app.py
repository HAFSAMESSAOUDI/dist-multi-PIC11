"""
Backend Flask pour Simulateur de Distillation Multicomposants
==============================================================
API REST pour la simulation de colonnes de distillation

Auteur: Prof. BAKHER Zine Elabidine
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import sys
import os
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour Flask
import matplotlib.pyplot as plt

# Configurer l'encodage UTF-8 pour éviter les erreurs de caractères
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from distillation_multicomposants import (
    Compound, ThermodynamicPackage, ShortcutDistillation
)
from visualization import DistillationVisualizer

app = Flask(__name__)
CORS(app)  # Activer CORS pour React

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état du serveur"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend de simulation de distillation est opérationnel'
    })

@app.route('/api/compounds', methods=['GET'])
def get_available_compounds():
    """Liste des composés disponibles"""
    compounds_list = [
        {'id': 'benzene', 'name': 'Benzène', 'formula': 'C₆H₆'},
        {'id': 'toluene', 'name': 'Toluène', 'formula': 'C₇H₈'},
        {'id': 'o-xylene', 'name': 'o-Xylène', 'formula': 'C₈H₁₀'},
        {'id': 'ethylbenzene', 'name': 'Éthylbenzène', 'formula': 'C₈H₁₀'},
        {'id': 'methanol', 'name': 'Méthanol', 'formula': 'CH₃OH'},
        {'id': 'ethanol', 'name': 'Éthanol', 'formula': 'C₂H₅OH'},
        {'id': 'propanol', 'name': 'Propanol', 'formula': 'C₃H₇OH'},
        {'id': 'butanol', 'name': 'Butanol', 'formula': 'C₄H₉OH'},
        {'id': 'water', 'name': 'Eau', 'formula': 'H₂O'},
        {'id': 'acetone', 'name': 'Acétone', 'formula': 'C₃H₆O'},
        {'id': 'hexane', 'name': 'Hexane', 'formula': 'C₆H₁₄'},
        {'id': 'heptane', 'name': 'Heptane', 'formula': 'C₇H₁₆'},
        {'id': 'octane', 'name': 'Octane', 'formula': 'C₈H₁₈'},
    ]
    return jsonify({'compounds': compounds_list})

@app.route('/api/compound-properties', methods=['POST'])
def get_compound_properties():
    """Obtenir les propriétés d'un composé"""
    try:
        data = request.get_json()
        compound_id = data.get('compound_id')

        compound = Compound(compound_id)

        properties = {
            'name': compound.name,
            'Tb': round(compound.Tb - 273.15, 2),  # °C
            'Tc': round(compound.Tc - 273.15, 2),  # °C
            'Pc': round(compound.Pc / 1e5, 2),  # bar
            'MW': round(compound.MW, 2),  # g/mol
            'omega': round(compound.omega, 4) if compound.omega else None
        }

        return jsonify({'success': True, 'properties': properties})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/simulate', methods=['POST'])
def simulate_distillation():
    """
    Endpoint principal de simulation

    Body JSON:
    {
        "compounds": ["benzene", "toluene", "o-xylene"],
        "compositions": [0.33, 0.33, 0.34],
        "flow_rate": 100.0,
        "pressure": 101325,
        "recovery_lk": 0.95,
        "recovery_hk": 0.95,
        "reflux_factor": 1.3,
        "feed_quality": 1.0,
        "efficiency": 0.70
    }
    """
    try:
        data = request.get_json()

        # Extraction des paramètres
        compound_names = data.get('compounds', ['benzene', 'toluene', 'o-xylene'])
        z_F = np.array(data.get('compositions', [0.33, 0.33, 0.34]))
        F = float(data.get('flow_rate', 100.0))
        P = float(data.get('pressure', 101325))
        recovery_LK_D = float(data.get('recovery_lk', 0.95))
        recovery_HK_B = float(data.get('recovery_hk', 0.95))
        R_factor = float(data.get('reflux_factor', 1.3))
        q = float(data.get('feed_quality', 1.0))
        efficiency = float(data.get('efficiency', 0.70))

        # Validation
        if len(compound_names) != len(z_F):
            return jsonify({
                'success': False,
                'error': 'Le nombre de composés ne correspond pas au nombre de compositions'
            }), 400

        if not np.isclose(np.sum(z_F), 1.0, atol=0.01):
            return jsonify({
                'success': False,
                'error': f'La somme des compositions doit être 1.0 (actuellement {np.sum(z_F):.3f})'
            }), 400

        # Créer les composés
        compounds = []
        for name in compound_names:
            try:
                comp = Compound(name)
                compounds.append(comp)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Impossible de charger le composé "{name}": {str(e)}'
                }), 400

        # Package thermodynamique
        thermo = ThermodynamicPackage(compounds)

        # Dimensionnement par méthodes simplifiées
        shortcut = ShortcutDistillation(thermo, F, z_F, P)

        results = shortcut.complete_shortcut_design(
            recovery_LK_D=recovery_LK_D,
            recovery_HK_B=recovery_HK_B,
            R_factor=R_factor,
            q=q,
            efficiency=efficiency
        )

        # Estimation des profils
        N_real = results['N_real']
        stages = np.arange(1, N_real + 1)

        x_profiles = np.zeros((N_real, len(compounds)))
        y_profiles = np.zeros((N_real, len(compounds)))
        temperatures = np.zeros(N_real)

        for j, stage in enumerate(stages):
            if stage <= results['feed_stage']:
                ratio = (stage - 1) / max(results['feed_stage'], 1)
                x_stage = results['x_D'] + ratio * (z_F - results['x_D'])
            else:
                ratio = (stage - results['feed_stage']) / max(N_real - results['feed_stage'], 1)
                x_stage = z_F + ratio * (results['x_B'] - z_F)

            x_stage = x_stage / np.sum(x_stage)
            x_profiles[j, :] = x_stage

            try:
                T_bubble, y_stage = thermo.bubble_temperature(P, x_stage)
                temperatures[j] = T_bubble
                y_profiles[j, :] = y_stage
            except:
                temperatures[j] = compounds[0].Tb + (compounds[-1].Tb - compounds[0].Tb) * (j / N_real)
                y_profiles[j, :] = x_stage

        # Préparer la réponse
        response_data = {
            'success': True,
            'results': {
                # Bilans matières
                'flow_feed': F,
                'flow_distillate': float(results['D']),
                'flow_bottom': float(results['B']),
                'composition_distillate': results['x_D'].tolist(),
                'composition_bottom': results['x_B'].tolist(),
                'composition_feed': z_F.tolist(),

                # Dimensionnement
                'N_min': float(results['N_min']),
                'R_min': float(results['R_min']),
                'R_operating': float(results['R']),
                'N_theoretical': float(results['N_theoretical']),
                'N_real': int(results['N_real']),
                'efficiency': float(results['efficiency']),
                'alpha_avg': float(results['alpha_avg']),
                'theta': float(results['theta']),

                # Configuration
                'N_rectification': int(results['N_R']),
                'N_stripping': int(results['N_S']),
                'feed_stage': int(results['feed_stage']),

                # Débits internes
                'liquid_rectification': float(results['L']),
                'vapor_rectification': float(results['V']),
                'liquid_stripping': float(results['L_prime']),
                'vapor_stripping': float(results['V_prime']),

                # Profils
                'stages': stages.tolist(),
                'liquid_profiles': x_profiles.tolist(),
                'vapor_profiles': y_profiles.tolist(),
                'temperatures': (temperatures - 273.15).tolist(),  # °C

                # Composés
                'compounds': compound_names,

                # Énergétique
                'temperature_top': float(temperatures[0] - 273.15),
                'temperature_bottom': float(temperatures[-1] - 273.15),
            }
        }

        return jsonify(response_data)

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/generate-plot', methods=['POST'])
def generate_plot():
    """
    Génère un graphique et le retourne en base64

    Body JSON:
    {
        "plot_type": "composition_profiles" | "temperature_profile" | "material_balance",
        "data": {...}
    }
    """
    try:
        data = request.get_json()
        plot_type = data.get('plot_type')
        plot_data = data.get('data')

        fig = None

        if plot_type == 'composition_profiles':
            fig = create_composition_plot(plot_data)
        elif plot_type == 'temperature_profile':
            fig = create_temperature_plot(plot_data)
        elif plot_type == 'material_balance':
            fig = create_material_balance_plot(plot_data)
        else:
            return jsonify({
                'success': False,
                'error': f'Type de graphique inconnu: {plot_type}'
            }), 400

        # Convertir en base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_composition_plot(data):
    """Crée le graphique des profils de composition"""
    stages = np.array(data['stages'])
    x_profiles = np.array(data['liquid_profiles'])
    compound_names = data['compounds']
    feed_stage = data['feed_stage']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    colors = plt.cm.Set3(np.linspace(0, 1, len(compound_names)))

    # Phase liquide
    for i, name in enumerate(compound_names):
        ax1.plot(x_profiles[:, i], stages, 'o-', linewidth=2.5,
                markersize=5, label=name, color=colors[i])

    ax1.axhline(y=feed_stage, color='blue', linestyle='--', linewidth=2,
               label='Plateau alimentation')
    ax1.set_xlabel('Fraction molaire liquide (x)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Numéro de plateau', fontsize=11, fontweight='bold')
    ax1.set_title('Phase Liquide', fontsize=12, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.invert_yaxis()
    ax1.set_xlim([0, 1])

    # Phase vapeur
    y_profiles = np.array(data.get('vapor_profiles', x_profiles))
    for i, name in enumerate(compound_names):
        ax2.plot(y_profiles[:, i], stages, 's-', linewidth=2.5,
                markersize=5, label=name, color=colors[i])

    ax2.axhline(y=feed_stage, color='blue', linestyle='--', linewidth=2,
               label='Plateau alimentation')
    ax2.set_xlabel('Fraction molaire vapeur (y)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Numéro de plateau', fontsize=11, fontweight='bold')
    ax2.set_title('Phase Vapeur', fontsize=12, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.invert_yaxis()
    ax2.set_xlim([0, 1])

    fig.suptitle('Profils de Composition dans la Colonne', fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig

def create_temperature_plot(data):
    """Crée le graphique du profil de température"""
    stages = np.array(data['stages'])
    temperatures = np.array(data['temperatures'])
    feed_stage = data['feed_stage']

    fig, ax = plt.subplots(figsize=(8, 10))

    ax.plot(temperatures, stages, 'o-', linewidth=3,
            markersize=8, color='orangered', label='Température')

    ax.axhline(y=feed_stage, color='blue', linestyle='--', linewidth=2,
              label=f'Plateau alimentation ({feed_stage})')

    ax.set_xlabel('Température (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Numéro de plateau', fontsize=12, fontweight='bold')
    ax.set_title('Profil de Température dans la Colonne',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()

    plt.tight_layout()
    return fig

def create_material_balance_plot(data):
    """Crée le graphique des bilans matières"""
    compound_names = data['compounds']
    F = data['flow_feed']
    D = data['flow_distillate']
    B = data['flow_bottom']
    z_F = np.array(data['composition_feed'])
    x_D = np.array(data['composition_distillate'])
    x_B = np.array(data['composition_bottom'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Bilans Matières de la Colonne', fontsize=14, fontweight='bold')

    # Graphique 1: Débits
    streams = ['Alimentation', 'Distillat', 'Résidu']
    flows = [F, D, B]
    colors_streams = ['blue', 'green', 'red']

    bars = ax1.bar(streams, flows, color=colors_streams, alpha=0.7,
                  edgecolor='black', linewidth=2)

    for bar, flow in zip(bars, flows):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{flow:.1f}\nkmol/h',
                ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax1.set_ylabel('Débit (kmol/h)', fontsize=11, fontweight='bold')
    ax1.set_title('Débits des flux', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Graphique 2: Compositions
    x = np.arange(len(compound_names))
    width = 0.25

    ax2.bar(x - width, z_F, width, label='Alimentation',
           color='blue', alpha=0.7, edgecolor='black')
    ax2.bar(x, x_D, width, label='Distillat',
           color='green', alpha=0.7, edgecolor='black')
    ax2.bar(x + width, x_B, width, label='Résidu',
           color='red', alpha=0.7, edgecolor='black')

    ax2.set_xlabel('Composé', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Fraction molaire', fontsize=11, fontweight='bold')
    ax2.set_title('Compositions des flux', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(compound_names, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim([0, 1.0])

    plt.tight_layout()
    return fig

@app.route('/api/reflux-study', methods=['POST'])
def reflux_study():
    """
    Étude paramétrique de l'effet du reflux
    """
    try:
        data = request.get_json()

        compound_names = data.get('compounds', ['benzene', 'toluene', 'o-xylene'])
        z_F = np.array(data.get('compositions', [0.33, 0.33, 0.34]))
        F = float(data.get('flow_rate', 100.0))
        P = float(data.get('pressure', 101325))
        efficiency = float(data.get('efficiency', 0.70))

        # Créer les composés
        compounds = [Compound(name) for name in compound_names]
        thermo = ThermodynamicPackage(compounds)

        shortcut = ShortcutDistillation(thermo, F, z_F, P)
        D, B, x_D, x_B = shortcut.material_balance()
        N_min, alpha_avg = shortcut.fenske_equation()
        R_min, theta = shortcut.underwood_method()

        # Varier le reflux
        R_factors = np.linspace(1.1, 3.0, 20)
        results_list = []

        for factor in R_factors:
            R = factor * R_min
            N = shortcut.gilliland_correlation(R)
            N_real = N / efficiency

            results_list.append({
                'R_factor': float(factor),
                'R': float(R),
                'N_theoretical': float(N),
                'N_real': float(N_real)
            })

        return jsonify({
            'success': True,
            'N_min': float(N_min),
            'R_min': float(R_min),
            'results': results_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  SERVEUR BACKEND FLASK - SIMULATEUR DE DISTILLATION")
    print("="*60)
    print(f"\n  URL: http://localhost:5000")
    print(f"  API Health: http://localhost:5000/api/health")
    print(f"\n  Endpoints disponibles:")
    print(f"    - GET  /api/health")
    print(f"    - GET  /api/compounds")
    print(f"    - POST /api/compound-properties")
    print(f"    - POST /api/simulate")
    print(f"    - POST /api/generate-plot")
    print(f"    - POST /api/reflux-study")
    print("\n" + "="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
