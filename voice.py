import queue, json, sounddevice as sd, threading
from vosk import Model, KaldiRecognizer
from commands_keyboard import execute_command


class VoiceListener:
    def __init__(self, model_path="models/vosk-model-it-0.22", samplerate=16000):
        self.model = Model(model_path)
        commands = ["comando control a", "comando control s", "comando control v",
            "comando control c", "comando control tab",
            "comando invio", "comando esci", "comando tab", "comando alt tab"]
        self.recognizer = KaldiRecognizer(self.model, samplerate, json.dumps(commands))
        self.audio_q = queue.Queue()
        self.text_q = queue.Queue()
        self.flag = threading.Event()
        self.samplerate = samplerate

        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_q.put(bytes(indata))

    def _listen_loop(self):
        while True:
            self.flag.wait()   # attende trigger
            self.flag.clear()

            print("Ascolto attivato...")
            with sd.RawInputStream(samplerate=self.samplerate,
                                   blocksize=8000, dtype='int16',
                                   channels=1, callback=self._audio_callback):
                while True:
                    data = self.audio_q.get()
                    if self.recognizer.AcceptWaveform(data):
                        result = self.recognizer.Result()
                        text = json.loads(result)["text"].strip()
                        if text:
                            print("Hai detto:", text)
                            execute_command(text)
                            self.text_q.put(text)
                            break

    def trigger_listen(self):
        self.flag.set()

    def get_texts(self):
        texts = []
        try:
            while True:
                texts.append(self.text_q.get_nowait())
        except queue.Empty:
            pass
        return texts
