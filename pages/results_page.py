import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from time import sleep

BAD_QUERY_HEADER = (By.XPATH, '//div[@class="bad_query"]/h1')
CLEAR_SEARCHES_BUTTON = (By.XPATH, '//a[@title="Remove all previous searches"]')
COMPANY_LOCATIONS = (By.XPATH, '//div[contains(@class, "slider_container")]//div[@class="companyLocation"]')
JOB_RESULTS = (By.CLASS_NAME, 'slider_container')
JOB_TITLES = (By.XPATH, '//div[contains(@class, "slider_container")]//h2[contains(@class, "jobTitle")]//span')
MY_RECENT_SEARCHES = (By.XPATH, '//h2[normalize-space()="My recent searches"]')
POPOVER_CLOSE_BUTTON = (By.XPATH, '//div[@id="popover-x"]')
RECENT_SEARCHES = (By.XPATH, '//div[@id="recentsearches"]/ul/li/a')


def header_text_by_title_and_location(title, location):
    return (
        By.XPATH,
        f'//h1[normalize-space()="{title} jobs in {location}"]'
    )


class ResultsPage(BasePage):
    @property
    def clear_searches_button(self):
        return self.wait.until(ec.element_to_be_clickable(CLEAR_SEARCHES_BUTTON))

    @property
    def company_locations(self):
        return self.wait.until(ec.presence_of_all_elements_located(COMPANY_LOCATIONS))

    @property
    def job_results(self):
        return self.wait.until(ec.presence_of_all_elements_located(JOB_RESULTS))

    @property
    def job_titles(self):
        return self.wait.until(ec.presence_of_all_elements_located(JOB_TITLES))

    @property
    def popover_close_button(self):
        return self.driver.find_element(*POPOVER_CLOSE_BUTTON)

    @property
    def recent_searches(self):
        return self.wait.until(ec.presence_of_all_elements_located(RECENT_SEARCHES))

    def click_clear_searches_button(self):
        logging.info('Clicking "clear searches" button.')
        self.clear_searches_button.click()

    def get_bad_query_header_text(self):
        logging.info('Getting bad query header text.')
        seconds_waited = 0

        while seconds_waited < 10:
            try:
                return self.driver.find_element(*BAD_QUERY_HEADER).text
            except NoSuchElementException:
                sleep(1)
                seconds_waited += 1

        return None

    def get_company_locations(self):
        logging.info('Getting company locations.')
        return [' '.join(element.get_attribute('innerText').split()).strip() for element in self.company_locations]

    def get_header_text(self, title, location):
        logging.info('Getting header text.')
        return self.wait.until(
            ec.visibility_of_element_located(header_text_by_title_and_location(title, location))).text

    def get_job_titles(self):
        logging.info('Getting job titles.')
        return [' '.join(element.text.split()).strip() for element in self.job_titles]

    def get_recent_searches(self):
        logging.info('Getting recent searches.')
        seconds_waited = 0

        while seconds_waited < 10:
            try:
                return [' '.join(element.text.split()).strip() for element in
                        self.driver.find_elements(*RECENT_SEARCHES)]
            except NoSuchElementException:
                sleep(1)
                seconds_waited += 1

        return []

    def wait_for_job_results_to_display(self):
        logging.info('Waiting for job results to fully display.')
        self.wait.until(ec.presence_of_all_elements_located(JOB_RESULTS))

    def wait_for_url_to_change(self, url):
        logging.info('Waiting for URL to change.')
        self.wait.until(ec.url_contains(f'indeed.com/jobs?q={url}'))
