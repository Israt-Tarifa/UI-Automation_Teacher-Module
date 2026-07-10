import random
import time
from dotenv import load_dotenv

load_dotenv()


def test_department_filter(teacher_page):
    teacher_page.select_page_size("100")
    time.sleep(2)

    target_dept = teacher_page.select_random_department_from_filter()
    print(f"Filtered data {target_dept}")

    teacher_page.click_filter_button()
    time.sleep(2)

    page_no = 1
    while True:
        records = teacher_page.get_table_data_as_a_dictionary()

        for record in records:
            dept_found = record["department"]
            print(f"[Page {page_no}] Search: {target_dept} | Found: {dept_found}")
            assert dept_found == target_dept, (
                f"Page {page_no}-e department mismatch! "
                f"Search  {target_dept} but found {dept_found}"
            )

        pagination_status = teacher_page.click_next_page()
        if pagination_status == "disabled":
            print(f"Reached the last page. Total {page_no} pages checked.")
            break
        page_no += 1


def test_search_by_name_filter(teacher_page):
    time.sleep(2)
    everyone = teacher_page.get_table_data_as_a_dictionary()
    picked_one = random.choice(everyone)
    name_to_search = picked_one["name"]

    print(f"🔍 Searching with this name: {name_to_search}")
    teacher_page.search_by_name(name_to_search)
    teacher_page.click_filter_button()
    time.sleep(2)

    search_results = teacher_page.get_table_data_as_a_dictionary()
    for res in search_results:
        assert name_to_search.lower() in res["name"].lower(), (
            f"Search kora '{name_to_search}' result-er '{res['name']}'-e nai"
        )
    print(" Name search filter is working correctly")


def test_pagination(teacher_page):
    existing_clear_btn = teacher_page.driver.find_elements(
        "xpath", "//button[text()='Clear']"
    )
    if existing_clear_btn:
        existing_clear_btn[0].click()
        time.sleep(1)

    pages_seen = 0
    while True:
        page_content = teacher_page.get_table_data_as_a_dictionary()
        assert len(page_content) > 0, f"No records found on page {pages_seen + 1}!"
        pages_seen += 1
        print(f"Page {pages_seen} has {len(page_content)} records")

        move_next = teacher_page.click_next_page()
        if move_next == "disabled":
            print(f"🏁 Pagination complete. Total {pages_seen} pages found.")
            break

    assert pages_seen >= 1, "No pages were found!"
    print(" Pagination is working correctly")

def test_page_size(teacher_page):
    sizes_to_check = ["10", "20", "50"]

    for each_size in sizes_to_check:
        teacher_page.select_page_size(each_size)
        time.sleep(2)

        current_rows = teacher_page.get_table_data_as_a_dictionary()
        print(f"Selecting size {each_size} displays {len(current_rows)} rows")

        assert len(current_rows) <= int(each_size), (
            f"Size {each_size} was selected, but {len(current_rows)} rows are being displayed!"
        )

    print(" Page size feature is working correctly")