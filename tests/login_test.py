import logging
import pytest
from pages.login_page import LoginPage
from pages.search_page import SearchPage


@pytest.mark.all
@pytest.mark.login
@pytest.mark.usefixtures('class_setup')
class TestLogin:
    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self):
        self.login_page = LoginPage(self.driver)
        self.search_page = SearchPage(self.driver)

        if self.driver.current_url != 'https://secure.indeed.com/':
            self.login_page.navigate()

            logging.info('Verifying that the header text is "Ready to take the next step?".')
            assert self.login_page.get_header_text() == 'Ready to take the next step?'
        yield

    # @pytest.mark.skip(reason="hCaptcha")
    def test_invalid_login_with_invalid_password(self):
        invalid_username = 'sepal31129@vasqa.com'
        password = 'qpalqpal1'

        self.login_page.enter_email_address(invalid_username)
        self.login_page.click_continue_button()

        self.login_page.enter_password(password)
        self.login_page.click_sign_in_button()

        logging.info('Verifying that the incorrect password error message is displayed.')
        expected_message = 'Error: Incorrect password'
        actual_message = self.login_page.incorrect_password_error_message.text
        logging.info(f'Expected message: {expected_message}')
        logging.info(f'Actual message:   {actual_message}')
        assert expected_message == actual_message

    # @pytest.mark.skip(reason="hCaptcha")
    def test_valid_login_with_valid_email_address_and_password(self):
        valid_username = 'sepal31129@vasqa.com'
        password = 'qpalqpal'

        self.login_page.enter_email_address(valid_username)
        self.login_page.click_continue_button()

        self.login_page.enter_password(password)
        self.login_page.click_sign_in_button()

        assert self.driver.current_url == 'https://secure.indeed.com/auth'

