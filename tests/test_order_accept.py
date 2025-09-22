"""
Тесты принятия заказов курьером
"""
import pytest
import allure
from config.settings import Config
from data.test_data import ResponseMessages


@allure.epic("Заказы")
@allure.feature("Принятие заказа")
class TestOrderAccept:
    """Тесты принятия заказов курьером"""
    
    @allure.title("Успешное принятие заказа возвращает ok:true")
    @allure.description("Проверяем, что курьер может принять заказ и получить ok:true")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_accept_order_success(self, courier_and_order_for_tests, order_api):
        """Тест успешного принятия заказа"""
        
        test_data = courier_and_order_for_tests
        courier_info = test_data['courier']
        order_info = test_data['order']
        
        # Получаем ID заказа по track номеру
        with allure.step("Получаем ID заказа по track номеру"):
            track = order_info['track']
            order_details = order_api.get_order_by_track(str(track))
            assert order_details['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                "Не удалось получить детали заказа"
            
            order_id = order_details['order']['id']
            allure.attach(str(order_id), "ID заказа", allure.attachment_type.TEXT)
        
        with allure.step("Принимаем заказ курьером"):
            courier_id = str(courier_info['courier_id'])
            allure.attach(courier_id, "ID курьера", allure.attachment_type.TEXT)
            
            result = order_api.accept_order(str(order_id), courier_id)
        
        with allure.step("Проверяем успешное принятие заказа"):
            assert result['status_code'] == Config.STATUS_CODES['SUCCESS_OK'], \
                f"Ожидался код {Config.STATUS_CODES['SUCCESS_OK']}, получен {result['status_code']}"
            assert result['response_text'] == ResponseMessages.ORDER_ACCEPTED_SUCCESS, \
                f"Ожидался ответ {ResponseMessages.ORDER_ACCEPTED_SUCCESS}, получен {result['response_text']}"
    
    @allure.title("Ошибка при принятии заказа без ID курьера")
    @allure.description("Проверяем, что принятие заказа без ID курьера возвращает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_accept_order_without_courier_id_fails(self, order_for_tests, order_api):
        """Тест принятия заказа без ID курьера"""
        
        order_info = order_for_tests
        
        # Получаем ID заказа
        with allure.step("Получаем ID заказа"):
            track = order_info['track']
            order_details = order_api.get_order_by_track(str(track))
            order_id = order_details['order']['id']
        
        with allure.step("Пытаемся принять заказ без ID курьера"):
            # Передаем пустую строку как ID курьера
            result = order_api.accept_order(str(order_id), "")
        
        with allure.step("Проверяем ошибку"):
            assert result['status_code'] == Config.STATUS_CODES['BAD_REQUEST'], \
                f"Ожидался код {Config.STATUS_CODES['BAD_REQUEST']}, получен {result['status_code']}"
    
    @allure.title("Ошибка при принятии несуществующего заказа")
    @allure.description("Проверяем, что принятие несуществующего заказа возвращает ошибку")
    @allure.severity(allure.severity_level.NORMAL)
    def test_accept_nonexistent_order_fails(self, courier_for_tests, order_api):
        """Тест принятия несуществующего заказа"""
        
        courier_info = courier_for_tests
        nonexistent_order_id = "99999999"
        
        with allure.step(f"Пытаемся принять несуществующий заказ: {nonexistent_order_id}"):
            courier_id = str(courier_info['courier_id'])
            allure.attach(nonexistent_order_id, "Несуществующий ID заказа", allure.attachment_type.TEXT)
            result = order_api.accept_order(nonexistent_order_id, courier_id)
        
        with allure.step("Проверяем ошибку"):
            assert result['status_code'] == Config.STATUS_CODES['NOT_FOUND'], \
                f"Ожидался код {Config.STATUS_CODES['NOT_FOUND']}, получен {result['status_code']}"
