import pytest
import allure

from api.entity_client import EntityClient
from config.settings import API_URL 
from tests.test_data import create_entity_model


@pytest.fixture
def cleanup_entity(api_client):
    """
    Фикстура для очистки созданных сущностей после теста.
    
    """
    entity_ids = []
    
    # Функция для добавления id сущностей, которые нужно удалить
    def add(entity_id):
        if entity_id:
            entity_ids.append(entity_id)
    
    yield add
    
    # Удаляем все созданные сущности после завершения теста
    with allure.step("Удаляем созданные сущности"):
        for entity_id in entity_ids:
            try:
                success = api_client.delete_entity(entity_id)
                if not success:
                    print(f"Предупреждение: не удалось удалить тестовую сущность с ID {entity_id}")
            except Exception as e:
                print(f"Ошибка при удалении тестовой сущности: {str(e)}")

@pytest.fixture
def api_client():
    client = EntityClient(API_URL)
    yield client

@pytest.fixture
def create_test_entity(api_client, cleanup_entity):
    """
    Создает тестовую сущность с уникальными данными и возвращает модель Entity.
    Автоматически удаляет созданную сущность после завершения теста.
    """
    # Создаем модель сущности с дефолтными значениями
    entity_model = create_entity_model()
    
    with allure.step("Создаем сущность"):
        # Создание сущности
        entity_id = api_client.create_entity(entity_model)
        assert entity_id is not None, "Не удалось создать тестовую сущность"
        
        # Регистрируем ID сущности для автоматической очистки
        cleanup_entity(entity_id)
        
        # Получаем созданную сущность с сервера
        created_entity = api_client.get_entity(entity_id)
        
        # Создаем структуру данных для теста
        test_data = {
            "id": entity_id,
            "entity": created_entity,  # Полученная сущность
        }
        
        # Передаем данные сущности в тест
        yield test_data


@pytest.fixture
def create_multiple_entities(api_client, cleanup_entity, count=3):
    """
    Создает несколько тестовых сущностей с моделями Entity и удаляет их после теста.
    Автоматически удаляет созданные сущности после завершения теста.
    
    Args:
        count (int, optional): Количество создаваемых сущностей. По умолчанию 3.
    """
    # Список для хранения данных созданных сущностей
    created_entities = []
    
    with allure.step(f"Создаем {count} сущностей"):
        # Создаем несколько моделей Entity
        for i in range(count):
            # Создаем модель с уникальными данными
            entity_model = create_entity_model(
                title=f"Тестовая сущность {i+1}",
                verified=i % 2 == 0,  # Чередуем True и False
                important_numbers=[i+1, i+2, i+3],
                additional_info=f"Информация о сущности {i+1}",
                additional_number=100 * (i + 1)
            )
            
            # Создаем сущность на сервере
            entity_id = api_client.create_entity(entity_model)
            assert entity_id is not None, "Не удалось создать тестовую сущность"
            
            # Регистрируем ID для автоматической очистки
            cleanup_entity(entity_id)
            
            # Получаем созданную сущность
            created_entity = api_client.get_entity(entity_id)
            
            # Добавляем данные сущности в список
            created_entities.append({
                "id": entity_id,
                "entity": created_entity  # Полученная сущность
            })
        
        # Передаем список созданных сущностей в тест
        yield created_entities
