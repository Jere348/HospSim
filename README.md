# HospSim – Hito 2 (Teoría de Compiladores 2026-2)

DSL para simular la atención en un hospital. Compilador en Python 3 + ANTLR4.

## Uso
    pip install antlr4-python3-runtime==4.13.1
    python3 main.py tests/entrada_completa.txt
    ./run_tests.sh           # ejecuta todas las pruebas y compara con tests/esperado/
    make generate            # (opcional) regenera gen/; gen/ ya viene incluido

## Ejemplo
    recurso medicos = 1;
    proceso atencion {
        etapa consulta usa medicos durante 15 minutos;
    }
    generar pacientes cada 5 minutos hacia atencion;
    simular durante 1 hora;
    mostrar pacientes_atendidos;      // = 4
    mostrar espera_promedio;          // = 15.00 minutos
    mostrar ocupacion(medicos);       // = 100.00 %

## Cambios respecto al Hito 1
- Gramática: corregida la precedencia (`*` y `/` antes que `+` y `-`).
- Analizador semántico completo: 15 errores (ver `docs/ARQUITECTURA.md`).
- Errores léxicos y sintácticos con mensajes propios y código de salida 1.
- Representación intermedia (`backend/modelo.py`) y back end que ejecuta la simulación (`backend/simulador.py`).
- Pruebas automáticas con salida esperada verificada a mano (`docs/PLAN_VALIDACION.md`).

## Documentos
- `docs/ARQUITECTURA.md` – fases, módulos, decisiones y lista de errores semánticos.
- `docs/PLAN_VALIDACION.md` – método, casos y cálculos a mano de los resultados.
