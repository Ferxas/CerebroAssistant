import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.set_spanish_voice()
        self.engine.setProperty('rate', 160)

    def set_spanish_voice(self):
        voices = self.engine.getProperty('voices')
        selected = None

        for voice in voices:
            name = voice.name.lower()
            langs = [l.decode().lower() if isinstance(l, bytes) else l.lower() for l in getattr(voice, "languages", [])]
            if "spanish" in name or any("es" in lang for lang in langs) or "spanish" in voice.id.lower():
                selected = voice
                break

        if selected:
            self.engine.setProperty('voice', selected.id)
            print(f"✅ Voz en español seleccionada: {selected.name}")
        else:
            print("❌ No se encontró una voz en español. Revisa la configuración de voces en tu sistema.")

    def speak(self, text):
        print("🔈 Hablando...")
        self.engine.say(text)
        self.engine.runAndWait()
