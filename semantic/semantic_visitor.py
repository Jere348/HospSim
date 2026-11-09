from .symbol_table import SymbolTable
from .errors import SemanticError
from gen.HospSimParser import HospSimParser
from gen.HospSimVisitor import HospSimVisitor

class SemanticVisitor(HospSimVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
        self.errors: list[SemanticError] = []

    def _error(self, msg: str, ctx):
        e = SemanticError(msg, ctx.start.line)
        self.errors.append(e)
        return 'error'

    # Evalúa una expresión; devuelve None si no es constante. Reporta ids no declarados y división entre 0.
    def _eval(self, e):
        if isinstance(e, HospSimParser.NumExprContext):
            return float(e.NUMBER().getText())
        if isinstance(e, HospSimParser.ParenExprContext):
            return self._eval(e.expr())
        if isinstance(e, HospSimParser.IdExprContext):
            name = e.ID().getText()
            sym = self.symtab.lookup(name)
            if sym is None:
                self._error(f"El identificador '{name}' no está declarado", e)
            else:
                sym.used = True
            return None
        a, b = self._eval(e.expr(0)), self._eval(e.expr(1))
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

    # Declaración de Recurso: recurso medicos = 1;
    def visitResourceDecl(self, ctx):
        name = ctx.ID().getText()
        line = ctx.start.line
        try:
            self.symtab.declare(name, 'recurso', line)
        except SemanticError as e:
            self.errors.append(e)

        self._check_positive(ctx.expr(), f"La capacidad del recurso '{name}'", ctx)

    # Declaración de Proceso: proceso atencion { ... }
    def visitProcessDecl(self, ctx):
        proc_name = ctx.ID().getText()
        line = ctx.start.line
        try:
            self.symtab.declare(proc_name, 'proceso', line)
        except SemanticError as e:
            self.errors.append(e)

        self.symtab.enter_scope(proc_name)
        for st in ctx.stageStmt():
            self.visit(st)
        self.symtab.exit_scope()

    # Declaración de Etapa: etapa consulta usa medicos durante 15 minutos;
    def visitStageStmt(self, ctx):
        stage_name = ctx.ID(0).getText()
        resource_name = ctx.ID(1).getText()
        line = ctx.start.line

        try:
            self.symtab.declare(stage_name, 'etapa', line).used = True  # una etapa vive dentro de su proceso
        except SemanticError as e:
            self.errors.append(e)

        self._check_positive(ctx.expr(), f"La duración de la etapa '{stage_name}'", ctx)

        res_sym = self.symtab.lookup(resource_name)
        if res_sym is None:
            self._error(f"Recurso '{resource_name}' utilizado en etapa '{stage_name}' no está declarado", ctx)
        elif res_sym.type_ != 'recurso':
            self._error(f"'{resource_name}' debe ser un 'recurso' válido", ctx)
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
        self._check_positive(ctx.expr(), "La duración de la simulación", ctx)

    # Sentencia Mostrar: mostrar pacientes_atendidos; ó mostrar ocupacion(medicos);
    def visitShowStmt(self, ctx):
        func_name = ctx.ID(0).getText()
        sym = self.symtab.lookup(func_name)

        if sym is None:
            self._error(f"La métrica o entidad '{func_name}' no existe", ctx)
        elif ctx.LPAREN():
            param_name = ctx.ID(1).getText()
            param_sym = self.symtab.lookup(param_name)
            if param_sym is None:
                self._error(f"El recurso '{param_name}' no existe para la consulta de ocupación", ctx)
            elif param_sym.type_ != 'recurso':
                self._error(f"No se puede medir ocupación sobre '{param_name}' porque no es un recurso", ctx)
            else:
                param_sym.used = True
