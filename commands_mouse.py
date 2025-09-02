from pynput.mouse import Button, Controller

# Controller mouse globale
mouse = Controller()

# -------------------------
# FUNZIONI CURSORE
# -------------------------
def get_position():
    return mouse.position

def set_position(x, y):
    mouse.position = (x, y)

def move(dx, dy):
    mouse.move(dx, dy)

# -------------------------
# CLICK
# -------------------------
def click_left(n=1):
    mouse.click(Button.left, n)

def click_right(n=1):
    mouse.click(Button.right, n)

def click_middle(n=1):
    """Click centrale (rotella)."""
    mouse.click(Button.middle, n)

def double_click_left():
    mouse.click(Button.left, 2)

# -------------------------
# PRESSIONE / RILASCIO
# -------------------------
def press_left():
    """Tiene premuto il tasto sinistro."""
    mouse.press(Button.left)

def release_left():
    """Rilascia il tasto sinistro."""
    mouse.release(Button.left)

def press_right():
    """Tiene premuto il tasto destro."""
    mouse.press(Button.right)

def release_right():
    """Rilascia il tasto destro."""
    mouse.release(Button.right)

def press_middle():
    """Tiene premuto il tasto centrale."""
    mouse.press(Button.middle)

def release_middle():
    """Rilascia il tasto centrale."""
    mouse.release(Button.middle)

# -------------------------
# SCROLL
# -------------------------
scroll_buffer = 0.0
def scroll_vertical(dy):
    global scroll_buffer
    scroll_buffer += dy  # accumula anche valori piccoli
    steps = int(scroll_buffer)  # parte intera
    if steps != 0:
        mouse.scroll(0, steps)
        scroll_buffer -= steps 

def scroll_horizontal(dx):
    """Scroll orizzontale (positivo = destra, negativo = sinistra)."""
    mouse.scroll(dx, 0)

# -------------------------
# ZOOM
# -------------------------
from pynput.keyboard import Controller as KeyboardController, Key

keyboard = KeyboardController()

def zoom_in(steps=1):
    """Zoom avanti: simula Ctrl + rotella su"""
    with keyboard.pressed(Key.ctrl):
        scroll_vertical(steps)

def zoom_out(steps=1):
    """Zoom indietro: simula Ctrl + rotella giù"""
    with keyboard.pressed(Key.ctrl):
        scroll_vertical(-steps)
