import logging

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from time import sleep

COMPANY_LOCATION = (By.XPATH, '//div[contains(@class, "jobsearch-JobInfoHeader-subtitle")]/div[2]/div')
COMPANY_NAME = (By.XPATH, '(//div[contains(@class, "jobsearch-JobInfoHeader-subtitle")]/div[1]/div//a)[1]')
CURRENT_FILTER = (By.XPATH, '//a[contains(@id, "filter")]')
JOB_DESCRIPTION_IFRAME = (By.ID, 'vjs-container-iframe')
PLACEHOLDER_CONTAINER = (By.ID, 'PlaceholderContainer')
POSTED_DATE = (By.CSS_SELECTOR, '.jobsearch-HiringInsights-entry--bullet span:nth-child(2)')
REPORT_JOB_BUTTON = (By.XPATH, '//button[normalize-space()="Report job"]')
TITLE = (By.XPATH, '//div[@class="jobsearch-JobInfoHeader-title-container "]/h1')


def filter_by_filter_name(filter_name):
    return (
        By.ID,
        f'filter-{filter_name}'
    )


def date_filter_by_date_posted(date_posted):
    return (
        By.XPATH,
        f'//a[text()="{date_posted}"]'
    )


class JobDescription(BasePage):
    @property
    def posted_date(self):
        return self.wait.until(ec.presence_of_element_located(POSTED_DATE)).text

    @property
    def title(self):
        return self.wait.until(ec.presence_of_element_located(TITLE)).text

    def click_date_filter_by_date_posted(self, date_posted):
        logging.info(f'Clicking "{date_posted}".')
        element = self.wait.until(ec.element_to_be_clickable(date_filter_by_date_posted(date_posted)))
        self.driver.execute_script("arguments[0].click();", element)

    def click_filter_by_filter_name(self, filter_name):
        logging.info(f'Clicking "{filter_name}" filter.')
        element = self.wait.until(ec.element_to_be_clickable(filter_by_filter_name(filter_name)))
        self.driver.execute_script("arguments[0].click();", element)

    def switch_to_default(self):
        logging.info('Switching to default.')
        self.driver.switch_to.default_content()

    def switch_to_iframe(self):
        logging.info('Switching to "Job Description" iframe.')
        iframe = self.wait.until(ec.visibility_of_element_located(JOB_DESCRIPTION_IFRAME))
        self.driver.switch_to.frame(iframe)

    def wait_for_placeholder_to_disappear(self):
        logging.info('Waiting for "Placeholder container" to disappear.')
        sleep(1)
        self.wait.until(ec.invisibility_of_element_located(PLACEHOLDER_CONTAINER))
