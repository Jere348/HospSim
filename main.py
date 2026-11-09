import sys
from antlr4 import CommonTokenStream, FileStream
from gen.HospSimLexer import HospSimLexer
from gen.HospSimParser import HospSimParser
from semantic.semantic_visitor import SemanticVisitor

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo_de_entrada>")
        return

    archivo = sys.argv[1]
    input_stream = FileStream(archivo, encoding='utf-8')
    lexer = HospSimLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HospSimParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print('Errores sintácticos encontrados. Abortando compilación.')
        return

    visitor = SemanticVisitor()
    visitor.visit(tree)

    if visitor.errors:
        print('\n=== ERRORES SEMÁNTICOS ===')
        for e in visitor.errors:
            print(' ', e)
    else:
        print('Análisis semántico: OK')

    warns = visitor.symtab.unused_warnings()
    if warns:
        print('\n=== ADVERTENCIAS ===')
        for w in warns:
            print(' ', w)

if __name__ == '__main__':
    main()
