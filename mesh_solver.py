"""
Résolution MESH Rigoureuse pour la Distillation Multicomposants
Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Implémentation de la méthode de Wang-Henke pour résoudre le système MESH :
- M: Material balances (bilans matières)
- E: Equilibrium relations (équilibres thermodynamiques)
- S: Summation equations (contraintes de sommation)
- H: Heat balances (bilans énergétiques)
"""

import numpy as np
from scipy.optimize import fsolve
from distillation_multicomposants import ThermodynamicPackage, Compound


class MESHSolver:
    """
    Résout le système d'équations MESH pour une colonne de distillation
    """

    def __init__(self, compounds, n_stages, feed_stage, pressure):
        """
        Parameters
        ----------
        compounds : list of Compound
            Liste des composés
        n_stages : int
            Nombre total de plateaux (incluant condenseur et rebouilleur)
        feed_stage : int
            Numéro du plateau d'alimentation
        pressure : float
            Pression de la colonne (Pa)
        """
        self.compounds = compounds
        self.n_comp = len(compounds)
        self.n_stages = n_stages
        self.feed_stage = feed_stage
        self.pressure = pressure
        self.thermo = ThermodynamicPackage(compounds)

        # Variables d'état
        self.T = None  # Températures [n_stages]
        self.x = None  # Compositions liquides [n_stages, n_comp]
        self.y = None  # Compositions vapeurs [n_stages, n_comp]
        self.L = None  # Débits liquides [n_stages]
        self.V = None  # Débits vapeurs [n_stages]
        self.K = None  # K-values [n_stages, n_comp]

    def initialize(self, F, z_F, R, D):
        """
        Initialise les variables d'état

        Parameters
        ----------
        F : float
            Débit d'alimentation (kmol/h)
        z_F : array
            Composition de l'alimentation [n_comp]
        R : float
            Rapport de reflux
        D : float
            Débit de distillat (kmol/h)
        """
        B = F - D  # Débit de résidu

        # Initialisation des températures (profil linéaire)
        T_top = self.compounds[0].Tb  # Température du composé le plus léger
        T_bottom = self.compounds[-1].Tb  # Température du composé le plus lourd
        self.T = np.linspace(T_top, T_bottom, self.n_stages)

        # Initialisation des débits (Constant Molar Overflow)
        self.L = np.zeros(self.n_stages)
        self.V = np.zeros(self.n_stages)

        # Section de rectification
        for j in range(1, self.feed_stage):
            self.L[j] = R * D
            self.V[j] = (R + 1) * D

        # Section d'épuisement
        for j in range(self.feed_stage, self.n_stages - 1):
            self.L[j] = R * D + F
            self.V[j] = (R + 1) * D + F - B

        # Condenseur (plateau 1)
        self.L[0] = R * D
        self.V[0] = (R + 1) * D

        # Rebouilleur (plateau N-1)
        self.L[-1] = self.L[-2]
        self.V[-1] = self.V[-2]

        # Initialisation des compositions (profils linéaires)
        self.x = np.zeros((self.n_stages, self.n_comp))
        self.y = np.zeros((self.n_stages, self.n_comp))

        # Estimer compositions distillat et résidu
        x_D = z_F.copy()  # Simplifié pour l'initialisation
        x_B = z_F.copy()

        for i in range(self.n_comp):
            # Profil linéaire entre distillat et résidu
            self.x[:, i] = np.linspace(x_D[i], x_B[i], self.n_stages)

        # Normaliser
        for j in range(self.n_stages):
            self.x[j, :] = self.x[j, :] / np.sum(self.x[j, :])

        # Initialiser K-values et compositions vapeurs
        self.update_K_values()
        for j in range(self.n_stages):
            self.y[j, :] = self.K[j, :] * self.x[j, :]
            self.y[j, :] = self.y[j, :] / np.sum(self.y[j, :])

        # Stocker les paramètres
        self.F = F
        self.z_F = z_F
        self.R = R
        self.D = D
        self.B = B

    def update_K_values(self):
        """
        Met à jour tous les K-values basés sur les températures actuelles
        """
        self.K = np.zeros((self.n_stages, self.n_comp))
        for j in range(self.n_stages):
            self.K[j, :] = self.thermo.K_values(self.T[j], self.pressure, self.x[j, :])

    def material_balances(self):
        """
        Résout les bilans matières par la méthode tridiagonale
        (Équations M du système MESH - équation 24 du PDF)
        """
        # Pour chaque composé, résoudre le système tridiagonal
        for i in range(self.n_comp):
            # Construire la matrice tridiagonale
            # A * x_new = b
            A = np.zeros((self.n_stages, self.n_stages))
            b = np.zeros(self.n_stages)

            for j in range(self.n_stages):
                if j == 0:  # Condenseur
                    A[j, j] = -(self.L[j] + self.V[j])
                    A[j, j+1] = self.L[j+1]
                    b[j] = -self.V[0] * self.y[0, i]

                elif j == self.n_stages - 1:  # Rebouilleur
                    A[j, j-1] = self.V[j-1]
                    A[j, j] = -(self.L[j] + self.V[j])
                    b[j] = 0

                elif j == self.feed_stage:  # Plateau d'alimentation
                    A[j, j-1] = self.V[j-1]
                    A[j, j] = -(self.L[j] + self.V[j])
                    A[j, j+1] = self.L[j+1]
                    b[j] = -self.F * self.z_F[i]

                else:  # Plateaux ordinaires
                    A[j, j-1] = self.V[j-1]
                    A[j, j] = -(self.L[j] + self.V[j])
                    A[j, j+1] = self.L[j+1]
                    b[j] = 0

            # Résoudre le système
            try:
                x_new = np.linalg.solve(A, b)
                self.x[:, i] = np.abs(x_new)  # Assurer positivité
            except np.linalg.LinAlgError:
                pass  # Garder les valeurs actuelles si singulier

    def equilibrium_relations(self):
        """
        Applique les relations d'équilibre
        (Équations E du système MESH - équation 30 du PDF)
        """
        self.update_K_values()
        for j in range(self.n_stages):
            self.y[j, :] = self.K[j, :] * self.x[j, :]

    def summation_equations(self):
        """
        Normalise les fractions molaires
        (Équations S du système MESH - équations 31-32 du PDF)
        """
        for j in range(self.n_stages):
            # Normaliser compositions liquides (équation 31)
            sum_x = np.sum(self.x[j, :])
            if sum_x > 0:
                self.x[j, :] = self.x[j, :] / sum_x

            # Normaliser compositions vapeurs (équation 32)
            sum_y = np.sum(self.y[j, :])
            if sum_y > 0:
                self.y[j, :] = self.y[j, :] / sum_y

    def calculate_temperatures(self):
        """
        Calcule les températures de bulle pour chaque plateau
        (Partie du système MESH - basé sur équation 8 du PDF)
        """
        for j in range(self.n_stages):
            # Température de bulle pour la composition liquide actuelle
            try:
                T_new = self.thermo.bubble_temperature(
                    self.pressure,
                    self.x[j, :],
                    T_guess=self.T[j]
                )
                self.T[j] = T_new
            except:
                pass  # Garder T actuelle si la convergence échoue

    def energy_balances(self):
        """
        Résout les bilans énergétiques pour mettre à jour L et V
        (Équations H du système MESH - équation 33 du PDF)

        Simplification : Constant Molar Overflow (CMO)
        Pour une résolution rigoureuse, il faudrait calculer les enthalpies
        """
        # Pour l'instant, on garde CMO (débits constants)
        # Une implémentation complète calculerait les enthalpies
        pass

    def convergence_criteria(self, T_old, x_old, L_old, V_old):
        """
        Vérifie les critères de convergence
        (Équations 36-39 du PDF)

        Returns
        -------
        converged : bool
        errors : dict
        """
        eps_T = np.max(np.abs(self.T - T_old))
        eps_x = np.max(np.abs(self.x - x_old))
        eps_L = np.max(np.abs((self.L - L_old) / (L_old + 1e-10)))
        eps_V = np.max(np.abs((self.V - V_old) / (V_old + 1e-10)))

        tol_T = 0.1  # K
        tol_x = 1e-6
        tol_L = 1e-4
        tol_V = 1e-4

        converged = (eps_T < tol_T and eps_x < tol_x and
                     eps_L < tol_L and eps_V < tol_V)

        errors = {
            'T': eps_T,
            'x': eps_x,
            'L': eps_L,
            'V': eps_V
        }

        return converged, errors

    def solve(self, F, z_F, R, D, max_iter=100, verbose=False):
        """
        Résout le système MESH par la méthode de Wang-Henke
        (Algorithme 1 du PDF - page 13)

        Parameters
        ----------
        F : float
            Débit d'alimentation (kmol/h)
        z_F : array
            Composition de l'alimentation
        R : float
            Rapport de reflux
        D : float
            Débit de distillat (kmol/h)
        max_iter : int
            Nombre maximum d'itérations
        verbose : bool
            Afficher les informations de convergence

        Returns
        -------
        results : dict
            Résultats de la simulation
        """
        # Initialisation
        self.initialize(F, z_F, R, D)

        if verbose:
            print(f"Résolution MESH : N={self.n_stages}, n_comp={self.n_comp}")
            print(f"F={F:.1f} kmol/h, R={R:.2f}, D={D:.1f} kmol/h")
            print("-" * 60)

        # Boucle d'itération (Algorithm 1 du PDF)
        for iteration in range(max_iter):
            # Sauvegarder l'état actuel
            T_old = self.T.copy()
            x_old = self.x.copy()
            L_old = self.L.copy()
            V_old = self.V.copy()

            # Étape 1 : Calcul des K-values
            self.update_K_values()

            # Étape 2 : Résolution des bilans matières (M)
            self.material_balances()

            # Étape 3 : Normalisation (S)
            self.summation_equations()

            # Étape 4 : Relations d'équilibre (E)
            self.equilibrium_relations()

            # Étape 5 : Normalisation finale
            self.summation_equations()

            # Étape 6 : Calcul des températures
            self.calculate_temperatures()

            # Étape 7 : Bilans énergétiques (H)
            self.energy_balances()

            # Étape 8 : Test de convergence
            converged, errors = self.convergence_criteria(T_old, x_old, L_old, V_old)

            if verbose and (iteration % 10 == 0 or converged):
                print(f"Iter {iteration:3d}: ε_T={errors['T']:.2e}, "
                      f"ε_x={errors['x']:.2e}, "
                      f"ε_L={errors['L']:.2e}, "
                      f"ε_V={errors['V']:.2e}")

            if converged:
                if verbose:
                    print(f"\n✓ Convergence atteinte en {iteration+1} itérations")
                break
        else:
            if verbose:
                print(f"\n⚠ Nombre maximum d'itérations atteint ({max_iter})")

        # Calculer les besoins énergétiques
        # Q_condenser (condenseur en tête) - chaleur à retirer
        lambda_avg = 35000  # kJ/kmol (estimation chaleur latente)
        Q_condenser = (self.R + 1) * self.D * lambda_avg  # kJ/h

        # Q_reboiler (rebouilleur en fond) - chaleur à fournir
        Q_reboiler = (self.R + 1) * self.D * lambda_avg  # kJ/h

        # Construire les résultats
        results = {
            'converged': converged,
            'iterations': iteration + 1,
            'temperatures': self.T.copy(),
            'compositions': {
                'liquid': self.x.copy(),
                'vapor': self.y.copy()
            },
            'flows': {
                'liquid': self.L.copy(),
                'vapor': self.V.copy()
            },
            'K_values': self.K.copy(),
            'distillate': {
                'flow': self.D,
                'composition': self.x[0, :].copy(),
                'temperature': self.T[0] - 273.15  # °C
            },
            'bottoms': {
                'flow': self.B,
                'composition': self.x[-1, :].copy(),
                'temperature': self.T[-1] - 273.15  # °C
            },
            'feed_stage': self.feed_stage,
            'reflux_ratio': self.R,
            'duties': {
                'condenser': Q_condenser,  # kJ/h
                'reboiler': Q_reboiler     # kJ/h
            }
        }

        return results

    def material_balance_check(self):
        """
        Vérifie le bilan matière global
        """
        # Vérifier F = D + B
        mass_balance = {
            'feed': self.F,
            'distillate': self.D,
            'bottoms': self.B,
            'closure': abs(self.F - (self.D + self.B)),
            'closure_percent': abs(self.F - (self.D + self.B)) / self.F * 100
        }

        # Vérifier par composé
        component_balance = []
        for i in range(self.n_comp):
            F_i = self.F * self.z_F[i]
            D_i = self.D * self.x[0, i]
            B_i = self.B * self.x[-1, i]
            closure = abs(F_i - (D_i + B_i))

            component_balance.append({
                'compound': self.compounds[i].name,
                'feed': F_i,
                'distillate': D_i,
                'bottoms': B_i,
                'closure': closure,
                'closure_percent': closure / F_i * 100 if F_i > 0 else 0
            })

        return {
            'global': mass_balance,
            'components': component_balance
        }


def compare_shortcut_vs_mesh(compounds, compositions, feed_rate, pressure,
                              light_recovery, heavy_recovery,
                              reflux_multiplier, efficiency):
    """
    Compare les méthodes simplifiées avec la méthode MESH rigoureuse

    Returns
    -------
    comparison : dict
        Comparaison des résultats
    """
    from scipy.optimize import brentq

    # Créer les objets composés
    compound_objects = [Compound(name) for name in compounds]
    thermo = ThermodynamicPackage(compound_objects)

    # Normaliser compositions
    compositions = np.array(compositions) / np.sum(compositions)

    # Indices des clés
    LK_idx = 0
    HK_idx = 1 if len(compounds) > 1 else 0

    # ===== MÉTHODES SIMPLIFIÉES =====

    # Calcul des débits
    D = feed_rate * compositions[LK_idx] * light_recovery
    B = feed_rate - D

    # Température moyenne
    T_avg = np.mean([comp.Tb for comp in compound_objects])
    K_values = thermo.K_values(T_avg, pressure)

    # Volatilités relatives
    alphas = K_values / K_values[HK_idx]
    alpha_avg = alphas[LK_idx]

    # Fenske
    x_LK_D = light_recovery * compositions[LK_idx] / (
        light_recovery * compositions[LK_idx] + (1 - heavy_recovery) * compositions[HK_idx]
    )
    x_HK_D = 1 - x_LK_D
    x_LK_B = (1 - light_recovery) * compositions[LK_idx] / (
        (1 - light_recovery) * compositions[LK_idx] + heavy_recovery * compositions[HK_idx]
    )
    x_HK_B = 1 - x_LK_B

    N_min = np.log((x_LK_D / x_HK_D) / (x_LK_B / x_HK_B)) / np.log(alpha_avg)

    # Underwood
    q = 1.0  # Liquide saturé

    def underwood_eq1(theta):
        return sum(alphas[i] * compositions[i] / (alphas[i] - theta)
                  for i in range(len(compounds))) - (1 - q)

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

    # Gilliland
    R = R_min * reflux_multiplier
    X = (R - R_min) / (R + 1)
    exponent = (1 + 54.4 * X) * (X - 1) / ((11 + 117.2 * X) * np.sqrt(X))
    Y = 1 - np.exp(exponent)
    N_theoretical = N_min + Y / (1 - Y)
    N_real = int(np.ceil(N_theoretical / efficiency))

    # Kirkbride
    ratio = (B / D) * (compositions[HK_idx] / compositions[LK_idx]) * (x_LK_B / x_HK_D) ** 2
    log_ratio = 0.206 * np.log(ratio)
    N_R_over_N_S = np.exp(log_ratio)
    N_S = N_real / (1 + N_R_over_N_S)
    N_R = N_real - N_S
    feed_stage = int(np.ceil(N_R)) + 1

    shortcut_results = {
        'N_min': N_min,
        'R_min': R_min,
        'R_operating': R,
        'N_theoretical': N_theoretical,
        'N_real': N_real,
        'feed_stage': feed_stage,
        'alpha_avg': alpha_avg
    }

    # ===== MÉTHODE MESH RIGOUREUSE =====

    solver = MESHSolver(
        compounds=compound_objects,
        n_stages=N_real,
        feed_stage=feed_stage,
        pressure=pressure
    )

    mesh_results = solver.solve(
        F=feed_rate,
        z_F=compositions,
        R=R,
        D=D,
        max_iter=100,
        verbose=False
    )

    # ===== COMPARAISON =====

    comparison = {
        'shortcut': shortcut_results,
        'mesh': mesh_results,
        'differences': {
            'T_top': {
                'shortcut': compound_objects[LK_idx].Tb - 273.15,
                'mesh': mesh_results['distillate']['temperature'],
                'diff': abs(compound_objects[LK_idx].Tb - 273.15 - mesh_results['distillate']['temperature'])
            },
            'T_bottom': {
                'shortcut': compound_objects[HK_idx].Tb - 273.15,
                'mesh': mesh_results['bottoms']['temperature'],
                'diff': abs(compound_objects[HK_idx].Tb - 273.15 - mesh_results['bottoms']['temperature'])
            }
        }
    }

    return comparison
