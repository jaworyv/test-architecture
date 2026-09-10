from playwright.sync_api import expect


def test_radio_button(browser, page):

    page.goto("https://demoqa.com/radio-button")

    yes_radio = page.locator("#yesRadio")
    impressive_radio = page.locator("#impressiveRadio")
    no_radio = page.locator("#noRadio")

    expect(yes_radio).to_be_visible()
    expect(impressive_radio).to_be_visible()
    expect(no_radio).to_be_visible()

    yes_radio.click()
    expect(yes_radio).to_be_checked()
    expect(page.locator(".text-success")).to_have_text("Yes")


    impressive_radio.click()
    expect(impressive_radio).to_be_checked()
    expect(page.locator(".text-success")).to_have_text("Impressive")

    expect(no_radio).to_be_disabled()
