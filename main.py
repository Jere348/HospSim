import sys
import argparse
from pathlib import Path
from backend.intermedio import emitir
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
    cli = argparse.ArgumentParser(description='Compilador y simulador HospSim')
    cli.add_argument('archivo', help='Programa fuente .txt')
    modos = cli.add_mutually_exclusive_group()
    modos.add_argument('--tokens', action='store_true', help='Mostrar solo tokens')
    modos.add_argument('--ir', action='store_true', help='Mostrar solo código intermedio')
    cli.add_argument('--guardar-ir', metavar='ARCHIVO', help='Guardar el código intermedio')
    opciones = cli.parse_args()
    solo_tokens = opciones.tokens
    if solo_tokens and opciones.guardar_ir:
        cli.error('--tokens no se puede combinar con --guardar-ir')
    args = [opciones.archivo]

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
        print('=== ADVERTENCIAS ===', file=sys.stderr if opciones.ir else sys.stdout)
        for w in warns:
            print(' ', w, file=sys.stderr if opciones.ir else sys.stdout)

    if semantico.errors:
        return 1
    if not opciones.ir:
        print('Análisis semántico: OK')

    # 3. Representación intermedia y ejecución (back end)
    modelo = ConstructorModelo().construir(tree)
    intermedio = emitir(modelo)
    if opciones.guardar_ir:
        try:
            Path(opciones.guardar_ir).write_text(intermedio, encoding='utf-8')
        except OSError as e:
            print(f'No se pudo guardar el código intermedio: {e}', file=sys.stderr)
            return 2
    if opciones.ir:
        print(intermedio, end='')
        return 0
    print('=== RESULTADOS ===')
    for linea in reporte(modelo, simular(modelo)):
        print(' ', linea)
    return 0


if __name__ == '__main__':
    sys.exit(main())
