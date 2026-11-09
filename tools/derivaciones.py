"""Genera derivaciones más a la izquierda (⇒lm) en la notación del curso a partir del árbol
que construye el parser de ANTLR. Así las derivaciones del informe salen del parser real.

Uso:  python3 tools/derivaciones.py            -> imprime todas las derivaciones del informe
      python3 tools/derivaciones.py --json     -> las mismas en JSON (para generar el informe)
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import TerminalNode
from gen.HospSimLexer import HospSimLexer
from gen.HospSimParser import HospSimParser

P = HospSimParser

# Nombre del no-terminal (notación del curso) para cada contexto de ANTLR
NOMBRES = {
    P.StatementContext: 'sentencia', P.ResourceDeclContext: 'decl_recurso',
    P.ProcessDeclContext: 'decl_proceso', P.StageStmtContext: 'decl_etapa',
    P.ArrivalStmtContext: 'sent_llegada', P.SimulateStmtContext: 'sent_simular',
    P.ShowStmtContext: 'sent_mostrar', P.TimeUnitContext: 'unidad',
    P.AddExprContext: 'E', P.TermExprContext: 'E',
    P.MultExprContext: 'T', P.FactorExprContext: 'T',
    P.NumExprContext: 'F', P.IdExprContext: 'F', P.ParenExprContext: 'F',
}


def terminal(t):
    tipo = t.getSymbol().type
    if tipo == P.ID:
        return 'id'
    if tipo == P.NUMBER:
        return 'num'
    return t.getText()


def lista(nombre, elementos):
    """X* de ANTLR  ->  lista → elem lista | ε"""
    if not elementos:
        return (nombre, [])
    return (nombre, [convertir(elementos[0]), lista(nombre, elementos[1:])])


def convertir(ctx):
    """Árbol de ANTLR -> (no_terminal, [hijos]) con hojas terminales como str."""
    if isinstance(ctx, P.ProgramContext):
        return ('programa', [lista('sentencias', ctx.statement())])
    if isinstance(ctx, P.ProcessDeclContext):
        hijos = [terminal(ctx.PROCESO()), terminal(ctx.ID()), '{', lista('etapas', ctx.stageStmt()), '}']
        return ('decl_proceso', hijos)
    hijos = [terminal(c) if isinstance(c, TerminalNode) else convertir(c) for c in ctx.getChildren()]
    return (NOMBRES[type(ctx)], [h for h in hijos if h != '<EOF>'])


def derivar(arbol):
    """Devuelve los pasos [(producción, forma_sentencial)] de la derivación más a la izquierda."""
    forma = [arbol]
    pasos = []
    while True:
        i = next((k for k, s in enumerate(forma) if isinstance(s, tuple)), None)
        if i is None:
            return pasos
        nt, hijos = forma[i]
        cuerpo = ' '.join(h if isinstance(h, str) else h[0] for h in hijos) or 'ε'
        forma = forma[:i] + hijos + forma[i + 1:]
        pasos.append((f'{nt} → {cuerpo}', [s if isinstance(s, str) else s[0] for s in forma]))


def parsear(texto, regla='program'):
    lexer = HospSimLexer(InputStream(texto))
    parser = HospSimParser(CommonTokenStream(lexer))
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    arbol = getattr(parser, regla)()
    assert parser.getNumberOfSyntaxErrors() == 0, f'Error sintáctico en el ejemplo: {texto!r}'
    return arbol


def derivacion(texto, inicio):
    """inicio: no-terminal desde el que se deriva ('programa', 'decl_recurso', 'E', ...)."""
    prog = parsear(texto)
    if inicio == 'programa':
        arbol = convertir(prog)
    elif inicio == 'E':
        arbol = convertir(prog.statement(0).resourceDecl().expr())
    else:
        arbol = convertir(prog.statement(0).getChild(0))
    assert arbol[0] == inicio, (arbol[0], inicio)
    return [{'produccion': p, 'forma': f} for p, f in derivar(arbol)]


# Ejemplos del informe: 4 por gramática
EJEMPLOS = {
    'programa': [
        'simular durante 8 horas;',
        'recurso medicos = 2;\nsimular durante 1 hora;',
        'recurso camas = 10;\nmostrar ocupacion(camas);',
        'proceso p { }\ngenerar pacientes cada 5 minutos hacia p;',
    ],
    'decl_recurso': [
        'recurso medicos = 3;',
        'recurso camas = 2 * 10;',
        'recurso sillas = medicos + 4;',
        'recurso boxes = (2 + 3) * 2;',
    ],
    'decl_proceso': [
        'proceso vacio { }',
        'proceso atencion { etapa consulta usa medicos durante 15 minutos; }',
        'proceso emergencia { etapa triaje usa enfermeros durante 5 minutos; etapa reanimacion usa medicos durante 1 hora; }',
        'proceso alta { etapa tramite usa admision durante 10 / 2 minutos; }',
    ],
    'sent_llegada': [
        'generar pacientes cada 5 minutos hacia atencion;',
        'generar pacientes cada 1 hora hacia emergencia;',
        'generar pacientes cada 2 * 3 minutos hacia triaje;',
        'generar pacientes cada 0.5 horas hacia consulta_externa;',
    ],
    'sent_simular': [
        'simular durante 8 horas;',
        'simular durante 90 minutos;',
        'simular durante 1 hora;',
        'simular durante 24 * 7 horas;',
    ],
    'sent_mostrar': [
        'mostrar pacientes_atendidos;',
        'mostrar espera_promedio;',
        'mostrar ocupacion(medicos);',
        'mostrar ocupacion(camas);',
    ],
    'E': [
        'recurso x = 2 + 3 * 4;',
        'recurso x = (2 + 3) * 4;',
        'recurso x = 20 - 5 - 3;',
        'recurso x = medicos / 2;',
    ],
}


# Gramática en notación del curso (la misma que aparece en el informe). Símbolo inicial: programa.
GRAMATICA = [
    ('programa', ['sentencias']),
    ('sentencias', ['sentencia sentencias', 'ε']),
    ('sentencia', ['decl_recurso', 'decl_proceso', 'sent_llegada', 'sent_simular', 'sent_mostrar']),
    ('decl_recurso', ['recurso id = E ;']),
    ('decl_proceso', ['proceso id { etapas }']),
    ('etapas', ['decl_etapa etapas', 'ε']),
    ('decl_etapa', ['etapa id usa id durante E unidad ;']),
    ('sent_llegada', ['generar pacientes cada E unidad hacia id ;']),
    ('sent_simular', ['simular durante E unidad ;']),
    ('sent_mostrar', ['mostrar id ;', 'mostrar id ( id ) ;']),
    ('unidad', ['minuto', 'minutos', 'hora', 'horas']),
    ('E', ['E + T', 'E - T', 'T']),
    ('T', ['T * F', 'T / F', 'F']),
    ('F', ['( E )', 'num', 'id']),
]
NO_TERMINALES = {cabeza for cabeza, _ in GRAMATICA}
PRODUCCIONES = {f'{cabeza} → {cuerpo}' for cabeza, cuerpos in GRAMATICA for cuerpo in cuerpos}


def todas():
    datos = _todas()
    for ejemplos in datos.values():  # autochequeo: toda producción usada existe en GRAMATICA
        for ej in ejemplos:
            for paso in ej['pasos']:
                assert paso['produccion'] in PRODUCCIONES, paso['produccion']
    return datos


def _todas():
    return {inicio: [{'entrada': t.replace('recurso x = ', '').rstrip(';') if inicio == 'E' else t,
                      'pasos': derivacion(t, inicio)} for t in textos]
            for inicio, textos in EJEMPLOS.items()}


if __name__ == '__main__':
    datos = todas()
    if '--json' in sys.argv:
        print(json.dumps(datos, ensure_ascii=False, indent=1))
    else:
        for inicio, ejemplos in datos.items():
            for ej in ejemplos:
                print(f"\n# {inicio}:  {ej['entrada']!r}")
                print(f"  {inicio}")
                for paso in ej['pasos']:
                    print(f"  ⇒lm {' '.join(paso['forma']):<70}   [{paso['produccion']}]")
