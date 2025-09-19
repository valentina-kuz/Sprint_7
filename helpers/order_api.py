"""
API методы для работы с заказами
"""
from typing import Dict, Any, Optional
from .api_client import APIClient
from config.settings import Config


class OrderAPI(APIClient):
    """Класс для работы с API заказов"""
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создает новый заказ
        
        Args:
            order_data: Данные заказа
            
        Returns:
            Словарь с результатом запроса
        """
        response = self.post(
            endpoint=Config.ENDPOINTS['CREATE_ORDER'],
            data=order_data,
            headers={'Content-Type': 'application/json'}
        )
        
        result = self._parse_response(response)
        
        # Добавляем track номер при успешном создании
        if response.status_code == 201 and response.text:
            try:
                json_data = response.json()
                result['track'] = json_data.get('track')
            except ValueError:
                pass
        
        return result
    
    def get_orders_list(self) -> Dict[str, Any]:
        """
        Получает список заказов
        
        Returns:
            Словарь с результатом запроса
        """
        response = self.get(endpoint=Config.ENDPOINTS['GET_ORDERS_LIST'])
        
        result = self._parse_response(response)
        
        # Добавляем список заказов при успешном запросе
        if response.status_code == 200 and response.text:
            try:
                json_data = response.json()
                result['orders'] = json_data.get('orders', [])
            except ValueError:
                pass
        
        return result
    
    def get_order_by_track(self, track_number: str) -> Dict[str, Any]:
        """
        Получает заказ по номеру отслеживания
        
        Args:
            track_number: Номер отслеживания заказа
            
        Returns:
            Словарь с результатом запроса
        """
        params = {'t': track_number}
        response = self.get(
            endpoint=Config.ENDPOINTS['GET_ORDER_BY_TRACK'],
            params=params
        )
        
        result = self._parse_response(response)
        
        # Добавляем объект заказа при успешном запросе
        if response.status_code == 200 and response.text:
            try:
                json_data = response.json()
                result['order'] = json_data.get('order')
            except ValueError:
                pass
        
        return result
    
    def accept_order(self, order_id: str, courier_id: str) -> Dict[str, Any]:
        """
        Принимает заказ курьером
        
        Args:
            order_id: ID заказа
            courier_id: ID курьера
            
        Returns:
            Словарь с результатом запроса
        """
        endpoint = f"{Config.ENDPOINTS['ACCEPT_ORDER']}{order_id}"
        params = {'courierId': courier_id}
        
        response = self.put(endpoint=endpoint, params=params)
        
        return self._parse_response(response)
    
    def cancel_order(self, track_number: str) -> Dict[str, Any]:
        """
        Отменяет заказ
        
        Args:
            track_number: Номер отслеживания заказа
            
        Returns:
            Словарь с результатом запроса
        """
        params = {'track': track_number}
        response = self.put(
            endpoint=Config.ENDPOINTS['CANCEL_ORDER'],
            params=params
        )
        
        return self._parse_response(response)
    
