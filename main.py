from audio.whisper_listener import WhisperListener
from llm.ollama_client import OllamaClient
from audio.tts import TextToSpeech
from vision.yolov_detector import YOLOvDetector
import threading

def start_vision(detector):
    detector.run()

if __name__ == "__main__":
    print("Iniciando sistema CEREBRO...")

    # Inicializar componentes
    whisper_listener = WhisperListener()
    ollama = OllamaClient()
    tts = TextToSpeech()
    detector = YOLOvDetector()

    # Esperar palabra clave "cerebro"
    whisper_listener.wait_for_trigger()

    # Una vez activado:
    print("Activado. CEREBRO está en línea.")
    tts.speak("Hola, soy CEREBRO. Estoy en línea y listo para ayudarte.")

    # Iniciar visión por computadora en segundo plano
    vision_thread = threading.Thread(target=start_vision, args=(detector,), daemon=True)
    vision_thread.start()

    # Bucle principal de conversación
    try:
        while True:
            print("🎤 Esperando entrada de voz...")
            whisper_listener.running = False
            whisper_listener.wait_for_trigger()  # Espera nuevo input

            # Transcribe la nueva frase (después de activación)
            print("🔄 Transcribiendo nueva entrada...")
            whisper_listener.running = True
            whisper_listener._listen_audio()  # Reutilizamos método privado
            user_input = " ".join(whisper_listener.model.transcribe(
                whisper_listener.q.get(), fp16=False, language='es')["text"].split())

            # Enviar a Ollama
            response = ollama.send_message(user_input)
            print("🧠 CEREBRO:", response)

            # Decir la respuesta
            tts.speak(response)

            # Mostrar lo que ve
            seen = detector.get_last_seen()
            if seen:
                print("👁️ CEREBRO ve:", seen)
    except KeyboardInterrupt:
        print("\n🛑 CEREBRO apagado.")