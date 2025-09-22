"""
Тесты авторизации курьеров
"""
import pytest
import allure
from config.settings import Config
from data.test_data import CourierTestData, ResponseMessages
from helpers.data_generator import DataGenerator


@allure.epic("Курьеры")
@allure.feature("Авторизация курьера")
class TestCourierLogin:
    """Тесты авторизации курьеров"""
    
    @allure.title("Успешная авторизация курьера возвращает ID")
    @allure.description("Проверяем, что при успешной авторизации возвращается ID курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_courier_login_success_returns_id(self, courier_for_tests):
        """Тест успешной авторизации курьера"""
        
        courier_info = courier_for_tests
        
        with allure.step("Проверяем данные авторизованного курьера"):
            assert courier_info['success'] is True, "Курьер должен быть успешно создан и авторизован"
            assert courier_info['courier_id'] is not None, "ID курьера не должен быть пустым"
            assert isinstance(courier_info['courier_id'], (str, int)), "ID курьера должен быть строкой или числом"
        
        with allure.step("Проверяем статус код авторизации"):
            login_result = courier_info['login_result']
            assert login_result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_OK']}, получен {login_result['status_code']}"
    
    @allure.title("Нельзя войти без обязательных полей")
    @allure.description("Проверяем, что авторизация без обязательных полей возвращает ошибку 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_courier_login_without_required_fields_fails(self, courier_api):
        """Тест авторизации без обязательных полей"""
        
        # Создаем генератор данных
        data_generator = DataGenerator()
        
        # Тестируем с пустым логином
        with allure.step("Тестируем авторизацию с пустым логином"):
            login_data = {
                "login": "",
                "password": data_generator.generate_random_string(8)
            }
            allure.attach(str(login_data), "Данные с пустым логином", allure.attachment_type.JSON)
            result = courier_api.login_courier(login_data)
            
            assert result['status_code'] == Config.STATUS_CODES['BAD_REQUEST'], \
                f"Ожидался код {Config.STATUS_CODES['BAD_REQUEST']}, получен {result['status_code']}"
            assert ResponseMessages.COURIER_INSUFFICIENT_DATA_LOGIN in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_INSUFFICIENT_DATA_LOGIN}', получен {result['response_text']}"
        
        # Тестируем с пустым паролем
        with allure.step("Тестируем авторизацию с пустым паролем"):
            login_data = {
                "login": data_generator.generate_random_string(8),
                "password": ""
            }
            allure.attach(str(login_data), "Данные с пустым паролем", allure.attachment_type.JSON)
            result = courier_api.login_courier(login_data)
            
            assert result['status_code'] == Config.STATUS_CODES['BAD_REQUEST'], \
                f"Ожидался код {Config.STATUS_CODES['BAD_REQUEST']}, получен {result['status_code']}"
            assert ResponseMessages.COURIER_INSUFFICIENT_DATA_LOGIN in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_INSUFFICIENT_DATA_LOGIN}', получен {result['response_text']}"
    
    
    @allure.title("Ошибка при авторизации несуществующего пользователя")
    @allure.description("Проверяем, что авторизация несуществующего пользователя возвращает ошибку 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_courier_login_nonexistent_user_fails(self, courier_api):
        """Тест авторизации несуществующего пользователя"""
        
        # Создаем генератор данных
        data_generator = DataGenerator()
        
        with allure.step("Пытаемся войти под несуществующим пользователем"):
            # Генерируем заведомо несуществующие данные
            nonexistent_data = {
                "login": data_generator.generate_random_string(12),
                "password": data_generator.generate_random_string(12)
            }
            allure.attach(str(nonexistent_data), "Данные несуществующего пользователя", allure.attachment_type.JSON)
            result = courier_api.login_courier(nonexistent_data)
        
        with allure.step("Проверяем ошибку 'не найден'"):
            assert result['status_code'] == Config.STATUS_CODES['NOT_FOUND'], \
                f"Ожидался код {Config.STATUS_CODES['NOT_FOUND']}, получен {result['status_code']}"
            assert ResponseMessages.COURIER_NOT_FOUND in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_NOT_FOUND}', получен {result['response_text']}"
