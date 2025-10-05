#API_KEY = "a9WI7WF5a1H4epzelCJOd8adPkkGLTFc" # ключ доступа к API
#MODEL_NAME = "mistral-large-latest" # название модели
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from pydantic import Field
from langchain_core.messages import HumanMessage

# вместо базы данных
ORDERS_STATUSES_DATA = {
    "a42": "Доставляется",
    "b61": "Выполнен",
    "k37": "Отменен",
}


#@tool — это декоратор, который автоматически превращает вашу обычную Python-функцию в полноценный Tool — инструмент, который языковая модель (LLM) может понимать и использовать

#Представьте, что у вас есть функция, и вы хотите, чтобы ИИ мог ею пользоваться. 
# Для этого ему нужно объяснить: что эта функция делает, какие параметры принимает и что возвращает. 
# Без @tool вам пришлось бы вручную создавать схему (например, на Pydantic) для описания этих правил. Декоратор @tool делает всю эту рутинную работу за вас.
@tool
def get_order_status(order_id: str = Field(description="Identifier of order")) -> str:
    #  это крайне важно. Декоратор использует ее как описание всего инструмента.
    #  Модель читает это описание, чтобы решить, нужно ли вызывать эту функцию для ответа на вопрос пользователя. Без docstring инструмент не будет работать правильно.
    """Get status of order by order identifier"""
    return ORDERS_STATUSES_DATA.get(order_id, f"Не существует заказа")

llm = ChatOllama(
    model="mistral",
    temperature=0
)

llm_with_tools = llm.bind_tools([get_order_status])
ai_message = llm_with_tools.invoke("What about my order with id equal to k37?")

for tool_call in ai_message.tool_calls:
    if tool_call["name"] == get_order_status.name:
        tool_message = get_order_status.invoke(tool_call)

result = llm_with_tools.invoke([
    HumanMessage("What about my order with id equal to k37?"),
    ai_message,
    tool_message
])