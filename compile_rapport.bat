@echo off
echo ========================================
echo Compilation du Rapport PDF
echo ========================================
echo.

REM Verifier si pdflatex est installe
where pdflatex >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] pdflatex n'est pas installe!
    echo.
    echo Veuillez installer MiKTeX:
    echo https://miktex.org/download
    echo.
    echo Ou utilisez Overleaf (en ligne):
    echo https://www.overleaf.com/
    echo.
    echo Consultez COMPILE_PDF.md pour plus d'informations
    pause
    exit /b 1
)

echo [INFO] pdflatex trouve! Compilation en cours...
echo.

REM Premiere compilation
echo [1/2] Premiere passe de compilation...
pdflatex -interaction=nonstopmode RAPPORT_COMPLET_APPLICATION.tex
if %errorlevel% neq 0 (
    echo [ERREUR] La compilation a echoue!
    pause
    exit /b 1
)

REM Deuxieme compilation (pour table des matieres)
echo.
echo [2/2] Deuxieme passe (table des matieres)...
pdflatex -interaction=nonstopmode RAPPORT_COMPLET_APPLICATION.tex
if %errorlevel% neq 0 (
    echo [ERREUR] La compilation a echoue!
    pause
    exit /b 1
)

REM Nettoyage des fichiers temporaires
echo.
echo [INFO] Nettoyage des fichiers temporaires...
del RAPPORT_COMPLET_APPLICATION.aux >nul 2>&1
del RAPPORT_COMPLET_APPLICATION.log >nul 2>&1
del RAPPORT_COMPLET_APPLICATION.out >nul 2>&1
del RAPPORT_COMPLET_APPLICATION.toc >nul 2>&1

echo.
echo ========================================
echo [SUCCES] PDF genere avec succes!
echo ========================================
echo.
echo Fichier: RAPPORT_COMPLET_APPLICATION.pdf
echo Taille: ~60+ pages
echo.

REM Ouvrir le PDF automatiquement
if exist RAPPORT_COMPLET_APPLICATION.pdf (
    echo Ouverture du PDF...
    start RAPPORT_COMPLET_APPLICATION.pdf
) else (
    echo [ERREUR] Le fichier PDF n'a pas ete trouve!
)

echo.
pause
