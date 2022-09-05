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
        self.search_page.enter_title('Quality Assurance Engineer')
        self.search_page.enter_location('Seattle, WA')
        self.search_page.submit_job_search()

        logging.info('Verifying that there are correct number of results.')
        expected_number = 15
        actual_number = len(self.results_page.job_results)
        logging.info(f'Expected number: {expected_number}')
        logging.info(f'Actual number:   {actual_number}')
        assert expected_number == actual_number

        sleep(5)
