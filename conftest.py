"""
Конфигурация pytest и фикстуры для тестов
"""
import pytest
import allure
from helpers.courier_api import CourierAPI
from helpers.order_api import OrderAPI
from helpers.data_generator import DataGenerator
from config.settings import Config


@pytest.fixture(scope="session")
def courier_api():
    """Фикстура для API курьеров"""
    return CourierAPI()


@pytest.fixture(scope="session")
def order_api():
    """Фикстура для API заказов"""
    return OrderAPI()


@pytest.fixture(scope="session")
def data_generator():
    """Фикстура для генератора данных"""
    return DataGenerator()


@pytest.fixture
def courier_for_tests(courier_api, data_generator):
    """
    Фикстура создает курьера перед тестом и удаляет после
    Возвращает данные созданного курьера включая ID
    """
    # Создаем курьера
    courier_data = data_generator.generate_courier_data()
    
    with allure.step(f"Создаем курьера для тестов: {courier_data['login']}"):
        result = courier_api.create_and_login_courier(courier_data)
        
        if not result['success']:
            pytest.fail(f"Не удалось создать курьера для тестов: {result.get('error')}")
    
    yield result
    
    # Удаляем курьера после теста
    if result.get('courier_id'):
        with allure.step(f"Удаляем курьера после теста: {courier_data['login']}"):
            courier_api.delete_courier(str(result['courier_id']))


@pytest.fixture
def order_for_tests(order_api, data_generator):
    """
    Фикстура создает заказ перед тестом
    Возвращает данные созданного заказа
    """
    # Создаем заказ
    order_data = data_generator.generate_order_data()
    
    with allure.step("Создаем заказ для тестов"):
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для тестов: {result}")
    
    order_info = {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    yield order_info
    
    # Отменяем заказ после теста (если есть track)
    if order_info.get('track'):
        with allure.step("Отменяем заказ после теста"):
            try:
                order_api.cancel_order(str(order_info['track']))
            except Exception:
                # Игнорируем ошибки отмены заказа в cleanup
                pass


@pytest.fixture
def courier_and_order_for_tests(courier_for_tests, order_for_tests):
    """
    Фикстура создает курьера и заказ для тестов
    Используется для тестов принятия заказа
    """
    return {
        'courier': courier_for_tests,
        'order': order_for_tests
    }
