from appium import webdriver
from appium.options.android import UiAutomator2Options
from typing import Dict
from selenium.common.exceptions import WebDriverException
from utils.logger import setup_logger

logger = setup_logger()

def init_driver(capabilities: Dict) -> webdriver.Remote:
    """
    Инициализирует сессию Appium драйвера на основе переданных capabilities.

    :param capabilities: словарь с параметрами устройства и приложения
    :return: экземпляр Appium WebDriver
    :raises KeyError: если в capabilities отсутствует необходимый ключ 'appium:serverURL'
    :raises WebDriverException: если не удалось подключиться к Appium Server
    """

    logger.info("Initializing Appium driver")

    # Проверяем наличие URL сервера
    if "appium:serverURL" not in capabilities:
        logger.error("Missing required capability: 'appium:serverURL'")
        raise KeyError("В capabilities отсутствует обязательный ключ 'appium:serverURL'")

    server_url = capabilities.pop("appium:serverURL")

    # Определяем платформу
    platform_name = capabilities.get("platformName", "").lower()

    try:
        if platform_name == "android":
            from appium.options.android import UiAutomator2Options
            options = UiAutomator2Options().load_capabilities(capabilities)
        elif platform_name == "ios":
            from appium.options.ios import XCUITestOptions
            options = XCUITestOptions().load_capabilities(capabilities)
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")

        logger.info(f"Connecting to Appium server at {server_url}")
        driver = webdriver.Remote(command_executor=server_url, options=options)
        logger.info("Driver initialized successfully")
        return driver

    except WebDriverException as e:
        logger.error(f"Failed to initialize driver: {e}")
        raise