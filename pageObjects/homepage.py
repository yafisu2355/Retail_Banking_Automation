from selenium.webdriver.common.by import By

from pageObjects.basepage import BasePage
from pageObjects.customerpage import CustomerPage
from pageObjects.managerpage import ManagerPage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.manager_login_btn = (By.XPATH, "//button[text()='Bank Manager Login']")
        self.customer_login_btn = (By.XPATH, "//button[text()='Customer Login']")


    def click_manager_login(self):
        self.click(self.manager_login_btn)
        managerpage = ManagerPage(self.driver)
        return managerpage

    def click_customer_login(self):
        self.click(self.customer_login_btn)
        customerpage = CustomerPage(self.driver)
        return customerpage


