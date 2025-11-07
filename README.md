# test_api_sdet_project
Этот проект содержит автоматизированные тесты [API сервиса](https://github.com/bondarenkokate73/simbirsoft_sdet_project). Тесты выполняют следующие проверки:
*   Получение сущности по ID; 
*   Получение всех сущностей; 
*   Обновление сущности; 
*   Создание сущности; 
*   Удаление сущности. 

## 📌 Содержание

*   [Структура проекта](#-структура-проекта)
*   [Требования](#-требования)
*   [Установка](#-установка)
*   [Запуск теста](#-запуск-теста) 
*   [Просмотр результатов](#-Просмотр-результатов)

## 📂 Структура проекта 

    ```bash
        test_api_adet_project/
    ├── api/                      # Модуль для работы с API
    │   ├── __init__.py
    │   ├── client.py             # Класс клиента API
    │   ├── endpoints.py          # Эндпоинты API
    │   └── models.py             # Модели данных Pydantic
    │
    ├── config/                   # Конфигурационные настройки
    │   ├── __init__.py
    │   └── settings.py           
    │
    ├── tests/                    # Тесты
    │   ├── __init__.py
    │   ├── conftest.py           # Фикстуры PyTest
    │   ├── test_data.py          # Тестовые данные
    │   └── test_entity_operations.py  
    │
    ├── .gitignore               
    ├── README.md                 
    └── requirements.txt          
    ```

## 🔧 Требования

*   Python 3.12 
*   Git (для клонирования репозитория)

## 🚀 Установка

1.  Клонируйте репозиторий:

    ```bash
    git clone https://github.com/MaxmiL1ian/test_api_sdet_project.git
    ```

2.  Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv .venv
    # Для Windows:
    .venv\Scripts\activate
    # Для Linux/macOS:
    source .venv/bin/activate
    ```

3.  Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## ⚡ Запуск теста

Выполните команду:

```bash
pytest tests/test_entity_operations.py --alluredir=./allure-results
```

Также проект поддерживает параллельный запуск тестов:

```bash
pytest -n auto tests/test_entity_operations.py --alluredir=./allure-results
```
## 🔎 Просмотр результатов

Выполните команду:

```bash
allure serve  (Путь до директории)/allure-results
```
