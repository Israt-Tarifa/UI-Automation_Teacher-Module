import time
from dotenv import load_dotenv

load_dotenv()

def test_view_added_teacher_information(teacher_page):
    "Adding a teacher, then verifying the data from the view modal."
    new_teacher = teacher_page.add_teacher()
    print("Teacher Added:", new_teacher)

    teacher_page.search_by_name(new_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    fetched_data = teacher_page.click_view_button_and_get_data()
    print("Teacher Fetched from View Modal:", fetched_data)

    assert fetched_data["name"] == new_teacher["name"]
    assert fetched_data["email"] == new_teacher["email"]
    assert fetched_data["department"] == new_teacher["department"]
    assert fetched_data["teacher_id"] == new_teacher["teacher_id"]
    assert fetched_data["designation"] == new_teacher["designation"]

    print(" Added teacher info successfully matched with view modal")


def test_create_teacher_with_empty_form(teacher_page):
    "Verifying if validation errors are displayed when submitting a blank form."
    teacher_page.open_add_teacher_modal()
    teacher_page.click_create_button()

    assert teacher_page.is_modal_still_open(), "The blank form should not be submitted!"
    print("Empty form validation is working correctly")


def test_create_teacher_with_invalid_email(teacher_page):
    "Attempting to create a teacher with an invalid email format."
    teacher_page.open_add_teacher_modal()
    teacher_page.fill_teacher_form(
        name="Test Teacher",
        email="invalidemail123",
        select_department=True,
        teacher_id="12345",
        designation="Professor"
    )
    teacher_page.click_create_button()

    assert teacher_page.is_modal_still_open(), "Invalid email format should not be accepted!"
    print("Invalid email validation is working correctly")


def test_create_teacher_with_duplicate_email(teacher_page):
    "Attempting to create a new teacher using an existing teacher's email."
    existing_teacher = teacher_page.add_teacher()
    print("Existing teacher created:", existing_teacher)
    time.sleep(1)

    teacher_page.open_add_teacher_modal()
    teacher_page.fill_teacher_form(
        name="Duplicate Teacher",
        email=existing_teacher["email"],
        select_department=True,
        teacher_id="99999",
        designation="Lecturer"
    )
    teacher_page.click_create_button()

    assert teacher_page.is_modal_still_open(), "Duplicate email should not be accepted!"
    print("Duplicate email validation is working correctly")