#!/bin/sh
# Ejecuta todas las entradas de tests/ y muestra el resultado de cada una.
for f in tests/*.txt; do echo "## $f"; python3 main.py "$f" 2>&1; echo; done
