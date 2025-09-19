"""
Генераторы тестовых данных
"""
import random
import string
from typing import Dict, Any

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False


class DataGenerator:
    """Генератор тестовых данных для API тестов"""
    
    def __init__(self):
        if FAKER_AVAILABLE:
            self.fake = Faker('ru_RU')
        else:
            self.fake = None
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Генерирует случайную строку заданной длины"""
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    
    def generate_courier_data(self, 
                            login: str = None, 
                            password: str = None, 
                            first_name: str = None) -> Dict[str, str]:
        """
        Генерирует данные для создания курьера
        
        Args:
            login: Логин курьера (если не указан, генерируется автоматически)
            password: Пароль курьера (если не указан, генерируется автоматически)
            first_name: Имя курьера (если не указано, генерируется автоматически)
            
        Returns:
            Словарь с данными курьера
        """
        return {
            "login": login or self.generate_random_string(10),
            "password": password or self.generate_random_string(10),
            "firstName": first_name or (self.fake.first_name() if self.fake else f"User{self.generate_random_string(5)}")
        }
    
    def generate_courier_login_data(self, login: str, password: str) -> Dict[str, str]:
        """Генерирует данные для логина курьера"""
        return {
            "login": login,
            "password": password
        }
    
    def generate_order_data(self, 
                          first_name: str = None,
                          last_name: str = None,
                          address: str = None,
                          metro_station: int = None,
                          phone: str = None,
                          rent_time: int = None,
                          delivery_date: str = None,
                          comment: str = None,
                          color: list = None) -> Dict[str, Any]:
        """
        Генерирует данные для создания заказа
        
        Returns:
            Словарь с данными заказа
        """
        order_data = {
            "firstName": first_name or (self.fake.first_name() if self.fake else f"Name{self.generate_random_string(3)}"),
            "lastName": last_name or (self.fake.last_name() if self.fake else f"Last{self.generate_random_string(3)}"),
            "address": address or (self.fake.address() if self.fake else f"Address {self.generate_random_string(5)}"),
            "metroStation": metro_station or random.randint(1, 200),
            "phone": phone or (self.fake.phone_number() if self.fake else f"+7{random.randint(1000000000, 9999999999)}"),
            "rentTime": rent_time or random.randint(1, 7),
            "deliveryDate": delivery_date or "2025-09-25",
            "comment": comment or (self.fake.text(max_nb_chars=50) if self.fake else f"Comment {self.generate_random_string(10)}")
        }
        
        if color is not None:
            order_data["color"] = color
            
        return order_data

