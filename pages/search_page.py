import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

FIND_JOBS_BUTTON = (By.XPATH, '//button[@type="submit"]')
LOCATION_FIELD = (By.ID, 'text-input-where')
TITLE_FIELD = (By.ID, 'text-input-what')


class SearchPage(BasePage):
    @property
    def find_jobs_button(self):
        return self.wait.until(ec.element_to_be_clickable(FIND_JOBS_BUTTON))

    @property
    def location_field(self):
        return self.wait.until(ec.visibility_of_element_located(LOCATION_FIELD))

    @property
    def title_field(self):
        return self.wait.until(lambda dr: dr.find_element(*TITLE_FIELD))

    def enter_location(self, location):
        logging.info(f'Entering "{location}".')
        self._clear_input(element=self.location_field)
        self.location_field.send_keys(location)

    def enter_title(self, title):
        logging.info(f'Entering "{title}".')
        self._clear_input(element=self.title_field)
        self.title_field.send_keys(title)
    
    def submit_job_search(self):
        logging.info('Submitting job search.')
        self.find_jobs_button.click()
