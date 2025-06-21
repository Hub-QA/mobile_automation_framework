# core/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator, timeout=10):
        """Кликает по элементу после его ожидания"""
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def find_element(self, locator, timeout=10):
        """Находит элемент после его ожидания"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def is_element_present(self, locator, timeout=10):
        """Проверяет наличие элемента на экране"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_element_and_click(self, locator, timeout=10):
        """Ожидает кликабельности элемента и кликает по нему"""
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()