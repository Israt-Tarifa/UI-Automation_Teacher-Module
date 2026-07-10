import os
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()


def _navigate_to_login_page(driver):
    """Navigates to the Base URL and returns a LoginPage object."""
    site_url = os.getenv("BASE_URL")
    driver.get(site_url)
    return LoginPage(driver)


def test_login_success(driver):
    login_page = _navigate_to_login_page(driver)
    login_page.login(os.getenv("SITE_USERNAME"), os.getenv("SITE_PASSWORD"))

    assert login_page.is_login_successful(), "Login failed despite using valid credentials!"
    print("Login completed successfully")


def test_login_with_wrong_password(driver):
    login_page = _navigate_to_login_page(driver)
    login_page.login(os.getenv("SITE_USERNAME"), "wrongpassword999")

    assert not login_page.is_login_successful(), "Login succeeded even with an incorrect password!"
    print("Incorrect password validation is working correctly")


def test_login_with_empty_credentials(driver):
    login_page = _navigate_to_login_page(driver)
    login_page.login("", "")

    assert not login_page.is_login_successful(), "Login succeeded even with empty credentials!"
    print("Empty credentials validation is working correctly")