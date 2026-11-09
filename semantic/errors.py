class SemanticError(Exception):
    def __init__(self, message: str, line: int = 0):
        super().__init__(f'[Error Semántico, línea {line}] {message}')
        self.line = line
