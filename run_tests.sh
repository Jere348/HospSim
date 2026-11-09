#!/bin/sh
# Compara la salida de main.py para cada tests/<caso>.txt con tests/esperado/<caso>.out
# Uso: ./run_tests.sh        -> ejecuta las pruebas
#      ./run_tests.sh -u     -> regenera las salidas esperadas (revisarlas antes de confirmarlas)
mkdir -p tests/esperado
fallos=0
for f in tests/*.txt; do
    caso=$(basename "$f" .txt)
    esperado="tests/esperado/$caso.out"
    if [ "$1" = "-u" ]; then
        python3 main.py "$f" > "$esperado" 2>&1
    elif python3 main.py "$f" 2>&1 | diff -u "$esperado" - > /dev/null 2>&1; then
        echo "OK     $caso"
    else
        echo "FALLA  $caso"; fallos=$((fallos + 1))
    fi
done
[ "$1" = "-u" ] && exit 0
echo "$fallos prueba(s) fallida(s)"
[ $fallos -eq 0 ]
