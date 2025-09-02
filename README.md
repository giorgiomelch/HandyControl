# Hand Gesture Recognition for Cursor Controlling

This project enables controlling your computer's mouse and keyboard using hand gestures and voice commands, leveraging MediaPipe for hand tracking and Vosk for speech recognition.\\
About the hand interaction, think of it like you are holding an invisible mouse: for example, pressing your index finger simulates a left click.

## Features

- **Hand Gesture Mouse Control:**  
  Move the cursor, click (left/right/double), scroll, and perform other mouse actions using intuitive hand gestures.

- **Voice Command Keyboard Control:**  
  Trigger voice recognition with a gesture and execute keyboard commands (e.g., Enter, Ctrl+C, Alt+Tab) by speaking.

- **Visual Feedback:**  
  The application displays hand landmarks and overlays to help guide your gestures.


## Installation

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    if you are using linux 
    
    ```sh
    apt-get install portaudio19-dev
    ```

2. **Download Vosk models:**  
   Place the model folders inside the `models/` directory as shown in the project structure.

## Usage

Run the main application:

```sh
python main.py
```

- Show your hand to the webcam.
- Use gestures to move the cursor and click.
- Make an "OK" sign to activate voice recognition, then speak a command.
- To exit, show both thumbs down or press `q`.

## File Structure

- `main.py` — Main application entry point.
- `gestures.py` — Hand gesture recognition and mouse control logic.
- `commands_mouse.py` — Mouse control functions.
- `commands_keyboard.py` — Keyboard command execution.
- `voice.py` — Voice recognition and command handling.
- `models/` — Vosk speech recognition models.
- `imgs/` — Images for help/commands.

## Supported Voice Commands

- "comando invio" — Press Enter
- "comando cancella" — Press Backspace
- "comando esci" — Press Esc
- "comando tab" — Press Tab
- "comando control a" — Ctrl+A
- "comando control s" — Ctrl+S
- "comando control c" — Ctrl+C
- "comando control v" — Ctrl+V
- "comando alt tab" — Alt+Tab
- "comando aiuto" — Show help image