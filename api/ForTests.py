from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# В коде ниже мы инициализируем значения для session_id и создаем объект пустой истории сообщений для единственного пользователя приложения. 
# В историю сообщений будут попадать сообщения пользователя и ответы модели.
DEFAULT_SESSION_ID = "default"
chat_history = InMemoryChatMessageHistory()


messages = [
    ("system", "You are an expert in {domain}. Your task is answer the question as short as possible"),
    MessagesPlaceholder("history"), # включаем историю
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=10,
    start_on="human",
    end_on="human",
    include_system=True,
    allow_partial=False
)

llm = ChatOllama(
    model="mistral",
    temperature=0,
    num_predict=150
)

# Наибольший интерес представляет итоговая цепочка Runnable-объектов. Для наглядности сначала составляется цепочка из промпта, триммера и модели. 
# Её входными данными будет словарь с доменом (domain), новым сообщением пользователя (question) и историей прошлого взаимодействия (history). 
# Выходным результатом этой цепочки будет сообщение-ответ модели типа AIMessage.
chain = prompt | trimmer | llm

# Как мы знаем, цепочка Runnable-компонентов также является Runnable-компонентом, поэтому мы её можем использовать в RunnableWithMessageHistory. 
# Заметим, что здесь используется параметр history_messages_key, который задает то, по какому ключу будут лежать данные о истории сообщений. 
# Другой параметр input_messages_key используется для того, чтобы указать, что входными данными для RunnableWithMessageHistory является словарь, 
# поэтому в качестве значения параметра используется один из ключей во входном словаре, например, question.
chain_with_history = RunnableWithMessageHistory(
    chain, lambda session_id: chat_history,
    input_messages_key="question", history_messages_key="history"
)

# Итоговая цепочка завершается с помощью Output Parser, который берет из выходного сообщения только текст контента ответа модели.
final_chain = chain_with_history | StrOutputParser()


domain = input('Choice domain area: ')
while True:
    print() # для красоты
    user_question = input('You: ')
    print('Ai: ', end="")
    for answer_chunk in final_chain.stream(
            {"domain": domain, "question": user_question},
            config={"configurable": {"session_id": DEFAULT_SESSION_ID}},
    ):
        print(answer_chunk, end="")
    print() # для красоты