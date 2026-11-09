"""Back end (Hito 2): ejecuta el Modelo con una simulación determinista.
Reglas:
  - Cada 'generar pacientes cada k' crea pacientes en t = 0, k, 2k, ... mientras t < duración.
  - Un paciente recorre las etapas de su proceso en orden; en cada etapa toma el servidor
    del recurso que se libere primero (cola FIFO por orden de llegada al sistema).
  - Un paciente cuenta como atendido si termina todas sus etapas dentro de la duración.
"""
from .modelo import Modelo


def simular(m: Modelo) -> dict:
    T = m.duracion
    libre = {r: [0.0] * c for r, c in m.recursos.items()}  # instante en que se libera cada servidor
    ocupado = dict.fromkeys(m.recursos, 0.0)                # minutos de uso dentro de [0, T]

    pacientes = sorted(
        (k * ll.intervalo, i, ll.proceso)
        for i, ll in enumerate(m.llegadas)
        for k in range(int(T // ll.intervalo) + 1)
        if k * ll.intervalo < T
    )

    atendidos, espera_total = 0, 0.0
    # shortcut: los pacientes se atienden de principio a fin en orden de llegada al sistema; un
    # paciente posterior no adelanta a uno anterior en una etapa intermedia. Para colas por etapa
    # haría falta una simulación por eventos (cola de prioridad), en el Hito 3 si se necesita.
    for t, _, proceso in pacientes:
        espera = 0.0
        for etapa in m.procesos[proceso]:
            servidores = libre[etapa.recurso]
            j = min(range(len(servidores)), key=servidores.__getitem__)
            inicio = max(t, servidores[j])
            fin = inicio + etapa.duracion
            servidores[j] = fin
            espera += inicio - t
            ocupado[etapa.recurso] += max(0.0, min(fin, T) - min(inicio, T))
            t = fin
        if t <= T:
            atendidos += 1
            espera_total += espera

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
