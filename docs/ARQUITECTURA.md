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
| `tools/derivaciones.py` | Genera derivaciones más a la izquierda (notación del curso) desde el parser real y verifica que usen solo producciones de la gramática. |

## Decisiones de diseño
- **Dos recorridos separados** (semántico y construcción del modelo): el back end nunca ve un árbol inválido, así no repite validaciones.
- **Representación intermedia propia**: desacopla el back end de ANTLR. En el Hito 3 se puede generar LLVM IR desde el mismo `Modelo` sin tocar el front end; el simulador en Python queda como oráculo para validar el código generado.
- **Simulación determinista** (sin aleatoriedad): las salidas son reproducibles y se pueden verificar a mano, requisito del plan de validación.

## Errores semánticos verificados (21)
1. Identificador duplicado en el mismo ámbito — `recurso m = 2;`
2. Recurso no declarado en una etapa — `etapa e usa enfermeros durante 5 minutos;`
3. Lo usado en una etapa no es un recurso — `etapa x usa p durante 5 minutos;`
4. Proceso destino no declarado — `... hacia fantasma;`
5. El destino de una llegada no es un proceso — `... hacia m;`
6. Identificador no declarado en una expresión — `recurso n = x + 1;`
7. Identificador que no es recurso en una expresión — `recurso n = p * 2;`
8. División entre cero — `recurso n = 4 / (2 - 2);`
9. Capacidad menor o igual a 0 — `recurso n = 2 - 5;`
10. Capacidad no entera — `recurso n = 3 / 2;`
11. Duración de etapa menor o igual a 0 — `etapa e usa m durante 0 minutos;`
12. Intervalo de llegada menor o igual a 0 — `generar pacientes cada 0 minutos hacia p;`
13. Duración de simulación menor o igual a 0 — `simular durante 0 horas;`
14. Proceso sin etapas — `proceso q { }`
15. Falta la sentencia simular — `(programa sin simular)`
16. Más de una sentencia simular — `simular ... (segunda vez)`
17. mostrar sobre algo que no es métrica — `mostrar m;`
18. ocupacion sin recurso — `mostrar ocupacion;`
19. Métrica que no recibe argumentos — `mostrar espera_promedio(m);`
20. ocupacion sobre algo que no es recurso — `mostrar ocupacion(p);`
21. ocupacion sobre un recurso inexistente — `mostrar ocupacion(rayos_x);`

Advertencia: recurso o proceso declarado y nunca usado.
