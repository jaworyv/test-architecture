from playwright.sync_api import expect

def test_click(page):
    page.goto('https://demoqa.com/buttons')

    dbl_click = page.locator("#doubleClickBtn")
    right_click = page.locator("#rightClickBtn")
    one_click = page.get_by_text("Click Me", exact=True)  # используем exact, чтобы найти точное совпадение по тексту

    dbl_click.dblclick()  # осуществляем двойной клик
    right_click.click(button="right")  # осуществляем правый клик
    one_click.click()  # осуществляем обычный клик

    expect(page.locator("#doubleClickMessage")).to_have_text("You have done a double click")
    expect(page.locator("#rightClickMessage")).to_have_text("You have done a right click")
    expect(page.locator("#dynamicClickMessage")).to_have_text("You have done a dynamic click")