def test_date_picker_select_option(page):
    page.goto("https://demoqa.com/date-picker")

    # Локатор поля даты
    date_input = page.locator("#datePickerMonthYearInput")
    date_input.click()  # открываем календарь

    # Выбираем месяц и год через select_option
    page.locator(".react-datepicker__month-select").select_option("7")  # август (0-based)
    page.locator(".react-datepicker__year-select").select_option("2025")  # год

    # Выбираем день (например, 25-е число)
    page.locator(".react-datepicker__day--025").click()

    # Проверяем, что значение инпута изменилось
    assert date_input.input_value() == "08/25/2025"

def test_date_and_time_picker_select_option(page):
    page.goto("https://demoqa.com/date-picker")
    data_input = page.locator('#dateAndTimePickerInput')
    data_input.click()

    month_input = page.locator(".react-datepicker__month-read-view")
    month_input.click()
    month = page.get_by_role('button', name='March')
    month.click()

    year_input = page.locator(".react-datepicker__year-read-view")
    year_input.click()
    year = page.get_by_role('button', name='2024')
    year.click()

    day_input = page.locator(".react-datepicker__day.react-datepicker__day--024.react-datepicker__day--weekend")
    day_input.click()

    time_input = page.get_by_role('option', name='20:00')
    time_input.click()

    assert data_input.input_value() == "March 24, 2024 8:00 PM"




