import time
import random
import requests
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

faker_instance = Faker()

def fetch_auth_token():
    resp = requests.post(
        url=f"{BASE_URL}/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    return resp.json().get("authToken")


def build_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def generate_teacher_payload():
    name = "API Test " + faker_instance.name()
    email = faker_instance.email()
    tid = random.randint(10000, 99999)
    dept = random.choice(["CSE", "BBA", "MBA", "LAW", "ENGLISH"])
    role = random.choice(["Professor", "Assistant Professor", "Lecturer"])

    return {
        "name": name,
        "email": email,
        "department": dept,
        "teacherId": tid,
        "designation": role
    }


def test_api_create_teacher_verify_in_ui(teacher_page):
    # ---- Step 1: Authenticate via API ----
    auth_token = fetch_auth_token()
    assert auth_token, "Auth token can not retrieved !"
    request_headers = build_auth_headers(auth_token)

    # ---- Step 2: Create a new teacher through API ----
    new_teacher = generate_teacher_payload()

    create_resp = requests.post(
        url=f"{BASE_URL}/api/teacher",
        json=new_teacher,
        headers=request_headers
    )
    assert create_resp.status_code in (200, 201), (
        f"Teacher creation ব্যর্থ হয়েছে! Status: {create_resp.status_code}, "
        f"Response: {create_resp.text}"
    )
    print(f"Teacher successfully created via API: {new_teacher['name']}")


    teacher_page.created_teachers.append({
        "name": new_teacher["name"],
        "api_teacher_id": new_teacher["teacherId"]
    })


    time.sleep(2)
    teacher_page.search_by_name(new_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(2)

    assert teacher_page.is_teacher_in_table(new_teacher["name"]), (
        f"The teacher named '{new_teacher['name']}' was not found in the UI!"
    )
    print(f"Teacher is confirmed using UI {new_teacher['name']}")


    modal_data = teacher_page.click_view_button_and_get_data()

    assert modal_data["name"] == new_teacher["name"]
    assert modal_data["email"] == new_teacher["email"]
    assert modal_data["department"] == new_teacher["department"]
    assert modal_data["teacher_id"] == str(new_teacher["teacherId"])
    assert modal_data["designation"] == new_teacher["designation"]

    print("API data & UI data are matched!")