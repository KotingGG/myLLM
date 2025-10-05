from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from pydantic import Field

ORDERS_STATUSES_DATA = {
    "a42": "Доставляется",
    "b61": "Выполнен",
    "k37": "Отменен",
}

@tool
def get_order_status(order_id: str = Field(description="Identifier of order")) -> str:
    #  это крайне важно. Декоратор использует ее как описание всего инструмента.
    #  Модель читает это описание, чтобы решить, нужно ли вызывать эту функцию для ответа на вопрос пользователя. Без docstring инструмент не будет работать правильно.
    """Get status of order by order identifier"""
    return ORDERS_STATUSES_DATA.get(order_id, f"Не существует заказа")

tools = [get_order_status]
llm = ChatOllama(
    model="mistral",
    temperature=0,
    num_predict=150
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "Твоя задача отвечать на вопросы клиентов об их заказах, используя вызов инструментов. Отвечай пользователю подробно и вежливо."
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(llm, tools, prompt)
# Для демонстрации мы установили параметр verbose=True, чтобы в консоли отображался "ход мыслей“ агента. 
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

memory = InMemoryChatMessageHistory()
agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="output"
)

config = {"configurable": {"session_id": "test-session"}}
while True:
    print()
    user_question = input('You: ')
    answer = agent_with_history.invoke({"input": user_question}, config)
    print("Bot: ", answer["output"])