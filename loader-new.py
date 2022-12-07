"""Carregador para programas LogoVM."""

def loader():
    """Ajustar endereços ao programa de rum."""
    for symbol, data in get_symbols_by_class("FUNC").items():
        code = data.get("code")
        if code is None:
            logging.error("Undefined function: %s", symbol)
            raise UndefinedReference("FUNCTION", symbol)
        for addr, cmd in enumerate(code):
            if cmd.startswith("LABEL"):
                _, name = cmd.split(" ", 2)
                set_symbol(name, pc=addr)