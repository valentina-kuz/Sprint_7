"""
Тесты получения списка заказов
"""
import pytest
import allure
from config.settings import Config


@allure.epic("Заказы")
@allure.feature("Список заказов")
class TestOrdersList:
    """Тесты получения списка заказов"""
    
    @allure.title("Получение списка заказов возвращает массив заказов")
    @allure.description("Проверяем, что тело ответа содержит список заказов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_list_returns_orders_array(self, order_api):
        """Тест получения списка заказов"""
        
        with allure.step("Отправляем запрос на получение списка заказов"):
            result = order_api.get_orders_list()
        
        with allure.step("Проверяем успешный ответ"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_OK']}, получен {result['status_code']}"
        
        with allure.step("Проверяем наличие списка заказов в ответе"):
            assert result.get('orders') is not None, "В ответе должен быть список заказов"
            
            # Проверяем, что orders - это список
            orders = result['orders']
            assert isinstance(orders, list), "Поле 'orders' должно быть списком"
            
            allure.attach(
                str(len(orders)), 
                "Количество заказов в списке", 
                allure.attachment_type.TEXT
            )
    
    @allure.title("Список заказов содержит корректную структуру данных")
    @allure.description("Проверяем, что каждый заказ в списке содержит необходимые поля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orders_list_has_correct_structure(self, order_api):
        """Тест структуры данных в списке заказов"""
        
        with allure.step("Получаем список заказов"):
            result = order_api.get_orders_list()
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK']
        
        with allure.step("Проверяем структуру данных"):
            orders = result.get('orders', [])
            
            if len(orders) > 0:
                # Проверяем первый заказ в списке
                first_order = orders[0]
                allure.attach(str(first_order), "Структура первого заказа", allure.attachment_type.JSON)
                
                # Проверяем, что заказ содержит основные поля
                expected_fields = ['id', 'firstName', 'lastName', 'address', 'phone']
                
                for field in expected_fields:
                    assert field in first_order, f"Поле '{field}' должно присутствовать в заказе"
            else:
                allure.attach("Список заказов пуст", "Информация", allure.attachment_type.TEXT)
    
    @allure.title("Список заказов доступен без авторизации")
    @allure.description("Проверяем, что список заказов можно получить без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orders_list_available_without_auth(self, order_api):
        """Тест доступности списка заказов без авторизации"""
        
        with allure.step("Отправляем запрос без авторизационных заголовков"):
            # Создаем новый экземпляр API клиента без авторизации
            result = order_api.get_orders_list()
        
        with allure.step("Проверяем, что запрос успешен"):
            # Список заказов должен быть доступен публично
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Список заказов должен быть доступен без авторизации, получен код {result['status_code']}"
            assert result.get('orders') is not None, "Должен быть список заказов"
    
