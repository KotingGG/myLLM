from openai import OpenAI


API_KEY = "a9WI7WF5a1H4epzelCJOd8adPkkGLTFc" # ключ доступа к API
BASE_URL = "https://api.mistral.ai/v1" # URL самого API 
MODEL_NAME = "mistral-large-latest" # название модели


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

message = "Как работает твой код?"

# выполняет сетевой запрос с указанными данными и возвращает ответ от LLM
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message,
        }
    ],
    model=MODEL_NAME,
    temperature=0.1
)

print(chat_completion.choices[0].message.content)