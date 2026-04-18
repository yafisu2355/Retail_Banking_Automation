import os
import pytest_html

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

def pytest_addoption(parser):
    parser.addoption("--browser_names", action="store",default="chrome")

@pytest.fixture(scope="function")
def BrowserInstance(request):
    browser = request.config.getoption("--browser_names")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # service = ChromeService("/Users/aarif/Documents/chromedriver")  # update path
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        # service = FirefoxService()  # OR give geckodriver path
        driver = webdriver.Firefox(options=options)

    # Common setup (no duplication)
    driver.implicitly_wait(5)
    # driver.maximize_window()
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("BrowserInstance", None)

        if driver:
            reports_dir = os.path.join(os.getcwd(), "reports")
            os.makedirs(reports_dir, exist_ok=True)

            file_name = report.nodeid.replace("::", "_").replace("/", "_") + ".png"
            file_path = os.path.join(reports_dir, file_name)

            driver.get_screenshot_as_file(file_path)

            extras.append(pytest_html.extras.image(file_path))

    report.extras = extras