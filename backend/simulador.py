"""Simulación determinista por eventos, con una cola FIFO por recurso.
Llegadas en [0, T); las finalizaciones en T sí cuentan. En empates se procesan
primero las finalizaciones y luego las llegadas, en orden de declaración.
La espera promedio corresponde solo a pacientes que completan el proceso.
"""
from collections import deque
from heapq import heappush, heappop
from itertools import count
from .modelo import Modelo


def simular(m: Modelo) -> dict:
    T = m.duracion
    libres = dict(m.recursos)
    colas = {r: deque() for r in m.recursos}
    ocupado = dict.fromkeys(m.recursos, 0.0)
    eventos, secuencia = [], count()
    atendidos, espera_total = 0, 0.0

    def programar(t, prioridad, tipo, datos):
        heappush(eventos, (t, prioridad, next(secuencia), tipo, datos))

    def atender(recurso, t):
        while libres[recurso] and colas[recurso]:
            proceso, indice, espera, llegada = colas[recurso].popleft()
            etapa = m.procesos[proceso][indice]
            libres[recurso] -= 1
            ocupado[recurso] += min(etapa.duracion, max(0.0, T - t))
            programar(t + etapa.duracion, 0, 'fin',
                      (proceso, indice, espera + t - llegada))

    def encolar(proceso, indice, espera, t):
        recurso = m.procesos[proceso][indice].recurso
        colas[recurso].append((proceso, indice, espera, t))
        atender(recurso, t)

    # Solo se agenda la siguiente llegada de cada flujo, evitando crear toda
    # la población por adelantado. El contador rompe empates de forma estable.
    for i, llegada in enumerate(m.llegadas):
        programar(0.0, 1, 'llegada', (i, 0))
    while eventos:
        t, _, _, tipo, datos = heappop(eventos)
        if t > T:
            break
        if tipo == 'llegada':
            if t >= T:
                continue
            flujo, k = datos
            llegada = m.llegadas[flujo]
            encolar(llegada.proceso, 0, 0.0, t)
            siguiente = (k + 1) * llegada.intervalo
            if siguiente < T:
                programar(siguiente, 1, 'llegada', (flujo, k + 1))
        else:
            proceso, indice, espera = datos
            recurso = m.procesos[proceso][indice].recurso
            libres[recurso] += 1
            # Los que ya esperan tienen prioridad frente a quien recién
            # termina una etapa y vuelve a pedir ese mismo recurso.
            atender(recurso, t)
            indice += 1
            if indice == len(m.procesos[proceso]):
                atendidos += 1
                espera_total += espera
            else:
                encolar(proceso, indice, espera, t)
    return {
        'pacientes_atendidos': atendidos,
        'espera_promedio': espera_total / atendidos if atendidos else 0.0,
        'ocupacion': {r: 100 * ocupado[r] / (c * T) for r, c in m.recursos.items()},
    }


def reporte(m: Modelo, res: dict) -> list[str]:
    lineas = []
    for metrica, arg in m.consultas:
        if metrica == 'ocupacion':
            lineas.append(f"ocupacion({arg}) = {res['ocupacion'][arg]:.2f} %")
        elif metrica == 'espera_promedio':
            lineas.append(f"espera_promedio = {res['espera_promedio']:.2f} minutos")
        else:
            lineas.append(f"pacientes_atendidos = {res['pacientes_atendidos']}")
    return lineas
