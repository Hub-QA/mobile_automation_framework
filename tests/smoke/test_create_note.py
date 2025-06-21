# tests/smoke/test_create_note.py

import logging
import time

from pages.main_page import MainPage
from pages.note_page import NotePage
from utils.screenshot import take_screenshot


def test_create_note(appium_driver, logger):
    """
    Тест: Создание новой текстовой заметки.
    Проверить, что пользователь может:
    1. Создать новую текстовую заметку
    2. Заполнить заголовок и описание
    3. Сохранить заметку
    4. Убедиться, что она появилась на главной странице
    """
    logger.info("=== Начало теста: создание заметки ===")

    main_page = MainPage(appium_driver)
    note_page = NotePage(appium_driver)

    try:
        # Шаг 1: Пропустить онбординг, если он есть
        logger.info("Пропускаем онбординг")
        main_page.skip_onboarding_if_present()

        # Шаг 2: Открыть меню создания заметки
        logger.info("Открываем меню создания заметки")
        main_page.tap_create_note()

        # Шаг 3: Выбрать тип 'Текст'
        logger.info("Выбираем тип 'Текст'")
        main_page.select_text_note_type()  # Теперь находится в MainPage

        # Шаг 4: Проверить, что редактор открыт
        assert note_page.is_editor_opened(), "Редактор не открылся после выбора типа 'Текст'"

        # Шаг 5: Ввести заголовок
        note_title = f"TestNote_{int(time.time())}"
        logger.info(f"Вводим заголовок: {note_title}")
        note_page.enter_title(note_title)

        # Шаг 6: Ввести содержимое заметки (опционально)
        note_content = "Это тестовый текст для проверки содержимого заметки."
        logger.info(f"Вводим содержимое: {note_content}")
        note_page.enter_content(note_content)

        # Шаг 7: Сохранить заметку
        logger.info("Сохраняем заметку")
        note_page.save_note()

        # Шаг 8: Проверить наличие заметки на главной странице
        logger.info("Проверяем наличие заметки на главной странице")
        assert main_page.is_note_exists(note_title), f"Заметка '{note_title}' не найдена на главной странице"

        # Все проверки пройдены — делаем скриншот
        take_screenshot(appium_driver, "note_created_successfully")
        logger.info("Скриншот сохранён: заметка успешно создана")

        logger.info("Тест успешно пройден: заметка создана и отображается на главной странице")

    except Exception as e:
        logger.error(f"❌ Ошибка при выполнении теста: {str(e)}")
        take_screenshot(appium_driver, "test_create_note_failure")
        raise