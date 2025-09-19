"""
Базовый клиент для работы с API
"""
import requests
import json
from typing import Dict, Any, Optional
from config.settings import Config


class APIClient:
    """Базовый клиент для работы с API Яндекс Самокат"""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        self.default_headers = Config.DEFAULT_HEADERS.copy()
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Выполняет HTTP запрос к API
        
        Args:
            method: HTTP метод (GET, POST, DELETE, etc.)
            endpoint: Эндпоинт API
            data: Данные для отправки в теле запроса
            params: Параметры запроса
            headers: Заголовки запроса
            
        Returns:
            Response объект
        """
        url = f"{self.base_url}{endpoint}"
        
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)
        
        request_data = None
        if data:
            if request_headers.get('Content-Type') == 'application/json':
                request_data = json.dumps(data)
            else:
                request_data = data
        
        response = requests.request(
            method=method,
            url=url,
            data=request_data,
            params=params,
            headers=request_headers,
            timeout=self.timeout
        )
        
        return response
    
    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Парсит ответ API в стандартный формат
        
        Args:
            response: Response объект
            
        Returns:
            Словарь с результатом запроса
        """
        return {
            'status_code': response.status_code,
            'response_text': response.text
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """GET запрос"""
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """POST запрос"""
        return self._make_request('POST', endpoint, data=data, params=params, headers=headers)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """PUT запрос"""
        return self._make_request('PUT', endpoint, data=data, params=params, headers=headers)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """DELETE запрос"""
        return self._make_request('DELETE', endpoint, params=params, headers=headers)
