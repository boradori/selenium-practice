import logging
import pytest
from pages.search_page import SearchPage
from pages.results_page import ResultsPage
from time import sleep


@pytest.mark.search
@pytest.mark.usefixtures('class_setup')
class TestSearch:
    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self):
        self.search_page = SearchPage(self.driver)
        self.results_page = ResultsPage(self.driver)
        yield

    def test_search_by_title_and_location(self):
        title = 'Quality Assurance Engineer'
        location = 'Seattle, WA'
        self.search_page.enter_title(title)
        self.search_page.enter_location(location)
        self.search_page.submit_job_search()

        logging.info('Verifying that the result header displays the correct title and location.')
        logging.info(f'Expected title: {title}')
        logging.info(f'Expected location: {location}')
        actual_header = self.results_page.header.text
        logging.info(f'Actual header: {actual_header}')
        assert title in actual_header and location in actual_header

        logging.info('Verifying that there are correct number of results.')
        expected_number = 15
        actual_number = len(self.results_page.job_results)
        logging.info(f'Expected number: {expected_number}')
        logging.info(f'Actual number:   {actual_number}')
        assert expected_number == actual_number

