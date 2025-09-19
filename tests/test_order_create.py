"""
Тесты создания заказов
"""
import pytest
import allure
from config.settings import Config
from data.test_data import OrderTestData


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestOrderCreate:
    """Тесты создания заказов"""
    
    @allure.title("Можно создать заказ с разными вариантами цвета")
    @allure.description("Проверяем, что можно создать заказ с BLACK, GREY, обоими цветами или без цвета")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("color_option", OrderTestData.COLOR_OPTIONS[:4],  # Исключаем последний вариант для отдельного теста
                           ids=[opt.get("description", "без поля color") for opt in OrderTestData.COLOR_OPTIONS[:4]])
    def test_create_order_with_different_colors(self, order_api, data_generator, color_option):
        """Тест создания заказа с разными цветами"""
        
        # Генерируем базовые данные заказа
        order_data = data_generator.generate_order_data()
        
        # Добавляем цвет из параметра
        if "color" in color_option:
            order_data["color"] = color_option["color"]
        
        color_description = color_option.get("description", "без поля color")
        
        with allure.step(f"Создаем заказ {color_description}"):
            allure.attach(str(order_data), f"Данные заказа ({color_description})", allure.attachment_type.JSON)
            result = order_api.create_order(order_data)
        
        with allure.step("Проверяем успешное создание заказа"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
        
        # Очистка: отменяем заказ
        with allure.step("Отменяем созданный заказ"):
            if result.get('track'):
                try:
                    order_api.cancel_order(str(result['track']))
                except Exception:
                    # Игнорируем ошибки отмены в cleanup
                    pass
    
    @allure.title("Ответ содержит track при успешном создании заказа")
    @allure.description("Проверяем, что в ответе на создание заказа содержится track номер")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_response_contains_track(self, order_api, data_generator):
        """Тест наличия track в ответе"""
        
        order_data = data_generator.generate_order_data()
        
        with allure.step("Создаем заказ"):
            result = order_api.create_order(order_data)
        
        with allure.step("Проверяем наличие track в ответе"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE']
            assert 'track' in result['response_text'], "В тексте ответа должно быть слово 'track'"
            assert result.get('track') is not None, "Track не должен быть пустым"
            assert isinstance(result['track'], int), "Track должен быть числом"
            
            # Дополнительная проверка track поля
            assert result.get('track') is not None, "Track должен быть в результате"
        
        # Очистка
        with allure.step("Отменяем созданный заказ"):
            if result.get('track'):
                try:
                    order_api.cancel_order(str(result['track']))
                except Exception:
                    pass
    
    @allure.title("Можно создать заказ с комбинацией BLACK и GREY")
    @allure.description("Проверяем, что можно создать заказ с двумя цветами одновременно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_both_colors(self, order_api, data_generator):
        """Тест создания заказа с двумя цветами"""
        
        order_data = data_generator.generate_order_data()
        order_data["color"] = ["BLACK", "GREY"]
        
        with allure.step("Создаем заказ с BLACK и GREY цветами"):
            allure.attach(str(order_data), "Данные заказа с двумя цветами", allure.attachment_type.JSON)
            result = order_api.create_order(order_data)
        
        with allure.step("Проверяем успешное создание"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE']
            assert result.get('track') is not None
        
        # Очистка
        with allure.step("Отменяем созданный заказ"):
            if result.get('track'):
                try:
                    order_api.cancel_order(str(result['track']))
                except Exception:
                    pass
