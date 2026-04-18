import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.basepage import BasePage


class CustomerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.customer_dropdown = (By.ID, "userSelect")
        self.customer_login_btn = (By.XPATH, "//button[@type='submit']")
        self.deposit_btn = (By.XPATH, "//button[@ng-click='deposit()']")
        self.input_amount = (By.XPATH, "//input[@ng-model='amount']")
        self.submit_transaction = (By.XPATH, "//button[@type='submit']")
        self.check_balance_text = (By.XPATH, "//strong[2]")
        self.transaction_text = (By.XPATH, "//span[@ng-show='message']")
        self.withdrawal_btn = (By.XPATH, "//button[@ng-click='withdrawl()']")
        self.transaction_btn = (By.XPATH, "//button[@ng-click='transactions()']")
        self.logout_btn = (By.CSS_SELECTOR, ".btn.logout")


    def select_customer(self,fname,lname):
        dropdown_customers = Select(self.driver.find_element(*self.customer_dropdown))
        dropdown_customers.select_by_visible_text(fname + " " + lname)
        # time.sleep(2) -- explicit wait since it takes 2 sec for login button to appear

    def click_customer_login(self):
        self.click(self.customer_login_btn)



    def get_balance(self):
        return int(self.get_text(self.check_balance_text))

    def click_deposit(self):
        self.click(self.deposit_btn)

    def deposit(self,deposit_amt):
        self.send_keys(self.input_amount, str(deposit_amt))
        self.click(self.submit_transaction)

        depost_message = self.get_text(self.transaction_text)
        balance_after_deposit = int(self.get_text(self.check_balance_text))
        return depost_message, balance_after_deposit

    def click_withdraw(self):
        self.click(self.withdrawal_btn)

    def withdraw(self, withdrawal_amt):
        self.click(self.withdrawal_btn)
        time.sleep(1)  # fallback for this buggy UI

        element = self.wait_for_visible(self.input_amount)
        element.clear()
        element.send_keys(str(withdrawal_amt))

        self.click(self.submit_transaction)
        time.sleep(1)

        withdrawal_message = self.get_text(self.transaction_text)
        balance_after_withdrawal = int(self.get_text(self.check_balance_text))

        return withdrawal_message, balance_after_withdrawal



    def click_transactions(self):
        self.click(self.transaction_btn)

    def get_transactions(self):
        creditz = []
        debitz = []
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//table"))
        )
        rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
        for row in rows:
            amount = int(row.find_element(By.XPATH, "td[2]").text)
            txn_type = row.find_element(By.XPATH, "td[3]").text
            if txn_type == "Credit":
                creditz.append(amount)
            else:
                debitz.append(amount)

        return creditz,debitz

    def customer_logout(self):
        self.click(self.logout_btn)










