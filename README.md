# HospSim – Hito 1 (Teoría de Compiladores 2026-2)

DSL para simular la atención en un hospital. ANTLR4 + Python 3.

## Uso
    make                     # (opcional) regenera gen/ con ANTLR 4.13.1; gen/ ya viene incluido
    python3 main.py tests/entrada_completa.txt
    ./run_tests.sh           # corre todas las entradas de tests/

Requiere `pip install antlr4-python3-runtime==4.13.1`.

## Errores semánticos verificados
Identificador duplicado en su ámbito · identificador/recurso/proceso no declarado · tipo incorrecto
(destino no es proceso, ocupación sobre algo que no es recurso) · capacidad, duración, intervalo y
simulación ≤ 0 (expresiones constantes se evalúan) · división entre cero. Advertencia: símbolos sin usar.

## Pruebas (`tests/`)
`entrada_correcta`, `entrada_completa` (válidas) · `error_lexico`, `error_sintactico` · `error_capacidad`,
`error_duplicado`, `error_tiempos`, `error_expr`, `error_tipos`, `entrada_error` (semánticos).
