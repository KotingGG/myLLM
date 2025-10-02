from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(
    model="mistral",
    temperature=0,
)
messages = [
    SystemMessage(content="You translate Russian to English. Translate the user sentence and write only result:"),
    HumanMessage(content="Я создам успешный AI-продукт!")
]

user_message = "Где растут кактусы?"
answer = llm.invoke(user_message)
print(answer.content)