# labels_page.py

from appium.webdriver.common.appiumby import AppiumBy
import logging

from core.base_page import BasePage


class LabelsPage(BasePage):
    """
    Страница работы с метками (Labels) в Google Keep.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    # === Локаторы элементов ===

    ADD_LABEL_BUTTON = (
        AppiumBy.ID,
        "com.google.android.keep:id/add_label_button"
    )

    LABEL_NAME_FIELD = (
        AppiumBy.ID,
        "com.google.android.keep:id/label_text"
    )

    SAVE_LABEL_BUTTON = (
        AppiumBy.ID,
        "com.google.android.keep:id/save"
    )

    LABEL_ITEM_TEMPLATE = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="com.google.android.keep:id/label_text" and @text="{label_name}"]'
    )

    DRAWER_LAYOUT = (
        AppiumBy.ID,
        "com.google.android.keep:id/drawer_layout"
    )

    ADD_LABEL_TEXT_FIELD = (
        AppiumBy.ID,
        "com.google.android.keep:id/add_label_text"
    )

    LABEL_ITEM = (
        AppiumBy.XPATH,
        '//*[@resource-id="com.google.android.keep:id/label_item"]'
    )

    # === Методы для работы с метками ===

    def is_menu_opened(self):
        """Проверяет, открыто ли меню меток"""
        self.logger.info("Проверка: открыто ли меню меток")
        return self.is_element_present(self.DRAWER_LAYOUT)

    def open_add_label_form(self):
        """Открывает форму добавления метки"""
        self.logger.info("Открытие формы добавления метки")
        self.click(self.ADD_LABEL_BUTTON)

    def is_add_label_form_opened(self):
        """Проверяет, открыта ли форма добавления метки"""
        self.logger.info("Проверка: открыта ли форма добавления метки")
        return self.is_element_present(self.ADD_LABEL_TEXT_FIELD)

    def add_label(self, name):
        """Добавляет новую метку с указанным именем"""
        self.logger.info(f"Добавление метки: {name}")
        name_field = self.find_element(self.ADD_LABEL_TEXT_FIELD)
        name_field.clear()
        name_field.send_keys(name)
        self.driver.press_keycode(66)  # Нажатие Enter

    def save_label(self):
        """Сохраняет созданную метку"""
        self.logger.info("Сохранение метки")
        self.click(self.SAVE_LABEL_BUTTON)

    def is_label_exists(self, name):
        """Проверяет существование метки с указанным именем"""
        self.logger.info(f"Проверка существования метки: {name}")
        label_locator = (
            AppiumBy.XPATH,
            f'//*[@resource-id="com.google.android.keep:id/label_item" and @text="{name}"]'
        )
        return self.is_element_present(label_locator)