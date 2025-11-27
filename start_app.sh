#!/bin/bash

echo "========================================"
echo " Distillation Multicomposants - PIC UH1"
echo " Démarrage de l'application React+Flask"
echo "========================================"
echo ""

# Démarrer le backend Flask
echo "[1/2] Démarrage du backend Flask..."
cd backend
python app.py &
BACKEND_PID=$!
echo "Backend démarré (PID: $BACKEND_PID)"
cd ..

# Attendre que le backend démarre
sleep 5

# Démarrer le frontend React
echo "[2/2] Démarrage du frontend React..."
cd frontend
npm start &
FRONTEND_PID=$!
echo "Frontend démarré (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "========================================"
echo " Application démarrée avec succès!"
echo " Backend: http://localhost:5000"
echo " Frontend: http://localhost:3000"
echo "========================================"
echo ""
echo "Pour arrêter l'application:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Attendre que l'utilisateur appuie sur Ctrl+C
wait
