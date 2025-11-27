@echo off
chcp 65001 > nul
echo.
echo ================================================================================
echo    🧪 DISTILLATION MULTICOMPOSANTS - APPLICATION STREAMLIT
echo ================================================================================
echo.
echo    Prof. BAKHER Zine Elabidine - Filière PIC - UH1
echo.
echo ================================================================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist ".venv\Scripts\activate.bat" (
    echo ⚠️  Environnement virtuel introuvable. Création en cours...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements_streamlit.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo ✅ Lancement de l'application Streamlit...
echo.
echo 📍 L'application va s'ouvrir dans votre navigateur
echo 📍 URL: http://localhost:8501
echo.
echo 💡 Pour arrêter l'application, appuyez sur Ctrl+C
echo.
echo ================================================================================
echo.

streamlit run streamlit_app.py

pause
