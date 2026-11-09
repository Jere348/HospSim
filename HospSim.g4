grammar HospSim;

// --- SINTAXIS ---

program
    : (statement)* EOF
    ;

statement
    : resourceDecl
    | processDecl
    | arrivalStmt
    | simulateStmt
    | showStmt
    ;

resourceDecl
    : RECURSO ID ASSIGN expr SEMI
    ;

processDecl
    : PROCESO ID LBRACE (stageStmt)* RBRACE
    ;

stageStmt
    : ETAPA ID USA ID DURANTE expr timeUnit SEMI
    ;

arrivalStmt
    : GENERAR PACIENTES CADA expr timeUnit HACIA ID SEMI
    ;

simulateStmt
    : SIMULAR DURANTE expr timeUnit SEMI
    ;

showStmt
    : MOSTRAR ID SEMI
    | MOSTRAR ID LPAREN ID RPAREN SEMI
    ;

expr
    : expr (PLUS | MINUS) expr     # AddExpr
    | expr (MULT | DIV) expr       # MultExpr
    | NUMBER                       # NumExpr
    | ID                           # IdExpr
    | LPAREN expr RPAREN           # ParenExpr
    ;

timeUnit
    : MINUTOS | MINUTO | HORAS | HORA
    ;

// --- LÉXICO ---

RECURSO   : 'recurso' ;
PROCESO   : 'proceso' ;
ETAPA     : 'etapa' ;
USA       : 'usa' ;
DURANTE   : 'durante' ;
GENERAR   : 'generar' ;
PACIENTES : 'pacientes' ;
CADA      : 'cada' ;
HACIA     : 'hacia' ;
SIMULAR   : 'simular' ;
MOSTRAR   : 'mostrar' ;

MINUTOS   : 'minutos' ;
MINUTO    : 'minuto' ;
HORAS     : 'horas' ;
HORA      : 'hora' ;

ASSIGN    : '=' ;
SEMI      : ';' ;
LBRACE    : '{' ;
RBRACE    : '}' ;
LPAREN    : '(' ;
RPAREN    : ')' ;

PLUS      : '+' ;
MINUS     : '-' ;
MULT      : '*' ;
DIV       : '/' ;

ID        : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER    : [0-9]+ ('.' [0-9]+)? ;

WS        : [ \t\r\n]+ -> skip ;
COMMENT   : '//' ~[\r\n]* -> skip ;
