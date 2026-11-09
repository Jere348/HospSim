from .errors import SemanticError

class Symbol:
    def __init__(self, name: str, type_: str, scope: str, line: int, value: float = None):
        self.name = name
        self.type_ = type_  # 'recurso', 'proceso', 'etapa', 'métrica'
        self.scope = scope
        self.line = line
        self.used = False
        self.value = value

    def __repr__(self):
        return f"Symbol({self.name}: {self.type_} @ {self.scope}, line {self.line})"


class SymbolTable:
    def __init__(self):
        self._table: dict[str, dict[str, Symbol]] = {}
        self._scope_stack: list[str] = ['global']
        
        self.enter_scope('global')
        for metric in ['pacientes_atendidos', 'espera_promedio', 'ocupacion']:
            sym = Symbol(metric, 'métrica', 'global', 0)
            sym.used = True
            self._table['global'][metric] = sym

    @property
    def current_scope(self) -> str:
        return self._scope_stack[-1]

    def enter_scope(self, name: str):
        self._scope_stack.append(name)
        self._table.setdefault(name, {})

    def exit_scope(self):
        self._scope_stack.pop()

    def declare(self, name: str, type_: str, line: int) -> Symbol:
        scope = self.current_scope
        if name in self._table.setdefault(scope, {}):
            raise SemanticError(f"El identificador '{name}' ya ha sido declarado en el ámbito '{scope}'.", line)
        sym = Symbol(name, type_, scope, line)
        self._table[scope][name] = sym
        return sym

    def lookup(self, name: str) -> Symbol | None:
        for scope in reversed(self._scope_stack):
            if name in self._table.get(scope, {}):
                return self._table[scope][name]
        return None

    def unused_warnings(self) -> list[str]:
        warns = []
        for scope_syms in self._table.values():
            for sym in scope_syms.values():
                if not sym.used and sym.type_ != 'métrica':
                    warns.append(f"ADVERTENCIA: '{sym.name}' ({sym.type_}) declarada en línea {sym.line} no se utiliza.")
        return warns
