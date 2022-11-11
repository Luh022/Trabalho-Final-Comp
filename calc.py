tokens = (
    'NAME', 'NUMBER',
)

literals = ['=', '+', '-', '*', '/', '(', ')', '**', '%', 'sin', 'cos', 'log', 'exp', 'ln', 'sqrt', 'tan', 'asin', 'acos', 'atan']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('left', '**', '%'),
    ('left', 'sin', 'cos'),
    ('left', 'log', 'exp'),
    ('left', 'ln', 'sqrt'),
    ('left', 'tan', 'asin'),
    ('left', 'acos', 'atan'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression'**' expression
                  | expression '%' expression
                  | expression 'sin' expression
                  | expression 'cos' expression
                  | expression 'log' expression
                  | expression 'exp' expression
                  | expression 'ln' expression
                  | expression 'sqrt' expression
                  | expression 'tan' expression
                  | expression 'asin' expression
                  | expression 'acos' expression
                  | expression 'atan' expression '''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '**':
        p[0] = p[1] ** p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == 'sin':
        p[0] = p[1] sin p[3]
    elif p[2] == 'cos':
        p[0] = p[1] cos p[3]
    elif p[2] == 'log':
        p[0] = p[1] log p[3]
    elif p[2] == 'exp':
        p[0] = p[1] exp p[3]
    elif p[2] == 'ln':
        p[0] = p[1] ln p[3]
    elif p[2] == 'sqrt':
        p[0] = p[1] sqrt p[3]
    elif p[2] == 'tan':
        p[0] = p[1] tan p[3]
    elif p[2] == 'asin':
        p[0] = p[1] asin p[3]
    elif p[2] == 'acos':
        p[0] = p[1] acos p[3]
    elif p[2] == 'atan':
        p[0] = p[1] atan p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)