import time
from dotenv import load_dotenv

load_dotenv()


def test_update_teacher(teacher_page):
    """Adds a teacher, verifies the pre-filled data in the edit modal, updates the details, and verifies the update."""
    original_teacher = teacher_page.add_teacher()
    print("Teacher created successfully:", original_teacher)

    teacher_page.search_by_name(original_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    teacher_page.click_edit_button()

    modal_name = teacher_page.get_edit_modal_prefilled_name()
    assert modal_name == original_teacher["name"], (
        f"Pre-filled name mismatch! Expected: {original_teacher['name']}, Got: {modal_name}"
    )
    print(f" Pre-filled name matches: {modal_name}")

    updated_name = "Updated Teacher Name"
    updated_designation = "Associate Professor"

    teacher_page.clear_and_update_name(updated_name)
    teacher_page.clear_and_update_designation(updated_designation)
    teacher_page.click_update_button()

    # Updating the name in the cleanup tracking list
    teacher_page.created_teachers[-1]["name"] = updated_name

    teacher_page.search_by_name(updated_name)
    teacher_page.click_filter_button()
    time.sleep(1)

    assert teacher_page.is_teacher_in_table(updated_name), (
        f"Updated teacher '{updated_name}' was not found in the table!"
    )
    print(f" Teacher updated successfully: {updated_name}")


def test_update_teacher_with_empty_name(teacher_page):
    """Attempts to update a teacher with an empty name field and verifies validation behavior."""
    temp_teacher = teacher_page.add_teacher()
    print("Teacher created successfully:", temp_teacher)

    teacher_page.search_by_name(temp_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    teacher_page.click_edit_button()
    teacher_page.clear_and_update_name("")
    teacher_page.driver.find_element(*teacher_page.update_button).click()
    time.sleep(1)

    assert teacher_page.is_update_modal_still_open(), (
        "The edit modal closed, indicating submission with an empty name was allowed!"
    )
    print("Empty name validation is working correctly")