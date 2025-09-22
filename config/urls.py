"""
URL-адреса и эндпоинты для API Яндекс Самокат
"""

class URLs:
    """Класс для управления URL-адресами API"""
    
    # Базовый URL тестового стенда
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Эндпоинты API (относительные пути)
    ENDPOINTS = {
        # Курьеры
        'CREATE_COURIER': '/api/v1/courier',
        'LOGIN_COURIER': '/api/v1/courier/login',
        'DELETE_COURIER': '/api/v1/courier/',
        
        # Заказы
        'CREATE_ORDER': '/api/v1/orders',
        'GET_ORDERS_LIST': '/api/v1/orders',
        'GET_ORDER_BY_TRACK': '/api/v1/orders/track',
        'ACCEPT_ORDER': '/api/v1/orders/accept/',
        'CANCEL_ORDER': '/api/v1/orders/cancel',
    }
    
    @classmethod
    def get_full_url(cls, endpoint_key: str) -> str:
        """Получить полный URL для эндпоинта"""
        endpoint = cls.ENDPOINTS.get(endpoint_key, '')
        return f"{cls.BASE_URL}{endpoint}"
    
    @classmethod
    def get_endpoint(cls, endpoint_key: str) -> str:
        """Получить относительный путь эндпоинта"""
        return cls.ENDPOINTS.get(endpoint_key, '')
