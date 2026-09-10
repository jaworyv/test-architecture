from playwright.sync_api import sync_playwright

def test_checkbox_mine():
   with sync_playwright() as p:
      browser = p.chromium.launch(headless=False) # headless=False, чтобы видеть браузер
      page = browser.new_page() # создаём новую вкладку
      page.goto("https://demoqa.com/checkbox")
      page.locator('.rc-tree-switcher.rc-tree-switcher_close').click()
      page.locator('.rc-tree-treenode:has([title="Desktop"]) > .rc-tree-switcher').click()
      page.locator('.rc-tree-treenode:has([title="Documents"]) > .rc-tree-switcher').click()
      page.locator('.rc-tree-treenode:has([title="Downloads"]) > .rc-tree-switcher').click()
      page.get_by_label('Select Notes').check()
      page.get_by_label('Select Commands').check()
      page.get_by_label('Select WorkSpace').check()
      page.get_by_label('Select Office').check()
      page.get_by_label('Select Word File.doc').check()
      page.get_by_label('Select Excel File.doc').check()
      assert page.locator("#result").inner_text() == 'You have selected :\nnotes\ncommands\ndesktop\nworkspace\nreact\nangular\nveu\noffice\npublic\nprivate\nclassified\ngeneral\ndocuments\nwordFile\nexcelFile\ndownloads\nhome'
      browser.close()

def test_checkbox_answer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        page.goto("https://demoqa.com/checkbox")

        for i in range(5):
            closed = page.locator(".rc-tree-switcher.rc-tree-switcher_close")
            if closed.count() > 0:
                closed.first.click()
                page.wait_for_timeout(300)
            else:
                break

        page.locator("span[aria-label='Select Desktop']").click()
        page.locator("span[aria-label='Select Documents']").click()
        page.locator("span[aria-label='Select Downloads']").click()

        result = page.locator("#result").inner_text()

        assert "home" in result

        browser.close()