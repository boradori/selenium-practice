import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')


@pytest.fixture(scope='class')
def class_setup(request):
    browser = request.config.getoption('--browser')

    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "ie":
        driver = webdriver.Ie()
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        driver = webdriver.Chrome()

    driver.get('https://indeed.com')
    driver.implicitly_wait(10)

    if request.cls:
        request.cls.driver = driver
        request.cls.browser = browser

    yield driver
    driver.quit()
