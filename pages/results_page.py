import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


HEADER = (By.ID, 'jobsInLocation')
JOBS = (By.CLASS_NAME, 'slider_container')


class ResultsPage(BasePage):
    @property
    def header(self):
        return self.wait.until(ec.visibility_of_element_located(HEADER))

    @property
    def job_results(self):
        return self.wait.until(ec.visibility_of_all_elements_located(JOBS))

