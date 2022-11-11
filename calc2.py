import ply.lex as lex
import ply.yacc as yacc
import os


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        # print self.debugfile

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile)

    def run(self):
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s:
                continue
            yacc.parse(s)


class Calc(Parser):

    tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
    )

    # Tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EXP = r'\*\*'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_MODULO = r'%'
    t_OR = r'\|'
    t_AND = r'&'
    t_NOT = r'~'
    t_XOR = r'\^'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'
    t_LOR = r'\|\|'
    t_LAND = r'&&'
    t_LNOT = r'!'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_EQ = r'=='
    t_NE = r'!='
    t_potency = r'**'
    t_sin = r'sin'
    t_cos = r'cos'
    t_log = r'log'
    t_exp = r'exp'
    t_ln = r'ln'
    t_sqrt = r'sqrt'
    t_tan = r'tan'
    t_asin = r'asin'
    t_acos = r'acos'
    t_atan = r'atan'

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('left', 'Modulo', 'OR'),
        ('left', 'AND', 'NOT'),
        ('left', 'XOR'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('left', 'LOR', 'LAND'),
        ('left', 'LNOT', 'LT'),
        ('left', 'GT', 'LE'),
        ('left', 'GE', 'EQ'),
        ('left', 'NE', 'potency'),
        ('left', 'sin', 'cos'),
        ('left', 'ln', 'sqrt'),
        ('left', 'tan', 'asin'),
        ('left', 'acos', 'atan')
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        'statement : NAME EQUALS expression'
        self.names[p[1]] = p[3]

    def p_statement_expr(self, p):
        'statement : expression'
        print(p[1])

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
                  | expression potency expression
                  | expression sin expression
                  | expression cos expression
                  | expression tan expression
                  | expression asin expression
                  | expression acos expression
                  | expression atan expression
        """
        # print [repr(p[i]) for i in range(0,4)]
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

    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : NAME'
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc()
    calc.run()