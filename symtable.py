"""Implementacao da tabela de simbolos."""

__symtable = {}
case_insensitive_symtable = False


class SymbolRedefinitionError(Exception):
    """Erro gerado quando um símbolo já está definido."""

    def __init__(self, symbol, lineno, original=None):
        """Erro de inicialização com mensagem adequada."""
        super().__init__(
            f"Redeclaration of symbol "
            f"'{original if original else symbol['name']}':{lineno}:"
            f"original declaration at line {symbol['lineno']}"
        )


class InternalError(Exception):
    """Erro gerado quando um símbolo já está definido."""

    def __init__(self, msg):
        """Erro de inicialização com mensagem adequada."""
        super().__init__(f"Internal error: {msg}")


def __tr_symbol(symbol):
    return symbol.upper() if case_insensitive_symtable else symbol, symbol


def add_symbol(symbol, sym_type, **kwargs):
    """Criar novo símbolo na tabela de símbolos."""
    symbol, original = __tr_symbol(symbol)

    obj = __symtable.get(symbol)
    if obj:
        lineno = symbol.get("lineno")
        if lineno >= 0:
            raise SymbolRedefinitionError(obj, lineno, original)
        obj.update(kwargs)
    else:
        kwargs["name"] = symbol
        kwargs["type"] = sym_type
        __symtable[symbol] = kwargs


def set_symbol(symbol, **kwargs):
    """Definir valores de um símbolo na tabela de símbolos."""
    symbol, original = __tr_symbol(symbol)
    obj = __symtable.get(symbol)
    if obj is None:
        raise InternalError(f"Symbol not defined: {original}")
    if "name" in kwargs:
        raise InternalError(
            f"Cannot modify symbol '{original}' attribute 'name'."
        )
    if "lineno" in kwargs and not obj.get("lineno", -1) < 0:
        raise InternalError(
            f"Cannot modify symbol {original} attribute 'line'."
        )
    obj.update(kwargs)


def get_symbol(symbol):
    """Recuperar símbolo da tabela de símbolos."""
    return __symtable.get(__tr_symbol(symbol)[0])


def get_symbols_by_class(symtype):
    """Recupere todos os símbolos com um determinado tipo da tabela de símbolos."""
    return {k: v for k, v in __symtable.items() if v["type"] == symtype}


def remove_symbol(symbol):
    """Remover símbolo da tabela de símbolos."""
    symbol, original = __tr_symbol(symbol)
    if symbol in __symtable:
        del __symtable[symbol]
    else:
        raise InternalError(f"Symbol not defined: {original}")


def increment_symbol_usage(symbol, lineno, amount=1):
    """Incrementar o atributo 'uso' do símbolo pelo valor especificado."""
    sym = get_symbol(symbol)
    if sym is None:
        raise Exception(f"Unknown symbol:{lineno}:'{symbol}'")
    usage = sym.get("usage", 0) + amount
    set_symbol(symbol, usage=usage)