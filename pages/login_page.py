import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

        # Locators
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.XPATH, "//button[text()='Sign In']")
        self.sms_panel_text = (By.XPATH, "//div/span[text()='SMS Panel']")

    def enter_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.username_input))
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_login_successful(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.sms_panel_text))
            return True
        except TimeoutException:
            return False