from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOllama(
    model="mistral",
    temperature=0,
    num_predict=150
)


messages = [
    ("system", "You are an expert in {domain}. Your task is answer the question as short as possible"),
    MessagesPlaceholder("history"),
]
prompt_template = ChatPromptTemplate(messages)


domain = input('Choice domain area: ')
history = []
while True:
    print()
    user_content = input('You: ')
    history.append(HumanMessage(content=user_content))
    full_ai_content = ""
    print('Ai: ', end="")

    # Чтобы укоротить память.
    trimmed_history = trim_messages( 
        messages=history, 
        strategy="last", # Отвечает за способ извлечения сообщений, может быть last, тогда извлекаются последние сообщения, может быть first, тогда извлекаются первые сообщения
        token_counter=len, # Отвечает за то, как считаются токены для сообщения. В данном случае установлена функция len, что означает, 
        # что одно сообщение будет эквивалентно одному токену. Может быть установлена конкретная LLM, тогда количество токенов для сообщения рассчитывается на основании модели
        max_tokens=10,  # Ограничиваем историю 10 последними сообщениями
        include_system=False, # Системное сообщение уже есть в шаблоне промпта
        allow_partial=False # Позволяет указать, что разрешается обрезать сообщения, если они не влезают по токену и в качестве token_counter установлена LLM
    )

    prompt_value = prompt_template.invoke({"domain": domain, "history": trimmed_history})
    for ai_message_chunk in llm.stream(prompt_value.to_messages()):
        print(ai_message_chunk.content, end="")
        full_ai_content += ai_message_chunk.content

    history.append(AIMessage(content=full_ai_content))
    print()

#Идеи для улучшения
# - Сделать зарезервированное слово для окончания разговора
# - Случайно менять область экспертности модели на каждой итерации
# + Передавать не всю историю сообщений, а только последние 10 сообщений
