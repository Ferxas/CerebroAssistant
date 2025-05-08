import requests
import re

class OllamaClient:
    def __init__(self, model="deepseek-r1:7b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/chat"
        self.system_prompt = {
            "role": "system",
            "content": (
                "Tu nombre es CEREBRO. Eres un cerebro artificial diseñado para conversar exclusivamente en español "
                "con humanos, responder preguntas, observar con visión por computadora y hablar en voz alta. "
                "Estás participando en una feria científica llamada Diverciencia. "
                "Tu creador es Luis Ruiz Román. Nunca hables en otro idioma que no sea español."
            )
        }
        self.history = [self.system_prompt]

    def clean_response(self, raw_text):
        return re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()

    def send_message(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()

            assistant_message = data["message"]["content"]
            cleaned_message = self.clean_response(assistant_message)

            self.history.append({"role": "assistant", "content": cleaned_message})
            return cleaned_message

        except Exception as e:
            print("❌ Error al contactar con Ollama:", e)
            return "Lo siento, hubo un error al intentar pensar."