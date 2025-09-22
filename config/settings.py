"""
Конфигурационные настройки для тестирования API Яндекс Самокат
"""

class Config:
    """Основная конфигурация проекта"""
    
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
