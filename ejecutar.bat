@echo off
title Calculadora IP - CIDR y VLSM (ESCOM - IPN)
echo Iniciando Calculadora de Subredes IPv4...
python app.py
if %errorlevel% neq 0 (
    echo.
    echo Intentando con comando py...
    py app.py
)
pause
