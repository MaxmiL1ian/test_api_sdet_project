import pytest
from api.client import ApiClient
from config.settings import API_URL 
from api.endpoints import Entity 
from api.models import Entity as EntityModel

@pytest.fixture
def api_client():
    client = ApiClient(API_URL)
    yield client

@pytest.fixture
def test_entity(api_client):
    """
    Создает тестовую сущность
    """
    # Данные для создания сущности
    entity_data = {
        "addition": {
            "additional_info": "Тестовая информация",
            "additional_number": 123
        },
        "important_numbers": [1,2,3],
        "title": "Тестовая сущность",
        "verified": True
        }
    
    entity_id = None
    
    try:
        # Создание сущности
        response = api_client.post(Entity.CREATING_ENTITY, json=entity_data)
        assert response.status_code == 200, f"Не удалось создать тестовую сущность: {response.text}"
        
        # Просто сохраняем ID без попытки десериализации
        entity_id = response.json()
        
        # Создаем структуру данных для теста
        test_data = {
            "id": entity_id,
            "original_data": entity_data,  # Исходные данные для сравнения
        }
        
        # Передаем десериализованную сущность в тест
        yield test_data
    
    finally:
        # Удаляем сущность после завершения теста, если она была создана
        if entity_id:
            try:
                delete_response = api_client.delete(Entity.DELETING_ENTITY.replace("{id}", str(entity_id)))
                if delete_response.status_code != 204:
                    print(f"Предупреждение: не удалось удалить тестовую сущность с ID {entity_id}")
            except Exception as e:
                print(f"Ошибка при удалении тестовой сущности: {str(e)}")


@pytest.fixture
def multiple_test_entities(api_client):
    """
    Создает несколько тестовых сущностей и удаляет их после теста
    """
    # Список для хранения ID созданных сущностей
    entity_ids = []
    # Список для хранения данных созданных сущностей
    created_entities = []
    
    try:
        # Создаем 3 тестовые сущности с разными данными
        for i in range(3):
            entity_data = {
                "addition": {
                    "additional_info": f"Информация о сущности {i+1}",
                    "additional_number": 100 * (i + 1)
                },
                "important_numbers": [i+1, i+2, i+3],
                "title": f"Тестовая сущность {i+1}",
                "verified": i % 2 == 0  # Чередуем True и False
            }
            
            # Создаем сущность
            response = api_client.post(Entity.CREATING_ENTITY, json=entity_data)
            assert response.status_code == 200, f"Не удалось создать тестовую сущность: {response.text}"
            
            # Получаем ID созданной сущности
            entity_id = response.json()
            entity_ids.append(entity_id)
            
            # Добавляем данные сущности в список
            created_entities.append({
                "id": entity_id,
                "original_data": entity_data
            })
        
        # Передаем список созданных сущностей в тест
        yield created_entities
        
    finally:
        # Удаляем все созданные сущности
        for entity_id in entity_ids:
            try:
                delete_response = api_client.delete(Entity.DELETING_ENTITY.replace("{id}", str(entity_id)))
                if delete_response.status_code != 204:  # Исправлена ошибка: not in 204 -> != 204
                    print(f"Предупреждение: не удалось удалить тестовую сущность с ID {entity_id}")
            except Exception as e:
                print(f"Ошибка при удалении тестовой сущности: {str(e)}")
