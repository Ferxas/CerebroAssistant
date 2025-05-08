from audio.whisper_listener import WhisperListener
from llm.ollama_client import OllamaClient
from audio.tts import TextToSpeech
from vision.yolov_detector import YOLOvDetector
import threading
import time
import keyboard

def start_vision(detector):
    detector.run_once()

if __name__ == "__main__":
    print("🧠 Iniciando sistema CEREBRO...")

    whisper_listener = WhisperListener()
    ollama = OllamaClient()
    tts = TextToSpeech()
    detector = YOLOvDetector()

    whisper_listener.wait_for_trigger()

    print("✅ Activado. CEREBRO está en línea.")
    tts.speak("Hola, soy CEREBRO. Estoy en línea y listo para ayudarte.")

    try:
        while True:
            print("🎤 Esperando entrada de voz...")
            whisper_listener.running = False
            whisper_listener.wait_for_trigger()

            print("🎙️ Escuchando tu pregunta (10 segundos)...")
            user_input = whisper_listener.listen_with_timeout(timeout=10)

            if keyboard.is_pressed('v'):
                print("🖱️ Tecla V detectada. Activando cámara.")
                start_vision(detector)
                continue

            if not user_input or user_input.strip() == "":
                print("🕐 Nadie respondió.")
                tts.speak("¿Estás ahí?")
                continue

            print("🗣️ Usuario dijo:", user_input)

            # Salida por voz
            if any(kw in user_input.lower() for kw in ["adiós", "duerme", "apágate", "termina"]):
                tts.speak("Está bien. Me desconecto. Hasta luego.")
                break

            # Activar cámara si se le dice
            if any(cmd in user_input.lower() for cmd in ["mira", "observa", "activa la cámara", "abre los ojos"]):
                tts.speak("Muy bien, observando el entorno.")
                start_vision(detector)
                continue

            response = ollama.send_message(user_input)
            print("🧠 CEREBRO:", response)
            tts.speak(response)

    except KeyboardInterrupt:
        print("\n🛑 CEREBRO apagado.")