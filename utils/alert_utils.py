from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class AlertUtils:

    def __init__(self,driver):
        self.driver = driver


    def accept_alert(self,timeout=10):
        alert = WebDriverWait(self.driver,timeout).until(expected_conditions.alert_is_present())
        text = alert.text
        alert.accept()
        return text