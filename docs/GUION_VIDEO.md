# Guion del video de demostración (máx. 5 minutos)

Grabar la pantalla con la terminal en la carpeta del repositorio. Cada bloque indica qué decir y qué ejecutar.

| Tiempo | Qué se dice | Qué se muestra |
|---|---|---|
| 0:00 – 0:30 | Presentación del grupo y del problema: decidir capacidad (médicos, camas) sin herramientas accesibles de simulación. | Diapositivas 1–2. |
| 0:30 – 1:00 | Qué es HospSim: recursos, procesos con etapas, llegadas, simulación y métricas. | `Get-Content tests/entrada_correcta.txt` |
| 1:00 – 1:30 | Fase léxica: secuencia de tokens y error léxico. | `python main.py --tokens tests/entrada_correcta.txt` y `python main.py tests/error_lexico.txt` |
| 1:30 – 2:15 | Fase sintáctica: gramática E/T/F, corrección de precedencia respecto al Hito 1, derivación más a la izquierda. | `python main.py tests/error_sintactico.txt` y `python tools/derivaciones.py` |
| 2:15 – 3:15 | Fase semántica: tabla de símbolos por ámbitos y ejemplos de errores. | `python main.py tests/error_tipos.txt`, `tests/error_tiempos.txt`, `tests/error_metricas.txt` |
| 3:15 – 4:15 | Back end: representación intermedia y simulación; explicar a mano el resultado de un caso. | `python main.py tests/sim_dos_etapas.txt` y `python main.py tests/entrada_completa.txt` |
| 4:15 – 4:45 | Validación: todas las pruebas automáticas pasan. | `python run_tests.py` |
| 4:45 – 5:00 | Próximo paso: ampliar validación y preparar la entrega final con código intermedio. | Diapositiva 11. |

Para mostrar la compilación: `python main.py --ir ejemplos/atencion.txt`. Para ejecutar el mismo ejemplo: `python main.py ejemplos/atencion.txt`.
