# conftest.py

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pathlib import Path
import json
import logging
import os


"""
Описание файла:

Этот файл содержит глобальные фикстуры Pytest для настройки тестового окружения.
Он используется для:
1. Загрузки конфигурации (capabilities) из JSON-файла.
2. Инициализации и завершения работы Appium драйвера.
3. Настройки логгирования.
4. Обеспечения повторного использования общего кода между тестами.

Фикстуры:
├── appium_capabilities    # Загрузка capabilities из JSON
├── appium_driver          # Инициализация и завершение работы Appium драйвера
└── logger                 # Настроенный логгер для тестов
"""


# Настройка логгирования
LOGGER = logging.getLogger(__name__)


# ФИКСТУРЫ

@pytest.fixture(scope="session")
def appium_capabilities():
    """
    Загружает capabilities из JSON-файла в папке config/capabilities/

    Returns:
        dict: Словарь с настройками Appium (desired capabilities)
    """
    config_dir = Path(__file__).parent.parent / "config" / "capabilities"
    config_path = config_dir / "Pixel_2_API_27.json"  # Указываем конкретный профиль

    LOGGER.info(f"Загрузка capabilities из файла: {config_path}")

    if not config_path.exists():
        raise FileNotFoundError(f"Capabilities файл не найден: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            caps = json.load(f)
        return caps
    except json.JSONDecodeError as e:
        raise ValueError(f"Неверный формат JSON в capabilities: {e}") from e


@pytest.fixture(scope="function")
def appium_driver(appium_capabilities):
    """
    Создаёт и настраивает Appium WebDriver перед каждым тестом.
    Завершает работу драйвера после выполнения теста.

    Args:
        appium_capabilities (dict): Desired capabilities для запуска сессии

    Yields:
        WebDriver: Инициализированный Appium WebDriver
    """
    options = UiAutomator2Options().load_capabilities(appium_capabilities)

    LOGGER.info("Инициализация Appium драйвера")
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options
    )

    yield driver  # Тест выполняется здесь

    LOGGER.info("Завершение работы Appium драйвера")
    driver.quit()


@pytest.fixture(scope="function")
def logger():
    """
    Возвращает настроенный логгер.

    Returns:
        logging.Logger: Логгер с настройками из utils.logger.setup_logger
    """
    from utils.logger import setup_logger
    return setup_logger()