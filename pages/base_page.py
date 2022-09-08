from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException


class BasePage:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                                  ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                      NoSuchElementException])

    def _clear_input(self, locator=None, element=None):
        if locator:
            element = self.driver.find_element(*locator)

        while len(element.get_attribute('value')) > 0:
            element.send_keys(Keys.BACKSPACE)

    def _scroll_to_bottom_of_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
