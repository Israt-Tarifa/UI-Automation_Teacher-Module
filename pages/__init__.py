class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)


        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.XPATH, "//button[text()='Sign In']")