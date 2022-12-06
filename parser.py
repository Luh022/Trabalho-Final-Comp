"""Implementando um interpretador para o Logo VM."""

import logging

from ply import yacc

from logoasm import lexer
from logoasm.symtable import (
    add_symbol,
    set_symbol,
    get_symbol,
    get_symbols_by_class,
    increment_symbol_usage,
)

from logovm.errors import UndefinedReference


parser_error = False 


class ParserObject(object):
    """Fornece um objeto com atributos arbitrários."""

    def __init__(self, *_, **kwargs):
        """Inicializar objeto com atributos padrão."""
        for k, v in kwargs.items():
            setattr(self, k, v)


def p_empty(_p):
    """empty :"""


def p_program(p):
    """program : start init data code"""
    p[0] = p[1] if not parser_error else None


def p_start(p):
    """start : START ID"""
    logging.log(5, "START: %s", p[2])
    add_symbol(p[2], "FUNC", usage=1)
    p[0] = p[2]


def p_init(p):
    """
    init : INIT NUMBER NUMBER NUMBER NUMBER
         | empty
    """
    if p[1] is not None:
        logging.log(5, "INIT parsed.")
        nums = []
        for i in range(2, len(p)):
            if isinstance(p[i], int):
                nums.append(p[i])
            else:
                raise Exception("INIT: InvalidType: Required INT got FLOAT.")

        add_symbol(
            "__turtle",
            "OBJECT",
            lineno=p.lineno(4),
            value=ParserObject(x=nums[0], y=nums[1], draw=True),
        )
        add_symbol(
            "__window",
            "OBJECT",
            lineno=p.lineno(2),
            value=ParserObject(w=nums[2], h=nums[3]),
        )


def p_data(_p):
    """
    data : DATA var_decl data_list
         | empty
    """


def p_var_decl(p):
    """var_decl : ID value"""
    logging.log(5, "VAR: %s", p[1])
    add_symbol(
        p[1], "VAR", lineno=p.lineno(1), value=p[2].value, var_type=p[2].type
    )


def p_data_list(_p):
    """
    data_list : var_decl data_list
              | empty
    """


def p_value(p):
    """
    value : STRING
          | NUMBER
    """
    p[0] = ParserObject(value=p[1], type=type(p[1]).__name__)


def p_code(_p):
    """code : CODE procedures"""


def p_procedures(_p):
    """
    procedures : procedure procedures
               | empty
    """


def p_procedure(p):
    """procedure : DEF ID COLON statements"""
    logging.log(5, "Procedure: %s", p[2])
    symbol = get_symbol(p[2])
    if symbol is None:
        add_symbol(p[2], "FUNC", lineno=p.lineno(2), code=p[4], usage=0)
    else:
        set_symbol(p[2], lineno=p.lineno(2), code=p[4])


def p_statements(p):  # noqa: D205, D400, D403, D415
    """statements : statement other_statements"""
    logging.log(5, "Statement(s): %s %s", p[1], repr(p[2]))
    st_list = [p[1]]
    st_list.extend(p[2] or [])
    p[0] = st_list


def p_other_statements(p):  # noqa: D205, D400, D403, D415
    """
    other_statements : statement other_statements
                     | empty
    """
    logging.log(5, "Statement(o): %s", p[1])
    if p[1]:
        other = []
        if len(p) > 2:
            other = p[2] or []
        st_list = [p[1]]
        st_list.extend(other)
        p[0] = st_list
    else:
        p[0] = []


def p_statement(p):  # noqa: D205, D400, D403, D415
    """
    statement : var_op
              | push_op
              | pop_op
              | call_op
              | end_op
              | jump
              | compare
              | label
              | DUP
              | operators
              | flag_ops
              | draw_ops
    """
    p[0] = "\n".join([p[i] for i in range(1, len(p))])
    logging.log(5, p[0])


def p_var_op(p):
    """
    var_op : LOAD ID
        | STOR ID
    """
    if get_symbol(p[2]) is None:
        raise Exception(f"Undefined symbol:{p.lineno(2)}:'{p[2]}' ")
    p[0] = " ".join([p[1], p[2]])


def p_push_op(p):
    """push_op : PUSH value"""
    p[0] = f"{p[1]} {p[2].value}"


def p_push_op_no_value(p):
    """push_op : PUSH ID"""
    logging.warning(
        "Expected value instead of ID: %d. Did you mean 'LOAD'?", p.lineno(2)
    )
    p[0] = " ".join([p[1], "$ERR"])

def p_push_op_pushf(p):
    """push_op : PUSHF"""
    p[0] = f"{p[1]}"


def p_pop_op(p):
    """pop_op : POP"""
    p[0] = p[1]


def p_call_op(p):
    """call_op : CALL ID"""
    function = get_symbol(p[2])
    if not function:
        add_symbol(p[2], "FUNC", code=None, usage=1)
    elif function["type"] not in ["FUNC", "INT"]:
        raise Exception(
            f"Unexpected symbol type:'FUNC or INT':'{function['type']}' "
        )
    increment_symbol_usage(p[2], p.lineno(2))
    p[0] = f"{p[1]} {p[2]}"


def p_end_op(p):
    """
    end_op : RET
        | HALT
    """
    p[0] = p[1]


def p_compare_value(p):
    """
    compare : CMP value
    """
    p[0] = f"{p[1]} {p[2].value}"


def p_compare_id(p):
    """
    compare : CMP ID
    """
    if get_symbol(p[2]) is None:
        raise Exception(f"Undefined symbol:{p.lineno(2)}:{p[2]}")
    p[0] = f"{p[1]} {p[2]}"


def p_jump(p):
    """
    jump : JP jmp_target
         | JZ jmp_target
         | JNZ jmp_target
         | JMORE jmp_target
         | JLESS jmp_target
    """
    p[0] = " ".join([p[1], p[2]])


def p_jump_skip(p):
    """
    jump : SKIPZ
         | SKIPNZ
    """
    p[0] = p[1]


def p_jmp_target_label(p):
    """
    jmp_target : LABEL
    """
    label = get_symbol(p[1])
    if label:
        if label["type"] != "LABEL":
            raise Exception(
                f"Unexpected Symbol Type:{p.lineno(1)}: '{p[1]}'"
            )
        increment_symbol_usage(p[1], p.lineno(1))
    else:
        add_symbol(p[1], "LABEL", usage=1)
    p[0] = p[1]


def p_jmp_target_number(p):
    """
    jmp_target : NUMBER
    """
    if not isinstance(p[1], int):
        raise Exception("Can't use 'float' with 'jump'.")
    p[0] = p[1]


def p_label(p):
    """label : LABEL"""
    lineno = p.lineno(1)
    sym = get_symbol(p[1])
    if sym is None:
        add_symbol(p[1], "LABEL", lineno=lineno, usage=0)
    else:
        if sym["type"] != "LABEL":
            raise Exception(f"Not a label:{lineno}: '{p[1]}'")
        set_symbol(p[1], lineno=lineno)
    logging.debug(
        "LABEL: %d: '%s' (%s)", lineno, p[1], "used" if sym else "unused"
    )
    p[0] = f"LABEL {p[1]}"


def p_operators(p):
    """
    operators : ADD
        | SUB
        | MUL
        | DIV
        | IDIV
        | POW
        | TRUNC
        | RAND
        | AND
        | OR
        | XOR
        | SHFTR
        | SHFTL
        | NOT
    """
    p[0] = p[1]


def p_flag_ops(p):
    """
    flag_ops : SET NUMBER
             | UNSET NUMBER
    """
    logging.log(5, "FLAG: %s: %s", p[1], p[2].value)
    if not isinstance(p[2], int):
        raise TypeError(f"Expected an integer value: {p[2].value}")
    p[0] = f"{p[1]} {p[2]}"


def p_drow_ops(p):
    """
    draw_ops : MVTO
             | SETPX
    """
    logging.log(5, "DRAW_CMD: %s", p[1])
    p[0] = p[1]


def p_error(p):
    """Provide a simple error message."""
    global parser_error
    if p:
        logging.critical("Invalid token:%d: %s:'%s'", p.lineno, p.type, p.value)
    else:
        logging.error("Syntax error at EOF.")


def check_references():
    """Check if all references and symbols are used throughout the code."""
    undefined = False
    min_by_type = {"LABEL": 1, "FUNC": 0}
    for symbol, data in get_symbols_by_class(("LABEL", "FUNC")).items():
        lineno = data.get("lineno")
        symtype = data.get("type")
        if lineno is None or lineno < min_by_type.get(symtype, 0):
            logging.error("Undefined symbol: '%s'", symbol)
            undefined = True
        if undefined:
            raise UndefinedReference("LABEL", symbol)
        if data.get("usage", 1) == 0:
            logging.warning("Unused symbol: '%s'", symbol)


def parse_program(filename):
    """Parse LogoASM program."""
    global symtable
    global tokens
    tokens = lexer.tokens
    logolex = lexer.lexer()
    parser = yacc.yacc(start="program", debug=True)
    with open(filename, "rt") as input_file:
        source = "\n".join(input_file.readlines())
    start_symbol = parser.parse(source, lexer=logolex, tracking=False)
    check_references()
    return start_symbol