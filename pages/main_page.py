from appium.webdriver.common.appiumby import AppiumBy
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

from core.base_page import BasePage


class MainPage(BasePage):
    """
    Страница главного экрана приложения Google Keep.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    # === Локаторы UI элементов ===

    CREATE_NOTE_BUTTON = (
        AppiumBy.ID,
        "com.google.android.keep:id/speed_dial_create_close_button"
    )

    SELECT_TEXT_OPTION = (
        AppiumBy.XPATH,
        '//android.widget.Button[@text="Текст"]'
    )

    NOTE_TITLE_TEMPLATE = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.google.android.keep:id/index_note_title" and @text="{title}"]'
    )

    NOTE_OVERFLOW_MENU = (
        AppiumBy.ACCESSIBILITY_ID,
        "Ещё"
    )

    DELETE_OPTION_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Удалить"]'
    )

    DELETE_CONFIRMATION_BUTTON_XPATH = (
        AppiumBy.XPATH,
        '//android.widget.Button[@text="Удалить"]'
    )

    SKIP_ONBOARDING_BUTTON = (
        AppiumBy.ID,
        "com.google.android.keep:id/skip_welcome"
    )

    # Новый локатор для поиска заметки по заголовку с улучшенной стабильностью
    NOTE_CARD_BY_TITLE = (
        AppiumBy.XPATH,
        '//androidx.cardview.widget.CardView[@content-desc="TestNote_{title}. Пустая заметка . "]'
    )

    # === Методы для взаимодействия ===

    def tap_create_note(self, timeout=15):
        """Нажимает на кнопку создания заметки"""
        self.logger.info("Клик по кнопке создания заметки")
        self.wait_for_element_and_click(self.CREATE_NOTE_BUTTON, timeout)

    def skip_onboarding_if_present(self, timeout=10):
        """Пропускает онбординг, если он отображается"""
        if self.is_element_present(self.SKIP_ONBOARDING_BUTTON, timeout):
            self.logger.info("Пропуск онбординга")
            self.click(self.SKIP_ONBOARDING_BUTTON, timeout)

    def select_text_note_type(self, timeout=10):
        """Выбирает тип заметки 'Текст'"""
        self.logger.info("Выбор типа заметки: Текст")
        self.wait_for_element_and_click(self.SELECT_TEXT_OPTION, timeout)

    def is_note_exists(self, title, timeout=10):
        """Проверяет существование заметки по заголовку"""
        note_locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@resource-id="com.google.android.keep:id/index_note_title" and @text="{title}"]'
        )
        return self.is_element_present(note_locator, timeout)

    def delete_note_directly_by_title(self, title, timeout=10):
        """
        Удаляет заметку напрямую через контекстное меню без открытия
        """
        self.logger.info(f"Удаление заметки '{title}' напрямую через контекстное меню")

        note_locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@resource-id="com.google.android.keep:id/index_note_title" and @text="{title}"]'
        )

        # Шаг 1: Найти заметку и выполнить долгое нажатие
        element = self.find_element(note_locator, timeout)
        self.long_press(element, duration=2)

        # Шаг 2: Кликнуть по три точкам (⋮) в верхней части экрана
        self.logger.info("Ждём появления три точек (⋮)")
        try:
            self.wait_for_element_and_click(self.NOTE_OVERFLOW_MENU, timeout)
        except Exception as e:
            raise Exception(f"Не удалось найти или кликнуть три точки (⋮). {str(e)}")

        # Шаг 3: Ждём появления пункта 'Удалить' в меню
        self.logger.info("Ждём появления пункта 'Удалить' в меню")
        try:
            self.wait_for_element_and_click(self.DELETE_OPTION_XPATH, timeout)
        except Exception as e:
            raise Exception(f"Не удалось найти или кликнуть пункт 'Удалить' в меню. {str(e)}")

        # Шаг 4: Подтвердить удаление, если есть диалог
        self.confirm_deletion(timeout)

    def open_note_by_title(self, title, timeout=10):
        """Открывает заметку по её заголовку"""
        self.logger.info(f"Открытие заметки '{title}'")
        note_locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@resource-id="com.google.android.keep:id/index_note_title" and @text="{title}"]'
        )
        self.wait_for_element_and_click(note_locator, timeout)

    def confirm_deletion(self, timeout=5):
        """Подтверждает удаление, если появилось модальное окно"""
        if self.is_element_present(self.DELETE_CONFIRMATION_BUTTON_XPATH, timeout):
            self.logger.info("Подтверждаем удаление")
            self.click(self.DELETE_CONFIRMATION_BUTTON_XPATH, timeout)

    def long_press(self, element, duration=2):
        """Выполняет долгое нажатие через W3C Actions"""
        self.logger.info("W3C: Выполняем долгое нажатие на элемент")
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        action = ActionBuilder(self.driver, mouse=finger)
        action.pointer_action.move_to(element).pointer_down().pause(duration).pointer_up()
        action.perform()

    def find_element(self, locator, timeout=10):
        """Безопасный поиск элемента с сообщением об ошибке"""
        self.logger.debug(f"Поиск элемента: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Не найден элемент: {locator}"
        )

    def click(self, locator, timeout=10):
        """Клик по элементу с ожиданием кликабельности"""
        element = self.wait_for_element_to_be_clickable(locator, timeout)
        self.logger.info(f"Клик по элементу: {locator}")
        element.click()

    def wait_for_element_and_click(self, locator, timeout=10):
        """Ожидает элемент и кликает по нему"""
        element = self.wait_for_element_to_be_clickable(locator, timeout)
        self.logger.info(f"Клик по элементу: {locator}")
        element.click()

    def is_element_present(self, locator, timeout=10):
        """Проверяет наличие элемента на странице"""
        try:
            self.find_element(locator, timeout)
            return True
        except:
            return False

    def wait_for_note_deletion(self, title, timeout=15):
        """Ожидает исчезновения заметки с главной страницы"""
        self.logger.info(f"Ожидаем исчезновения заметки '{title}'")

        note_locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@resource-id="com.google.android.keep:id/index_note_title" and @text="{title}"]'
        )

        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(note_locator)
            )
            return True
        except:
            self.logger.warning(f"Заметка '{title}' всё ещё отображается")
            return False

    # === Вспомогательные методы ===

    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """Ожидает, пока элемент станет кликабельным"""
        by, value = locator
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value)),
            message=f"Элемент не стал кликабельным за {timeout} секунд"
        )