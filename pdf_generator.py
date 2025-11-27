"""
Générateur de Rapport PDF pour les Résultats de Simulation
Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Génère un rapport LaTeX puis PDF avec les résultats de simulation
"""

import os
import subprocess
import tempfile
from datetime import datetime


class SimulationPDFGenerator:
    """
    Génère un rapport PDF professionnel des résultats de simulation
    """

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def generate_latex_report(self, simulation_results, method="Méthodes Simplifiées"):
        """
        Génère le code LaTeX du rapport

        Parameters
        ----------
        simulation_results : dict
            Dictionnaire contenant tous les résultats de simulation
        method : str
            Méthode utilisée ("Méthodes Simplifiées", "MESH Rigoureux", "Comparaison")

        Returns
        -------
        latex_code : str
            Code LaTeX complet
        """

        # Extraire les informations
        params = simulation_results.get('parameters', {})
        results = simulation_results.get('results', {})

        # En-tête LaTeX
        latex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fancyhdr}

\geometry{margin=2cm}

\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{lightblue}{RGB}{59,130,246}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Rapport de Simulation - Distillation}
\fancyhead[R]{\small """ + datetime.now().strftime("%d/%m/%Y") + r"""}
\fancyfoot[C]{\thepage}

\begin{document}

% Page de titre
\begin{center}
{\Huge\bfseries Rapport de Simulation\\[0.3cm]}
{\Large Distillation Multicomposants\\[1cm]}

\begin{tabular}{rl}
\textbf{Module:} & Modélisation et Simulation des Procédés \\
\textbf{Professeur:} & BAKHER Zine Elabidine \\
\textbf{Filière:} & Procédés Industriels et Chimiques (PIC) \\
\textbf{Université:} & Hassan 1er \\[0.5cm]
\textbf{Date:} & """ + datetime.now().strftime("%d %B %Y") + r""" \\
\textbf{Méthode:} & """ + method + r""" \\
\end{tabular}
\end{center}

\vfill

\tableofcontents
\newpage

% Section 1: Paramètres d'entrée
\section{Paramètres d'Entrée}

"""

        # Composés
        if 'compounds' in params:
            latex += r"\subsection{Composés Sélectionnés}" + "\n\n"
            latex += r"\begin{table}[h]" + "\n"
            latex += r"\centering" + "\n"
            latex += r"\begin{tabular}{lcc}" + "\n"
            latex += r"\toprule" + "\n"
            latex += r"\textbf{Composé} & \textbf{Fraction Molaire} & \textbf{Débit (kmol/h)} \\" + "\n"
            latex += r"\midrule" + "\n"

            total_flow = params.get('feed_flow', 100)
            for comp in params['compounds']:
                name = comp.get('name', 'Inconnu')
                frac = comp.get('fraction', 0)
                flow = frac * total_flow
                latex += f"{name} & {frac:.4f} & {flow:.2f} \\\\\n"

            latex += r"\midrule" + "\n"
            latex += f"\\textbf{{Total}} & 1.0000 & {total_flow:.2f} \\\\\n"
            latex += r"\bottomrule" + "\n"
            latex += r"\end{tabular}" + "\n"
            latex += r"\caption{Composition de l'alimentation}" + "\n"
            latex += r"\end{table}" + "\n\n"

        # Conditions opératoires
        latex += r"\subsection{Conditions Opératoires}" + "\n\n"
        latex += r"\begin{itemize}" + "\n"
        latex += f"\\item \\textbf{{Débit d'alimentation:}} {params.get('feed_flow', 100):.2f} kmol/h\n"
        latex += f"\\item \\textbf{{Pression:}} {params.get('pressure', 1.013):.3f} bar\n"
        latex += f"\\item \\textbf{{Récupération composé léger:}} {params.get('recovery_light', 98):.1f}\\%\n"
        latex += f"\\item \\textbf{{Récupération composé lourd:}} {params.get('recovery_heavy', 98):.1f}\\%\n"
        latex += f"\\item \\textbf{{Condition thermique (q):}} {params.get('q', 1.0):.2f}\n"
        latex += f"\\item \\textbf{{Multiplicateur de reflux:}} {params.get('reflux_mult', 1.3):.2f}\n"
        latex += f"\\item \\textbf{{Efficacité des plateaux:}} {params.get('efficiency', 0.70):.2f}\n"
        latex += r"\end{itemize}" + "\n\n"

        # Section 2: Résultats
        latex += r"\section{Résultats de Simulation}" + "\n\n"

        if method == "Méthodes Simplifiées" or method == "Comparaison":
            latex += self._add_shortcut_results(results)

        if method == "MESH Rigoureux" or method == "Comparaison":
            latex += self._add_mesh_results(results)

        # Section 3: Bilans
        latex += r"\section{Bilans Matière et Énergétique}" + "\n\n"
        latex += self._add_material_energy_balances(results, params)

        # Section 4: Analyse économique
        if 'economic' in results:
            latex += r"\section{Analyse Économique}" + "\n\n"
            latex += self._add_economic_analysis(results['economic'])

        # Conclusion
        latex += r"\section{Conclusion}" + "\n\n"
        latex += "Cette simulation a permis de dimensionner une colonne de distillation "
        latex += f"pour séparer un mélange de {len(params.get('compounds', []))} composés. "

        if 'column_design' in results:
            n_real = results['column_design'].get('total_stages', 0)
            latex += f"Le nombre de plateaux réels requis est de {n_real:.0f}. "

        latex += r"\end{document}"

        return latex

    def _add_shortcut_results(self, results):
        """Ajoute les résultats des méthodes simplifiées"""

        latex = r"\subsection{Méthodes Simplifiées}" + "\n\n"

        if 'shortcut_methods' in results:
            shortcut = results['shortcut_methods']

            # Tableau récapitulatif
            latex += r"\begin{table}[h]" + "\n"
            latex += r"\centering" + "\n"
            latex += r"\begin{tabular}{lcc}" + "\n"
            latex += r"\toprule" + "\n"
            latex += r"\textbf{Méthode} & \textbf{Paramètre} & \textbf{Valeur} \\" + "\n"
            latex += r"\midrule" + "\n"

            # Fenske
            if 'fenske' in shortcut:
                fenske = shortcut['fenske']
                latex += f"Fenske (Éq. 1) & $N_{{\\min}}$ & {fenske.get('N_min', 0):.2f} plateaux \\\\\n"
                latex += f" & $\\alpha_{{avg}}$ & {fenske.get('alpha_avg', 0):.3f} \\\\\n"
                latex += r"\midrule" + "\n"

            # Underwood
            if 'underwood' in shortcut:
                underwood = shortcut['underwood']
                latex += f"Underwood (Éq. 2-3) & $R_{{\\min}}$ & {underwood.get('R_min', 0):.3f} \\\\\n"
                latex += f" & $\\theta$ & {underwood.get('theta', 0):.3f} \\\\\n"
                latex += r"\midrule" + "\n"

            # Gilliland
            if 'gilliland' in shortcut:
                gilliland = shortcut['gilliland']
                latex += f"Gilliland (Éq. 4-6) & $N$ théorique & {gilliland.get('N_theoretical', 0):.2f} plateaux \\\\\n"
                latex += r"\midrule" + "\n"

            # Efficacité
            if 'column_design' in results:
                design = results['column_design']
                latex += f"Avec efficacité (Éq. 7) & $N_{{\\text{{réel}}}}$ & {design.get('total_stages', 0):.0f} plateaux \\\\\n"
                latex += r"\midrule" + "\n"

            # Kirkbride
            if 'kirkbride' in shortcut:
                kirkbride = shortcut['kirkbride']
                latex += f"Kirkbride (Éq. 8) & Plateau alimentation & {kirkbride.get('feed_stage', 0):.0f} \\\\\n"
                latex += f" & Rectification & {kirkbride.get('N_rectification', 0):.0f} plateaux \\\\\n"
                latex += f" & Épuisement & {kirkbride.get('N_stripping', 0):.0f} plateaux \\\\\n"

            latex += r"\bottomrule" + "\n"
            latex += r"\end{tabular}" + "\n"
            latex += r"\caption{Résultats des méthodes simplifiées}" + "\n"
            latex += r"\end{table}" + "\n\n"

        return latex

    def _add_mesh_results(self, results):
        """Ajoute les résultats MESH"""

        latex = r"\subsection{Méthode MESH Rigoureuse}" + "\n\n"

        latex += "La méthode MESH (Material, Equilibrium, Summation, Heat) "
        latex += "a été utilisée pour résoudre rigoureusement le système plateau par plateau "
        latex += "selon les équations 9-13.\n\n"

        if 'convergence' in results:
            conv = results['convergence']
            latex += f"\\textbf{{Convergence:}} {conv.get('iterations', 0)} itérations, "
            latex += f"erreur finale = {conv.get('error', 0):.2e}\n\n"

        return latex

    def _add_material_energy_balances(self, results, params):
        """Ajoute les bilans matière et énergétique"""

        latex = r"\subsection{Bilan Matière}" + "\n\n"

        # Tableau des débits
        latex += r"\begin{table}[h]" + "\n"
        latex += r"\centering" + "\n"
        latex += r"\begin{tabular}{lccc}" + "\n"
        latex += r"\toprule" + "\n"
        latex += r"\textbf{Flux} & \textbf{Débit (kmol/h)} & \textbf{Température (°C)} & \textbf{Pression (bar)} \\" + "\n"
        latex += r"\midrule" + "\n"

        F = params.get('feed_flow', 100)
        P = params.get('pressure', 1.013)

        if 'flows' in results:
            flows = results['flows']
            D = flows.get('distillate', 0)
            B = flows.get('bottoms', 0)
        else:
            D = F * 0.5
            B = F * 0.5

        if 'temperatures' in results:
            temps = results['temperatures']
            T_top = temps.get('top', 80)
            T_bottom = temps.get('bottom', 140)
            T_feed = temps.get('feed', 110)
        else:
            T_top = 80
            T_bottom = 140
            T_feed = 110

        latex += f"Alimentation & {F:.2f} & {T_feed:.1f} & {P:.3f} \\\\\n"
        latex += f"Distillat & {D:.2f} & {T_top:.1f} & {P:.3f} \\\\\n"
        latex += f"Résidu & {B:.2f} & {T_bottom:.1f} & {P:.3f} \\\\\n"
        latex += r"\midrule" + "\n"
        latex += f"\\textbf{{Vérification}} & {D+B:.2f} & & \\\\\n"
        latex += f"\\textbf{{Erreur}} & {abs(F-D-B):.2e} & & \\\\\n"
        latex += r"\bottomrule" + "\n"
        latex += r"\end{tabular}" + "\n"
        latex += r"\caption{Bilan matière global}" + "\n"
        latex += r"\end{table}" + "\n\n"

        # Bilan énergétique
        latex += r"\subsection{Bilan Énergétique}" + "\n\n"

        if 'energy' in results:
            energy = results['energy']
            Q_cond = energy.get('Q_condenser', 0)
            Q_reb = energy.get('Q_reboiler', 0)

            latex += r"\begin{itemize}" + "\n"
            latex += f"\\item \\textbf{{Condenseur:}} {abs(Q_cond):.2f} kW\n"
            latex += f"\\item \\textbf{{Rebouilleur:}} {abs(Q_reb):.2f} kW\n"
            latex += r"\end{itemize}" + "\n\n"

        return latex

    def _add_economic_analysis(self, economic):
        """Ajoute l'analyse économique"""

        latex = r"\begin{table}[h]" + "\n"
        latex += r"\centering" + "\n"
        latex += r"\begin{tabular}{lc}" + "\n"
        latex += r"\toprule" + "\n"
        latex += r"\textbf{Poste de Coût} & \textbf{Montant (€/an)} \\" + "\n"
        latex += r"\midrule" + "\n"

        if 'capital' in economic:
            cap = economic['capital']
            latex += f"Investissement (colonne) & {cap.get('column', 0):,.0f} \\\\\n"
            latex += f"Investissement (condenseur) & {cap.get('condenser', 0):,.0f} \\\\\n"
            latex += f"Investissement (rebouilleur) & {cap.get('reboiler', 0):,.0f} \\\\\n"
            latex += r"\midrule" + "\n"

        if 'operating' in economic:
            oper = economic['operating']
            latex += f"Exploitation (énergie) & {oper.get('energy', 0):,.0f} \\\\\n"
            latex += f"Exploitation (refroidissement) & {oper.get('cooling', 0):,.0f} \\\\\n"
            latex += r"\midrule" + "\n"

        if 'maintenance' in economic:
            latex += f"Maintenance & {economic['maintenance']:,.0f} \\\\\n"
            latex += r"\midrule" + "\n"

        if 'TAC' in economic:
            latex += f"\\textbf{{TAC Total}} & \\textbf{{{economic['TAC']:,.0f}}} \\\\\n"

        latex += r"\bottomrule" + "\n"
        latex += r"\end{tabular}" + "\n"
        latex += r"\caption{Analyse économique (TAC - Éq. 17-20)}" + "\n"
        latex += r"\end{table}" + "\n\n"

        return latex

    def generate_pdf(self, simulation_results, method="Méthodes Simplifiées"):
        """
        Génère le PDF complet

        Parameters
        ----------
        simulation_results : dict
            Résultats de simulation
        method : str
            Méthode utilisée

        Returns
        -------
        pdf_bytes : bytes
            Contenu du PDF généré, ou None si échec
        """

        # Générer le LaTeX
        latex_code = self.generate_latex_report(simulation_results, method)

        # Créer un fichier temporaire
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"rapport_distillation_{timestamp}.tex"
        tex_path = os.path.join(self.temp_dir, tex_filename)
        pdf_path = os.path.join(self.temp_dir, f"rapport_distillation_{timestamp}.pdf")

        try:
            # Écrire le fichier .tex
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)

            # Compiler avec pdflatex (si disponible)
            try:
                # Première compilation
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', self.temp_dir, tex_path],
                    check=True,
                    capture_output=True,
                    timeout=30
                )

                # Deuxième compilation (pour table des matières)
                subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', self.temp_dir, tex_path],
                    check=True,
                    capture_output=True,
                    timeout=30
                )

                # Lire le PDF généré
                if os.path.exists(pdf_path):
                    with open(pdf_path, 'rb') as f:
                        pdf_bytes = f.read()

                    # Nettoyer les fichiers temporaires
                    for ext in ['.tex', '.aux', '.log', '.toc', '.out']:
                        temp_file = pdf_path.replace('.pdf', ext)
                        if os.path.exists(temp_file):
                            os.remove(temp_file)

                    return pdf_bytes
                else:
                    return None

            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # pdflatex non disponible ou erreur de compilation
                # Retourner le code LaTeX comme fallback
                return latex_code.encode('utf-8')

        except Exception as e:
            print(f"Erreur génération PDF: {e}")
            return None

    def generate_latex_only(self, simulation_results, method="Méthodes Simplifiées"):
        """
        Génère uniquement le code LaTeX (sans compilation PDF)

        Returns
        -------
        latex_code : str
            Code LaTeX du rapport
        """
        return self.generate_latex_report(simulation_results, method)
