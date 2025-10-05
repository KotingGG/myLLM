# LangGraph

#Создание агентных приложений с использованием AgentExecutor является устаревшим, но еще работающим способом. 
# Разработчики LangChain создали специализированную библиотеку LangGraph, заточенную на построение агентных и мультиагентных систем 
# (несколько взаимодействующих между собой агентов).

#Особенности:
# Компоненты LangChain могут использоваться в LangGraph
# Возможность управления состоянием
# Возможность построения более предсказуемых процессов
# Гибкая маршрутизация запросов
# Встроенные механизмы для визуализации

#LangGraph - это фреймворк для создания LLM-приложений на базе графов. 
# Каждый узел графа представляет собой операцию: 
# вызов LLM или выполнение какой-то предопределенной функции. 
# Каждое ребро содержит направление и отвечает за связывание между собой узлов.


import random
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# --------------------------------- State ---------------------------------------
#Состояние (State) представляет словарь с информацией, 
# которая может быть полезна при реализации процесс обработки запроса пользователя. 
# Она включает изначальный запрос, а также другие поля, которые мы можем указать.

class State(TypedDict):
    query: str
    resolver: str
    answer: str


# --------------------------------- Nodes ---------------------------------------
#Узел графа (Node) это функция, которая принимает состояние как аргумент и возвращает измененное состояние. 
# Функция может выполнять любую операцию: вызов LLM, вызов тулов, определение следующего узла для обработки, 
# какая-то специфическая логика (например, отправка электронного письма).

def choice_resolver(state: State) -> State:
    resolver = "support" if random.random() > 0.5 else "llm"
    state["resolver"] = resolver
    return state


def send_to_support(state: State) -> State:
    print(f"New message for Support: {state['query']}")
    return state


def llm(state: State) -> State:
    messages = [
        ("system", "You are a friendly chatbot. Your task is answer the question as short as possible"),
        ("human", "{question}"),
    ]
    prompt = ChatPromptTemplate(messages)
    mistral = ChatOllama(
        model="mistral",
        temperature=0
    )
    chain = prompt | mistral | StrOutputParser()
    answer = chain.invoke({"question": state["query"]})
    state["answer"] = answer
    return state


def send_to_user(state: State) -> State:
    print(f"New message for User: {state['answer']}")
    return state


# --------------------------------- Edges ---------------------------------------
#Ребро графа (Edge) это способ связать узлы графа друг с другом. Они могут быть двух видов:

#  Direct: соединяет один узел с другим напрямую (в примере выше это llm -> send_to_user)
#  Conditional: содержит логику по определению следующего узла для обработки (в примере выше это choice_resolver -> {send_to_support | llm})

#В качестве примера напишем условное ребро, которое будет по полю resolver в state отправлять запрос на обработку в соответствующий узел. 
# На самом деле логику по определению исполнителя мы могли бы реализовать прям здесь, это бы и сократило общий код и позволило бы избавиться от лишнего поля в состоянии. 
# Заметим, что возвращаемым значением является название узла.

def route_by_resolver(state: State) -> Literal["send_to_support", "llm"]:
    if state["resolver"] == "support":
        return "send_to_support"
    else:
        return "llm"


# ---------------------------- Graph Building -----------------------------------
# Сборка графа. Для запуска процесса необходимо собрать граф, указав узлы и связи между ними.

builder = StateGraph(State)
builder.add_node("choice_resolver", choice_resolver)
builder.add_node("send_to_support", send_to_support)
builder.add_node("llm", llm)
builder.add_node("send_to_user", send_to_user)

builder.add_edge(START, "choice_resolver")
builder.add_conditional_edges("choice_resolver", route_by_resolver)
builder.add_edge("send_to_support", END)
builder.add_edge("llm", "send_to_user")
builder.add_edge("send_to_user", END)

graph = builder.compile()


# ------------------------ Graph Visualization ---------------------------------
# Визуализация графа
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())


# ------------------------ Graph Invoke ---------------------------------
# Запуск графа
result = graph.invoke({"query" : "Hi, my computer is not working!"})
print(result)