from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate


messages = [
    ("system", "You are helpful assistant. Current date: {current_date} and time: {current_time}"),
    ("human", "Какое сейчас время?"),
]
prompt_template = ChatPromptTemplate(messages)

current_datetime = datetime.now()
prompt_value = prompt_template.invoke(
    {"current_date": current_datetime.date(), "current_time": current_datetime.time()}
)
print(prompt_value.to_messages())
# [
#    SystemMessage(content='You are helpful assistant. Current date: 2025-10-02 and time: 17:44:17.146247', ..), 
#    HumanMessage(content='Какое сейчас время?', ...)
#]