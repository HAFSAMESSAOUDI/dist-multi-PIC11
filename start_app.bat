@echo off
echo ========================================
echo  Distillation Multicomposants - PIC UH1
echo  Demarrage de l'application React+Flask
echo ========================================
echo.

REM Démarrer le backend Flask
echo [1/2] Demarrage du backend Flask...
start "Backend Flask" cmd /k "cd backend && python app.py"
timeout /t 5 /nobreak >nul

REM Démarrer le frontend React
echo [2/2] Demarrage du frontend React...
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo  Application demarree avec succes!
echo  Backend: http://localhost:5000
echo  Frontend: http://localhost:3000
echo ========================================
echo.
pause
