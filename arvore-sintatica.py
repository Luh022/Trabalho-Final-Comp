def p_value_expr_id(prod): # noqa: D205, D400, D403, D415
    """value_expr : ID"""
    node = new_node("value_expr")
    leaf = new_leaf("ID", value=prod[1])
    append_node(node, leaf)
    prod[0] = node

def p_value_expr_par(prod):  # noqa: D205, D400, D403, D415
    """value_expr : OPEN_PAR value_expr CLOSE_PAR"""
    node = new_node("value_expr")
    append_node(node, new_leaf("OPEN_PAR", value="("))
    append_nde(p[2])
    append_node(node, new_leaf("CLOSE_PAR", value=")"))
    prod[0] = node

def new_node(name):
    """Criar um novo objeto de nó."""
    return dict(name=name, children=[])


def append_node(node, new_node):
    """Anexar um nó ou folha a um nó."""
    assert isinstance(node, dict) and "children" in node
    node["children"].append(new_node)


def new_leaf(name, **kwargs):
    """Criar um novo objeto folha."""
    return dict(name=name, value=kwargs)