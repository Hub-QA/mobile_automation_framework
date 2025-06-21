# utils/logger.py

import logging
import os
from pathlib import Path

"""
Описание файла:
После вызова setup_logger():
1. Все предыдущие логи удаляются.
2. Создаётся новая чистая папка: ~/Desktop/logs/
3. В ней создаётся файл: test_run.log
4. Все логи из тестов пишутся в этот файл с метками времени и приоритетом.
"""

def setup_logger(log_dir="~/Desktop/logs", log_file="test_run.log"):
    # Расширяем путь (~ -> домашняя директория)
    log_path = Path(log_dir).expanduser()
    
    # Удаляем старую папку и создаём новую
    if log_path.exists():
        for f in log_path.glob("*"):  # Удаляем содержимое
            f.unlink()
    log_path.mkdir(exist_ok=True)

    # Полный путь к файлу лога
    log_filepath = log_path / log_file

    # Настройка логгера
    logger = logging.getLogger("mobile_tests")
    logger.setLevel(logging.DEBUG)

    # Удаляем предыдущие хендлеры (если есть)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Файловый хендлер
    file_handler = logging.FileHandler(log_filepath, mode='w')  # 'w' — перезапись файла
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger