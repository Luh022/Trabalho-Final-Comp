"""Carregador para programas LogoVM."""

import logging

from logoasm.symtable import get_symbols_by_class, set_symbol
from logovm.errors import UndefinedReference


def loader():
    """Ajustar endereços ao programa de rum."""
    # Uses global symtable.
    for symbol, data in get_symbols_by_class("FUNC").items():
        code = data.get("code")
        if code is None:
            logging.error("Undefined function: %s", symbol)
            raise UndefinedReference("FUNCTION", symbol)
        for addr, cmd in enumerate(code):
            if cmd.startswith("LABEL"):
                _, name = cmd.split(" ", 1)
                set_symbol(name, pc=addr)