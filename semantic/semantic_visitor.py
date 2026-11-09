from .symbol_table import SymbolTable
from .errors import SemanticError
from gen.HospSimParser import HospSimParser
from gen.HospSimVisitor import HospSimVisitor

METRICAS_CON_ARGUMENTO = {'ocupacion'}  # el resto de métricas no reciben argumento


class SemanticVisitor(HospSimVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
        self.errors: list[SemanticError] = []
        self.simulaciones = 0

    def _error(self, msg: str, ctx):
        self.errors.append(SemanticError(msg, ctx.start.line))

    def _declare(self, name: str, type_: str, ctx):
        try:
            return self.symtab.declare(name, type_, ctx.start.line)
        except SemanticError as e:
            self.errors.append(e)
            return None

    # Evalúa una expresión constante; devuelve None si no se puede (ya se reportó el error).
    def _eval(self, e):
        if isinstance(e, HospSimParser.NumExprContext):
            return float(e.NUMBER().getText())
        if isinstance(e, (HospSimParser.TermExprContext, HospSimParser.FactorExprContext)):
            return self._eval(e.getChild(0))
        if isinstance(e, HospSimParser.ParenExprContext):
            return self._eval(e.expr())
        if isinstance(e, HospSimParser.IdExprContext):
            name = e.ID().getText()
            sym = self.symtab.lookup(name)
            if sym is None:
                self._error(f"El identificador '{name}' no está declarado", e)
                return None
            if sym.type_ != 'recurso':
                self._error(f"'{name}' es de tipo '{sym.type_}'; en una expresión solo se pueden usar recursos", e)
                return None
            sym.used = True
            return sym.value
        a, b = self._eval(e.getChild(0)), self._eval(e.getChild(2))  # AddExpr / MultExpr
        op = e.getChild(1).getText()
        if op == '/' and b == 0:
            self._error("División entre cero", e)
            return None
        if a is None or b is None:
            return None
        return {'+': a + b, '-': a - b, '*': a * b, '/': a / b if b else None}[op]

    def _check_positive(self, expr, what, ctx):
        val = self._eval(expr)
        if val is not None and val <= 0:
            self._error(f"{what} debe ser mayor a 0", ctx)

    # Programa: debe existir exactamente una sentencia 'simular'
    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        if self.simulaciones == 0:
            self.errors.append(SemanticError("Falta la sentencia 'simular durante ...'", (ctx.stop or ctx.start).line))  # programa vacío: stop es None

    # Declaración de Recurso: recurso medicos = 1;
    def visitResourceDecl(self, ctx):
        name = ctx.ID().getText()
        val = self._eval(ctx.expr())  # antes de declarar: 'recurso m = m + 1;' es un error
        if val is not None:
            if val <= 0:
                self._error(f"La capacidad del recurso '{name}' debe ser mayor a 0", ctx)
            elif abs(val - round(val)) > 1e-9:
                self._error(f"La capacidad del recurso '{name}' debe ser un número entero (se obtuvo {val:g})", ctx)
        sym = self._declare(name, 'recurso', ctx)
        if sym:
            sym.value = val

    # Declaración de Proceso: proceso atencion { ... }
    def visitProcessDecl(self, ctx):
        proc_name = ctx.ID().getText()
        self._declare(proc_name, 'proceso', ctx)
        if not ctx.stageStmt():
            self._error(f"El proceso '{proc_name}' no tiene etapas", ctx)

        self.symtab.enter_scope(proc_name)
        for st in ctx.stageStmt():
            self.visit(st)
        self.symtab.exit_scope()

    # Declaración de Etapa: etapa consulta usa medicos durante 15 minutos;
    def visitStageStmt(self, ctx):
        stage_name = ctx.ID(0).getText()
        resource_name = ctx.ID(1).getText()

        res_sym = self.symtab.lookup(resource_name)  # antes de declarar: 'etapa medicos usa medicos' es válido
        sym = self._declare(stage_name, 'etapa', ctx)
        if sym:
            sym.used = True  # una etapa vive dentro de su proceso
        self._check_positive(ctx.expr(), f"La duración de la etapa '{stage_name}'", ctx)

        if res_sym is None:
            self._error(f"Recurso '{resource_name}' utilizado en etapa '{stage_name}' no está declarado", ctx)
        elif res_sym.type_ != 'recurso':
            self._error(f"'{resource_name}' es de tipo '{res_sym.type_}'; una etapa solo puede usar un recurso", ctx)
        else:
            res_sym.used = True

    # Llegada de pacientes: generar pacientes cada 5 minutos hacia atencion;
    def visitArrivalStmt(self, ctx):
        proc_name = ctx.ID().getText()
        proc_sym = self.symtab.lookup(proc_name)
        self._check_positive(ctx.expr(), "El intervalo de llegada de pacientes", ctx)

        if proc_sym is None:
            self._error(f"El proceso de destino '{proc_name}' no ha sido declarado", ctx)
        elif proc_sym.type_ != 'proceso':
            self._error(f"'{proc_name}' no es un proceso válido de destino", ctx)
        else:
            proc_sym.used = True

    # Simulación: simular durante 8 horas;
    def visitSimulateStmt(self, ctx):
        self.simulaciones += 1
        if self.simulaciones > 1:
            self._error("Solo se permite una sentencia 'simular'", ctx)
        self._check_positive(ctx.expr(), "La duración de la simulación", ctx)

    # Sentencia Mostrar: mostrar pacientes_atendidos; ó mostrar ocupacion(medicos);
    def visitShowStmt(self, ctx):
        func_name = ctx.ID(0).getText()
        sym = self.symtab.lookup(func_name)

        if sym is None or sym.type_ != 'métrica':
            self._error(f"'{func_name}' no es una métrica (use pacientes_atendidos, espera_promedio u ocupacion)", ctx)
        elif func_name in METRICAS_CON_ARGUMENTO and not ctx.LPAREN():
            self._error(f"La métrica '{func_name}' requiere un recurso: {func_name}(recurso)", ctx)
        elif func_name not in METRICAS_CON_ARGUMENTO and ctx.LPAREN():
            self._error(f"La métrica '{func_name}' no recibe argumentos", ctx)
        elif ctx.LPAREN():
            param_name = ctx.ID(1).getText()
            param_sym = self.symtab.lookup(param_name)
            if param_sym is None:
                self._error(f"El recurso '{param_name}' no existe para la consulta de ocupación", ctx)
            elif param_sym.type_ != 'recurso':
                self._error(f"No se puede medir ocupación sobre '{param_name}' porque no es un recurso", ctx)
            else:
                param_sym.used = True
