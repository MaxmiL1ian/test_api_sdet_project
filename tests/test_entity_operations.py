import allure

from api.models import Entity as EntityModel
from tests.test_data import create_entity_model

class TestEntityOperations: 
    @allure.title("Получение сущности по id")
    @allure.description('Тест проверяет возможность получения сущности по id')
    def test_get_entity(self, api_client, create_test_entity):
        entity_id = create_test_entity["id"]
        original_entity = create_test_entity["entity"]
        
        with allure.step("Получаем сущность по ID и проверяем её данные"):
            entity = api_client.get_entity(entity_id)
            assert entity is not None, "Сущность не найдена"
            
            # Прямое сравнение моделей
            assert entity == original_entity, "Полученная сущность не соответствует ожидаемой"

    @allure.title("Обновление сущности")
    @allure.description('Тест проверяет возможность обновления сущности')
    def test_update_entity(self, api_client, create_test_entity): 
        entity_id = create_test_entity["id"] 
        
        with allure.step("Создаем модель с обновленными данными"):
            update_model = create_entity_model(
                title="Обновленная сущность", 
                verified=False, 
                important_numbers=[4, 5, 6], 
                additional_info="Обновленная информация", 
                additional_number=456
            )
            update_model.id = entity_id
            
        with allure.step("Обновляем сущность и проверяем результат"):
            success = api_client.update_entity(entity_id, update_model)
            assert success, "Не удалось обновить сущность"
            
        with allure.step("Проверяем, что данные действительно обновились"):
            updated_entity = api_client.get_entity(entity_id)
            assert updated_entity is not None, "Не удалось получить обновленную сущность"
            
            # Прямое сравнение моделей
            assert updated_entity == update_model, "Обновленная сущность не соответствует ожидаемой"

    @allure.title("Получение всех сущностей")
    @allure.description('Тест проверяет возможность получения всех сущностей')
    def test_get_all_entities(self, api_client, create_multiple_entities):
        with allure.step("Получаем все сущности"):
            entities_list = api_client.get_all_entities()
        
        with allure.step("Проверяем, что список сущностей получен и содержит наши сущности"):
            assert entities_list is not None, "Не удалось получить список сущностей"
            
            # Получаем список ID из созданных сущностей
            created_ids = [entity["id"] for entity in create_multiple_entities]
            
            # Находим наши созданные сущности в полученном списке
            found_entities = [entity for entity in entities_list.entity if entity.id in created_ids]
            assert found_entities, "Созданные тестовые сущности не найдены в полученном списке"
            
            with allure.step("Проверяем, что данные сущностей соответствуют ожидаемым"):
                # Для каждой найденной сущности проверяем соответствие данных
                for entity in found_entities:
                    # Находим соответствующую сущность из наших тестовых данных
                    original_entity = next(e for e in create_multiple_entities if e["id"] == entity.id)
                    test_entity = original_entity["entity"]
                    
                    # Прямое сравнение моделей с установкой одинакового ID
                    entity_copy = entity.model_copy()
                    test_entity_copy = test_entity.model_copy()
                    entity_copy.id = test_entity_copy.id = None  # Устанавливаем одинаковое значение ID
                    assert entity_copy == test_entity_copy, "Полученная сущность не соответствует ожидаемой"

    @allure.title("Создание новой сущности")
    @allure.description('Тест проверяет возможность создания новой сущности')
    def test_create_entity(self, api_client, cleanup_entity):
        with allure.step("Создаем модель сущности с тестовыми данными"):
            entity_model = create_entity_model(
                title="Новая тестовая сущность",
                verified=True,
                important_numbers=[7, 8, 9],
                additional_info="Информация о новой сущности",
                additional_number=999
            )
        
        with allure.step("Создаем сущность и регистрируем ее для автоматического удаления"):
            entity_id = api_client.create_entity(entity_model)
            cleanup_entity(entity_id)
            assert entity_id is not None, "Не удалось создать сущность"
            
        with allure.step("Проверяем, что сущность создана корректно"):
            created_entity = api_client.get_entity(entity_id)
            assert created_entity is not None, "Не удалось получить созданную сущность"
            
            # Проверка ID отдельно
            assert created_entity.id == entity_id, "ID сущности не соответствует"
            
            # Прямое сравнение моделей с установкой ID в ожидаемой модели
            expected_entity = entity_model.model_copy()
            expected_entity.id = entity_id
            assert created_entity == expected_entity, "Созданная сущность не соответствует ожидаемой"

    @allure.title("Удаление сущности")
    @allure.description('Тест проверяет возможность удаления сущности')
    def test_delete_entity(self, api_client, cleanup_entity): 
        with allure.step("Создаем сущность для проверки удаления"):
            entity_model = create_entity_model(
                title="Тестовая сущность для удаления",
                verified=False,
                important_numbers=[5, 5, 5],
                additional_info="Сущность для удаления",
                additional_number=555
            )
            
            entity_id = api_client.create_entity(entity_model)

            cleanup_entity(entity_id)
            assert entity_id is not None, "Не удалось создать сущность для теста удаления"
            
            # Проверяем, что сущность действительно создана
            entity = api_client.get_entity(entity_id)
            assert entity is not None, "Не удалось получить созданную сущность"
            
        with allure.step("Удаляем сущность и проверяем результат"):
            success = api_client.delete_entity(entity_id)
            assert success, "Не удалось удалить сущность"
            
            # Проверяем, что сущность больше не существует
            entity_after_delete = api_client.get_entity(entity_id)
            assert entity_after_delete is None, "Сущность не была удалена (ожидается, что API вернет 500)"
