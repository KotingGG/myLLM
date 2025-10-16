from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


knowledge_store = [
    Document(page_content="Большая языковая модель это языковая модель, состоящая из нейронной сети со множеством параметров (обычно миллиарды весовых коэффициентов и более), обученной на большом количестве неразмеченного текста с использованием обучения без учителя.")
]

retriever = BM25Retriever.from_documents(knowledge_store)


def format_documents(documents: list[Document]):
    return "\n\n".join(doc.page_content for doc in documents)


prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an assistant for QA. Use the following pieces of retrieved context to answer the question. "
       "If you don't know the answer, just say that you don't know. Answer as short as possible. "
       "Context: {context} \nQuestion: {question}"
        )
    )
])

llm = ChatOllama(
    model="mistral",
    temperature=0
)


chain = RunnableParallel(
    context=retriever | format_documents, question=lambda data: data
) | prompt | llm | StrOutputParser()
result = chain.invoke("Что такое большая языковая модель?")
print(result)