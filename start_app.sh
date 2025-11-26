#!/bin/bash

echo "========================================"
echo "  LANCEUR APPLICATION WEB DISTILLATION"
echo "========================================"
echo ""

echo "[1/2] Démarrage du backend Flask..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

sleep 5

echo "[2/2] Démarrage du frontend React..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  APPLICATION EN COURS DE DÉMARRAGE"
echo "========================================"
echo ""
echo "Backend Flask : http://localhost:5000"
echo "Frontend React: http://localhost:3000"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Pour arrêter l'application:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Ou appuyez sur Ctrl+C"
echo ""

# Attendre que l'utilisateur arrête l'application
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
