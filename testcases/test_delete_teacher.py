import time
from dotenv import load_dotenv

load_dotenv()


def test_delete_teacher(teacher_page):
    added_teacher = teacher_page.add_teacher()
    print("Added teacher:", added_teacher)

    teacher_page.search_by_name(added_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    teacher_page.click_delete_button()
    teacher_page.confirm_delete()


    teacher_page.created_teachers.clear()

    teacher_page.search_by_name(added_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    assert not teacher_page.is_teacher_in_table(added_teacher["name"]), (
        f"Teacher '{added_teacher['name']}' should have been deleted!"
    )
    print(f"Teacher deleted successfully: {added_teacher['name']}")


def test_delete_teacher_and_verify_gone(teacher_page):
    added_teacher = teacher_page.add_teacher()
    print("Added teacher:", added_teacher)

    teacher_page.search_by_name(added_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    assert teacher_page.is_teacher_in_table(added_teacher["name"]), (
        f"Teacher '{added_teacher['name']}' should exist before delete!"
    )
    print("Teacher exists before delete — confirmed")

    teacher_page.click_delete_button()
    teacher_page.confirm_delete()

    teacher_page.created_teachers.clear()

    teacher_page.search_by_name(added_teacher["name"])
    teacher_page.click_filter_button()
    time.sleep(1)

    assert not teacher_page.is_teacher_in_table(added_teacher["name"]), (
        f"Teacher '{added_teacher['name']}' should not exist after delete!"
    )
    print("Teacher does not exist after delete — confirmed")