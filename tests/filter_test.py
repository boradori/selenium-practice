import logging

import pytest
from pages.search_page import SearchPage
from pages.results_page import ResultsPage
from components.job_description import JobDescription
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.all
@pytest.mark.filter
@pytest.mark.usefixtures('class_setup')
class TestFilter:
    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self):
        self.search_page = SearchPage(self.driver)
        self.results_page = ResultsPage(self.driver)
        self.jd = JobDescription(self.driver)
        yield

    def test_user_can_filter_by_date_posted(self):
        if self.driver.name == 'firefox':
            self.search_page.switch_to_iframe()
            self.search_page.close_google_sign_in()
            self.search_page.switch_to_default()

        title = 'Quality Assurance Engineer'
        location = 'Seattle, WA'
        self.search_page.enter_title(title)
        self.search_page.enter_location(location)
        self.search_page.submit_job_search_by_pressing_enter()

        if self.driver.name == 'firefox':
            self.jd.wait_for_placeholder_to_disappear()

        self.jd.click_filter_by_filter_name('dateposted')
        self.jd.click_date_filter_by_date_posted('Last 24 hours')

        if self.driver.name == 'firefox':
            self.jd.wait_for_placeholder_to_disappear()

        try:
            close_button = self.results_page.popover_close_button
            close_button.click()
            logging.info('Pop up is closed.')
        except NoSuchElementException:
            logging.info('Pop up is not displayed.')

        try:
            self.driver.find_element('id', 'vjs-container-iframe')
            logging.info('Iframe')

            for job_card in self.results_page.job_cards:
                job_card.click()
                self.jd.switch_to_iframe()

                logging.info('Verifying that the job description is posted in last 24 hours.')
                expected_post_date = ['posted today', 'posted just posted', 'posted 1 day ago']
                actual_post_date = self.jd.posted_date.lower()
                logging.info(f'Expected post dates: {expected_post_date}')
                logging.info(f'Actual post date:    {actual_post_date}')
                assert actual_post_date in expected_post_date

                self.jd.switch_to_default()
        except NoSuchElementException:
            logging.info('No iframe')

            for job_card in self.results_page.job_cards:
                job_card.click()

                logging.info('Verifying that the job description is posted in last 24 hours.')
                expected_post_date = ['posted today', 'posted just posted', 'posted 1 day ago']
                actual_post_date = self.jd.posted_date.lower()
                logging.info(f'Expected post dates: {expected_post_date}')
                logging.info(f'Actual post date:    {actual_post_date}')
                assert actual_post_date in expected_post_date
