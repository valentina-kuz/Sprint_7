"""
Тесты создания заказов
"""
import pytest
import allure
from config.settings import Config


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestOrderCreate:
    """Тесты создания заказов"""
    
    
    @allure.title("Ответ содержит track при успешном создании заказа")
    @allure.description("Проверяем, что в ответе на создание заказа содержится track номер")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_response_contains_track(self, order_for_creation_test):
        """Тест наличия track в ответе"""
        
        result = order_for_creation_test['create_result']
        
        with allure.step("Проверяем наличие track в ответе"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE']
            assert 'track' in result['response_text'], "В тексте ответа должно быть слово 'track'"
            assert result.get('track') is not None, "Track не должен быть пустым"
            assert isinstance(result['track'], int), "Track должен быть числом"
            
            assert result.get('track') is not None, "Track должен быть в результате"
    
    @allure.title("Можно создать заказ только с черным цветом")
    @allure.description("Проверяем, что можно создать заказ с цветом BLACK")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_black_color(self, order_with_black_color):
        """Тест создания заказа с черным цветом"""
        
        result = order_with_black_color['create_result']
        
        with allure.step("Проверяем успешное создание заказа с черным цветом"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
    
    @allure.title("Можно создать заказ только с серым цветом")
    @allure.description("Проверяем, что можно создать заказ с цветом GREY")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_grey_color(self, order_with_grey_color):
        """Тест создания заказа с серым цветом"""
        
        result = order_with_grey_color['create_result']
        
        with allure.step("Проверяем успешное создание заказа с серым цветом"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
    
    @allure.title("Можно создать заказ с обоими цветами")
    @allure.description("Проверяем, что можно создать заказ с цветами BLACK и GREY")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_both_colors(self, order_with_both_colors):
        """Тест создания заказа с обоими цветами"""
        
        result = order_with_both_colors['create_result']
        
        with allure.step("Проверяем успешное создание заказа с обоими цветами"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
    
    @allure.title("Можно создать заказ без цвета")
    @allure.description("Проверяем, что можно создать заказ с пустым массивом цветов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_color(self, order_without_color):
        """Тест создания заказа без цвета"""
        
        result = order_without_color['create_result']
        
        with allure.step("Проверяем успешное создание заказа без цвета"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
    
    @allure.title("Можно создать заказ без поля color")
    @allure.description("Проверяем, что можно создать заказ без поля color вообще")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_color_field(self, order_without_color_field):
        """Тест создания заказа без поля color"""
        
        result = order_without_color_field['create_result']
        
        with allure.step("Проверяем успешное создание заказа без поля color"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result.get('track') is not None, "В ответе должен быть track номер"
            assert isinstance(result['track'], int), "Track должен быть числом"
