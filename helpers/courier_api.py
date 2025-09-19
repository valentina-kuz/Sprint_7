"""
API методы для работы с курьерами
"""
from typing import Dict, Any, Optional
from .api_client import APIClient
from config.settings import Config


class CourierAPI(APIClient):
    """Класс для работы с API курьеров"""
    
    def create_courier(self, courier_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Создает нового курьера
        
        Args:
            courier_data: Данные курьера (login, password, firstName)
            
        Returns:
            Словарь с результатом запроса
        """
        response = self.post(
            endpoint=Config.ENDPOINTS['CREATE_COURIER'],
            data=courier_data,
            headers={'Content-Type': 'application/json'}
        )
        
        return self._parse_response(response)
    
    def login_courier(self, login_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Авторизует курьера
        
        Args:
            login_data: Данные для входа (login, password)
            
        Returns:
            Словарь с результатом запроса включая ID курьера
        """
        response = self.post(
            endpoint=Config.ENDPOINTS['LOGIN_COURIER'],
            data=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        result = self._parse_response(response)
        
        # Добавляем ID курьера при успешном логине
        if response.status_code == 200 and response.text:
            try:
                json_data = response.json()
                result['courier_id'] = json_data.get('id')
            except ValueError:
                pass
        
        return result
    
    def delete_courier(self, courier_id: str) -> Dict[str, Any]:
        """
        Удаляет курьера
        
        Args:
            courier_id: ID курьера для удаления
            
        Returns:
            Словарь с результатом запроса
        """
        endpoint = f"{Config.ENDPOINTS['DELETE_COURIER']}{courier_id}"
        response = self.delete(endpoint=endpoint)
        
        return self._parse_response(response)
    
    def create_and_login_courier(self, courier_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Создает курьера и сразу авторизует его
        
        Args:
            courier_data: Данные курьера
            
        Returns:
            Словарь с данными созданного и авторизованного курьера
        """
        # Создаем курьера
        create_result = self.create_courier(courier_data)
        
        if create_result['status_code'] != 201:
            return {
                'success': False,
                'create_result': create_result,
                'error': 'Failed to create courier'
            }
        
        # Логинимся
        login_data = {
            'login': courier_data['login'],
            'password': courier_data['password']
        }
        login_result = self.login_courier(login_data)
        
        if login_result['status_code'] != 200:
            return {
                'success': False,
                'create_result': create_result,
                'login_result': login_result,
                'error': 'Failed to login courier'
            }
        
        return {
            'success': True,
            'courier_data': courier_data,
            'courier_id': login_result.get('courier_id'),
            'create_result': create_result,
            'login_result': login_result
        }
