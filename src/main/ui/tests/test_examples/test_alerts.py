url = "https://demoqa.com/alerts"

def test_simple_alert(page):
        page.goto(url)
        # Подписываемся на простой alert
        def handle_alert(dialog):
            assert dialog.message == "You clicked a button"
            dialog.accept()

        page.once("dialog", handle_alert)
        page.locator("#alertButton").click()

def test_alert_after_5_sec(page):
    page.goto(url)

    def handle_alert(dialog):
        assert dialog.message == "This alert appeared after 5 seconds"
        dialog.accept()

    page.once("dialog", handle_alert)
    page.locator("#timerAlertButton").click()
    page.wait_for_event("dialog", timeout=6000)
    
def test_confirm_box_alert(page):
    page.goto(url)

    def handle_alert(dialog):
        assert dialog.message == "Do you confirm action?"
        dialog.accept()

    page.once("dialog", handle_alert)
    page.locator("#confirmButton").click()
    assert 'Ok' in page.locator('#confirmResult').inner_text()

def test_promt_alert(page):
    page.goto(url)

    def handle_alert(dialog):
        assert dialog.message == "Please enter your name"
        dialog.accept('ИГОРЬ')

    page.once("dialog", handle_alert)
    page.locator("#promtButton").click()
    assert 'ИГОРЬ' in page.locator('#promptResult').inner_text()

