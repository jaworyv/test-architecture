from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage


def test_auth_standart_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert page.url == "https://www.saucedemo.com/inventory.html", "Ожидаем редирект на страницу каталога"

def test_auth_locked_out_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user", "secret_sauce")
    assert page.url == LoginPage.URL, "Ожидаем остаться на странице логина"
    error_text = login_page.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout_standart_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    catalog = CatalogPage(page)
    assert catalog.get_products_count() > 0
    catalog.logout()
    expect(page).to_have_url(LoginPage.URL)

def test_logout_visual_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user", "secret_sauce")
    catalog = CatalogPage(page)
    assert catalog.get_products_count() > 0
    catalog.logout()
    expect(page).to_have_url(LoginPage.URL)