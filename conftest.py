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


@pytest.fixture
def courier_for_deletion_test(courier_api):
    """
    Фикстура создает курьера для тестов удаления
    Используется когда нужно протестировать удаление курьера
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем курьера
    courier_data = data_generator.generate_courier_data()
    
    with allure.step(f"Создаем курьера для теста удаления: {courier_data['login']}"):
        result = courier_api.create_and_login_courier(courier_data)
        
        if not result['success']:
            pytest.fail(f"Не удалось создать курьера для теста удаления: {result.get('error')}")
    
    yield {
        'courier_data': courier_data,
        'courier_id': result['courier_id'],
        'create_result': result
    }


@pytest.fixture
def courier_for_creation_test(courier_api):
    """
    Фикстура создает курьера только для тестов создания
    Используется когда нужно проверить создание курьера
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем курьера
    courier_data = data_generator.generate_courier_data()
    
    with allure.step(f"Создаем курьера для теста создания: {courier_data['login']}"):
        result = courier_api.create_courier(courier_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать курьера для теста: {result}")
    
    yield {
        'courier_data': courier_data,
        'create_result': result
    }
    
    # Удаляем курьера после теста
    with allure.step(f"Удаляем курьера после теста создания: {courier_data['login']}"):
        try:
            login_data = data_generator.generate_courier_login_data(
                courier_data['login'], courier_data['password']
            )
            login_result = courier_api.login_courier(login_data)
            if login_result.get('courier_id'):
                courier_api.delete_courier(str(login_result['courier_id']))
        except Exception:
            # Игнорируем ошибки удаления в cleanup
            pass


@pytest.fixture
def courier_for_tests(courier_api):
    """
    Фикстура создает курьера перед тестом и удаляет после
    Возвращает данные созданного курьера включая ID
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
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
def order_with_black_color(order_api):
    """
    Фикстура создает заказ с черным цветом для тестов
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ с черным цветом
    order_data = data_generator.generate_order_data()
    order_data["color"] = ["BLACK"]
    
    with allure.step("Создаем заказ с черным цветом"):
        allure.attach(str(order_data), "Данные заказа с черным цветом", allure.attachment_type.JSON)
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ с черным цветом после теста"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass


@pytest.fixture
def order_with_grey_color(order_api):
    """
    Фикстура создает заказ с серым цветом для тестов
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ с серым цветом
    order_data = data_generator.generate_order_data()
    order_data["color"] = ["GREY"]
    
    with allure.step("Создаем заказ с серым цветом"):
        allure.attach(str(order_data), "Данные заказа с серым цветом", allure.attachment_type.JSON)
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ с серым цветом после теста"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass


@pytest.fixture
def order_with_both_colors(order_api):
    """
    Фикстура создает заказ с обоими цветами для тестов
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ с обоими цветами
    order_data = data_generator.generate_order_data()
    order_data["color"] = ["BLACK", "GREY"]
    
    with allure.step("Создаем заказ с обоими цветами"):
        allure.attach(str(order_data), "Данные заказа с обоими цветами", allure.attachment_type.JSON)
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ с обоими цветами после теста"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass


@pytest.fixture
def order_without_color(order_api):
    """
    Фикстура создает заказ без цвета для тестов
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ без цвета
    order_data = data_generator.generate_order_data()
    order_data["color"] = []
    
    with allure.step("Создаем заказ без цвета"):
        allure.attach(str(order_data), "Данные заказа без цвета", allure.attachment_type.JSON)
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ без цвета после теста"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass


@pytest.fixture
def order_without_color_field(order_api):
    """
    Фикстура создает заказ без поля color для тестов
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ без поля color
    order_data = data_generator.generate_order_data()
    # Не добавляем поле color вообще
    
    with allure.step("Создаем заказ без поля color"):
        allure.attach(str(order_data), "Данные заказа без поля color", allure.attachment_type.JSON)
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ без поля color после теста"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass

@pytest.fixture
def order_for_creation_test(order_api):
    """
    Фикстура создает заказ только для тестов создания
    Используется когда нужно проверить создание заказа
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
    # Создаем заказ
    order_data = data_generator.generate_order_data()
    
    with allure.step("Создаем заказ для теста создания"):
        result = order_api.create_order(order_data)
        
        if result['status_code'] != Config.STATUS_CODES['SUCCESS_CREATE']:
            pytest.fail(f"Не удалось создать заказ для теста: {result}")
    
    yield {
        'order_data': order_data,
        'track': result.get('track'),
        'create_result': result
    }
    
    # Отменяем заказ после теста
    if result.get('track'):
        with allure.step("Отменяем заказ после теста создания"):
            try:
                order_api.cancel_order(str(result['track']))
            except Exception:
                # Игнорируем ошибки отмены в cleanup
                pass


@pytest.fixture
def order_for_tests(order_api):
    """
    Фикстура создает заказ перед тестом
    Возвращает данные созданного заказа
    """
    # Создаем генератор данных
    data_generator = DataGenerator()
    
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
