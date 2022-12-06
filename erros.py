"""Definicao de excecao para a LogoVM."""


class LogoVMError(Exception):
    """Classe base para todos os erros do LogoVM."""


class EmptyStackError(LogoVMError):
    """Erro de pilha vazia."""

    def __init__(self):
        """Inicializar com mensagem adequada."""
        super().__init__("No values on stack.")


class StackOverflowError(LogoVMError):
    """Erro de estouro de pilha."""

    def __init__(self):
        super().__init__("Stack Overflow.")


class InvalidAddress(LogoVMError):
    """Tentei acessar um endereço inválido."""

    def __init__(self, value):
        super().__init__(f"Invalid address: {value}")


class TypeMismatch(LogoVMError):
    """Incompatibilidade de tipo de valor para instrução."""

    def __init__(self, instruction, expected, observed):
        super().__init__(
            f"Type mismatch: '{instruction}':'{expected}':'{observed}'"
        )


class UndefinedReference(LogoVMError):
    """O símbolo é referenciado, mas não foi definido."""

    def __init__(self, symtype, symbol):
        super().__init__(f"Undefined reference for '{symtype}': '{symbol}'")