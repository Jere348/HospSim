# Plan de validación del compilador HospSim

## Objetivo
Comprobar que cada fase acepta los programas válidos, rechaza los inválidos con el mensaje y la
línea correctos, y que el back end produce métricas correctas.

## Método
Pruebas de caja negra con salida esperada (*golden files*):

- Cada caso es un programa `tests/<caso>.txt` con su salida esperada `tests/esperado/<caso>.out`.
- `./run_tests.sh` ejecuta `main.py` sobre cada caso y compara con `diff`; termina con código ≠ 0 si algo falla.
- `./run_tests.sh -u` regenera las salidas esperadas; **toda salida nueva se revisa a mano antes de
  confirmarla** (si no, la prueba solo repetiría lo que el compilador ya hace).

## Casos

| Fase | Casos | Qué se verifica |
|---|---|---|
| Léxica | `error_lexico` | Carácter inválido (`@`) reportado con línea y columna. |
| Sintáctica | `error_sintactico` | `;` faltante e identificador faltante. |
| Semántica | `error_duplicado`, `error_capacidad`, `error_capacidad_entera`, `error_expr`, `error_tiempos`, `error_tipos`, `error_tipo_expresion`, `error_estructura`, `error_simular_doble`, `error_metricas`, `error_vacio`, `entrada_error` | Errores semánticos y la advertencia de símbolos sin usar (los 21 mensajes están en el informe, sección 6.2). |
| Gramática | `sim_precedencia`, `sim_asociatividad` | `2 + 3 * 4 = 14`, `(2 + 3) * 2 = 10`, `20 - 5 - 3 = 12`, `24 / 4 / 2 = 3`. |
| Back end | `entrada_correcta`, `sim_dos_servidores`, `sim_dos_etapas`, `sim_precedencia`, `sim_asociatividad`, `entrada_completa` | Métricas calculadas a mano (abajo). |

## Resultados esperados calculados a mano

**`entrada_correcta`** — 1 médico, consulta 15 min, llegada cada 5 min, 60 min.
Pacientes en 0, 5, …, 55. Atenciones 0–15, 15–30, 30–45, 45–60, 60–75 (fuera).
Atendidos 4; espera (0+10+20+30)/4 = **15.00**; médico ocupado 60/60 = **100.00 %**.

**`sim_dos_servidores`** — igual con 2 médicos.
Servidor A: 0–15, 15–30, 30–45, 45–60; servidor B: 5–20, 20–35, 35–50, 50–65.
Atendidos 7 (el de 50–65 termina tarde); espera (0+0+5+5+10+10+15)/7 = **6.43**;
ocupación (60+55)/120 = **95.83 %**.

**`sim_dos_etapas`** — triaje 5 min (1 enfermero) y consulta 12 min (1 médico), llegada cada 10 min.
Consultas 5–17, 17–29, 29–41, 41–53, 53–65 (fuera). Esperas 0, 2, 4, 6 → **3.00**; atendidos **4**;
enfermero 6×5/60 = **50.00 %**; médico (48+7)/60 = **91.67 %**.

**`sim_precedencia`** — 14 camas, internamiento 60 min, llegada cada 30 min, 120 min.
Fines 60, 90, 120, 150 → atendidos **3**; ocupación (60+60+60+30)/(14×120) = **12.50 %**
(con la precedencia errónea serían 20 camas y 8.75 %); sillas sin uso **0.00 %**.

**`entrada_completa`** — 2 médicos (triaje 10 min), 5 camas (60 min), llegada cada 5 min, 480 min.
Triaje sin espera; en camas el paciente *i* = 5q + r empieza en 5r + 10 + 60q y espera 35q.
Terminan a tiempo q = 0…6 → **35** atendidos; espera 35·(0+…+6)·5/35 = **105.00**;
médicos 955/960 = **99.48 %**; camas Σ(470 − 5r)/2400 = **95.83 %**.

**`sim_asociatividad`** — `20 - 5 - 3` = 12 médicos, `24 / 4 / 2` = 3 camas, `0.1 * 30` = 3 sillas (no es error de
capacidad no entera). Llegada cada hora, 180 min; etapas de 60 min (médicos) y 30 min (camas).
Fines 90, 150, 210 → atendidos **2**, espera **0.00**; médicos 180/2160 = **8.33 %**; camas 60/540 = **11.11 %**.

## Criterio de aceptación
Todos los casos en `OK` (`0 prueba(s) fallida(s)`). Todo error nuevo o cambio de gramática se
acompaña de al menos un caso nuevo.

## Regresiones y ejecución en Windows

Ejecutar `python run_tests.py`. Comprueba salida y código de retorno de los 20 casos originales y ejecuta 11 pruebas adicionales en `tests/test_regresiones.py`.

- Recurso compartido: proceso largo utiliza a durante 100 min y luego b durante 1 min; proceso corto utiliza b durante 1 min. Ambos llegan en t=0. En 10 min: 1 atendido, ocupación de b 10 %.
- FIFO: largo alcanza b en t=2 y corto lo ocupa de 0 a 5. Largo termina en 6: 2 atendidos, espera promedio 1.5 min y ocupación de b 60 % en 10 min.
- Reentrada al mismo recurso: dos pacientes y dos etapas de 2 min. Finalizan en 6 y 8: espera promedio 3 min y ocupación 100 %.
- Finalización exactamente en el horizonte incluida; llegada exactamente en el horizonte excluida.
- Ausencia de llegadas: métricas cero.
- Capacidad 0.0000000001 rechazada; 0.1 * 30 aceptada como 3.
- Nombre de proceso `global` permitido sin mezclar ámbitos.
- Número fuera del rango finito rechazado sin excepción de Python.
- Código intermedio idéntico al ejemplo calculado, en pantalla y en archivo.
- Programa inválido: no se emiten instrucciones intermedias.
