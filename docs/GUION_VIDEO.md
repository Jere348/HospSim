# Guion del video de demostración (máx. 5 minutos)

Grabar la pantalla con la terminal en la carpeta del repositorio. Cada bloque indica qué decir y qué ejecutar.

| Tiempo | Qué se dice | Qué se muestra |
|---|---|---|
| 0:00 – 0:30 | Presentación del grupo y del problema: decidir capacidad (médicos, camas) sin herramientas accesibles de simulación. | Diapositivas 1–2. |
| 0:30 – 1:00 | Qué es HospSim: recursos, procesos con etapas, llegadas, simulación y métricas. | `cat tests/entrada_correcta.txt` |
| 1:00 – 1:30 | Fase léxica: secuencia de tokens y error léxico. | `python3 main.py --tokens tests/entrada_correcta.txt` y `python3 main.py tests/error_lexico.txt` |
| 1:30 – 2:15 | Fase sintáctica: gramática E/T/F, corrección de precedencia respecto al Hito 1, derivación más a la izquierda. | `python3 main.py tests/error_sintactico.txt` y `python3 tools/derivaciones.py \| head -40` |
| 2:15 – 3:15 | Fase semántica: tabla de símbolos por ámbitos y ejemplos de errores. | `python3 main.py tests/error_tipos.txt`, `tests/error_tiempos.txt`, `tests/error_metricas.txt` |
| 3:15 – 4:15 | Back end: representación intermedia y simulación; explicar a mano el resultado de un caso. | `python3 main.py tests/sim_dos_etapas.txt` y `python3 main.py tests/entrada_completa.txt` |
| 4:15 – 4:45 | Validación: todas las pruebas automáticas pasan. | `./run_tests.sh` |
| 4:45 – 5:00 | Próximo paso: generación de código LLVM en el Hito 3. | Diapositiva 11. |
