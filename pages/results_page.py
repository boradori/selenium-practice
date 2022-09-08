import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from time import sleep

ACTIVATE_BUTTON = (By.ID, 'DesktopSERPJobAlertActivateButton')
BAD_QUERY_HEADER_1 = (By.CSS_SELECTOR, '.jobsearch-NoResult-messageHeader')
BAD_QUERY_HEADER_2 = (By.CSS_SELECTOR, '.bad_query h1')
CLEAR_SEARCHES_BUTTON = (By.XPATH, '//a[@title="Remove all previous searches"]')
COMPANY_LOCATIONS = (By.XPATH, '//div[contains(@class, "slider_container")]//div[@class="companyLocation"]')
JOB_DESCRIPTION_IFRAME = (By.ID, 'vjs-container-iframe')
JOB_RESULTS = (By.CLASS_NAME, 'slider_container')
JOB_TITLES = (By.XPATH, '//div[contains(@class, "slider_container")]//h2[contains(@class, "jobTitle")]//span')
MY_RECENT_SEARCHES = (By.XPATH, '//h2[normalize-space()="My recent searches"]')
NEXT_PAGE = (By.XPATH, "//a[@aria-label='Next Page']")
POPOVER_CLOSE_BUTTON = (By.XPATH, '//div[@id="popover-x"]')
RECENT_SEARCHES_1 = (By.CSS_SELECTOR, '.jobsearch-DesktopRecentSearches ul li a')
RECENT_SEARCHES_2 = (By.CSS_SELECTOR, '#recentsearches ul li a')


def header_text_by_title_and_location(title, location):
    return (
        By.XPATH,
        f'//h1[normalize-space()="{title} jobs in {location}"]'
    )


def pagination_button_by_page_number(page_number):
    return (
        By.XPATH,
        f'//*[@aria-label="{page_number}"]'
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

    def click_clear_searches_button(self):
        logging.info('Clicking "clear searches" button.')
        self.clear_searches_button.click()

    def click_pagination_by_page_number(self, page_number):
        logging.info(f'Clicking page number: {page_number}.')
        seconds_waited = 0

        while seconds_waited < 10:
            try:
                element = self.driver.find_element(*pagination_button_by_page_number(page_number))
                self._scroll_to_element(element)
                element.click()
                break
            except NoSuchElementException:
                sleep(1)
                seconds_waited += 1

        sleep(2)

    def get_bad_query_header_text(self):
        logging.info('Getting bad query header text.')
        try:
            element = self.driver.find_element(*BAD_QUERY_HEADER_1)
        except NoSuchElementException:
            element = self.driver.find_element(*BAD_QUERY_HEADER_2)

        return element.text

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
        try:
            self.driver.find_element(By.CLASS_NAME, 'jobsearch-DesktopRecentSearches')
            elements = self.driver.find_elements(*RECENT_SEARCHES_1)
        except NoSuchElementException:
            self.driver.find_element(By.ID, 'recentsearches')
            elements = self.driver.find_elements(*RECENT_SEARCHES_2)

        return [' '.join(element.text.split()).strip() for element in elements]

    def switch_to_default(self):
        logging.info('Switching to default.')
        self.driver.switch_to.default_content()

    def switch_to_iframe(self):
        logging.info('Switching to "Job Description" iframe.')
        iframe = self.wait.until(ec.visibility_of_element_located(JOB_DESCRIPTION_IFRAME))
        self.driver.switch_to.frame(iframe)

    def wait_for_job_results_to_display(self):
        logging.info('Waiting for job results to fully display.')
        self.wait.until(ec.presence_of_all_elements_located(JOB_RESULTS))

    def wait_for_url_to_change(self, url):
        logging.info('Waiting for URL to change.')
        self.wait.until(ec.url_contains(f'indeed.com/jobs?q={url}'))
