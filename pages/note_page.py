from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

from core.base_page import BasePage


class NotePage(BasePage):
    """
    Страница создания/редактирования заметки в Google Keep.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger('mobile_tests')

    # === Локаторы UI элементов ===

    TITLE_FIELD = (
        AppiumBy.ID,
        'com.google.android.keep:id/editable_title'
    )

    CONTENT_FIELD = (
        AppiumBy.ID,
        'com.google.android.keep:id/edit_note_text'
    )

    BACK_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Назад"
    )

    ACTION_MENU_BUTTON = (
        AppiumBy.ID,
        "com.google.android.keep:id/editor_action_button"
    )

    NOTE_OVERFLOW_MENU = (
        AppiumBy.ACCESSIBILITY_ID,
        "Ещё"  # Контекстное меню (три точки) в открытой заметке
    )

    DELETE_CONTAINER_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.LinearLayout[.//android.widget.TextView[@text="Удалить"]]'
    )

    DELETE_CONFIRMATION_BUTTON_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.Button[@text="Удалить"]'
    )

    ARCHIVE_OPTION_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.Button[@content-desc="Поместить в архив"]'
    )

    # === Методы для взаимодействия ===

    def enter_title(self, text, timeout=20):
        """Ввод текста в поле заголовка"""
        try:
            self.logger.info(f"Попытка ввода текста в заголовок: '{text}'")

            if not self.is_editor_opened(timeout):
                raise Exception("Редактор заметки не открылся")

            title_field = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.TITLE_FIELD),
                message="Поле заголовка не кликабельное"
            )
            title_field.click()
            title_field.clear()
            title_field.send_keys(text)

        except Exception as e:
            self.logger.error(f"Ошибка ввода заголовка: {str(e)}")
            raise

    def enter_content(self, text, timeout=20):
        """Ввод текста в основное поле заметки"""
        try:
            self.logger.info(f"Ввод текста в содержание: '{text}'")

            content_field = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.CONTENT_FIELD),
                message="Поле содержания не кликабельное"
            )
            content_field.click()
            content_field.clear()
            content_field.send_keys(text)

        except Exception as e:
            self.logger.error(f"Ошибка ввода содержания: {str(e)}")
            raise

    def is_editor_opened(self, timeout=10):
        """Проверяет, открыт ли редактор заметки"""
        self.logger.debug("Проверяем, открыт ли редактор заметки")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.TITLE_FIELD)
            )
            return True
        except:
            self.logger.warning("Редактор не открылся за указанное время")
            return False

    def save_note(self, timeout=10):
        """Сохраняет заметку через кнопку 'Назад'"""
        self.logger.info("Сохранение заметки")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.BACK_BUTTON)
            ).click()
        except Exception as e:
            raise Exception(f"Не удалось сохранить заметку: {str(e)}")

    def open_action_bottom_sheet(self, timeout=10):
        """Открывает боттомшит действий"""
        self.logger.info("Открытие меню действий (боттомшит)")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.ACTION_MENU_BUTTON)
            ).click()
        except Exception as e:
            raise Exception(f"Не удалось открыть боттомшит: {str(e)}")

    def delete_note_via_bottom_sheet(self, timeout=10):
        """Выбирает пункт 'Удалить' из боттомшита"""
        self.logger.info("Выбор пункта 'Удалить' из боттомшита")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.DELETE_CONTAINER_XPATH),
                message="Пункт 'Удалить' не найден"
            ).click()

            self.confirm_deletion(timeout)

        except Exception as e:
            raise Exception(f"Не удалось найти или кликнуть 'Удалить': {str(e)}")

    def delete_note_directly(self, timeout=10):
        """Удаляет заметку через глобальное контекстное меню в верхней части экрана"""
        self.logger.info("Удаление заметки через глобальное меню")
        try:
            # Открытие меню "ещё" (три точки)
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.NOTE_OVERFLOW_MENU)
            ).click()

            # Выбор "Удалить"
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.DELETE_CONTAINER_XPATH)
            ).click()

            self.confirm_deletion(timeout)

        except Exception as e:
            raise Exception(f"Не удалось удалить заметку напрямую: {str(e)}")

    def confirm_deletion(self, timeout=5):
        """Подтверждает удаление, если появилось модальное окно"""
        if self.is_element_present(self.DELETE_CONFIRMATION_BUTTON_XPATH, timeout):
            self.logger.info("Подтверждаем удаление")
            self.click(self.DELETE_CONFIRMATION_BUTTON_XPATH, timeout)

    def _safe_send_keys(self, element, text):
        """Безопасный ввод текста — посимвольно, если обычный ввод не работает"""
        self.logger.info(f"Безопасный ввод текста: {text[:20]}...")
        try:
            element.clear()
            element.send_keys(text)
        except:
            for char in text:
                element.send_keys(char)
                time.sleep(0.1)