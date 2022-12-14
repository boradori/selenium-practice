import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


CREDENTIAL_PICKER_IFRAME = (By.XPATH, '//iframe[@title="Sign in with Google Dialog"]')
FIND_JOBS_BUTTON = (By.XPATH, '//button[@class="yosegi-InlineWhatWhere-primaryButton"]')
GOOGLE_SIGN_IN_CLOSE_BUTTON = (By.ID, 'close')
LOCATION_FIELD = (By.ID, 'text-input-where')
SIGN_IN_BUTTON = (By.XPATH, '(//a[contains(@href, "https://secure.indeed.com/account/login")])[1]')
TITLE_FIELD = (By.ID, 'text-input-what')


class SearchPage(BasePage):
    @property
    def find_jobs_button(self):
        return self.wait.until(ec.element_to_be_clickable(FIND_JOBS_BUTTON))

    @property
    def google_sign_in_close_button(self):
        return self.wait.until(ec.visibility_of_element_located(GOOGLE_SIGN_IN_CLOSE_BUTTON))

    @property
    def location_field(self):
        return self.wait.until(ec.presence_of_element_located(LOCATION_FIELD))

    @property
    def sign_in_button(self):
        return self.wait.until(ec.element_to_be_clickable(SIGN_IN_BUTTON))

    @property
    def title_field(self):
        return self.wait.until(ec.presence_of_element_located(TITLE_FIELD))

    def click_sign_in_button(self):
        logging.info('Clicking Sign in button.')
        self.sign_in_button.click()

    def close_google_sign_in(self):
        logging.info('Closing Google Sign in container.')
        self.driver.execute_script('arguments[0].click();', self.google_sign_in_close_button)

    def enter_location(self, location):
        logging.info(f'Entering "{location}" in location field.')
        self._clear_input(element=self.location_field)
        self.location_field.send_keys(location)

    def enter_title(self, title):
        logging.info(f'Entering "{title}" in title field.')
        self.wait.until(ec.presence_of_element_located(TITLE_FIELD))
        self._clear_input(element=self.title_field)
        self.title_field.send_keys(title)

    def navigate(self):
        logging.info('Navigating to the "Search" page.')
        self.driver.get('https://indeed.com/')
    
    def submit_job_search(self):
        logging.info('Submitting job search.')
        self.find_jobs_button.click()

    def submit_job_search_by_pressing_enter(self):
        logging.info('Submitting job search.')
        self.title_field.send_keys(Keys.ENTER)

    def switch_to_default(self):
        logging.info('Switching to default.')
        self.driver.switch_to.default_content()

    def switch_to_iframe(self):
        logging.info('Switching to "Google Sign in" iframe.')
        iframe = self.wait.until(ec.visibility_of_element_located(CREDENTIAL_PICKER_IFRAME))
        self.driver.switch_to.frame(iframe)
