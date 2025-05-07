import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.set_spanish_voice()
        self.engine.setProperty('rate', 160)

    def set_spanish_voice(self):
        for voice in self.engine.getProperty('voices'):
            lang_info = ""
            if hasattr(voice, "languages") and voice.languages:
                try:
                    lang_info = voice.languages[0].decode().lower()
                except:
                    pass
            if "spanish" in voice.name.lower() or "es" in lang_info or "es" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                print(f"✅ Voz española seleccionada: {voice.name}")
                return
        print("❌ No se encontró una voz en español. Revisa la configuración de voces del sistema.")

    def speak(self, text):
        print("🔈 Hablando...")
        self.engine.say(text)
        self.engine.runAndWait()