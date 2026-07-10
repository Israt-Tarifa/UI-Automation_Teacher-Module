import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time
from pages.login_page import LoginPage
from pages.teacher_page import TeacherPage

load_dotenv()


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service)
    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


@pytest.fixture
def teacher_page(driver):
    base_url = os.getenv("BASE_URL")
    username = os.getenv("SITE_USERNAME")
    password = os.getenv("SITE_PASSWORD")

    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login(username, password)
    time.sleep(2)

    page = TeacherPage(driver)
    page.go_to_teacher_page()

    created_teachers = []
    page.created_teachers = created_teachers

    original_add_teacher = page.add_teacher

    def tracked_add_teacher():
        teacher = original_add_teacher()
        created_teachers.append(teacher)
        return teacher

    page.add_teacher = tracked_add_teacher

    yield page

    # Teardown — test pass ba fail jaiho cleanup cholbe
    for teacher in created_teachers:
        try:
            page.search_by_name(teacher["name"])
            page.click_filter_button()
            time.sleep(1)
            if page.is_teacher_in_table(teacher["name"]):
                page.click_delete_button()
                page.confirm_delete()
                print(f"Cleaned up teacher: {teacher['name']}")
        except Exception as e:
            print(f"Cleanup failed for teacher {teacher['name']}: {e}")