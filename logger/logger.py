import logging
from logging.handlers import RotatingFileHandler
import sys


class Logger:
    def __init__(self, name, log_file='data/logs/app.log', level=logging.INFO):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Форматтер для логов, включающий имя, имя файла и функцию
        formatter = logging.Formatter(f'%(asctime)s | {name} | %(levelname)s | %(message)s')

        # Обработчик для вывода в файл
        file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Обработчик для вывода в консоль
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    # Методы логирования. Здесь не нужно передавать уровень логирования,
    # так как каждый метод уже имеет определенный уровень.
    def info(self, message):
        self.logger.info(message)  # Убираем передачу уровня

    def error(self, message):
        self.logger.error(message)  # Убираем передачу уровня

    def warning(self, message):
        self.logger.warning(message)  # Убираем передачу уровня

    def debug(self, message):
        self.logger.debug(message)  # Убираем передачу уровня

    def critical(self, message):
        self.logger.critical(message)  # Убираем передачу уровня
