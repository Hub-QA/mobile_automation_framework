# utils/screenshot.py

from pathlib import Path
import logging
from datetime import datetime


def take_screenshot(driver, test_name):
    """
    Описание файла:
    1. Делает скриншот экрана и сохраняет его в папку 'screenshots' с уникальным именем.
    2. При наличии установленного Allure, скриншот прикрепляется к отчёту.
    
    Args:
        driver (Union[AppiumDriver, WebDriver]): Экземпляр драйвера Appium или Selenium.
        test_name (str): Имя теста для использования в имени файла скриншота.
        
    Returns:
        Optional[str]: Полный путь к файлу скриншота, если успешно. Иначе — None.
        
    Raises:
        Исключения не выбрасываются, но логируются через модуль logging.
    """
    try:
        # Создаём папку, если её нет
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        # Генерируем уникальное имя с timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{test_name}_{timestamp}.png"
        file_path = screenshots_dir / file_name

        # Сохраняем скриншот
        driver.save_screenshot(str(file_path))
        logging.info(f"Screenshot saved: {file_path}")

        # Для интеграции с Allure
        try:
            import allure
            allure.attach.file(str(file_path), name=test_name, attachment_type=allure.attachment_type.PNG)
        except ImportError:
            pass

        return str(file_path)

    except Exception as e:
        logging.error(f"Failed to take screenshot: {e}")
        return None