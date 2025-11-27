@echo off
echo ========================================
echo  Distillation Multicomposants - PIC UH1
echo  Build et Lancement Application Integree
echo ========================================
echo.

REM Vérifier si le dossier frontend/build existe
if not exist "frontend\build" (
    echo [1/2] Build du frontend React...
    cd frontend
    call npm run build
    cd ..
    echo.
    echo ✅ Frontend builde avec succes!
    echo.
) else (
    echo ✅ Frontend deja builde (frontend\build existe)
    echo.
)

REM Lancer l'application intégrée
echo [2/2] Lancement de l'application integree...
echo.
echo 📍 Ouvrez votre navigateur sur: http://localhost:5000
echo.
python app.py

pause
