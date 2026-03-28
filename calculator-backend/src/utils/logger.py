import logging
import sys
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


class Logger:
    """Универсальный класс для логирования"""
    
    _instances = {}
    
    def __new__(cls, name: str = 'app', level: str = 'INFO'):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]
    
    def __init__(self, name: str = 'app', level: str = 'INFO'):
        if self._initialized:
            return
            
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Устанавливаем уровень логирования
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))
        
        # Создаем форматтер
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Добавляем обработчик для вывода в консоль
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self._initialized = True
    
    def debug(self, message: str, *args, **kwargs):
        """Отладочное сообщение"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Информационное сообщение"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Предупреждение"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Сообщение об ошибке"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Критическая ошибка"""
        self.logger.critical(message, *args, **kwargs)
    
    def log(self, level: str, message: str, *args, **kwargs):
        """Логирование с указанным уровнем"""
        level_map = {
            'DEBUG': self.logger.debug,
            'INFO': self.logger.info,
            'WARNING': self.logger.warning,
            'ERROR': self.logger.error,
            'CRITICAL': self.logger.critical
        }
        level_map.get(level.upper(), self.logger.info)(message, *args, **kwargs)
    
    def set_level(self, level: str):
        """Изменить уровень логирования"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))
    
    def add_file_handler(self, filename: str, level: str = 'INFO'):
        """Добавить логирование в файл"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        file_handler = logging.FileHandler(filename, encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level_map.get(level.upper(), logging.INFO))
        self.logger.addHandler(file_handler)


# Создаем глобальный экземпляр для простого импорта
logger = Logger()


def log_function_call(func: Callable) -> Callable:
    """Декоратор для логирования вызовов функций"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Вызов функции: {func.__name__}")
        logger.debug(f"Аргументы: args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Результат {func.__name__}: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper


def log_execution_time(func: Callable) -> Callable:
    """Декоратор для логирования времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logger.debug(f"Начало выполнения: {func.__name__}")
        result = func(*args, **kwargs)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.debug(f"Завершение {func.__name__}. Время: {duration:.3f} сек")
        return result
    return wrapper

# Устанавливаем уровень DEBUG для отладки и получения сообщения DEBUG
logger.set_level('DEBUG')