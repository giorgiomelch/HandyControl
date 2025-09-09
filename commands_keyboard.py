from pynput.keyboard import Controller, Key
import cv2
import os
from PIL import Image

def show_help():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "imgs/aiuto.jpg")

    help_img = cv2.imread(image_path)
    if help_img is None:
        print(f"Errore: OpenCV non riesce a leggere {image_path}")
        return

    cv2.namedWindow("Comandi disponibili", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Comandi disponibili", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Comandi disponibili", help_img)

    # Rimane aperta finché l’utente non preme ESC o Q
    while True:
        if cv2.waitKey(1) & 0xFF in (27, ord('q')):
            break

    cv2.destroyWindow("Comandi disponibili")

keyboard = Controller()

def execute_command(text: str):
    text = text.lower()

    if "comando invio" in text:
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Premuto ENTER")

    elif "comando cancella" in text:
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
        print("Premuto BACKSPACE")

    elif "comando esci" in text:
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        print("Premuto ESC")

    elif "comando tab" in text:
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        print("Premuto TAB")

    elif "comando control a" in text or "comando ctrl a" in text:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('a')
            keyboard.release('a')
        print("CTRL + A (Seleziona tutto)")

    elif "comando control s" in text or "comando ctrl s" in text:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('s')
            keyboard.release('s')
        print("CTRL + S (Salva)")

    elif "comando control c" in text or "comando ctrl c" in text:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        print("CTRL + C (Copia)")

    elif "comando control v" in text or "comando ctrl v" in text:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        print("CTRL + V (Incolla)")

    elif "comando alt tab" in text:
        with keyboard.pressed(Key.alt):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
        print("ALT + TAB (cambia finestra)")
    elif "comando aiuto" in text:
        print("AIUTO: compare schermata di guida")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "imgs/aiuto.jpg")

        if os.path.exists(image_path):
            try:
                Image.open(image_path).show()
            except Exception as e:
                print("Errore mostrando l'immagine:", e)
        else:
            print("Immagine non trovata:", image_path)

    else:
        # scrive il testo normalmente
        keyboard.type(text + " ")
