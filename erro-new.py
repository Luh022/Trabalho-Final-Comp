"""Definicao de excecao para a LogoVM."""

class LogoVMError(Exception):

class EmptyStackError(LogoVMError):
    def __init__(self):
        super().__init__("No values on stack.")


class StackOverflowError(LogoVMError):
    def __init__(self):
        super().__init__("Stack Overflow.")


class InvalidAddress(LogoVMError):
    def __init__(self, value):
        super().__init__(f"Invalid address: {value}")


class TypeMismatch(LogoVMError):
    def __init__(self, instruction, expected, observed):
        super().__init__(
            f"Type mismatch: '{instruction}':'{expected}':'{observed}'"
        )


class UndefinedReference(LogoVMError):
    def __init__(self, symtype, symbol):
        super().__init__(f"Undefined reference for '{symtype}': '{symbol}'")