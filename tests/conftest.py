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
                if delete_response.status_code not in 204:
                    print(f"Предупреждение: не удалось удалить тестовую сущность с ID {entity_id}")
            except Exception as e:
                print(f"Ошибка при удалении тестовой сущности: {str(e)}")