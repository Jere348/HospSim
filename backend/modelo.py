"""Representación intermedia: el árbol ya validado se convierte en un Modelo con todos
los valores evaluados y los tiempos normalizados a minutos."""
from dataclasses import dataclass, field
from gen.HospSimParser import HospSimParser
from gen.HospSimVisitor import HospSimVisitor

MINUTOS_POR_UNIDAD = {'minuto': 1, 'minutos': 1, 'hora': 60, 'horas': 60}


@dataclass
class Etapa:
    nombre: str
    recurso: str
    duracion: float  # minutos


@dataclass
class Llegada:
    proceso: str
    intervalo: float  # minutos


@dataclass
class Modelo:
    recursos: dict[str, int] = field(default_factory=dict)          # nombre -> capacidad
    procesos: dict[str, list[Etapa]] = field(default_factory=dict)  # nombre -> etapas en orden
    llegadas: list[Llegada] = field(default_factory=list)
    duracion: float = 0.0                                            # minutos
    consultas: list[tuple[str, str | None]] = field(default_factory=list)  # (métrica, argumento)


class ConstructorModelo(HospSimVisitor):
    """Solo se usa si el análisis semántico no reportó errores."""

    def __init__(self):
        self.modelo = Modelo()

    def construir(self, tree) -> Modelo:
        self.visit(tree)
        return self.modelo

    def _valor(self, e) -> float:
        if isinstance(e, HospSimParser.NumExprContext):
            return float(e.NUMBER().getText())
        if isinstance(e, HospSimParser.IdExprContext):
            return self.modelo.recursos[e.ID().getText()]
        if isinstance(e, HospSimParser.ParenExprContext):
            return self._valor(e.expr())
        a, b = self._valor(e.expr(0)), self._valor(e.expr(1))
        op = e.getChild(1).getText()
        return a + b if op == '+' else a - b if op == '-' else a * b if op == '*' else a / b

    def _minutos(self, expr, unidad) -> float:
        return self._valor(expr) * MINUTOS_POR_UNIDAD[unidad.getText()]

    def visitResourceDecl(self, ctx):
        self.modelo.recursos[ctx.ID().getText()] = int(self._valor(ctx.expr()))

    def visitProcessDecl(self, ctx):
        self.modelo.procesos[ctx.ID().getText()] = [
            Etapa(st.ID(0).getText(), st.ID(1).getText(), self._minutos(st.expr(), st.timeUnit()))
            for st in ctx.stageStmt()
        ]

    def visitArrivalStmt(self, ctx):
        self.modelo.llegadas.append(Llegada(ctx.ID().getText(), self._minutos(ctx.expr(), ctx.timeUnit())))

    def visitSimulateStmt(self, ctx):
        self.modelo.duracion = self._minutos(ctx.expr(), ctx.timeUnit())

    def visitShowStmt(self, ctx):
        self.modelo.consultas.append((ctx.ID(0).getText(), ctx.ID(1).getText() if ctx.LPAREN() else None))
