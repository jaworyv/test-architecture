from src.main.ui.utils.constants import Urls
from src.main.ui.pages.login_page import LoginPage
from ui.pages.catalog_page import CatalogPage
from ui.steps.catalog_steps import CatalogSteps
from ui.steps.login_steps import LoginSteps


def test_auth_standart_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    assert page.url == CatalogPage.CATALOG, "Ожидаем редирект на страницу каталога"

def test_auth_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")
    assert page.url == LoginPage.BASE, "Ожидаем остаться на странице логина"
    assert "locked out" in steps.get_error_text(), "Ожидаем сообщение о заблокированном пользователе"


def test_logout_standart_user(page):
    steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)

    steps.open_login_page().login("locked_out_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0

    catalog_steps.logout()
    assert page.url == LoginPage.BASE, "Ожидаем возврат на страницу логина"

def test_logout_visual_user(page):
    steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)

    steps.open_login_page().login("visual_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0

    catalog_steps.logout()
    assert page.url == LoginPage.BASE, "Ожидаем возврат на страницу логина"