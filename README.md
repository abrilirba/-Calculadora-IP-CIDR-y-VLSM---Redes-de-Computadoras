# Proyecto 2: Calculadora IP — CIDR y VLSM

Calculadoras de subredes usando las metodologías CIDR y VLSM.

Herramienta modular desarrollada en Python 3 para la materia de **Redes de Computadoras** (ESCOM - IPN). Permite realizar cálculos de direccionamiento IPv4 mediante notación CIDR y asignación dinámica de subredes mediante VLSM, tanto desde una interfaz gráfica de escritorio (`Tkinter`) como desde consola (CLI).

## Requisitos del Sistema
- **Sistema Operativo:** Windows 10/11, Linux o macOS.
- **Python:** Versión 3.8 o superior (incluye `tkinter` e `ipaddress` en su librería estándar).
- **Dependencias externas:** Ninguna (no requiere `pip install`).

## Estructura del Proyecto
```text
Proyecto2/
├── app.py              # Punto de entrada de la interfaz gráfica (GUI)
├── main.py             # Punto de entrada de la interfaz en consola (CLI)
├── ejecutar.bat        # Script ejecutable para abrir la GUI en Windows
├── README.md           # Documentación rápida y guía de ejecución
├── cidr/
│   ├── __init__.py
│   ├── calculos.py     # Cálculos de red, máscara, wildcard, rangos y división en subredes
│   ├── validaciones.py # Validación de formato IPv4/prefijo y direcciones de red
│   ├── gui.py          # Pestaña gráfica para Calculadora CIDR
│   └── interfaz.py     # Menú en consola para Calculadora CIDR
└── vlsm/
    ├── __init__.py
    ├── calculos.py     # Algoritmo VLSM descendente y asignación contigua
    ├── validaciones.py # Validación de red base y requerimientos de hosts
    ├── gui.py          # Pestaña gráfica para Calculadora VLSM
    └── interfaz.py     # Menú en consola para Calculadora VLSM
```

## Instrucciones de Ejecución
1. Descomprimir el archivo ZIP en una carpeta local.
2. **Modo Gráfico (Windows - Directo):** Hacer doble clic sobre el archivo `ejecutar.bat`.
3. **Modo Gráfico (Terminal):**
   ```bash
   python app.py
   ```
4. **Modo Consola (Terminal):**
   ```bash
   python main.py
   ```

## Casos de Prueba Verificados
1. **Calculadora CIDR (`192.168.10.0/24`):**
   - Dirección de red: `192.168.10.0/24`
   - Máscara de subred: `255.255.255.0`
   - Rango de hosts útiles: `192.168.10.1` - `192.168.10.254`
   - Broadcast: `192.168.10.255` (254 hosts utilizables)
2. **Calculadora VLSM (`192.168.0.0/24` con A=100, B=50, C=25, D=10):**
   - Subred A: `192.168.0.0/25` (126 hosts útiles)
   - Subred B: `192.168.0.128/26` (62 hosts útiles)
   - Subred C: `192.168.0.192/27` (30 hosts útiles)
   - Subred D: `192.168.0.224/28` (14 hosts útiles)
   - Espacio restante: 16 direcciones (`192.168.0.240/28`)
3. **Caso Límite / Validación de Error (`192.168.0.0/24` con 300 hosts):**
   - El sistema bloquea el cálculo y muestra el mensaje: *"Espacio insuficiente: se necesitan 512 direcciones, pero la red solo tiene 256."*

## Integrantes del Equipo y Roles
- **Herrera Pérez Pamela:** Desarrollo de la Calculadora 1 (Módulo CIDR: lógica matemática, validaciones e interfaz).
- **García García Miguel:** Desarrollo de la Calculadora 1 (Módulo CIDR: cálculo de subredes por prefijo/división, pruebas e interfaz).
- **Chávez Jurado Abril Aleksandra:** Desarrollo de la Calculadora 2 (Módulo VLSM: interfaz gráfica en Tkinter, tablas de resultados y conexión de eventos).
- **Haro Molina Luis Elias:** Desarrollo de la Calculadora 2 (Módulo VLSM: algoritmo de ordenamiento descendente, asignación contigua y validaciones).
- **García Domínguez José Antonio:** Documentación técnica (reporte PDF y README), creación del script ejecutable (`ejecutar.bat`), casos de prueba y organización de entregables.
