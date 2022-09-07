import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


CONTINUE_BUTTON = (By.XPATH, '//button[@data-tn-element="auth-page-email-submit-button"]')
EMAIL_FIELD = (By.XPATH, '//input[@name="__email"]')
HEADER = (By.XPATH, '//h1[@data-tn-section="auth-page-header--enter-email"]')
INCORRECT_PASSWORD_ERROR_MESSAGE = (By.XPATH, '//div[contains(text(),"Error: Incorrect password")]')
PASSWORD_FIELD = (By.XPATH, '//input[@name="__password"]')
SIGN_IN_BUTTON = (By.XPATH, '//button[@data-tn-element="auth-page-sign-in-password-form-submit-button"]')


class LoginPage(BasePage):
    @property
    def continue_button(self):
        return self.wait.until(ec.element_to_be_clickable(CONTINUE_BUTTON))

    @property
    def email_field(self):
        return self.wait.until(ec.visibility_of_element_located(EMAIL_FIELD))

    @property
    def incorrect_password_error_message(self):
        return self.wait.until(ec.visibility_of_element_located(INCORRECT_PASSWORD_ERROR_MESSAGE))

    @property
    def password_field(self):
        return self.wait.until(ec.visibility_of_element_located(PASSWORD_FIELD))

    @property
    def sign_in_button(self):
        return self.wait.until(ec.visibility_of_element_located(SIGN_IN_BUTTON))

    def click_continue_button(self):
        self.continue_button.click()

    def click_sign_in_button(self):
        self.sign_in_button.click()

    def enter_email_address(self, email_address):
        logging.info(f'Entering email address, {email_address}.')
        self._clear_input(element=self.email_field)
        self.email_field.send_keys(email_address)

    def enter_password(self, password):
        logging.info('Entering password.')
        self._clear_input(element=self.password_field)
        self.password_field.send_keys(password)

    def get_header_text(self):
        return self.wait.until(ec.visibility_of_element_located(HEADER)).text

    def navigate(self):
        logging.info('Navigating to the "Login" page.')
        self.driver.get('https://secure.indeed.com/')
