"""LogoVM lexer."""

import logging

from ply import lex
from ply.lex import TOKEN


class IllegalCharacter(Exception):
    """Excecao Lexer."""

    def __init__(self, char, line):
        """Erro de inicialização com char inválido detectado."""
        super().__init__(f"Illegal character: '{char}', at line {line}")


# Caracteres ignorados pelo lexer.
t_ignore = " \t\r" 

RESERVED = (
    ".CODE",
    ".DATA",
    ".INIT",
    ".START",
    "RET",
    "HALT",
    "CALL",
    "PUSH",
    "POP",
    "DUP",
    "LOAD",
    "STOR",
    "CMP",
    "JP",
    "JZ",
    "JNZ",
    "JMORE",
    "JLESS",
    "SKIPZ",
    "SKIPNZ",
    "DEF",
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "IDIV",
    "POW",
    "TRUNC",
    "RAND",
    "SET",
    "UNSET",
    "PUSHF",
    "MVTO",
    "SETPX",
    "AND",
    "OR",
    "XOR",
    "SHFTR",
    "SHFTL",
    "NOT",
)
NON_RESERVED = ("NUMBER", "STRING", "ID", "LABEL")
OPERATORS = {

    ":": "COLON",
    r"\"|\'": "QUOTE",
    r"\*\*": "POWER",
    "\+": "PLUS",
    "-": "MINUS",
    "\*": "TIMES",
    "/": "DIVIDE",
    "%": "MODULUS",
    "==": "EQUALTO",
    "=": "ASSIGN",
    ">": "GT",
    "<": "LT",
    ">=": "GE",
    "<=": "LE",
    r"\&\&": "AND",
    r"\|\|": "OR",
}

tokens = tuple(
    tuple(r[1:] if r.startswith(".") else r for r in RESERVED)
    + NON_RESERVED
    + tuple(OPERATORS.values())
)

globals().update({f"t_{v}": k for k, v in OPERATORS.items()})


@TOKEN(r"[.](CODE|DATA|START|INIT)")
def t_CODE(t):  # pylint: disable=invalid-name
    """Extrair diretivas de código."""
    logging.log(5, "DIRECTIVE: '%s'", t.value)
    t.value = t.value[1:].upper()
    t.type = t.value
    return t


@TOKEN(r"[_@a-zA-Z][_@.a-zA-Z0-9]*")
def t_ID(t):
    """Identificacao de uma extracao."""
    logging.log(5, "ID: '%s'", t.value)
    uppervalue = t.value.upper()
    if uppervalue in RESERVED:
        t.type = uppervalue
    else:
        t.type = "ID"
    return t


@TOKEN(r"[:][_@a-zA-Z][_@.a-zA-Z0-9]*")
def t_LABEL(t):
    """Extrair uma definição de rótulo."""
    logging.log(5, "LABEL: '%s'", t.value)
    t.value = t.value[1:]
    return t


@TOKEN(r"'[^']*'|\"[^\"]*\"")
def t_STRING(t):
    """Extrair uma string."""
    logging.log(5, "STRING: '%s'", t.value)
    t.value = t.value[1:-1]
    return t


@TOKEN(r"[+-]?\d+([.]\d*)?")
def t_NUMBER(t):
    """Extrair um numero."""
    logging.log(5, "NUMBER: '%s'", t.value)
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


@TOKEN(r"[#][^\n]*")
def t_COMMENT(token):
    logging.log(5, "Comment: '%s'", token.value)


@TOKEN(r"\n+")
def t_newline(token):
    """Contar novas linhas."""
    logging.log(5, "NL: %d", len(token.value))
    token.lexer.lineno += len(token.value) // 2


def t_error(tokenizer):
    """Reportar erro no lexer."""
    raise IllegalCharacter(tokenizer.value[0], tokenizer.lexer.lineno)


def lexer():
    """Criar novo objeto no lexer."""
    return lex.lex()