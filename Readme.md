# Teacher Module — UI Automation Framework

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-1E90FF?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Automation](https://img.shields.io/badge/Selenium-Web%20Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Reporting](https://img.shields.io/badge/Allure-Report-E40046?style=for-the-badge&logo=testinglibrary&logoColor=white)](https://docs.qameta.io/allure/)
[![Automation Level](https://img.shields.io/badge/Test%20Automation-Advanced-2ECC71?style=for-the-badge)]()

## About This Project

This repository contains an end-to-end UI automation suite built around the Teacher Module of an SMS Panel web application. Selenium WebDriver drives the browser interactions while Pytest orchestrates test execution.

The suite exercises the complete lifecycle of a teacher record — creation, retrieval, modification, and removal — alongside dedicated coverage for search/filter behavior, pagination, and a hybrid API-to-UI verification flow. The codebase follows the Page Object Model (POM) pattern to keep locators and actions decoupled from test logic, and supports two reporting formats: pytest-html and Allure.

---

## Tech Stack

- Python
- Pytest
- Selenium WebDriver
- WebDriver Manager
- Requests
- python-dotenv
- Faker
- pytest-html
- Allure
- GitHub

---

## 📂 Repository Layout

```text
WebAutomationAssignment/
│
├── pages/                        # Page Object Model layer
│   ├── login_page.py             # Login page locators & actions
│   └── teacher_page.py           # Teacher page locators & actions
│
├── testcases/                    # Test scripts
│   ├── test_teacher_login.py
│   ├── test_teacher_filter.py
│   ├── test_create_teacher.py
│   ├── test_update_teacher.py
│   ├── test_delete_teacher.py
│   └── test_api_ui_teacher.py
│
├── .env                          # Sensitive credentials (not committed)
├── .gitignore                    # Ignored files list
├── conftest.py                   # Fixtures & global setup
├── requirements.txt              # Project dependencies
└── README.md


## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/aburayhan01/Web_automation_student_api.git
cd Web_automation_student_api
```

### 2. Create and Activate Virtual Environment

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment File

Create a `.env` file in the project root:
```
# UI
BASE_URL=https://qa-sms-panel.netlify.app/signin
SITE_USERNAME=your_username
SITE_PASSWORD=your_password

# API
API_BASE_URL=http://your-api-url
API_USERNAME=your_api_username
API_PASSWORD=your_api_password
```
> Note: Never commit `.env` to GitHub. It is listed in `.gitignore`.

### 5. Run All Tests

```bash
pytest testcases/ -v -s
```

### 6. Run a Specific Test File

```bash
pytest testcases/test_create_teacher.py -v -s
```

### 7. Run a Specific Test Function

```bash
pytest testcases/test_delete_teacher.py::test_delete_teacher -v -s
```

---

## Generate & View HTML Report

```bash
pytest testcases/ -v -s --html=reports/report.html --self-contained-html
```

To view on Windows:
```bash
start reports/report.html
```
To view on macOS:
```bash
open reports/report.html
```

![img.png](img.png)

---

## Generate & View Allure Report

### Generate Allure Results:
```bash
pytest testcases/ -v -s --alluredir=reports/allure-results
```

### View Allure Report:
```bash
allure serve reports/allure-results
```

## Allure Test Report Dashboard

### 📌 Executive Overview (Allure Summary)

![img_1.png](img_1.png)

---

### Test Execution Trends & Graphical Analysis

![img_2.png](img_2.png)

---

### Test behaviour Analysis

![img_3.png](img_3.png)

---

## Test Cases

### Login
- Login with valid credentials → SMS Panel visible
- Login with wrong password → Login fails
- Login with empty credentials → Login fails

### Filter & Search
- Filter teachers by department → All rows match selected department across all pages
- Search teacher by name → Matching results returned
- Pagination → All pages navigated successfully
- Page size → Correct number of records displayed for each page size

### Create Teacher
- Add teacher with valid dynamic data → Teacher added & info verified via View modal
- Create with empty form → Form does not submit
- Create with invalid email → Form does not submit
- Create with duplicate email → Form does not submit

### Update Teacher
- Update teacher name & designation → Updated data visible in table
- Update with empty name → Form does not submit

### Delete Teacher
- Delete teacher → Teacher removed from table
- Delete teacher and verify gone → Confirmed before & after deletion

### API + UI Integration
- Create teacher via API → Verify teacher appears in UI with correct data

---

## Test Coverage Summary

| File | Tests | Result |
|------|-------|--------|
| test_teacher_login.py | 3 | ✅ Passed |
| test_teacher_filter.py | 4 | ✅ Passed |
| test_create_teacher.py | 4 | ✅ Passed |
| test_update_teacher.py | 2 | ✅ Passed |
| test_delete_teacher.py | 2 | ✅ Passed |
| test_api_ui_teacher.py | 1 | ✅ Passed |

**Total: 16 test cases — All Passed ✅**

---

## Author 
Israt Jahan Tarifa
