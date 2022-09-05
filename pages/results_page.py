import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


JOBS = (By.CLASS_NAME, 'slider_container')


class ResultsPage(BasePage):
    @property
    def job_results(self):
        return self.wait.until(lambda dr: dr.find_elements(*JOBS))
