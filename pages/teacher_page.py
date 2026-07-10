import random
import time
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class TeacherPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    # -------------------------Sidebar-------------------------
    teachers_link = (By.XPATH, "//a[@href='/dashboard/teachers']")

    # -------------------------Page size dropdown-------------------------
    page_size_dropdown = (By.XPATH, "//select")

    # -------------------------Department filter-------------------------
    department_dropdown_filter = (By.XPATH, "//button[@role='combobox']")
    dropdown_options = (By.XPATH, "//div[@role='option']")

    # -------------------------Filter button-------------------------
    filter_button = (By.XPATH, "//button[text()='Filter']")

    # -------------------------Table-------------------------
    table_data = (By.XPATH, "//tbody/tr")

    #------------------------- Pagination-------------------------
    next_button = (By.XPATH, "//button[text()='Next']")

    # -------------------------Search by name-------------------------
    search_name = (By.XPATH, "//input[@placeholder='Filter by name...']")

    # -------------------------Add Teacher modal-------------------------
    add_teacher_button = (By.XPATH, "//button[contains(text(), 'Add Teacher')]")
    name_input = (By.ID, "name")
    email_input = (By.ID, "email")
    department_dropdown_form = (By.XPATH, "//button[span[text()='Select department']]")
    teacher_id_input = (By.ID, "teacherId")
    designation_input = (By.ID, "designation")
    create_button = (By.XPATH, "//button[text()='Create']")
    cancel_button = (By.XPATH, "//button[text()='Cancel']")

    # -------------------------Action buttons-------------------------
    view_button = (By.XPATH, "//button[.//*[contains(@class,'lucide-eye')]]")
    edit_button = (By.XPATH, "//button[.//*[contains(@class,'lucide-pencil')]]")
    delete_button = (By.XPATH, "//button[.//*[contains(@class,'lucide-trash2')]]")

    # Edit modal
    edit_name_input = (By.ID, "name")
    edit_designation_input = (By.ID, "designation")
    update_button = (By.XPATH, "//button[text()='Update']")

    # -------------------------Delete modal-------------------------
    confirm_delete_button = (By.XPATH, "//button[text()='Delete']")

    # -------------------------Navigation-------------------------

    def go_to_teacher_page(self):
        link = self.wait.until(EC.element_to_be_clickable(self.teachers_link))
        link.click()
        self.wait.until(EC.visibility_of_element_located(self.add_teacher_button))

    # ------------------------Page Size-------------------------

    def select_page_size(self, page_size):
        dropdown = self.wait.until(
            lambda d: d.find_element(*self.page_size_dropdown)
        )
        select = Select(dropdown)
        select.select_by_visible_text(str(page_size))
        print(f"Selected page size: {page_size}")
        time.sleep(2)

    # -------------------------Table -------------------------

    def get_table_data_as_a_dictionary(self):
        table_data = []
        rows = self.driver.find_elements(*self.table_data)
        for row in rows:
            columns = row.find_elements(By.XPATH, "./td")
            if len(columns) >= 5:
                row_data = {
                    "name": columns[0].text,
                    "email": columns[1].text,
                    "department": columns[2].text,
                    "teacher_id": columns[3].text,
                    "designation": columns[4].text
                }
                table_data.append(row_data)
        return table_data

    # ------------------------- Pagination-------------------------

    def click_next_page(self):
        next_btn = self.driver.find_element(*self.next_button)
        is_disabled = next_btn.get_attribute("disabled")
        if is_disabled:
            print("Next button is disabled")
            return "disabled"
        next_btn.click()
        print("Clicked Next button")
        time.sleep(1)
        return "clicked"

    # -------------------------Filter-------------------------

    def select_random_department_from_filter(self):
        self.driver.find_element(*self.department_dropdown_filter).click()
        time.sleep(1)
        departments = self.driver.find_elements(*self.dropdown_options)
        random_department = random.choice(departments)
        selected_department = random_department.text
        random_department.click()
        time.sleep(2)
        return selected_department

    def click_filter_button(self):
        filter_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.filter_button)
        )
        self.driver.execute_script("arguments[0].click();", filter_btn)

    def search_by_name(self, name):
        input_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.search_name)
        )
        ActionChains(self.driver).move_to_element(input_box).click().perform()
        time.sleep(0.3)
        input_box.clear()
        input_box.send_keys(name)
        time.sleep(1)

        actual_value = input_box.get_attribute("value")
        print(f"Typed name  : {name}")
        print(f"Input value : {actual_value}")

    # -------------------------Add Teacher------------------------

    def open_add_teacher_modal(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.add_teacher_button))
        btn.click()
        self.wait.until(EC.visibility_of_element_located(self.create_button))

    def fill_teacher_form(self, name="", email="", select_department=False, teacher_id="", designation=""):
        if name:
            name_field = self.wait.until(EC.visibility_of_element_located(self.name_input))
            name_field.send_keys(name)

        if email:
            self.driver.find_element(*self.email_input).send_keys(email)

        if select_department:
            self.driver.find_element(*self.department_dropdown_form).click()
            departments = self.wait.until(
                lambda d: d.find_elements("xpath", "//div[@role='option']")
            )
            departments[0].click()

        if teacher_id:
            self.driver.find_element(*self.teacher_id_input).send_keys(str(teacher_id))

        if designation:
            self.driver.find_element(*self.designation_input).send_keys(designation)

    def click_create_button(self):
        self.driver.find_element(*self.create_button).click()
        time.sleep(1)

    def is_modal_still_open(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.create_button)
            )
            return True
        except TimeoutException:
            return False

    def add_teacher(self):
        fake = Faker()

        teacher_name = fake.name()
        teacher_email = fake.email()
        teacher_id = fake.random_number(digits=5)
        designation = random.choice(["Professor", "Assistant Professor", "Lecturer"])

        self.open_add_teacher_modal()

        name_field = self.wait.until(EC.visibility_of_element_located(self.name_input))
        name_field.send_keys(teacher_name)

        self.driver.find_element(*self.email_input).send_keys(teacher_email)

        self.driver.find_element(*self.department_dropdown_form).click()
        departments = self.wait.until(
            lambda d: d.find_elements("xpath", "//div[@role='option']")
        )
        random_department = random.choice(departments)
        department_name = random_department.text
        random_department.click()

        self.driver.find_element(*self.teacher_id_input).send_keys(str(teacher_id))
        self.driver.find_element(*self.designation_input).send_keys(designation)

        self.driver.find_element(*self.create_button).click()

        self.wait.until(EC.visibility_of_element_located(self.add_teacher_button))

        return {
            "name": teacher_name,
            "email": teacher_email,
            "department": department_name,
            "teacher_id": str(teacher_id),
            "designation": designation
        }

    # -------------------------View Teacher-------------------------

    def click_view_button_and_get_data(self):
        view_btn = self.wait.until(EC.element_to_be_clickable(self.view_button))
        view_btn.click()

        name = self.wait.until(
            lambda d: d.find_element("xpath", "//span[text()='Name']/following-sibling::span")
        ).text
        email = self.driver.find_element(
            "xpath", "//span[text()='Email']/following-sibling::span"
        ).text
        department = self.driver.find_element(
            "xpath", "//span[text()='Department']/following-sibling::span"
        ).text
        teacher_id = self.driver.find_element(
            "xpath", "//span[text()='Teacher ID']/following-sibling::span"
        ).text
        designation = self.driver.find_element(
            "xpath", "//span[text()='Designation']/following-sibling::span"
        ).text

        time.sleep(2)

        teacher_data = {
            "name": name,
            "email": email,
            "department": department,
            "teacher_id": teacher_id,
            "designation": designation
        }
        print(teacher_data)
        return teacher_data

    # -------------------------Edit Teacher------------------------

    def click_edit_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.edit_button))
        btn.click()
        self.wait.until(EC.visibility_of_element_located(self.update_button))

    def get_edit_modal_prefilled_name(self):
        name_field = self.wait.until(EC.visibility_of_element_located(self.edit_name_input))
        return name_field.get_attribute("value")

    def clear_and_update_name(self, new_name):
        name_field = self.wait.until(EC.visibility_of_element_located(self.edit_name_input))
        name_field.clear()
        name_field.send_keys(new_name)

    def clear_and_update_designation(self, new_designation):
        designation_field = self.driver.find_element(*self.edit_designation_input)
        designation_field.clear()
        designation_field.send_keys(new_designation)

    def click_update_button(self):
        self.driver.find_element(*self.update_button).click()
        self.wait.until(EC.visibility_of_element_located(self.add_teacher_button))
        time.sleep(1)

    def is_update_modal_still_open(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.update_button)
            )
            return True
        except TimeoutException:
            return False

    # -------------------------Delete Teacher-------------------------

    def click_delete_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.delete_button))
        btn.click()
        self.wait.until(EC.visibility_of_element_located(self.confirm_delete_button))

    def confirm_delete(self):
        self.driver.find_element(*self.confirm_delete_button).click()
        self.wait.until(EC.visibility_of_element_located(self.add_teacher_button))
        time.sleep(1)

    def cancel_delete(self):
        self.driver.find_element(*self.cancel_button).click()
        time.sleep(1)

    def is_teacher_in_table(self, name):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//tbody/tr/td[text()='{name}']")
                )
            )
            return True
        except TimeoutException:
            return False