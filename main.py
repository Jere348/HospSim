import sys
from antlr4 import CommonTokenStream, FileStream
from antlr4.error.ErrorListener import ErrorListener
from gen.HospSimLexer import HospSimLexer
from gen.HospSimParser import HospSimParser
from semantic.semantic_visitor import SemanticVisitor
from backend.modelo import ConstructorModelo
from backend.simulador import simular, reporte


class ColectorErrores(ErrorListener):
    def __init__(self, tipo: str):
        self.tipo = tipo
        self.errores: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errores.append(f"[Error {self.tipo}, línea {line}:{column}] {msg}")


def mostrar_tokens(lexer) -> None:
    """Modo --tokens: imprime la secuencia de tokens que produce el analizador léxico."""
    for tok in lexer.getAllTokens():
        print(f"{tok.line}:{tok.column:<4} {HospSimLexer.symbolicNames[tok.type]:<10} '{tok.text}'")


def main() -> int:
    solo_tokens = '--tokens' in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != '--tokens']
    if not args:
        print("Uso: python3 main.py [--tokens] <archivo_de_entrada>")
        return 2

    # 1. Análisis léxico y sintáctico
    try:
        entrada = FileStream(args[0], encoding='utf-8')
    except OSError as e:
        print(f"No se pudo leer '{args[0]}': {e.strerror}")
        return 2
    lexer = HospSimLexer(entrada)
    err_lex = ColectorErrores('Léxico')
    lexer.removeErrorListeners()
    lexer.addErrorListener(err_lex)
    if solo_tokens:
        mostrar_tokens(lexer)
        for e in err_lex.errores:
            print(' ', e)
        return 1 if err_lex.errores else 0

    parser = HospSimParser(CommonTokenStream(lexer))
    err_sin = ColectorErrores('Sintáctico')
    parser.removeErrorListeners()
    parser.addErrorListener(err_sin)
    tree = parser.program()

    if err_lex.errores or err_sin.errores:
        print('=== ERRORES LÉXICOS / SINTÁCTICOS ===')
        for e in err_lex.errores + err_sin.errores:
            print(' ', e)
        return 1

    # 2. Análisis semántico
    semantico = SemanticVisitor()
    semantico.visit(tree)

    if semantico.errors:
        print('=== ERRORES SEMÁNTICOS ===')
        for e in semantico.errors:
            print(' ', e)

    warns = semantico.symtab.unused_warnings()
    if warns:
        print('=== ADVERTENCIAS ===')
        for w in warns:
            print(' ', w)

    if semantico.errors:
        return 1
    print('Análisis semántico: OK')

    # 3. Representación intermedia y ejecución (back end)
    modelo = ConstructorModelo().construir(tree)
    print('=== RESULTADOS ===')
    for linea in reporte(modelo, simular(modelo)):
        print(' ', linea)
    return 0


if __name__ == '__main__':
    sys.exit(main())
