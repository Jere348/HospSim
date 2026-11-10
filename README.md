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

## Alcance del avance

Incluye análisis léxico, sintáctico y semántico, representación intermedia, emisión textual y simulador por eventos discretos. El alcance aprobado no requiere LLVM. El archivo `.ir` describe el modelo; la ejecución utiliza el mismo `Modelo` interno, no un lector del archivo `.ir`.

## Equipo

- Alvaro Jerry Rivera Calderón (u20231h075)
- Ericks Santiago Alarcon Castellanos (U202322704)
- Rodrigo Aaron Colonio Soto (u202323598)

Ciencias de la Computación · Sección 4889
Profesor: JOSE LUIS SONCCO ALVAREZ

## Inicio en Windows PowerShell

1. Extraer el ZIP completo.
2. Abrir la carpeta `HospSim` en VS Code y abrir una terminal PowerShell.
3. Ejecutar:

```powershell
python -m pip install -r requirements.txt
python main.py ejemplos/atencion.txt
python main.py --ir ejemplos/atencion.txt
python main.py --ir --guardar-ir salida.ir ejemplos/atencion.txt
python run_tests.py
```

El primer ejemplo produce 4 pacientes atendidos, espera promedio 15.00 minutos y ocupación 100.00 %. El último comando comprueba 20 casos originales y 11 regresiones. Se requiere Python 3.10 o posterior. No hace falta VirtualBox ni Java para ejecutar; `gen/` ya contiene los archivos ANTLR generados.

## Reglas de simulación

Cada recurso mantiene una cola FIFO común a los procesos que lo usan. Se procesan eventos cronológicamente. A igual tiempo, las finalizaciones preceden a las llegadas; después desempata el orden de inserción. Los que ya esperan conservan prioridad. Se generan llegadas antes del horizonte, y se incluyen finalizaciones exactamente en él. La espera promedio considera solo pacientes que terminan; la ocupación incluye trabajo parcial dentro del horizonte.
