"""
Конфигурационные настройки для тестирования API Яндекс Самокат
"""

class Config:
    """Основная конфигурация проекта"""
    
    # Базовый URL API
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Эндпоинты API
    ENDPOINTS = {
        'CREATE_COURIER': '/api/v1/courier',
        'LOGIN_COURIER': '/api/v1/courier/login',
        'DELETE_COURIER': '/api/v1/courier/',
        'CREATE_ORDER': '/api/v1/orders',
        'GET_ORDERS_LIST': '/api/v1/orders',
        'GET_ORDER_BY_TRACK': '/api/v1/orders/track',
        'ACCEPT_ORDER': '/api/v1/orders/accept/',
        'CANCEL_ORDER': '/api/v1/orders/cancel',
    }
    
    # Таймаут
    REQUEST_TIMEOUT = 30
    
    # Заголовки по умолчанию
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json'
    }
    
    # Коды ответов
    STATUS_CODES = {
        'SUCCESS_CREATE': 201,
        'SUCCESS_OK': 200,
        'BAD_REQUEST': 400,
        'NOT_FOUND': 404,
        'CONFLICT': 409
    }
