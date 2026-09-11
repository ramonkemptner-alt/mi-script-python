# Quantum Anti-Register

Ejemplo educativo de Qiskit que construye un circuito cuántico y su inverso Hermitiano para cancelar la transformación aplicada al registro.

## Autoría

Creado por **RAMON FERNANDO DANIEL KEMPTNER** el **2026-09-11 a las 00:23:13 (-03:00)**.

## Requisitos

- Python 3.11 o compatible
- Qiskit 2.5.2
- Qiskit Aer 0.17.2

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecución

```powershell
python antiq.py
```

El ejemplo aplica puertas Hadamard, CNOT y una rotación `Rx`; después compone el circuito inverso. La simulación debe devolver `000` en las 1000 mediciones cuando se usa el circuito anti-inverso.

## Nota

En este proyecto, "anti-qubit" describe el circuito inverso de una transformación, no una antipartícula física. El código tiene finalidad educativa y de experimentación con circuitos cuánticos.

## Licencia

Este repositorio no incluye todavía una licencia. Añade una licencia antes de aceptar contribuciones o distribuirlo como software reutilizable.