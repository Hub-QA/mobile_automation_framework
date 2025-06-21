# tests/smoke/test_delete_note.py

import logging
import time

from pages.main_page import MainPage
from pages.note_page import NotePage  
from utils.screenshot import take_screenshot


def test_create_and_delete_note(appium_driver, logger):
    """
    Тест: Создание и удаление заметки напрямую через контекстное меню
    End-to-end сценарий проверить, что пользователь может:
    1. Заметка успешно создана
    2. Сохранена в приложении
    3. Удалена через контекстное меню
    4. Исчезла с главной страницы
    """
    logger.info("=== Начало теста: создание и удаление напрямую ===")

    main_page = MainPage(appium_driver)
    note_page = NotePage(appium_driver)

    try:
        # Шаг 1: Пропустить онбординг
        main_page.skip_onboarding_if_present()

        # Шаг 2: Создать новую текстовую заметку
        main_page.tap_create_note()
        main_page.select_text_note_type()

        note_title = f"TestNote_{int(time.time())}"
        logger.info(f"Вводим заголовок: {note_title}")
        note_page.enter_title(note_title)

        logger.info("Вводим содержимое")
        note_page.enter_content("Это тестовая заметка для удаления")

        logger.info("Сохраняем заметку")
        note_page.save_note()

        # Шаг 3: Проверяем, что заметка отображается
        assert main_page.is_note_exists(note_title), f"Заметка '{note_title}' не найдена"

        # Шаг 4: Удаляем напрямую через контекстное меню
        main_page.delete_note_directly_by_title(note_title)

        # Шаг 5: Ждём исчезновения
        assert main_page.wait_for_note_deletion(note_title), f"Заметка '{note_title}' всё ещё существует"

        # Все проверки пройдены — делаем скриншот
        take_screenshot(appium_driver, "note_deleted_successfully")
        logger.info("Скриншот сохранён: заметка успешно удалена")

        logger.info("Тест успешно пройден: заметка удалена напрямую")

    except Exception as e:
        logger.error(f"❌ Ошибка при выполнении теста: {str(e)}")
        take_screenshot(appium_driver, "test_delete_failure")
        raise