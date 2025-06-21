# tests/smoke/test_check_ui_ux.py

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from utils.screenshot import take_screenshot


def test_check_element_exists(appium_driver, logger):
    """
    Тест: Проверяет наличие ключевых элементов интерфейса на главной странице Google Keep.

    Проверяемые элементы:
    1. Кнопка создания заметки
    2. Поле поиска
    3. Меню навигации
    4. Наличие хотя бы одной заметки
    """
    logger.info("=== Начало теста: проверка наличия ключевых элементов ===")

    try:
        # 1. Проверка кнопки создания заметки
        logger.info("Проверяем кнопку 'Создать заметку'")
        create_note_button = WebDriverWait(appium_driver, 15).until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.google.android.keep:id/speed_dial_create_close_button"))
        )
        logger.info(f"Кнопка создания найдена. Позиция: {create_note_button.location}")

        # 2. Проверка поля поиска
        logger.info("Проверяем поле поиска")
        search_field = WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.google.android.keep:id/toolbar"))
        )
        logger.info(f"Поле поиска найдено. hint: {search_field.get_attribute('text')}")

        # 3. Проверка меню навигации (иконка аккаунта)
        logger.info("Проверяем меню навигации")
        nav_menu = WebDriverWait(appium_driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.keep:id/menu_account_particle"))
        )
        logger.info("Меню навигации доступно")

        # 4. Проверка наличия хотя бы одной заметки
        logger.info("Проверяем наличие хотя бы одной заметки")
        note_title = WebDriverWait(appium_driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.google.android.keep:id/index_note_title"))
        )
        logger.info(f"Заметка найдена: {note_title.text}")

        # Все проверки пройдены — делаем скриншот
        take_screenshot(appium_driver, "main_page_elements_verified")
        logger.info("Все ключевые элементы интерфейса отображаются корректно")

    except Exception as e:
        logger.error(f"❌ Ошибка при проверке элементов: {str(e)}")
        take_screenshot(appium_driver, "check_element_failure")
        logger.debug(f"Текущий page source:\n{appium_driver.page_source[:1000]}...")
        raise