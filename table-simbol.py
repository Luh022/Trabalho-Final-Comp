""Implementação da tabela de símbolos."""

__symtable = {}


class SymbolRedefinitionError(Exception):
    """Erro gerado quando um símbolo já está definido."""

    def __init__(self, obj, lineno):
        """Erro de inicialização com mensagem adequada."""
        super().__init__(
            f"Redeclaration of symbol: {obj['name']}:{lineno}: "
            + f"Previously declared at line {obj['lineno']}"
        )


class InternalError(Exception):
    """Erro gerado quando um símbolo já está definido."""

    def __init__(self, msg):
        """Erro de inicialização com mensagem adequada."""
        super().__init__(f"Internal error: {msg}")


def add_symbol(symbol, sym_type, lineno, **kwargs):
    """Criar um novo símbolo na tabela de símbolos."""
    obj = get_symbol(symbol)

    if obj:
        raise SymbolRedefinitionError(obj, lineno)

    kwargs["name"] = symbol
    kwargs["type"] = sym_type
    kwargs["lineno"] = lineno
    __symtable[symbol] = kwargs
    return __symtable[symbol]


def set_symbol(symbol, **kwargs):
    """Definir valores de um símbolo na tabela de símbolos."""
    obj = get_symbol(symbol)
    if obj is None:
        raise InternalError(f"Symbol not defined: {symbol}")
    if "name" in kwargs:
        raise InternalError(
            f"Cannot modify symbol '{symbol}' attribute 'name'."
        )
    if "lineno" in kwargs:
        raise InternalError(f"Cannot modify symbol {symbol} attribute 'line'.")
    obj.update(kwargs)


def get_symbol(symbol):
    """Recuperar símbolo da tabela de símbolos."""
    return __symtable.get(symbol)

#Gerando uma árvore sintática
#Ao reduzira as regras de derivação da gramática,
# o parser LALR(1) cria uma árvore de derivação a partir das folhas em direção à raiz,
# por isso dizemos que é uma estratégia ascendente (bottom-up) de analise sintática.
-------------------------------------------------------------------------------------------------
#Essa árvore de derivação é a árvore sintática do programa,
# e podemos ver a árvore criando nós internos ou folhas durante a execução do analisador sintático.
# Por exemplo, podemos criar um nó folha em uma regra que avalia um símbolo terminal,
# e associar esse nó ao nó interno do não terminal da regra:

def p_value_expr_id(prod):
    """value_expr : ID"""
    node = new_node("value_expr")
    leaf = new_leaf("ID", value=prod[1])
    append_node(node, leaf)
    prod[0] = node