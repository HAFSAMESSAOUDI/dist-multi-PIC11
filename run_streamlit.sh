#!/bin/bash

echo ""
echo "================================================================================"
echo "   🧪 DISTILLATION MULTICOMPOSANTS - APPLICATION STREAMLIT"
echo "================================================================================"
echo ""
echo "   Prof. BAKHER Zine Elabidine - Filière PIC - UH1"
echo ""
echo "================================================================================"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "⚠️  Environnement virtuel introuvable. Création en cours..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements_streamlit.txt
else
    source .venv/bin/activate
fi

echo ""
echo "✅ Lancement de l'application Streamlit..."
echo ""
echo "📍 L'application va s'ouvrir dans votre navigateur"
echo "📍 URL: http://localhost:8501"
echo ""
echo "💡 Pour arrêter l'application, appuyez sur Ctrl+C"
echo ""
echo "================================================================================"
echo ""

streamlit run streamlit_app.py
