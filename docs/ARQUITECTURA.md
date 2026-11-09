# Arquitectura del compilador HospSim

```
programa.txt
    │
    ▼
┌───────────────────┐   gen/HospSimLexer.py (ANTLR4)
│ Analizador léxico │   tokens; errores → ColectorErrores('Léxico')
└───────────────────┘
    │ CommonTokenStream
    ▼
┌──────────────────────┐   gen/HospSimParser.py (ANTLR4)
│ Analizador sintáctico│   árbol de análisis; errores → ColectorErrores('Sintáctico')
└──────────────────────┘
    │ árbol (ParseTree)                         ── si hay errores: se reportan y termina
    ▼
┌──────────────────────┐   semantic/semantic_visitor.py + symbol_table.py
│ Analizador semántico │   Visitor + tabla de símbolos con ámbitos (global / por proceso)
└──────────────────────┘
    │ árbol validado                            ── si hay errores: se reportan y termina
    ▼
┌──────────────────────────┐   backend/modelo.py (ConstructorModelo)
│ Representación intermedia│   Modelo: recursos, procesos→etapas, llegadas, duración, consultas
└──────────────────────────┘   (expresiones evaluadas, tiempos normalizados a minutos)
    │ Modelo
    ▼
┌──────────────────────┐   backend/simulador.py
│ Back end (Hito 2)    │   simulación determinista → métricas → reporte
└──────────────────────┘
    │
    ▼
pacientes_atendidos / espera_promedio / ocupacion(recurso)
```

## Módulos

| Módulo | Responsabilidad |
|---|---|
| `HospSim.g4` | Gramática léxica y sintáctica (ANTLR4). |
| `gen/` | Lexer, parser y visitor generados por ANTLR 4.13.1 (`make generate`). |
| `main.py` | Driver: encadena las fases, centraliza los mensajes de error y define el código de salida (0 OK, 1 error). |
| `semantic/symbol_table.py` | Tabla de símbolos con pila de ámbitos: `declare`, `lookup`, advertencias de símbolos sin usar. Las métricas se predeclaran en el ámbito global. |
| `semantic/semantic_visitor.py` | Recorre el árbol, llena la tabla de símbolos y verifica los errores semánticos. Evalúa expresiones constantes (los recursos usados en expresiones aportan su capacidad). |
| `semantic/errors.py` | `SemanticError` con número de línea. |
| `backend/modelo.py` | Convierte el árbol validado en el `Modelo` (representación intermedia independiente de ANTLR). |
| `backend/simulador.py` | Ejecuta el `Modelo` y formatea las consultas `mostrar`. |

## Decisiones de diseño
- **Dos recorridos separados** (semántico y construcción del modelo): el back end nunca ve un árbol inválido, así no repite validaciones.
- **Representación intermedia propia**: desacopla el back end de ANTLR. En el Hito 3 se puede generar LLVM IR desde el mismo `Modelo` sin tocar el front end; el simulador en Python queda como oráculo para validar el código generado.
- **Simulación determinista** (sin aleatoriedad): las salidas son reproducibles y se pueden verificar a mano, requisito del plan de validación.

## Errores semánticos verificados (15)
1. Identificador declarado dos veces en el mismo ámbito.
2. Recurso usado en una etapa no declarado.
3. Lo usado en una etapa no es un recurso.
4. Proceso destino de `generar` no declarado.
5. El destino de `generar` no es un proceso.
6. Identificador no declarado dentro de una expresión.
7. Identificador de tipo distinto a recurso dentro de una expresión.
8. División entre cero.
9. Capacidad de recurso ≤ 0.
10. Capacidad de recurso no entera.
11. Duración de etapa, intervalo de llegada o duración de simulación ≤ 0.
12. Proceso sin etapas.
13. Falta la sentencia `simular` / hay más de una.
14. `mostrar` sobre algo que no es una métrica.
15. Aridad incorrecta de la métrica (`ocupacion` sin recurso, otra métrica con argumento) u `ocupacion` sobre algo que no es recurso.

Advertencia: símbolo declarado y nunca usado.
