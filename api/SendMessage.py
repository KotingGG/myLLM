# Отправка сообщения модели
import json
import requests


OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
SEND_MESSAGE_URL = "api/generate"
URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/{SEND_MESSAGE_URL}"

MODEL_NAME = "mistral"
PROMPT = "How are you?" # Сообщение пользователя
PARAMETERS = {
    "model": MODEL_NAME,
    "prompt": PROMPT,
    "stream": False, # Определяет, как будет возвращаться ответ
}

response = requests.post(url=URL, json=PARAMETERS)
data = response.json()
print(json.dumps(data, indent=4))