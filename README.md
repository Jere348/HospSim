# HospSim

Lenguaje de dominio específico para simular la atención en un hospital y su compilador
(Python 3 + ANTLR4). Trabajo del curso Teoría de Compiladores (1ACC0218), UPC 2026-2.

```
recurso medicos = 1;
proceso atencion {
    etapa consulta usa medicos durante 15 minutos;
}
generar pacientes cada 5 minutos hacia atencion;
simular durante 1 hora;
mostrar pacientes_atendidos;      // = 4
mostrar espera_promedio;          // = 15.00 minutos
mostrar ocupacion(medicos);       // = 100.00 %
```

## Uso

```bash
pip install antlr4-python3-runtime==4.13.1
python3 main.py tests/entrada_completa.txt          # compila y ejecuta
python3 main.py --tokens tests/entrada_correcta.txt # solo análisis léxico
python3 tools/derivaciones.py                        # derivaciones más a la izquierda
./run_tests.sh                                       # pruebas automáticas
make generate                                        # (opcional) regenera gen/ con ANTLR 4.13.1
```

## Estructura

| Ruta | Contenido |
|---|---|
| `HospSim.g4` | Gramática léxica y sintáctica (ANTLR4). |
| `gen/` | Código generado por ANTLR (incluido para no requerir Java). |
| `main.py` | Driver: léxico → sintáctico → semántico → representación intermedia → simulación. |
| `semantic/` | Tabla de símbolos por ámbitos y analizador semántico (21 verificaciones). |
| `backend/` | Representación intermedia (`modelo.py`) y back end de simulación (`simulador.py`). |
| `tools/derivaciones.py` | Derivaciones más a la izquierda en la notación del curso, generadas desde el parser. |
| `tests/` | Programas de prueba y salidas esperadas (`tests/esperado/`). |
| `docs/` | Informe, presentación, arquitectura, plan de validación y guion del video. |

## Entregables del Hito 2

- Informe: [`docs/informe/Informe_Hito2_HospSim.pdf`](docs/informe/Informe_Hito2_HospSim.pdf) (editable en `.docx`)
- Presentación: [`docs/presentacion/Presentacion_Hito2_HospSim.pdf`](docs/presentacion/Presentacion_Hito2_HospSim.pdf) (editable en `.pptx`)
- Arquitectura: [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md)
- Plan de validación: [`docs/PLAN_VALIDACION.md`](docs/PLAN_VALIDACION.md)
- Guion del video: [`docs/GUION_VIDEO.md`](docs/GUION_VIDEO.md)

## Historial

- **Hito 1** (tag `hito-1`): analizadores léxico, sintáctico y semántico inicial.
- **Hito 2** (tag `hito-2`): gramática estratificada E/T/F (corrige la precedencia del Hito 1),
  analizador semántico completo, representación intermedia, simulador, pruebas y documentación.
- **Hito 3**: generación de código LLVM con llvmlite, validada contra el simulador.
