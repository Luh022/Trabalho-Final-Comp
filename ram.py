"""Funções internas do LogoVM."""

def read_input():
    """Implementacao do comando READ."""
    value = input()
    try:
        try:
            reg[6] = int(value)
        except ValueError:
            reg[6] = float(value)
    except ValueError:
        reg[6] = value
    stack_push(reg[6])


def write_output():
    """Implementacao do comando WRITE."""

    def escape(string):
        chars = {"\\n": "\n", "\\t": "\t"}
        for a, b in chars.items():
            string = string.replace(a, b)
        return string

    global stack
    count = reg[0] = stack_pop()
    data = []
    while count > 0:
        data.append(escape(str(stack_pop())))
        count -= 1
    print("".join(data[::-1]), end="")


def __rad(angle):
    """Converter graus em radianos."""
    return angle * pi / 180


def move():
    """Implementacao da instrucao MOVE."""
    global __turtle
    length = stack_pop()
    angle = -__rad(stack_pop())
    get_pos()
    reg[2] = reg[0] + cos(angle) * (length - 1)
    reg[4] = reg[1] + sin(angle) * (length - 1)
    draw_line()


internal = {
    "READ": read_input,
    "WRITE": write_output,
    "CLRSCR": reset_video,
    "MOVE": move,
}