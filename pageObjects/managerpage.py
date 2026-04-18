from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pageObjects.basepage import BasePage


class ManagerPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.add_customer_btn = (By.XPATH, "//button[@ng-click='addCust()']")
        self.fn_input = (By.XPATH, "//input[@ng-model='fName']")
        self.ln_input = (By.XPATH, "//input[@ng-model='lName']")
        self.postalCode_input = (By.XPATH, "//input[@ng-model='postCd']")
        self.submit_customer = (By.XPATH, "//button[@type='submit']")
        self.open_account_btn = (By.XPATH, "//button[@ng-click='openAccount()']")
        self.submit_account_btn = (By.XPATH, "//button[@type='submit']")
        self.show_customers_btn = (By.XPATH, "//button[@ng-click='showCust()']")
        self.list_fnames = (By.XPATH, "//tbody/tr/td[1]")
        self.list_accnumbers = (By.XPATH, "//tbody/tr/td[4]")
        self.click_home_btn = (By.CSS_SELECTOR, ".btn.home")
        self.customer_rows = (By.XPATH, "//tbody/tr")


    def add_customer(self,fname,lname,postalCode):
        self.click(self.add_customer_btn)
        self.send_keys(self.fn_input,fname)
        self.send_keys(self.ln_input,lname)
        self.send_keys(self.postalCode_input,postalCode)
        self.click(self.submit_customer)

    def open_account(self,fname,lname,currency):
        self.click(self.open_account_btn)
        dropdown_customers = Select(self.driver.find_element(By.ID, "userSelect"))
        dropdown_customers.select_by_visible_text(fname + " " + lname)
        dropdown_currency = Select(self.driver.find_element(By.ID, "currency"))
        dropdown_currency.select_by_value(currency)
        self.click(self.submit_account_btn)


    def get_customer_data(self):
        fnames = []
        acc_numbers = []
        # self.driver.find_element(*self.show_customers_btn).click()
        self.click(self.show_customers_btn)
        self.wait_for_visible(self.customer_rows)
        firstNames = self.driver.find_elements(*self.list_fnames)
        for firstname in firstNames:
            fnames.append(firstname.text)
        # print(fnames)

        accnumbers = self.driver.find_elements(*self.list_accnumbers)
        for accnumber in accnumbers:
            acc_numbers.append(accnumber.text)
        # print(acc_numbers)
        return fnames, acc_numbers

    def click_home(self):
        self.click(self.click_home_btn)
        # self.driver.find_element(*self.click_home_btn).click()


