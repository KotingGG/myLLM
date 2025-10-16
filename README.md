# TrainingLLM

Данный репозиторий используется исключительно для обучения. Главный объект обучения - **LLM (Large Language Model)**. 
Обучение происходит параллельно с изучением [бесплатного курса](https://stepik.org/course/215591/info) на площадке **Stepik**. 

## Предварительные требования

1. **Для запуска локального LLM: Ollama** с [официального сайта](https://ollama.ai/).
2. **Необходимая LLM-модель** через Ollama. Для этого проекта используется `mistral 7B` (базовый):
```bash
ollama run mistral
```
3. **Фреймфорки, библиотеки:** 
- Используются до жути много библиотек, ведь тестируются разные методы. Самые популярные:
```bash
pip install langchain
pip install langchain_ollama
pip install langchain_community
pip install langchain_core
pip install langgraph
pip install pydantic
```
# Другое

Для удобства и в целях обучения сделана простейшая архитектура (если вот ЭТО можно так назвать).