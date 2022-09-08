import logging

import pytest
from pages.search_page import SearchPage
from pages.results_page import ResultsPage
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.all
@pytest.mark.search
@pytest.mark.usefixtures('class_setup')
class TestSearch:
    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self):
        self.search_page = SearchPage(self.driver)
        self.results_page = ResultsPage(self.driver)
        yield

    def test_search_by_title_and_location(self):
        if self.driver.name == 'firefox':
            self.search_page.switch_to_iframe()
            self.search_page.close_google_sign_in()
            self.search_page.switch_to_default()

        title = 'Quality Assurance Engineer'
        location = 'Seattle, WA'
        self.search_page.enter_title(title)
        self.search_page.enter_location(location)
        self.search_page.submit_job_search_by_pressing_enter()

        logging.info('Verifying that the results page header displays the correct title and location.')
        expected_header = f'{title} jobs in {location}'
        actual_header = self.results_page.get_header_text(title, location)
        logging.info(f'Expected header: {expected_header}')
        logging.info(f'Actual header:   {actual_header}')
        assert expected_header == actual_header

        try:
            close_button = self.results_page.popover_close_button
            close_button.click()
            logging.info("Pop up is closed.")
        except NoSuchElementException:
            logging.info("Pop up did not show up.")

        logging.info('Verifying that there are correct number of results.')
        expected_number = 15
        actual_number = len(self.results_page.job_results)
        logging.info(f'Expected number: {expected_number}')
        logging.info(f'Actual number:   {actual_number}')
        assert expected_number == actual_number

    def test_search_results_contain_correct_job_titles(self):
        logging.info('Verifying that the results contain the correct job titles.')
        actual_titles = self.results_page.get_job_titles()

        for title in actual_titles:
            logging.info(f'Actual title: {title}')
            assert 'quality' in title.lower() or 'test' in title.lower() or 'QA' in title or 'SDET' in title or 'automation' in title.lower()

    def test_search_results_contain_correct_location(self):
        logging.info('Verifying that the results contain the correct company locations.')
        actual_locations = self.results_page.get_company_locations()

        for location in actual_locations:
            logging.info(f'Actual location: {location}')
            assert 'WA' in location or 'Washington State'.lower() in location.lower()

    def test_user_can_paginate(self):
        self.results_page.click_pagination_by_page_number('2')

        try:
            close_button = self.results_page.popover_close_button
            close_button.click()
            logging.info("Pop up is closed.")
        except NoSuchElementException:
            logging.info("Pop up did not show up.")

        logging.info('Verifying that there are correct number of results.')
        expected_number = 15
        actual_number = len(self.results_page.job_results)
        logging.info(f'Expected number: {expected_number}')
        logging.info(f'Actual number:   {actual_number}')
        assert expected_number == actual_number

        logging.info('Verifying that the results contain the correct job titles.')
        actual_titles = self.results_page.get_job_titles()

        for title in actual_titles:
            logging.info(f'Actual title: {title}')
            assert 'quality' in title.lower() or 'test' in title.lower() or 'qa' in title.lower() or 'sdet' in title.lower() or 'automation' in title.lower()

        logging.info('Verifying that the results contain the correct company locations.')
        actual_locations = self.results_page.get_company_locations()

        for location in actual_locations:
            logging.info(f'Actual location: {location}')
            assert 'WA' in location or 'Washington State'.lower() in location.lower()

    def test_search_by_invalid_title(self):
        title = 'asdfasdf'
        location = 'Seattle, WA'
        self.search_page.enter_title(title)
        self.search_page.enter_location(location)
        self.search_page.submit_job_search_by_pressing_enter()

        self.results_page.wait_for_url_to_change(title)

        try:
            close_button = self.results_page.popover_close_button
            close_button.click()
            logging.info("Pop up is closed.")
        except NoSuchElementException:
            logging.info("Pop up did not show up.")

        logging.info('Verifying that the bad query header text contains the job title (search term).')
        expected_bad_query_header_text = f'The search {title} jobs in {location} did not match any jobs.'
        actual_bad_query_header_text = self.results_page.get_bad_query_header_text()
        logging.info(f'Expected bad query header text: {expected_bad_query_header_text}')
        logging.info(f'Actual bad query header text:   {actual_bad_query_header_text}')
        assert actual_bad_query_header_text in expected_bad_query_header_text

        logging.info('Verifying that the recent searches contain the previous searches.')
        expected_recent_searches = ['Quality Assurance Engineer - Seattle, WA']
        actual_recent_searches = self.results_page.get_recent_searches()
        logging.info(f'Expected recent searches: {expected_recent_searches}')
        logging.info(f'Actual recent searches:   {actual_recent_searches}')
        assert expected_recent_searches == actual_recent_searches
