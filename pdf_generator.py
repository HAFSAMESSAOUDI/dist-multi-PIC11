"""
Générateur de Rapport PDF pour les Résultats de Simulation
Module: Modélisation et Simulation des Procédés
Prof. BAKHER Zine Elabidine - Filière PIC - UH1

Génère un rapport LaTeX puis PDF avec les résultats de simulation
"""

import os
import subprocess
import tempfile
import requests
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
\usepackage{hyperref}

\geometry{margin=2.5cm}

% Définition des couleurs
\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{lightblue}{RGB}{59,130,246}
\definecolor{titleblue}{RGB}{25,25,112}

% Configuration hyperref pour la table des matières cliquable
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,
    filecolor=darkblue,
    urlcolor=lightblue,
    citecolor=darkblue,
    pdftitle={Rapport de Simulation - Distillation Multicomposants},
    pdfauthor={Simulation App},
    pdfsubject={Distillation},
    pdfkeywords={distillation, simulation, génie chimique}
}

% Style de page
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{darkblue}{Rapport de Simulation}}
\fancyhead[R]{\small\textcolor{darkblue}{""" + datetime.now().strftime("%d/%m/%Y") + r"""}}
\fancyfoot[C]{\textcolor{darkblue}{\thepage}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}

\begin{document}

% Page de garde professionnelle
\begin{titlepage}
    \centering

    % Espace supérieur
    \vspace*{2cm}

    % Titre principal
    {\Huge\bfseries\textcolor{titleblue}{Rapport de Simulation}\par}
    \vspace{1cm}
    {\LARGE\textcolor{darkblue}{Distillation Multicomposants}\par}

    \vspace{2cm}

    % Ligne de séparation
    \textcolor{lightblue}{\rule{\textwidth}{2pt}}

    \vspace{1.5cm}

    % Informations de simulation
    \begin{flushleft}
    \large
    \textbf{\textcolor{darkblue}{Méthode de calcul:}} """ + method + r"""\\[0.5cm]
    \textbf{\textcolor{darkblue}{Date de génération:}} """ + datetime.now().strftime("%d %B %Y") + r"""\\[0.5cm]
    \textbf{\textcolor{darkblue}{Heure:}} """ + datetime.now().strftime("%H:%M") + r"""\\
    \end{flushleft}

    \vfill

    % Ligne de séparation
    \textcolor{lightblue}{\rule{\textwidth}{2pt}}

    \vspace{0.5cm}

    % Pied de page
    {\large\textit{Génie des Procédés Industriels et Chimiques}\par}
    {\normalsize Application de Simulation de Distillation\par}

    \vspace{1cm}
\end{titlepage}

% Table des matières automatique avec titre personnalisé
\newpage
\thispagestyle{empty}
\vspace*{1cm}
{\LARGE\bfseries\textcolor{titleblue}{Table des Matières}\par}
\vspace{0.5cm}
\textcolor{lightblue}{\rule{\textwidth}{1pt}}
\vspace{0.5cm}

\tableofcontents

\clearpage

% Réinitialiser la numérotation des pages
\setcounter{page}{1}

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

        # Résumé de la simulation
        num_compounds = len(params.get('compounds', []))
        latex += f"Cette simulation a permis de dimensionner une colonne de distillation pour séparer "
        latex += f"un mélange de {num_compounds} composés. "

        # Méthode utilisée
        if method == "Méthodes Simplifiées":
            latex += "Les méthodes simplifiées (Fenske, Underwood, Gilliland et Kirkbride) ont été utilisées "
            latex += "pour obtenir rapidement une première estimation de la configuration de la colonne. "
        elif method == "MESH Rigoureux":
            latex += "La méthode MESH rigoureuse a été utilisée pour une résolution plateau par plateau "
            latex += "en tenant compte de tous les équilibres thermodynamiques et bilans matière/énergie. "

        # Résultats principaux
        if 'column_design' in results:
            design = results['column_design']
            n_real = design.get('total_stages', 0)
            latex += f"\n\nLes principaux résultats obtenus sont:\n"
            latex += r"\begin{itemize}" + "\n"
            latex += f"\\item Nombre de plateaux réels: {n_real:.0f}\n"

            if 'feed_stage' in design:
                latex += f"\\item Plateau d'alimentation: {design.get('feed_stage', 0):.0f}\n"

        # Conditions opératoires
        latex += f"\\item Débit d'alimentation: {params.get('feed_flow', 100):.2f} kmol/h\n"
        latex += f"\\item Pression opératoire: {params.get('pressure', 1.013):.3f} bar\n"
        latex += r"\end{itemize}" + "\n\n"

        # Note finale
        latex += r"\vspace{0.5cm}" + "\n"
        latex += r"\noindent\textit{Ce rapport a été généré automatiquement par l'application de simulation "
        latex += r"de distillation multicomposants. Les résultats doivent être validés avant toute utilisation "
        latex += r"dans un projet industriel.}" + "\n\n"

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

    def _compile_online_latex(self, latex_code):
        """
        Compile LaTeX en utilisant LaTeX-on-HTTP (service gratuit en ligne)

        Parameters
        ----------
        latex_code : str
            Code LaTeX à compiler

        Returns
        -------
        result : dict
            {
                'success': bool,
                'pdf_bytes': bytes (si succès),
                'error': str (si erreur)
            }
        """
        try:
            # Service LaTeX-on-HTTP
            url = "https://latex.ytotech.com/builds/sync"

            # Préparer les fichiers pour la requête multipart
            files = {
                'compiler': (None, 'pdflatex'),
                'resources[]': ('rapport.tex', latex_code.encode('utf-8'), 'text/plain')
            }

            # Envoyer la requête
            response = requests.post(
                url,
                files=files,
                timeout=60  # 60 secondes max
            )

            # Vérifier la réponse (200 OK ou 201 Created)
            if response.status_code in [200, 201]:
                # Le PDF est dans la réponse
                pdf_bytes = response.content

                # Vérifier que c'est bien un PDF
                if pdf_bytes and len(pdf_bytes) > 4 and pdf_bytes[:4] == b'%PDF':
                    return {
                        'success': True,
                        'pdf_bytes': pdf_bytes
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Réponse invalide (taille: {len(pdf_bytes)} bytes, début: {pdf_bytes[:10]})'
                    }
            else:
                return {
                    'success': False,
                    'error': f'Erreur service compilation (HTTP {response.status_code})'
                }

        except requests.Timeout:
            return {
                'success': False,
                'error': 'Timeout du service de compilation (>60s)'
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Erreur réseau: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erreur compilation en ligne: {str(e)}'
            }

    def _compile_local_pdflatex(self, latex_code):
        """
        Compile LaTeX en utilisant pdflatex local (fallback)

        Parameters
        ----------
        latex_code : str
            Code LaTeX à compiler

        Returns
        -------
        result : dict
            {
                'success': bool,
                'pdf_bytes': bytes (si succès),
                'error': str (si erreur)
            }
        """
        # Créer un fichier temporaire
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"rapport_distillation_{timestamp}.tex"
        tex_path = os.path.join(self.temp_dir, tex_filename)
        pdf_path = os.path.join(self.temp_dir, f"rapport_distillation_{timestamp}.pdf")

        try:
            # Écrire le fichier .tex
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)

            # Vérifier si pdflatex est disponible
            try:
                subprocess.run(['pdflatex', '--version'],
                             capture_output=True,
                             timeout=5,
                             check=True)
                pdflatex_available = True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                return {
                    'success': False,
                    'error': 'pdflatex non installé localement'
                }

            # Première compilation
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', self.temp_dir, tex_path],
                capture_output=True,
                timeout=30,
                text=True
            )

            # Deuxième compilation (pour table des matières)
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', self.temp_dir, tex_path],
                capture_output=True,
                timeout=30,
                text=True
            )

            # Lire le PDF généré
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_bytes = f.read()

                # Nettoyer les fichiers temporaires
                for ext in ['.tex', '.aux', '.log', '.toc', '.out']:
                    temp_file = pdf_path.replace('.pdf', ext)
                    if os.path.exists(temp_file):
                        try:
                            os.remove(temp_file)
                        except:
                            pass

                return {
                    'success': True,
                    'pdf_bytes': pdf_bytes
                }
            else:
                return {
                    'success': False,
                    'error': 'PDF non généré après compilation locale'
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout compilation locale (>30s)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erreur compilation locale: {str(e)}'
            }

    def generate_pdf(self, simulation_results, method="Méthodes Simplifiées"):
        """
        Génère le PDF complet (compile automatiquement en ligne ou localement)

        Parameters
        ----------
        simulation_results : dict
            Résultats de simulation
        method : str
            Méthode utilisée

        Returns
        -------
        result : dict
            {
                'success': bool,
                'pdf_bytes': bytes (si PDF généré),
                'latex_code': str (toujours disponible),
                'error': str (si erreur),
                'method': str ('online', 'pdflatex', ou 'latex_only')
            }
        """

        # Générer le LaTeX
        latex_code = self.generate_latex_report(simulation_results, method)

        try:
            # MÉTHODE 1: Compilation en ligne (prioritaire - pas besoin d'installation)
            online_result = self._compile_online_latex(latex_code)

            if online_result['success']:
                return {
                    'success': True,
                    'pdf_bytes': online_result['pdf_bytes'],
                    'latex_code': latex_code,
                    'method': 'online'
                }

            # MÉTHODE 2: Fallback sur pdflatex local si disponible
            local_result = self._compile_local_pdflatex(latex_code)

            if local_result['success']:
                return {
                    'success': True,
                    'pdf_bytes': local_result['pdf_bytes'],
                    'latex_code': latex_code,
                    'method': 'pdflatex'
                }

            # Aucune méthode n'a fonctionné
            return {
                'success': False,
                'latex_code': latex_code,
                'error': f"Compilation échouée - En ligne: {online_result.get('error', 'erreur inconnue')}, Local: {local_result.get('error', 'non disponible')}",
                'method': 'latex_only'
            }

        except Exception as e:
            return {
                'success': False,
                'latex_code': latex_code,
                'error': f'Erreur: {str(e)}',
                'method': 'latex_only'
            }

    def generate_latex_only(self, simulation_results, method="Méthodes Simplifiées"):
        """
        Génère uniquement le code LaTeX (sans compilation PDF)

        Returns
        -------
        latex_code : str
            Code LaTeX du rapport
        """
        return self.generate_latex_report(simulation_results, method)
