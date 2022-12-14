#Funções Globais quq a LogoVM usa

try:
    from PIL import Image
except ImportError:
    HAS_PIL_IMAGE = False
else:
    HAS_PIL_IMAGE = True


__turtle_default = (0, 0)
__turtle = (0, 0)
__window = None

flags = 0
reg = [None] * 6
stack = []
pc_stack = []
image_format = "PNG"

MAXSTACKSIZE = 256 * (2**20)

class Flags:
    """Flag mappings."""

    PEN = 1
    DRAW = 2
    ERASE = 3
    _UNUSED = 4
    EXC = 5
    VERR = 15
    MAXFLAG = VERR


def __get_flag_index(flag):
    """Ensure flag index is valid."""
    flag = int(flag)
    if not 1 <= flag <= Flags.MAXFLAG:
        raise ValueError("Flag index must be in [1,{Flags.MAXFLAG}]")
    return flag


def set_flag(flag):
    """Set a flag."""
    global flags
    logging.debug("BSET: %s: 0b%s", flag, f"{flags:0{Flags.MAXFLAG+1}b}")
    flag = __get_flag_index(flag)
    flags |= 1 << flag
    logging.debug("SET: %s: 0b%s", flag, f"{flags:0{Flags.MAXFLAG+1}b}")


def unset_flag(flag):
    """Unset a flag."""
    global flags
    logging.debug("BUNSET: %s: 0b%s", flag, f"{flags:0{Flags.MAXFLAG+1}b}")
    flag = __get_flag_index(flag)
    flags &= ~(1 << flag)
    logging.debug("UNSET: %s: 0b%s", flag, f"{flags:0{Flags.MAXFLAG+1}b}")


def isset(flag):
    """Check if a flag is set."""
    logging.debug("ISSET: %d %s", flag, f"{flags:0{Flags.MAXFLAG+1}b}")
    return bool(flags & (1 << __get_flag_index(flag)))


def __init_video(width, height):
    """Initialize video memory."""
    global __window
    bpp = 1
    vidmem = [0] * (height * width * bpp)
    logging.debug(
        "width=%d  height=%d  bpp=%d  stride=%d",
        width,
        height,
        bpp,
        width * bpp,
    )
    __window = [width, height, bpp, width * bpp, vidmem]


def reset_video():
    """Resetar o video da memoria."""
    __init_video(__window[0], __window[1])
    unset_flag(Flags.DRAW)


def __save_video(filename):
    """Salvar memória de vídeo em um nome de arquivo filename."""
    logging.debug("save_video: %s", filename)
    if isset(Flags.VERR):
        logging.warning("A video error occured.")
    if isset(Flags.DRAW):
        if HAS_PIL_IMAGE and image_format.lower() in ["jpg", "png"]:
            __save_as_PIL(filename)
        elif image_format.lower() in ["ppm", "pnm", "pgm", "netpbm", "pbm"]:
            __save_as_PPM(filename)


def __save_as_PIL(filename):
    logging.debug("Saving with PIL: %s %s", filename, image_format)
    logging.debug("WINDOW: %s", repr(__window))
    width, height, bpp, _stride, data = __window
    data = bytes(data)
    mode = "L" if bpp == 1 else "RGB"
    img = Image.frombytes(mode, (width, height), data)
    img.save(f"{filename}.{image_format.lower()}")


def __save_as_PPM(filename):
    logging.debug("Saving PNM: %s", filename)
    logging.debug("WINDOW: %s", repr(__window))
    width, height, bpp, stride, data = __window
    mode = "P2" if bpp == 1 else "P3"
    ext = "pgm" if bpp == 1 else "ppm"
    with open(f"{filename}.{ext}", "w", encoding="ascii") as out:
        print(mode, file=out)
        print(f"# {filename}.{ext}", file=out)
        print(f"{width} {height}", file=out)
        print("255", file=out)
        if isset(Flags.VERR):
            print("# WARNING: A video error occured.", file=out)
        for j in range(height):
            start = stride * j
            print(
                " ".join(str(v) for v in data[start : start + stride]),
                file=out,
            )
            print("".join(f"{v: 4d}" for v in data[start : start + stride]))


def __plot(x, y, color=255):
    """Defina um pixel com a cor dada."""
    width, height, bpp, stride, vidmem = __window
    logging.debug("params: x=%s y=%s width=%s height=%s", x, y, width, height)
    if not 0 <= x < width:
        return
    if not 0 <= y < height:
        return
    if isinstance(color, (int, float)):
        color = [int(color)]
    else:
        color = [int(v) for v in color]
    if len(color) != bpp:
        set_flag(Flags.VERR)
        if bpp == 1:
            color = sum(color, 0) // len(color)
        else:
            color = color * 3
    color = color[0] if bpp == 1 else color
    x = round(x)
    y = round(y)
    position = stride * y + x * bpp
    vidmem[position] = color
    logging.debug("vidmem:x=%s y=%s c=%s pos=%s", x, y, color, position)
    set_flag(Flags.DRAW)


def set_pixel():
    """Implementar a instrucao: SETPX."""
    if isset(Flags.PEN):
        __plot(*__turtle[:2], 0 if isset(Flags.ERASE) else 255)


def draw_line():
    """Desenhe um segmento de linha na memória de vídeo da posição atual até o alvo."""
    x0, y0, x1, y1 = reg[:6]
    logging.debug("x0=%d y0=%d x1=%d y1=%d", x0, y0, x1, y1)
    if isset(Flags.PEN):
        dx = abs(x1 - x0)
        sx = copysign(1, x1 - x0)
        dy = -abs(y1 - y0)
        sy = copysign(1, y1 - y0)
        error = dx + dy

        while True:
            __plot(x0, y0)
            if round(x0) == round(x1) and round(y0) == round(y1):
                break
            error2 = 2 * error
            logging.debug("dx %s dy %s error %s e2 %s", dx, dy, error, error2)
            if error2 >= dy:
                if round(x0) == round(x1):
                    break
                error = error + dy
                x0 = x0 + sx
            if error2 <= dx:
                if round(y0) == round(y1):
                    break
                error = error + dx
                y0 = y0 + sy

    stack_push(x1, y1)
    set_pos()


def get_pos():
    """Obtenha a posição do ponteiro como (R0, R1)."""
    logging.debug("TURTLE: %s", repr(__turtle))
    reg[0] = __turtle[0]
    reg[1] = __turtle[1]
    return (reg[0], reg[1])


def set_pos():
    """Defina a posição do ponteiro para (R0, R1)."""
    global __turtle
    _, _, *extra = __turtle
    reg[1] = stack_pop()
    reg[0] = stack_pop()
    __turtle = (reg[0], reg[1], *extra)
    logging.debug("TURTLE: %s", repr(__turtle))

def stack_peek():
    """Peek valor no topo da pilha."""
    return stack[-1] if stack else None


def stack_pop():
    """Retirar um valor da pilha."""
    if not stack:
        raise EmptyStackError()
    value = stack.pop()
    logging.debug("STACK: %s", repr(stack))
    return value


def stack_push(*args):
    """Empurre um valor para a pilha."""
    for value in args:
        if len(stack) < MAXSTACKSIZE:
            stack.append(value)
        else:
            raise StackOverflowError()
    logging.debug("STACK: %s", repr(stack))


def halt():
    """Delisgamento da maquina."""
    filename = datetime.now().strftime("%Y%m%d-%H%M%S.%s")
    logging.debug("HALT: %s %s", filename, image_format)
    pc_stack.clear()
    __save_video(filename)


def init(**kwargs):

    global __turtle
    global __turtle_default
    width, height = kwargs.get("width", 456), kwargs.get("height", 182)
    x, y = kwargs.get("x", width // 2), kwargs.get("y", height // 2)
    __turtle_default = (x, y)
    __turtle = (x, y)
    __init_video(width, height)
    unset_flag(Flags.DRAW)