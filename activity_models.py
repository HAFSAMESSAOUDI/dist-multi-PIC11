"""
Modèles d'Activité pour Mélanges Non-Idéaux
Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Implémentation des modèles thermodynamiques pour mélanges non-idéaux
Section 10.1 du PDF - Équation 40
"""

import numpy as np
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')


class ActivityModel:
    """
    Classe de base pour les modèles d'activité
    """

    def __init__(self, compounds, parameters=None):
        """
        Parameters
        ----------
        compounds : list
            Liste des composés
        parameters : dict
            Paramètres du modèle
        """
        self.compounds = compounds
        self.n_comp = len(compounds)
        self.parameters = parameters or {}

    def activity_coefficients(self, x, T):
        """
        Calcule les coefficients d'activité

        Parameters
        ----------
        x : array
            Fractions molaires liquides
        T : float
            Température (K)

        Returns
        -------
        gamma : array
            Coefficients d'activité
        """
        raise NotImplementedError("Doit être implémenté dans les sous-classes")

    def K_values_nonideal(self, T, P, x=None):
        """
        Calcule les K-values pour mélanges non-idéaux
        K_i = (γ_i * P_i^sat) / P

        Parameters
        ----------
        T : float
            Température (K)
        P : float
            Pression (Pa)
        x : array
            Fractions molaires liquides (optionnel)

        Returns
        -------
        K : array
            K-values
        """
        if x is None:
            x = np.ones(self.n_comp) / self.n_comp

        # Coefficients d'activité
        gamma = self.activity_coefficients(x, T)

        # Pressions de vapeur saturante
        P_sat = np.array([comp.vapor_pressure(T) for comp in self.compounds])

        # K-values (Équation 40 du PDF)
        K = (gamma * P_sat) / P

        return K


class WilsonModel(ActivityModel):
    """
    Modèle de Wilson pour mélanges non-idéaux

    ln(γ_i) = 1 - ln(Σ_j x_j Λ_ij) - Σ_k (x_k Λ_ki / Σ_j x_j Λ_kj)

    Λ_ij = (V_j / V_i) * exp(-a_ij / T)
    """

    def __init__(self, compounds, parameters=None):
        """
        Parameters
        ----------
        compounds : list
            Liste des composés
        parameters : dict
            Paramètres Wilson: {'a_ij': array (n_comp x n_comp),
                                'V_i': array (n_comp)}
        """
        super().__init__(compounds, parameters)

        # Paramètres par défaut si non fournis
        if 'a_ij' not in self.parameters:
            # Matrice d'interaction (K)
            self.parameters['a_ij'] = np.zeros((self.n_comp, self.n_comp))

        if 'V_i' not in self.parameters:
            # Volumes molaires (m³/mol) - estimation par défaut
            self.parameters['V_i'] = np.array([100e-6] * self.n_comp)

    def calculate_Lambda(self, T):
        """
        Calcule la matrice Λ_ij

        Parameters
        ----------
        T : float
            Température (K)

        Returns
        -------
        Lambda : array
            Matrice Λ_ij (n_comp x n_comp)
        """
        a_ij = self.parameters['a_ij']
        V_i = self.parameters['V_i']

        Lambda = np.zeros((self.n_comp, self.n_comp))

        for i in range(self.n_comp):
            for j in range(self.n_comp):
                if i == j:
                    Lambda[i, j] = 1.0
                else:
                    Lambda[i, j] = (V_i[j] / V_i[i]) * np.exp(-a_ij[i, j] / T)

        return Lambda

    def activity_coefficients(self, x, T):
        """
        Calcule les coefficients d'activité selon le modèle de Wilson

        Parameters
        ----------
        x : array
            Fractions molaires liquides
        T : float
            Température (K)

        Returns
        -------
        gamma : array
            Coefficients d'activité
        """
        Lambda = self.calculate_Lambda(T)

        gamma = np.zeros(self.n_comp)

        for i in range(self.n_comp):
            # Premier terme: 1 - ln(Σ_j x_j Λ_ij)
            sum1 = np.sum(x * Lambda[i, :])
            term1 = 1 - np.log(sum1)

            # Deuxième terme: - Σ_k (x_k Λ_ki / Σ_j x_j Λ_kj)
            term2 = 0
            for k in range(self.n_comp):
                sum2 = np.sum(x * Lambda[k, :])
                term2 += x[k] * Lambda[k, i] / sum2

            ln_gamma = term1 - term2
            gamma[i] = np.exp(ln_gamma)

        return gamma


class NRTLModel(ActivityModel):
    """
    Modèle NRTL (Non-Random Two-Liquid)

    ln(γ_i) = [Σ_j x_j τ_ji G_ji / Σ_k x_k G_ki] +
               Σ_j [x_j G_ij / Σ_k x_k G_kj] * [τ_ij - (Σ_m x_m τ_mj G_mj / Σ_k x_k G_kj)]

    G_ij = exp(-α_ij τ_ij)
    τ_ij = a_ij / T
    """

    def __init__(self, compounds, parameters=None):
        """
        Parameters
        ----------
        compounds : list
            Liste des composés
        parameters : dict
            Paramètres NRTL: {'a_ij': array (n_comp x n_comp),
                              'alpha_ij': array (n_comp x n_comp)}
        """
        super().__init__(compounds, parameters)

        # Paramètres par défaut
        if 'a_ij' not in self.parameters:
            # Paramètres d'interaction (K)
            self.parameters['a_ij'] = np.zeros((self.n_comp, self.n_comp))

        if 'alpha_ij' not in self.parameters:
            # Paramètres de non-randomness (généralement 0.2-0.47)
            self.parameters['alpha_ij'] = np.ones((self.n_comp, self.n_comp)) * 0.3
            # Diagonale à 0
            for i in range(self.n_comp):
                self.parameters['alpha_ij'][i, i] = 0.0

    def calculate_tau_G(self, T):
        """
        Calcule les matrices τ_ij et G_ij

        Parameters
        ----------
        T : float
            Température (K)

        Returns
        -------
        tau : array
            Matrice τ_ij (n_comp x n_comp)
        G : array
            Matrice G_ij (n_comp x n_comp)
        """
        a_ij = self.parameters['a_ij']
        alpha_ij = self.parameters['alpha_ij']

        tau = a_ij / T
        G = np.exp(-alpha_ij * tau)

        # Diagonale
        for i in range(self.n_comp):
            tau[i, i] = 0.0
            G[i, i] = 1.0

        return tau, G

    def activity_coefficients(self, x, T):
        """
        Calcule les coefficients d'activité selon le modèle NRTL

        Parameters
        ----------
        x : array
            Fractions molaires liquides
        T : float
            Température (K)

        Returns
        -------
        gamma : array
            Coefficients d'activité
        """
        tau, G = self.calculate_tau_G(T)

        gamma = np.zeros(self.n_comp)

        for i in range(self.n_comp):
            # Premier terme: Σ_j x_j τ_ji G_ji / Σ_k x_k G_ki
            numerator1 = np.sum(x * tau[:, i] * G[:, i])
            denominator1 = np.sum(x * G[:, i])
            term1 = numerator1 / denominator1

            # Deuxième terme
            term2 = 0
            for j in range(self.n_comp):
                sum_xG = np.sum(x * G[:, j])
                sum_xtauG = np.sum(x * tau[:, j] * G[:, j])

                term2 += (x[j] * G[i, j] / sum_xG) * (tau[i, j] - sum_xtauG / sum_xG)

            ln_gamma = term1 + term2
            gamma[i] = np.exp(ln_gamma)

        return gamma


class UNIQUACModel(ActivityModel):
    """
    Modèle UNIQUAC (Universal Quasi-Chemical)

    ln(γ_i) = ln(γ_i^combinatorial) + ln(γ_i^residual)

    Partie combinatoire:
    ln(γ_i^C) = ln(Φ_i/x_i) + z/2 * q_i * ln(θ_i/Φ_i) + l_i - (Φ_i/x_i) * Σ_j x_j l_j

    Partie résiduelle:
    ln(γ_i^R) = q_i * [1 - ln(Σ_j θ_j τ_ji) - Σ_j (θ_j τ_ij / Σ_k θ_k τ_kj)]

    Φ_i = x_i r_i / Σ_j x_j r_j  (fraction de volume)
    θ_i = x_i q_i / Σ_j x_j q_j  (fraction de surface)
    l_i = z/2 * (r_i - q_i) - (r_i - 1)
    τ_ij = exp(-a_ij / T)
    """

    def __init__(self, compounds, parameters=None):
        """
        Parameters
        ----------
        compounds : list
            Liste des composés
        parameters : dict
            Paramètres UNIQUAC: {'a_ij': array (n_comp x n_comp),
                                 'r_i': array (n_comp),  # volumes
                                 'q_i': array (n_comp)}  # surfaces
        """
        super().__init__(compounds, parameters)

        self.z = 10  # Coordination number

        # Paramètres par défaut
        if 'a_ij' not in self.parameters:
            # Paramètres d'interaction (K)
            self.parameters['a_ij'] = np.zeros((self.n_comp, self.n_comp))

        if 'r_i' not in self.parameters:
            # Volumes relatifs (estimation par défaut)
            self.parameters['r_i'] = np.ones(self.n_comp)

        if 'q_i' not in self.parameters:
            # Surfaces relatives (estimation par défaut)
            self.parameters['q_i'] = np.ones(self.n_comp)

    def calculate_fractions(self, x):
        """
        Calcule les fractions de volume Φ_i et de surface θ_i

        Parameters
        ----------
        x : array
            Fractions molaires liquides

        Returns
        -------
        Phi : array
            Fractions de volume
        theta : array
            Fractions de surface
        """
        r_i = self.parameters['r_i']
        q_i = self.parameters['q_i']

        # Fractions de volume
        sum_xr = np.sum(x * r_i)
        Phi = x * r_i / sum_xr

        # Fractions de surface
        sum_xq = np.sum(x * q_i)
        theta = x * q_i / sum_xq

        return Phi, theta

    def calculate_tau(self, T):
        """
        Calcule la matrice τ_ij

        Parameters
        ----------
        T : float
            Température (K)

        Returns
        -------
        tau : array
            Matrice τ_ij (n_comp x n_comp)
        """
        a_ij = self.parameters['a_ij']
        tau = np.exp(-a_ij / T)

        # Diagonale à 1
        for i in range(self.n_comp):
            tau[i, i] = 1.0

        return tau

    def activity_coefficients(self, x, T):
        """
        Calcule les coefficients d'activité selon le modèle UNIQUAC

        Parameters
        ----------
        x : array
            Fractions molaires liquides
        T : float
            Température (K)

        Returns
        -------
        gamma : array
            Coefficients d'activité
        """
        r_i = self.parameters['r_i']
        q_i = self.parameters['q_i']

        Phi, theta = self.calculate_fractions(x)
        tau = self.calculate_tau(T)

        # Paramètre l_i
        l_i = self.z / 2 * (r_i - q_i) - (r_i - 1)

        gamma = np.zeros(self.n_comp)

        for i in range(self.n_comp):
            # Partie combinatoire
            term1 = np.log(Phi[i] / x[i])
            term2 = self.z / 2 * q_i[i] * np.log(theta[i] / Phi[i])
            term3 = l_i[i]
            term4 = -(Phi[i] / x[i]) * np.sum(x * l_i)

            ln_gamma_C = term1 + term2 + term3 + term4

            # Partie résiduelle
            sum1 = np.sum(theta * tau[:, i])

            sum2 = 0
            for j in range(self.n_comp):
                sum_theta_tau = np.sum(theta * tau[:, j])
                sum2 += theta[j] * tau[i, j] / sum_theta_tau

            ln_gamma_R = q_i[i] * (1 - np.log(sum1) - sum2)

            # Total
            ln_gamma = ln_gamma_C + ln_gamma_R
            gamma[i] = np.exp(ln_gamma)

        return gamma


class IdealModel(ActivityModel):
    """
    Modèle idéal (γ_i = 1 pour tous les composés)
    """

    def activity_coefficients(self, x, T):
        """
        Retourne des coefficients d'activité unitaires

        Parameters
        ----------
        x : array
            Fractions molaires liquides
        T : float
            Température (K)

        Returns
        -------
        gamma : array
            Coefficients d'activité (tous égaux à 1)
        """
        return np.ones(self.n_comp)


def fit_parameters_from_data(model_type, compounds, T_data, x_data, gamma_data):
    """
    Ajuste les paramètres d'un modèle à partir de données expérimentales

    Parameters
    ----------
    model_type : str
        Type de modèle ('Wilson', 'NRTL', 'UNIQUAC')
    compounds : list
        Liste des composés
    T_data : array
        Températures des points expérimentaux (K)
    x_data : array
        Compositions des points expérimentaux
    gamma_data : array
        Coefficients d'activité expérimentaux

    Returns
    -------
    model : ActivityModel
        Modèle avec paramètres ajustés
    """
    n_comp = len(compounds)

    # Fonction objectif à minimiser
    def objective(params):
        # Créer le modèle avec les paramètres
        if model_type == 'Wilson':
            model = WilsonModel(compounds)
            model.parameters['a_ij'] = params[:n_comp**2].reshape((n_comp, n_comp))

        elif model_type == 'NRTL':
            n_params = n_comp**2
            model = NRTLModel(compounds)
            model.parameters['a_ij'] = params[:n_params].reshape((n_comp, n_comp))
            model.parameters['alpha_ij'] = params[n_params:].reshape((n_comp, n_comp))

        elif model_type == 'UNIQUAC':
            n_params = n_comp**2
            model = UNIQUACModel(compounds)
            model.parameters['a_ij'] = params[:n_params].reshape((n_comp, n_comp))
            model.parameters['r_i'] = params[n_params:n_params+n_comp]
            model.parameters['q_i'] = params[n_params+n_comp:]
        else:
            raise ValueError(f"Modèle inconnu: {model_type}")

        # Calculer l'erreur
        error = 0
        for T, x, gamma_exp in zip(T_data, x_data, gamma_data):
            gamma_calc = model.activity_coefficients(x, T)
            error += np.sum((gamma_calc - gamma_exp)**2)

        return error

    # Estimation initiale des paramètres
    if model_type == 'Wilson':
        n_params = n_comp**2

    elif model_type == 'NRTL':
        n_params = 2 * n_comp**2

    elif model_type == 'UNIQUAC':
        n_params = n_comp**2 + 2 * n_comp

    initial_guess = np.zeros(n_params)

    # Optimisation
    from scipy.optimize import minimize
    result = minimize(objective, initial_guess, method='Nelder-Mead')

    # Créer le modèle final
    if model_type == 'Wilson':
        model = WilsonModel(compounds)
        model.parameters['a_ij'] = result.x[:n_comp**2].reshape((n_comp, n_comp))

    elif model_type == 'NRTL':
        n_params = n_comp**2
        model = NRTLModel(compounds)
        model.parameters['a_ij'] = result.x[:n_params].reshape((n_comp, n_comp))
        model.parameters['alpha_ij'] = result.x[n_params:].reshape((n_comp, n_comp))

    elif model_type == 'UNIQUAC':
        n_params = n_comp**2
        model = UNIQUACModel(compounds)
        model.parameters['a_ij'] = result.x[:n_params].reshape((n_comp, n_comp))
        model.parameters['r_i'] = result.x[n_params:n_params+n_comp]
        model.parameters['q_i'] = result.x[n_params+n_comp:]

    return model


def compare_models(compounds, x, T, models=['Ideal', 'Wilson', 'NRTL', 'UNIQUAC']):
    """
    Compare différents modèles d'activité

    Parameters
    ----------
    compounds : list
        Liste des composés
    x : array
        Fractions molaires liquides
    T : float
        Température (K)
    models : list
        Modèles à comparer

    Returns
    -------
    results : dict
        Résultats de comparaison
    """
    results = {}

    for model_name in models:
        if model_name == 'Ideal':
            model = IdealModel(compounds)
        elif model_name == 'Wilson':
            model = WilsonModel(compounds)
        elif model_name == 'NRTL':
            model = NRTLModel(compounds)
        elif model_name == 'UNIQUAC':
            model = UNIQUACModel(compounds)
        else:
            continue

        gamma = model.activity_coefficients(x, T)

        results[model_name] = {
            'gamma': gamma,
            'model': model
        }

    return results
