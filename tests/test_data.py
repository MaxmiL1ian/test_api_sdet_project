# Базовая сущность
DEFAULT_ENTITY = {
    "addition": {
        "additional_info": "Тестовая информация",
        "additional_number": 123
    },
    "important_numbers": [1, 2, 3],
    "title": "Тестовая сущность",
    "verified": True
}

# Данные для теста обновления
UPDATED_ENTITY = {
    "addition": {
        "additional_info": "Обновленная информация",
        "additional_number": 456
    },
    "important_numbers": [4, 5, 6],
    "title": "Обновленная сущность",
    "verified": False
}

# Сущность для удаления
ENTITY_FOR_DELETE = {
    "addition": {
        "additional_info": "Сущность для удаления",
        "additional_number": 555
    },
    "important_numbers": [5, 5, 5],
    "title": "Тестовая сущность для удаления",
    "verified": False
}

# Данные для теста создания
CREATE_ENTITY = {
    "addition": {
        "additional_info": "Информация о новой сущности",
        "additional_number": 999
    },
    "important_numbers": [7, 8, 9],
    "title": "Новая тестовая сущность",
    "verified": True
}

# Функция для создания нескольких уникальных сущностей
def get_multiple_entities(count=3):
    """
    Создает список из нескольких уникальных тестовых сущностей
    
    Args:
        count (int): Количество создаваемых сущностей
        
    Returns:
        list: Список словарей с данными сущностей
    """
    entities = []
    for i in range(count):
        entity = {
            "addition": {
                "additional_info": f"Информация о сущности {i+1}",
                "additional_number": 100 * (i + 1)
            },
            "important_numbers": [i+1, i+2, i+3],
            "title": f"Тестовая сущность {i+1}",
            "verified": i % 2 == 0  # Чередуем True и False
        }
        entities.append(entity)
    return entities
