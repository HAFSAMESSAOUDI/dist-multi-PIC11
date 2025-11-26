@echo off
echo ========================================
echo   LANCEUR APPLICATION WEB DISTILLATION
echo ========================================
echo.

echo [1/2] Demarrage du backend Flask...
start "Backend Flask" cmd /k "cd backend && python app.py"

timeout /t 5 /nobreak > nul

echo [2/2] Demarrage du frontend React...
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   APPLICATION EN COURS DE DEMARRAGE
echo ========================================
echo.
echo Backend Flask : http://localhost:5000
echo Frontend React: http://localhost:3000
echo.
echo Patientez quelques secondes...
echo Le navigateur s'ouvrira automatiquement.
echo.
echo Pour arreter l'application, fermez les 2 fenetres de commande.
echo.
pause
