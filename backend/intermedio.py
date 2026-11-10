"""Emisión textual del Modelo validado. Tiempos expresados en minutos.
La salida describe recursos, flujos y las operaciones de cada proceso.
El simulador ejecuta el mismo Modelo; no vuelve a analizar el archivo .ir.
"""
from .modelo import Modelo


def emitir(m: Modelo) -> str:
    lineas = ['; HospSim IR 1 - tiempos en minutos']
    for nombre, capacidad in m.recursos.items():
        lineas += [f'RESOURCE {nombre} {capacidad}', f'QUEUE {nombre} FIFO']
    for nombre in m.procesos:
        lineas.append(f'PROCESS {nombre} {nombre}_inicio')
    for llegada in m.llegadas:
        lineas.append(f'ARRIVALS {llegada.proceso} EVERY {llegada.intervalo:g} FROM 0')
    lineas.append(f'RUN_UNTIL {m.duracion:g}')
    for metrica, arg in m.consultas:
        lineas.append(f'REPORT {metrica}' + (f' {arg}' if arg else ''))
    lineas.append('HALT')
    for nombre, etapas in m.procesos.items():
        lineas.append(f'{nombre}_inicio:')
        for etapa in etapas:
            lineas += [f'  ; etapa {etapa.nombre}', f'  ACQUIRE {etapa.recurso}',
                       f'  DELAY {etapa.duracion:g}', f'  RELEASE {etapa.recurso}']
        lineas.append('  COMPLETE')
    return '\n'.join(lineas) + '\n'
