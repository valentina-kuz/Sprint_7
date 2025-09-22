"""
Тесты получения заказа по номеру отслеживания
"""
import pytest
import allure
from config.settings import Config
from data.test_data import ResponseMessages


@allure.epic("Заказы")
@allure.feature("Получение заказа по номеру")
class TestOrderGetByTrack:
    """Тесты получения заказа по номеру отслеживания"""
    
    @allure.title("Успешный запрос возвращает объект заказа")
    @allure.description("Проверяем, что по корректному номеру отслеживания возвращается объект заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_order_by_track_success(self, order_for_tests, order_api):
        """Тест успешного получения заказа по track номеру"""
        
        order_info = order_for_tests
        track = order_info['track']
        
        with allure.step(f"Получаем заказ по track номеру: {track}"):
            allure.attach(str(track), "Track номер", allure.attachment_type.TEXT)
            result = order_api.get_order_by_track(str(track))
        
        with allure.step("Проверяем успешный ответ"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_OK']}, получен {result['status_code']}"
        
        with allure.step("Проверяем наличие объекта заказа в ответе"):
            assert result.get('order') is not None, "В ответе должен быть объект заказа"
            
            order = result['order']
            assert isinstance(order, dict), "Заказ должен быть объектом"
            
            allure.attach(str(order), "Полученный объект заказа", allure.attachment_type.JSON)
    
    @allure.title("Ошибка при запросе без номера заказа")
    @allure.description("Проверяем, что запрос без номера заказа возвращает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order_without_track_number_fails(self, order_api):
        """Тест получения заказа без track номера"""
        
        with allure.step("Отправляем запрос без track номера"):
            # Передаем пустую строку как track номер
            result = order_api.get_order_by_track("")
        
        with allure.step("Проверяем ошибку"):
            assert result['status_code'] == Config.STATUS_CODES['BAD_REQUEST'], \
                f"Ожидался код {Config.STATUS_CODES['BAD_REQUEST']}, получен {result['status_code']}"
            assert ResponseMessages.ORDER_TRACK_NOT_PROVIDED in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.ORDER_TRACK_NOT_PROVIDED}', получен {result['response_text']}"
    
    @allure.title("Ошибка при запросе с несуществующим номером заказа")
    @allure.description("Проверяем, что запрос с несуществующим номером заказа возвращает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order_with_nonexistent_track_fails(self, order_api):
        """Тест получения заказа с несуществующим track номером"""
        
        nonexistent_track = "99999999"
        
        with allure.step(f"Отправляем запрос с несуществующим track номером: {nonexistent_track}"):
            allure.attach(nonexistent_track, "Несуществующий track номер", allure.attachment_type.TEXT)
            result = order_api.get_order_by_track(nonexistent_track)
        
        with allure.step("Проверяем ошибку"):
            assert result['status_code'] == Config.STATUS_CODES['NOT_FOUND'], \
                f"Ожидался код {Config.STATUS_CODES['NOT_FOUND']}, получен {result['status_code']}"
            assert ResponseMessages.ORDER_NOT_FOUND in result['response_text'], \
                f"Ожидалось сообщение '{ResponseMessages.ORDER_NOT_FOUND}', получен {result['response_text']}"