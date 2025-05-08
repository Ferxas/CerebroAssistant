# audio/whisper_listener.py

import queue
import sounddevice as sd
import numpy as np
import whisper
import threading
import time

class WhisperListener:
    def __init__(self, model_size="base", trigger_word="cerebro"):
        self.model = whisper.load_model(model_size)
        self.trigger_word = trigger_word.lower()
        self.running = False
        self.q = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print("Audio input error:", status)
        self.q.put(indata.copy())

    def _listen_audio(self):
        with sd.InputStream(samplerate=16000, channels=1, callback=self._callback):
            print("🔊 Escuchando... Di 'cerebro' para activar.")
            audio_data = np.empty((0, 1), dtype=np.float32)
            while not self.running:
                try:
                    data = self.q.get(timeout=1)
                    audio_data = np.concatenate((audio_data, data))
                    if len(audio_data) > 16000 * 5:  # 5 segundos de audio
                        audio_segment = np.squeeze(audio_data[-16000 * 5:])
                        sd.stop()
                        self._transcribe(audio_segment)
                        audio_data = np.empty((0, 1), dtype=np.float32)
                except queue.Empty:
                    continue

    def _transcribe(self, audio):
        print("📝 Procesando...")
        result = self.model.transcribe(audio, fp16=False, language='es')
        text = result["text"].lower()
        print("🗣️ Dices:", text)
        if self.trigger_word in text:
            print("✅ Activado con la palabra clave.")
            self.running = True

    def wait_for_trigger(self):
        self.running = False
        t = threading.Thread(target=self._listen_audio)
        t.start()
        t.join()

    def listen_with_timeout(self, timeout=10):
        print(f"🎤 Tienes {timeout} segundos para hablar...")
        self.running = True
        audio_data = np.empty((0, 1), dtype=np.float32)
        start_time = time.time()

        with sd.InputStream(samplerate=16000, channels=1, callback=self._callback):
            while time.time() - start_time < timeout:
                try:
                    data = self.q.get(timeout=1)
                    audio_data = np.concatenate((audio_data, data))
                except queue.Empty:
                    continue

        if len(audio_data) < 16000:  # silencio o casi nada
            return None

        audio_segment = np.squeeze(audio_data)
        result = self.model.transcribe(audio_segment, fp16=False, language='es')
        return result["text"].strip()
