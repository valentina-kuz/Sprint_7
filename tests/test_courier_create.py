"""
Тесты создания курьеров
"""
import pytest
import allure
from config.settings import Config
from data.test_data import CourierTestData, ResponseMessages


@allure.epic("Курьеры")
@allure.feature("Создание курьера")
class TestCourierCreate:
    """Тесты создания курьеров"""
    
    @allure.title("Успешное создание курьера")
    @allure.description("Проверяем, что курьера можно создать с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, courier_api, data_generator):
        """Тест успешного создания курьера"""
        
        # Генерируем данные курьера
        courier_data = data_generator.generate_courier_data()
        
        with allure.step("Отправляем запрос на создание курьера"):
            allure.attach(str(courier_data), "Данные курьера", allure.attachment_type.JSON)
            result = courier_api.create_courier(courier_data)
        
        with allure.step("Проверяем успешный ответ"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_CREATE']}, получен {result['status_code']}"
            assert result['response_text'] == ResponseMessages.COURIER_CREATED_SUCCESS, \
                f"Ожидался ответ {ResponseMessages.COURIER_CREATED_SUCCESS}, получен {result['response_text']}"
        
        # Очистка: логинимся и удаляем курьера
        with allure.step("Удаляем созданного курьера"):
            login_data = data_generator.generate_courier_login_data(
                courier_data['login'], courier_data['password']
            )
            login_result = courier_api.login_courier(login_data)
            if login_result.get('courier_id'):
                courier_api.delete_courier(str(login_result['courier_id']))
    
    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("Проверяем, что нельзя создать двух курьеров с одинаковыми данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_courier_fails(self, courier_api, data_generator):
        """Тест создания дубликата курьера"""
        
        # Генерируем данные курьера
        courier_data = data_generator.generate_courier_data()
        
        with allure.step("Создаем первого курьера"):
            first_result = courier_api.create_courier(courier_data)
            assert first_result['status_code'] == Config.STATUS_CODES['SUCCESS_CREATE']
        
        with allure.step("Пытаемся создать курьера с теми же данными"):
            allure.attach(str(courier_data), "Данные дубликата курьера", allure.attachment_type.JSON)
            second_result = courier_api.create_courier(courier_data)
        
        with allure.step("Проверяем ошибку дублирования"):
            assert second_result['status_code'] == Config.STATUS_CODES['CONFLICT'], \
                f"Ожидался код {Config.STATUS_CODES['CONFLICT']}, получен {second_result['status_code']}"
            assert ResponseMessages.COURIER_LOGIN_EXISTS in second_result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_LOGIN_EXISTS}', получен {second_result['response_text']}"
        
        # Очистка: удаляем первого курьера
        with allure.step("Удаляем первого курьера"):
            login_data = data_generator.generate_courier_login_data(
                courier_data['login'], courier_data['password']
            )
            login_result = courier_api.login_courier(login_data)
            if login_result.get('courier_id'):
                courier_api.delete_courier(str(login_result['courier_id']))
    
    @allure.title("Создание курьера без обязательных полей возвращает ошибку")
    @allure.description("Проверяем, что создание курьера без обязательных полей возвращает ошибку 400")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("test_case", CourierTestData.INVALID_COURIER_DATA_SETS, 
                           ids=[case["description"] for case in CourierTestData.INVALID_COURIER_DATA_SETS])
    def test_create_courier_without_required_fields_fails(self, courier_api, test_case):
        """Тест создания курьера без обязательных полей"""
        
        courier_data = test_case["data"]
        description = test_case["description"]
        
        with allure.step(f"Отправляем запрос на создание курьера {description}"):
            allure.attach(str(courier_data), f"Невалидные данные ({description})", allure.attachment_type.JSON)
            result = courier_api.create_courier(courier_data)
        
        with allure.step("Проверяем ошибку валидации"):
            assert result['status_code'] == Config.STATUS_CODES['BAD_REQUEST'], \
                f"Ожидался код {Config.STATUS_CODES['BAD_REQUEST']}, получен {result['status_code']}"
            assert ResponseMessages.COURIER_INSUFFICIENT_DATA_CREATE in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_INSUFFICIENT_DATA_CREATE}', получен {result['response_text']}"
