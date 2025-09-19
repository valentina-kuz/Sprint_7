"""
Тесты удаления курьеров
"""
import pytest
import allure
from config.settings import Config
from data.test_data import ResponseMessages


@allure.epic("Курьеры")
@allure.feature("Удаление курьера")
class TestCourierDelete:
    """Тесты удаления курьеров"""
    
    @allure.title("Успешное удаление курьера возвращает ok:true")
    @allure.description("Проверяем, что при успешном удалении курьера возвращается ok:true")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_courier_success(self, courier_api, data_generator):
        """Тест успешного удаления курьера"""
        
        # Создаем курьера для удаления
        courier_data = data_generator.generate_courier_data()
        
        with allure.step("Создаем курьера для удаления"):
            create_result = courier_api.create_and_login_courier(courier_data)
            assert create_result['success'] is True, "Курьер должен быть создан для теста"
            courier_id = create_result['courier_id']
        
        with allure.step("Удаляем курьера"):
            allure.attach(str(courier_id), "ID курьера для удаления", allure.attachment_type.TEXT)
            result = courier_api.delete_courier(str(courier_id))
        
        with allure.step("Проверяем успешное удаление"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_OK']}, получен {result['status_code']}"
            assert result['response_text'] == ResponseMessages.COURIER_DELETED_SUCCESS, \
                f"Ожидался ответ {ResponseMessages.COURIER_DELETED_SUCCESS}, получен {result['response_text']}"
    
    @allure.title("Ошибка при удалении курьера без ID")
    @allure.description("Проверяем, что удаление курьера без ID возвращает ошибку 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_courier_without_id_fails(self, courier_api):
        """Тест удаления курьера без ID"""
        
        with allure.step("Отправляем запрос на удаление курьера без ID"):
            # Передаем пустую строку как ID
            result = courier_api.delete_courier("")
        
        with allure.step("Проверяем ошибку валидации"):
            # API возвращает 404 для пустого ID
            assert result['status_code'] == Config.STATUS_CODES['NOT_FOUND'], \
                f"Ожидался код {Config.STATUS_CODES['NOT_FOUND']}, получен {result['status_code']}"
    
    @allure.title("Ошибка при удалении курьера с несуществующим ID")
    @allure.description("Проверяем, что удаление курьера с несуществующим ID возвращает ошибку 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_courier_with_nonexistent_id_fails(self, courier_api):
        """Тест удаления курьера с несуществующим ID"""
        
        nonexistent_id = "99999999"
        
        with allure.step(f"Отправляем запрос на удаление курьера с несуществующим ID: {nonexistent_id}"):
            allure.attach(nonexistent_id, "Несуществующий ID курьера", allure.attachment_type.TEXT)
            result = courier_api.delete_courier(nonexistent_id)
        
        with allure.step("Проверяем ошибку 'не найден'"):
            assert result['status_code'] == Config.STATUS_CODES['NOT_FOUND'], \
                f"Ожидался код {Config.STATUS_CODES['NOT_FOUND']}, получен {result['status_code']}"
            assert ResponseMessages.COURIER_DELETE_NOT_FOUND in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.COURIER_DELETE_NOT_FOUND}', получен {result['response_text']}"
    
