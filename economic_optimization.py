"""
Optimisation Économique de Colonnes de Distillation
Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Implémentation de l'optimisation basée sur le TAC (Total Annualized Cost)
Équations 43-50 du PDF
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
import warnings
warnings.filterwarnings('ignore')


class EconomicOptimizer:
    """
    Optimisation économique d'une colonne de distillation
    """

    def __init__(self, simulate_function):
        """
        Parameters
        ----------
        simulate_function : callable
            Fonction de simulation qui prend (R, N, P) et retourne les résultats
        """
        self.simulate_function = simulate_function

        # Paramètres économiques par défaut (€)
        self.costs = {
            # Coûts d'investissement
            'column_per_m': 15000,  # €/m de colonne
            'tray_per_unit': 800,   # €/plateau
            'condenser_per_kW': 2000,  # €/kW
            'reboiler_per_kW': 2500,   # €/kW

            # Coûts opératoires
            'energy_per_kWh': 0.08,  # €/kWh
            'cooling_per_kWh': 0.02,  # €/kWh
            'maintenance_fraction': 0.05,  # 5% du capital/an

            # Paramètres financiers
            'CRF': 0.15,  # Capital Recovery Factor (15%/an)
            'operating_hours': 8000  # h/an
        }

    def set_costs(self, **kwargs):
        """
        Met à jour les paramètres économiques
        """
        self.costs.update(kwargs)

    def calculate_column_cost(self, N, diameter=1.5):
        """
        Calcule le coût de la colonne

        Parameters
        ----------
        N : int
            Nombre de plateaux
        diameter : float
            Diamètre de la colonne (m)

        Returns
        -------
        cost : float
            Coût de la colonne (€)
        """
        # Hauteur de la colonne (espacement de 0.6m par plateau)
        height = N * 0.6  # m

        # Coût de la colonne
        C_column = self.costs['column_per_m'] * height

        # Coût des plateaux
        C_trays = self.costs['tray_per_unit'] * N

        return C_column + C_trays

    def calculate_heat_exchanger_cost(self, Q_kW):
        """
        Calcule le coût d'un échangeur de chaleur

        Parameters
        ----------
        Q_kW : float
            Puissance thermique (kW)

        Returns
        -------
        cost : float
            Coût de l'échangeur (€)
        """
        return abs(Q_kW) * self.costs['condenser_per_kW']

    def calculate_capital_cost(self, N, Q_condenser, Q_reboiler, diameter=1.5):
        """
        Calcule le coût d'investissement total
        (Équation 44 du PDF)

        Parameters
        ----------
        N : int
            Nombre de plateaux
        Q_condenser : float
            Puissance du condenseur (kW)
        Q_reboiler : float
            Puissance du rebouilleur (kW)
        diameter : float
            Diamètre de la colonne (m)

        Returns
        -------
        capital_cost : dict
            Détails des coûts d'investissement
        """
        C_column = self.calculate_column_cost(N, diameter)
        C_condenser = self.calculate_heat_exchanger_cost(Q_condenser)
        C_reboiler = self.costs['reboiler_per_kW'] * abs(Q_reboiler)

        total = C_column + C_condenser + C_reboiler

        return {
            'column': C_column,
            'condenser': C_condenser,
            'reboiler': C_reboiler,
            'total': total
        }

    def calculate_operating_cost(self, Q_condenser, Q_reboiler):
        """
        Calcule le coût d'exploitation annuel
        (Équation 45 du PDF)

        Parameters
        ----------
        Q_condenser : float
            Puissance du condenseur (kW)
        Q_reboiler : float
            Puissance du rebouilleur (kW)

        Returns
        -------
        operating_cost : dict
            Détails des coûts d'exploitation annuels
        """
        hours = self.costs['operating_hours']

        # Coût énergétique (rebouilleur)
        C_energy = abs(Q_reboiler) * self.costs['energy_per_kWh'] * hours

        # Coût de refroidissement (condenseur)
        C_cooling = abs(Q_condenser) * self.costs['cooling_per_kWh'] * hours

        total = C_energy + C_cooling

        return {
            'energy': C_energy,
            'cooling': C_cooling,
            'total': total
        }

    def calculate_TAC(self, N, R, Q_condenser, Q_reboiler, diameter=1.5):
        """
        Calcule le Total Annualized Cost (TAC)
        (Équation 43 du PDF)

        TAC = C_capital * CRF + C_operating + C_maintenance

        Parameters
        ----------
        N : int
            Nombre de plateaux
        R : float
            Rapport de reflux
        Q_condenser : float
            Puissance du condenseur (kW)
        Q_reboiler : float
            Puissance du rebouilleur (kW)
        diameter : float
            Diamètre de la colonne (m)

        Returns
        -------
        TAC : dict
            Total Annualized Cost et détails
        """
        # Coûts d'investissement
        capital = self.calculate_capital_cost(N, Q_condenser, Q_reboiler, diameter)

        # Coûts d'exploitation
        operating = self.calculate_operating_cost(Q_condenser, Q_reboiler)

        # Coût de maintenance (% du capital)
        C_maintenance = capital['total'] * self.costs['maintenance_fraction']

        # TAC
        TAC = capital['total'] * self.costs['CRF'] + operating['total'] + C_maintenance

        return {
            'TAC': TAC,
            'capital': capital,
            'operating': operating,
            'maintenance': C_maintenance,
            'annualized_capital': capital['total'] * self.costs['CRF']
        }

    def optimize_reflux(self, N_min, R_min, simulate_func, reflux_range=(1.1, 3.0), n_points=20):
        """
        Optimise le reflux pour un nombre de plateaux donné

        Parameters
        ----------
        N_min : float
            Nombre minimum de plateaux
        R_min : float
            Reflux minimum
        simulate_func : callable
            Fonction de simulation(R) -> results
        reflux_range : tuple
            Range des multiplicateurs de reflux (min, max)
        n_points : int
            Nombre de points à évaluer

        Returns
        -------
        optimization_results : dict
            Résultats de l'optimisation
        """
        # Générer les multiplicateurs de reflux
        multipliers = np.linspace(reflux_range[0], reflux_range[1], n_points)

        results = []

        for mult in multipliers:
            R = R_min * mult

            # Simuler
            try:
                sim_results = simulate_func(R)

                if sim_results['success']:
                    # Extraire les résultats
                    N = sim_results['results']['column_design']['total_stages']
                    Q_c = sim_results['results']['energy']['Q_condenser']
                    Q_r = sim_results['results']['energy']['Q_reboiler']

                    # Calculer le TAC
                    tac = self.calculate_TAC(N, R, Q_c, Q_r)

                    results.append({
                        'multiplier': mult,
                        'R': R,
                        'N': N,
                        'Q_condenser': Q_c,
                        'Q_reboiler': Q_r,
                        'TAC': tac['TAC'],
                        'TAC_details': tac
                    })
            except Exception as e:
                continue

        if not results:
            return None

        # Trouver l'optimum
        TACs = [r['TAC'] for r in results]
        optimal_idx = np.argmin(TACs)
        optimal = results[optimal_idx]

        return {
            'optimal': optimal,
            'all_results': results,
            'R_min': R_min,
            'N_min': N_min
        }

    def multi_objective_optimization(self, simulate_func, bounds, weights=None):
        """
        Optimisation multi-objectifs : minimiser TAC et maximiser pureté
        (Extension des équations 43-50 du PDF)

        Parameters
        ----------
        simulate_func : callable
            Fonction de simulation(R, N, P) -> results
        bounds : dict
            Limites des variables {'R': (min, max), 'N': (min, max), 'P': (min, max)}
        weights : dict
            Poids des objectifs {'cost': w1, 'purity': w2}

        Returns
        -------
        optimization_results : dict
        """
        if weights is None:
            weights = {'cost': 0.7, 'purity': 0.3}

        def objective(x):
            """
            Fonction objectif multi-objectifs

            x = [R, N, P]
            """
            R, N, P = x
            N = int(round(N))

            try:
                # Simuler
                results = simulate_func(R, N, P)

                if not results['success']:
                    return 1e10  # Pénalité

                # Extraire résultats
                Q_c = results['results']['energy']['Q_condenser']
                Q_r = results['results']['energy']['Q_reboiler']

                # Calculer TAC
                tac = self.calculate_TAC(N, R, Q_c, Q_r)
                cost_normalized = tac['TAC'] / 1e6  # Normaliser

                # Pureté (à maximiser, donc on minimise son inverse)
                purity_D = results['results']['compositions']['distillate'][0]['fraction']
                purity_normalized = 1 - purity_D

                # Objectif combiné
                obj = weights['cost'] * cost_normalized + weights['purity'] * purity_normalized

                return obj

            except Exception as e:
                return 1e10  # Pénalité

        # Limites
        bounds_list = [
            (bounds['R'][0], bounds['R'][1]),
            (bounds['N'][0], bounds['N'][1]),
            (bounds['P'][0], bounds['P'][1])
        ]

        # Optimisation globale par évolution différentielle
        result = differential_evolution(
            objective,
            bounds_list,
            maxiter=100,
            popsize=15,
            tol=0.01,
            seed=42
        )

        R_opt, N_opt, P_opt = result.x
        N_opt = int(round(N_opt))

        # Simuler avec les paramètres optimaux
        optimal_results = simulate_func(R_opt, N_opt, P_opt)

        return {
            'optimal_R': R_opt,
            'optimal_N': N_opt,
            'optimal_P': P_opt,
            'objective_value': result.fun,
            'simulation_results': optimal_results,
            'optimization_status': result.message
        }


def parametric_study_reflux(simulate_func, R_min, reflux_multipliers):
    """
    Étude paramétrique de l'effet du reflux
    (Section 9.1 du PDF)

    Parameters
    ----------
    simulate_func : callable
        Fonction de simulation(R) -> results
    R_min : float
        Reflux minimum
    reflux_multipliers : array
        Multiplicateurs à tester

    Returns
    -------
    study_results : list
        Résultats de l'étude paramétrique
    """
    results = []

    for mult in reflux_multipliers:
        R = R_min * mult

        try:
            sim_results = simulate_func(R)

            if sim_results['success']:
                results.append({
                    'multiplier': mult,
                    'R': R,
                    'N_real': sim_results['results']['column_design']['total_stages'],
                    'Q_condenser': sim_results['results']['energy']['Q_condenser'],
                    'Q_reboiler': sim_results['results']['energy']['Q_reboiler']
                })
        except:
            continue

    return results


def parametric_study_pressure(simulate_func, pressures):
    """
    Étude paramétrique de l'effet de la pression
    (Section 9.2 du PDF)

    Parameters
    ----------
    simulate_func : callable
        Fonction de simulation(P) -> results
    pressures : array
        Pressions à tester (Pa)

    Returns
    -------
    study_results : list
        Résultats de l'étude paramétrique
    """
    results = []

    for P in pressures:
        try:
            sim_results = simulate_func(P)

            if sim_results['success']:
                results.append({
                    'pressure_Pa': P,
                    'pressure_bar': P / 101325,
                    'alpha_avg': sim_results['results']['shortcut_methods']['fenske']['alpha_avg'],
                    'N_min': sim_results['results']['shortcut_methods']['fenske']['N_min'],
                    'T_top': sim_results['results']['temperatures']['top'],
                    'T_bottom': sim_results['results']['temperatures']['bottom'],
                    'Q_total': (sim_results['results']['energy']['Q_condenser'] +
                               sim_results['results']['energy']['Q_reboiler'])
                })
        except:
            continue

    return results


def sensitivity_analysis(simulate_func, base_params, vary_param, vary_range, n_points=10):
    """
    Analyse de sensibilité d'un paramètre

    Parameters
    ----------
    simulate_func : callable
        Fonction de simulation(**params) -> results
    base_params : dict
        Paramètres de base
    vary_param : str
        Nom du paramètre à varier
    vary_range : tuple
        (min, max) du paramètre
    n_points : int
        Nombre de points

    Returns
    -------
    sensitivity_results : dict
    """
    values = np.linspace(vary_range[0], vary_range[1], n_points)
    results = []

    for val in values:
        params = base_params.copy()
        params[vary_param] = val

        try:
            sim_results = simulate_func(**params)

            if sim_results['success']:
                results.append({
                    'parameter_value': val,
                    'results': sim_results['results']
                })
        except:
            continue

    return {
        'parameter': vary_param,
        'values': values,
        'results': results
    }
