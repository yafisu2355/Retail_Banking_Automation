import json
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.customerpage import CustomerPage
from pageObjects.homepage import HomePage
from pageObjects.managerpage import ManagerPage
from utils.alert_utils import AlertUtils

# test_data_path = "/Users/aarif/Desktop/pythonn/examples/Retail_Banking_Automation/data/test_endToendGlobalSQA.json"
# with open(test_data_path) as json_file:
#     test_data = json.load(json_file)
#     data_list = test_data["data"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
test_data_path = os.path.join(BASE_DIR, "data", "test_endToendGlobalSQA.json")

with open(test_data_path) as json_file:
    test_data = json.load(json_file)
    data_list = test_data["data"]

@pytest.mark.parametrize("item",data_list)
def test_endToend(BrowserInstance,item):
    driver = BrowserInstance

    homepage = HomePage(driver)
    managerpage = homepage.click_manager_login()
    managerpage.add_customer(item["fname"], item["lname"],item["postalCode"])

    alert_util = AlertUtils(driver)
    customer_text = alert_util.accept_alert()
    print(customer_text)

    managerpage.open_account(item["fname"], item["lname"],item["currency"])
    account_creation_text = alert_util.accept_alert()
    account_number_generated = account_creation_text.split(":")[-1]

    fnames, acc_numbers = managerpage.get_customer_data()
    dict_name_acc = dict(zip(fnames, acc_numbers))
    assert account_number_generated == dict_name_acc[item["fname"]]

    managerpage.click_home()

    customerpage = homepage.click_customer_login()
    customerpage.select_customer(item["fname"], item["lname"])
    customerpage.click_customer_login()
    initial_balance = customerpage.get_balance()
    customerpage.click_deposit()
    depost_message, balance_after_deposit = customerpage.deposit(item["deposit_amt"])
    assert "successful" in depost_message.lower()
    assert balance_after_deposit == initial_balance + item["deposit_amt"]
    customerpage.click_withdraw()
    withdrawal_message, balance_after_withdrawal = customerpage.withdraw(item["withdrawal_amt"])
    assert "successful" in withdrawal_message.lower()
    assert balance_after_withdrawal == initial_balance + item["deposit_amt"] - item["withdrawal_amt"]
    customerpage.click_transactions()
    creditz, debitz = customerpage.get_transactions()
    expected_bal = sum(creditz) - sum(debitz)
    assert expected_bal == balance_after_withdrawal

    customerpage.customer_logout()
