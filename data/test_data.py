"""
Тестовые данные для API тестов
"""
from typing import Dict, Any


class CourierTestData:
    """Тестовые данные для курьеров"""
    
    # Невалидные данные для параметризации тестов
    INVALID_COURIER_DATA_SETS = [
        # Без логина
        {
            "data": {"password": "test123", "firstName": "Тест"},
            "description": "без поля login"
        },
        # Без пароля
        {
            "data": {"login": "testuser", "firstName": "Тест"},
            "description": "без поля password"
        },
        # Пустой логин
        {
            "data": {"login": "", "password": "test123", "firstName": "Тест"},
            "description": "с пустым login"
        },
        # Пустой пароль
        {
            "data": {"login": "testuser", "password": "", "firstName": "Тест"},
            "description": "с пустым password"
        }
    ]
    
    # Невалидные данные для логина
    INVALID_LOGIN_DATA_SETS = [
        # Без логина
        {
            "data": {"password": "test123"},
            "description": "без поля login"
        },
        # Без пароля
        {
            "data": {"login": "testuser"},
            "description": "без поля password"
        },
        # Пустой логин
        {
            "data": {"login": "", "password": "test123"},
            "description": "с пустым login"
        },
        # Пустой пароль
        {
            "data": {"login": "testuser", "password": ""},
            "description": "с пустым password"
        }
    ]
    
    # Несуществующие данные для логина
    NON_EXISTENT_LOGIN_DATA = {
        "login": "nonexistentuser123",
        "password": "wrongpassword123"
    }


class OrderTestData:
    """Тестовые данные для заказов"""
    
    # Варианты цветов для параметризации
    COLOR_OPTIONS = [
        {"color": ["BLACK"], "description": "только черный"},
        {"color": ["GREY"], "description": "только серый"},
        {"color": ["BLACK", "GREY"], "description": "черный и серый"},
        {"color": [], "description": "без цвета"},
        {}, # Вариант без поля color вообще
    ]
    


class ResponseMessages:
    """Ожидаемые сообщения в ответах API"""

    COURIER_CREATED_SUCCESS = '{"ok":true}'
    COURIER_LOGIN_EXISTS = "Этот логин уже используется"
    COURIER_INSUFFICIENT_DATA_CREATE = "Недостаточно данных для создания учетной записи"
    COURIER_INSUFFICIENT_DATA_LOGIN = "Недостаточно данных для входа"
    COURIER_NOT_FOUND = "Учетная запись не найдена"
    COURIER_DELETED_SUCCESS = '{"ok":true}'
    COURIER_DELETE_INSUFFICIENT_DATA = "Недостаточно данных для удаления курьера"
    COURIER_DELETE_NOT_FOUND = "Курьера с таким id нет"
    ORDER_ACCEPTED_SUCCESS = '{"ok":true}'
    ORDER_NOT_FOUND = "Заказ не найден"
    ORDER_TRACK_NOT_PROVIDED = "Недостаточно данных для поиска"
