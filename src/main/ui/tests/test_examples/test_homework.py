import pytest
from playwright.sync_api import expect


def test_homework(page, tmp_path):
    page.goto('https://demoqa.com/automation-practice-form')
    first_name = page.locator("#firstName")
    first_name.fill('John')
    last_name = page.locator("#lastName")
    last_name.fill('Red')
    email = page.locator("#userEmail")
    email.fill('redjohn@test.com')
    gender = page.locator("#gender-radio-1")
    gender.click(force=True)
    mobile = page.locator("#userNumber")
    mobile.fill('1234567890')
    date_of_birth = page.locator("#dateOfBirthInput")
    date_of_birth.click()
    page.locator('.react-datepicker__month-select').select_option("2")
    page.locator(".react-datepicker__day.react-datepicker__day--024").click()
    expected_date_of_birth = "24 March,2026"
    subjects = page.locator("#subjectsInput")
    subjects.fill('Eng')
    page.get_by_role("option", name="English", exact=True).click()
    selected_subject = page.locator("#subjectsContainer .subjects-auto-complete__multi-value__label")
    hobbies_sport = page.get_by_label("Sports", exact=True)
    hobbies_sport.check(force=True)
    hobbies_music = page.get_by_label("Music", exact=True)
    hobbies_music.check(force=True)
    expected_hobbies = "Sports, Music"
    file_path = tmp_path / "demoqa_test_file.txt"
    file_path.write_text("Hello, this is a test file for DemoQA upload!")
    picture = page.locator("#uploadPicture")
    picture.set_input_files(str(file_path))
    current_address = page.locator("#currentAddress")
    current_address.fill('Moscow never sleep')
    state = page.locator("#state")
    state.click()
    page.get_by_role("option", name="Haryana", exact=True).click()
    city = page.locator("#city")
    city.click()
    page.get_by_role("option", name="Karnal", exact=True).click()
    state_value = state.locator("[class*='singleValue']").inner_text()
    city_value = city.locator("[class*='singleValue']").inner_text()
    submit = page.locator("#submit").click()
    modal = page.get_by_role("dialog")
    #assert (page.locator('#example-modal-sizes-title-lg')).inner_text() == "Thanks for submitting the form"
    student_name = (modal.get_by_role("row").filter(has_text="Student Name").get_by_role("cell").nth(1))
    assert (f"{first_name.input_value()} {last_name.input_value()}" == student_name.inner_text())
    student_email = (modal.get_by_role("row").filter(has_text="Student Email").get_by_role("cell").nth(1))
    assert email.input_value() == student_email.inner_text()
    student_gender = (modal.get_by_role("row").filter(has_text="Gender").get_by_role("cell").nth(1))
    assert gender.input_value() == student_gender.inner_text()
    student_mobile = (modal.get_by_role("row").filter(has_text="Mobile").get_by_role("cell").nth(1))
    assert mobile.input_value() == student_mobile.inner_text()
    student_date_of_birth = (modal.get_by_role("row").filter(has_text="Date of Birth").get_by_role("cell").nth(1))
    assert expected_date_of_birth == student_date_of_birth.inner_text()
    student_subjects = (modal.get_by_role("row").filter(has_text="Subjects").get_by_role("cell").nth(1))
    assert selected_subject.inner_text() == student_subjects.inner_text()
    student_hobbies = (modal.get_by_role("row").filter(has_text="Sports, Music").get_by_role("cell").nth(1))
    assert expected_hobbies == student_hobbies.inner_text()
    student_picture = (modal.get_by_role("row").filter(has_text="Picture").get_by_role("cell").nth(1))
    assert picture.input_value() == f'C:\\fakepath\\{student_picture.inner_text()}'
    student_address = (modal.get_by_role("row").filter(has_text="Address").get_by_role("cell").nth(1))
    assert current_address.input_value() == student_address.inner_text()
    student_state_and_city = (modal.get_by_role("row").filter(has_text="State and City").get_by_role("cell").nth(1))
    assert f'{state_value} {city_value}' == student_state_and_city.inner_text()


def test_automation_practice_form_stable_complete(page):
    page.goto("https://demoqa.com/automation-practice-form")

    # Заполняем имя и фамилию
    page.get_by_placeholder("First Name").fill("Andrew")
    page.get_by_placeholder("Last Name").fill("U")

    # Заполняем почту
    page.get_by_placeholder("name@example.com").fill("theBest@example.com")

    # Выставляем гендер
    page.locator("label[for='gender-radio-2']").click(force=True)

    # Заполняем номер телефона
    page.get_by_placeholder("Mobile Number").fill("888888889")

    # Проставляем дату
    date_input = page.locator("#dateOfBirthInput")
    date_input.click()
    page.locator(".react-datepicker__month-select").select_option("7")
    page.locator(".react-datepicker__year-select").select_option("2025")
    page.locator(".react-datepicker__day--008:not(.react-datepicker__day--outside-month)").click()
    assert "08 Aug 2025" in date_input.input_value()

    # Заполняем предмет
    subjects_input = page.locator("#subjectsInput")
    subjects_input.fill("Maths")

    # Выбираем хобби
    page.locator("label[for='hobbies-checkbox-1']").click(force=True)

    # Пишем адрес
    page.get_by_placeholder("Current Address").fill("123 Test Street")

    # Выбираем штат
    page.locator("#state").click()
    page.locator("div[id^='react-select-3-option']:has-text('NCR')").click()

    # Выбираем город
    page.locator("#city").click()
    page.locator("div[id^='react-select-4-option']:has-text('Delhi')").click()

    # Жмем на "Submit"
    page.locator("#submit").click(force=True)



