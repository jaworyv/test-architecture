from playwright.sync_api import expect


def test_dynamic_element(page):
    page.goto("https://demoqa.com/dynamic-properties")

    # --- Кнопка, которая появляется через 5 секунд ---
    dynamic_btn = page.locator("#visibleAfter")

    # Ждём, пока кнопка станет видимой
    expect(dynamic_btn).to_be_visible(timeout=6000)  # таймаут чуть больше 5 секунд

    # Кликаем после того, как она появилась
    dynamic_btn.click()

    # --- Кнопка, которая активна через 5 секунд ---
    enable_btn = page.locator("#enableAfter")
    expect(enable_btn).to_be_enabled(timeout=6000)
    enable_btn.click()