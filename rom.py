"""LogoVM internal functions."""

# import math

from math import pi, sin, cos

from logovm.machinery import (
    reg,
    reset_video,
    stack_push,
    stack_pop,
    get_pos,
    draw_line,
)


def read_input():
    """Implement command READ."""
    value = input()
    try:
        try:
            reg[4] = int(value)
        except ValueError:
            reg[4] = float(value)
    except ValueError:
        reg[4] = value
    stack_push(reg[4])


def write_output():
    """Implement command WRITE."""

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
    """Convert degrees to radians."""
    return angle * pi / 180


def move():
    """Implement instruction MOVE."""
    global __turtle
    length = stack_pop()
    angle = -__rad(stack_pop())
    get_pos()
    reg[2] = reg[0] + cos(angle) * (length - 1)
    reg[3] = reg[1] + sin(angle) * (length - 1)
    draw_line()


internal = {
    "READ": read_input,
    "WRITE": write_output,
    "CLRSCR": reset_video,
    "MOVE": move,
}