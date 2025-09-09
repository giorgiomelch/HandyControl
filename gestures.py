import commands_mouse as mouse
import math
import time
import cv2

#### Classe principale per il controllo della mano ####
class HandController:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.cx, self.cy = w // 2, h // 2
        self.radii = [int(h/2), int(h/3), int(h/5), int(h/15)]
        self.last_ok_time = 0
        self.ok_cooldown = 2.0
        
        self.ok_active = False
        self.ok_block_time = 1  # blocca click per 1s dopo OK

    def handle_one_hand(self, hand, voice_listener):
        if not is_hand_closed(hand):
            now = time.time()
            ok_sign = detect_ok_sign(hand, False)
            if ok_sign and (time.time() - self.last_ok_time > self.ok_cooldown):
                voice_listener.trigger_listen()
                self.last_ok_time = time.time()
                self.last_ok_time = now
                self.ok_active = True
                self.ok_start_time = now
            # Blocca click subito dopo OK
            elif self.ok_active and (now - self.ok_start_time < self.ok_block_time):
                pass  # ignora click temporaneamente
            else:
                self.ok_active = False
                # esegui gesti normali
                if not (detect_thumb_down(hand) or detect_thumb_up(hand)):
                    detect_left_clicking(hand)
                    detect_cursor_movement(hand, self.w, self.h, self.cx, self.cy, self.radii)
                    detect_right_clicking(hand)
            detect_thumb_down(hand) 
            detect_thumb_up(hand)

    def handle_two_hands(self, hand1, hand2):
        if (detect_thumb_down(hand1, 2) and is_hand_closed(hand2)) or (detect_thumb_down(hand2, 2) and is_hand_closed(hand1)):
            mouse.zoom_out()
        elif (detect_thumb_up(hand1, 2) and is_hand_closed(hand2)) or (detect_thumb_up(hand2, 2) and is_hand_closed(hand1)):
            mouse.zoom_in()
        elif detect_thumb_down(hand1) and detect_thumb_down(hand2):
            return True
        return False 

    def draw_overlay(self, frame):
        cv2.circle(frame, (self.cx, self.cy), self.radii[0], (0, 255, 0), 2)
        cv2.circle(frame, (self.cx, self.cy), self.radii[1], (0, 0, 255), 2)
        cv2.circle(frame, (self.cx, self.cy), self.radii[2], (255, 0, 0), 2)
        cv2.circle(frame, (self.cx, self.cy), self.radii[3], (255, 255, 0), 2)
        return frame
    
    # Elissi al posto dei cerchi
    def draw_overlay_2(self, frame):
        axes_orizzontal_factor = 1.5 
        for i, r in enumerate(self.radii):
            axes = (int(r * axes_orizzontal_factor), r)  # (rx, ry)
            color = [(0,255,0), (0,0,255), (255,0,0), (255,255,0)][i]
            cv2.ellipse(frame, (self.cx, self.cy), axes, 0, 0, 360, color, 2)

        return frame

##### Funzioni di riconoscimento gesti #####
def is_hand_open(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    middle_finger_tip = hand_landmarks.landmark[12]
    ring_finger_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]

    thumb_ip = hand_landmarks.landmark[3]
    middle_finger_mcp = hand_landmarks.landmark[9]
    ring_finger_mcp = hand_landmarks.landmark[13]
    pinky_mcp = hand_landmarks.landmark[17]

    return ((thumb_tip.y < thumb_ip.y or thumb_tip.x < thumb_ip.x) and
            middle_finger_tip.y < middle_finger_mcp.y and
            ring_finger_tip.y < ring_finger_mcp.y and
            pinky_tip.y < pinky_mcp.y)

def is_hand_closed(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[8]
    middle_finger_tip = hand_landmarks.landmark[12]
    ring_finger_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]

    index_finger_mcp = hand_landmarks.landmark[5]
    middle_finger_mcp = hand_landmarks.landmark[9]
    ring_finger_mcp = hand_landmarks.landmark[13]
    pinky_mcp = hand_landmarks.landmark[17]

    return (index_finger_tip.y > index_finger_mcp.y and
            middle_finger_tip.y > middle_finger_mcp.y and
            ring_finger_tip.y > ring_finger_mcp.y and
            pinky_tip.y > pinky_mcp.y)

def detect_cursor_movement(hand_landmarks, w, h, center_x, center_y, raggi):
        center_hand_x = int(hand_landmarks.landmark[9].x * w)
        center_hand_y = int(hand_landmarks.landmark[9].y * h)
        distance = math.dist((center_hand_x, center_hand_y), (center_x, center_y))
        gain = 0
        if distance > raggi[3]:  
            gain = 40
        elif distance > raggi[2]:
            gain = 100
        elif distance > raggi[1]:
            gain = 300
        elif distance > raggi[0]:
            gain = 1000
        x_movement = -(center_hand_x - center_x) / w * gain
        y_movement =  (center_hand_y - center_y) / h * gain
        mouse.move(x_movement, y_movement)

def calculate_distance(point1, point2):
    dx = point1.x - point2.x
    dy = point1.y - point2.y
    return (dx**2 + dy**2) ** 0.5


last_click_time = 0
click_in_progress = False
press_start_time = None

def detect_left_clicking(hand_landmarks):
    global last_click_time, click_in_progress, press_start_time

    index_finger_tip = hand_landmarks.landmark[8].y
    index_finger_dip = hand_landmarks.landmark[7].y

    middle_finger_tip = hand_landmarks.landmark[12]
    middle_finger_mcp = hand_landmarks.landmark[9]
    ring_finger_tip = hand_landmarks.landmark[16]
    ring_finger_mcp = hand_landmarks.landmark[13]

    # Gesto di click = indice piegato, medio e anulare alzati
    click_gesture = (index_finger_tip > index_finger_dip and
        middle_finger_tip.y < middle_finger_mcp.y and
        ring_finger_tip.y < ring_finger_mcp.y)

    now = time.time()

    if click_gesture:
        if not click_in_progress:
            click_in_progress = True
            press_start_time = now
    else:
        if click_in_progress:
            press_duration = now - press_start_time

            if press_duration < 0.3:  # tap veloce
                if now - last_click_time < 0.5:  # entro 300ms → doppio click
                    mouse.double_click_left()
                    print("Double click")
                    last_click_time = 0
                else:
                    mouse.click_left()
                    print("Single click")
                    last_click_time = now

            elif press_duration >= 0.5:  # pressione lunga
                mouse.press_left()
                time.sleep(0.1)  # evita flood
                print("Long press")

            click_in_progress = False
            press_start_time = None


right_click_active = False

def detect_right_clicking(hand_landmarks):
    global right_click_active
    middle_finger_tip_y = hand_landmarks.landmark[12].y
    middle_finger_mcp_y = hand_landmarks.landmark[9].y 

    thumb_pip_x = hand_landmarks.landmark[4].x
    thumb_mcp_x = hand_landmarks.landmark[2].x
    
    gesture = (middle_finger_tip_y > middle_finger_mcp_y and
        thumb_pip_x > thumb_mcp_x)
    if gesture and not right_click_active:
        mouse.click_right()
        print("Right click")
        right_click_active = True
    elif not gesture:
        right_click_active = False
right_click_active = False

def detect_thumb_down(hand_landmarks, n_hands=1):
    thumb_tip = hand_landmarks.landmark[4].y
    thumb_ip = hand_landmarks.landmark[3].y
    thumb_mcp = hand_landmarks.landmark[2].y
    if thumb_tip > thumb_ip > thumb_mcp:
        index_finger_mcp = hand_landmarks.landmark[5]
        middle_finger_mcp = hand_landmarks.landmark[9]
        ring_finger_mcp = hand_landmarks.landmark[13]
        pinky_mcp = hand_landmarks.landmark[17]
        if (index_finger_mcp.y > middle_finger_mcp.y > ring_finger_mcp.y > pinky_mcp.y) and (thumb_tip > index_finger_mcp.y):
            if n_hands == 1:
                mouse.scroll_vertical(-1)
            return True
    return False
        
def detect_thumb_up(hand_landmarks, n_hands=1):
    thumb_tip = hand_landmarks.landmark[4].y
    thumb_ip = hand_landmarks.landmark[3].y
    thumb_mcp = hand_landmarks.landmark[2].y
    if thumb_tip < thumb_ip < thumb_mcp:
        index_finger_mcp = hand_landmarks.landmark[5]
        middle_finger_mcp = hand_landmarks.landmark[9]
        ring_finger_mcp = hand_landmarks.landmark[13]
        pinky_mcp = hand_landmarks.landmark[17]
        if (index_finger_mcp.y < middle_finger_mcp.y < ring_finger_mcp.y < pinky_mcp.y) and (thumb_tip < index_finger_mcp.y):
            if n_hands == 1:
                mouse.scroll_vertical(1)
            return True
    return False


def detect_ok_sign(hand_landmarks, ok_sign_state, threshold=0.05):
    if ok_sign_state == False:
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip, ring_tip, pinky_tip = hand_landmarks.landmark[12], hand_landmarks.landmark[16], hand_landmarks.landmark[20]
        middle_mcp, ring_mcp, pinky_mcp = hand_landmarks.landmark[9], hand_landmarks.landmark[13], hand_landmarks.landmark[17]

        # Controllo pollice-indice vicini
        thumb_index_dist = calculate_distance(thumb_tip, index_tip)
        close_enough = thumb_index_dist < threshold
        # Controllo altre dita aperte 
        middle_open = middle_tip.y < middle_mcp.y
        ring_open   = ring_tip.y < ring_mcp.y
        pinky_open  = pinky_tip.y < pinky_mcp.y

        if close_enough and middle_open and ring_open and pinky_open:
            print("OK sign detected")
            return True
        return False
    
