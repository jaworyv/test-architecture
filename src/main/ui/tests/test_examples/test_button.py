from playwright.sync_api import sync_playwright

def test_text_box():
   with sync_playwright() as p:
      browser = p.chromium.launch(headless=False) # headless=False, чтобы видеть браузер
      page = browser.new_page() # создаём новую вкладку
      page.goto("https://demoqa.com/text-box")
      page.get_by_placeholder('Full Name').fill("Test Testovyi")
      page.get_by_placeholder('name@example.com').fill("qatest@example.com")
      page.locator('#currentAddress').fill("Москва, ул. Радожская, 1")
      page.locator('#permanentAddress').fill("Москва, ул. 64 Армии, 6")
      page.get_by_role("button", name='Submit').click()
      browser.close()