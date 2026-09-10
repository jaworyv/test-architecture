from playwright.sync_api import expect

from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage


def test_add_item_and_check_in_cart(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    catalog = CatalogPage(page)
    catalog.add_to_cart('Sauce Labs Backpack')
    basket = BasketPage(page)
    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Backpack')

def test_add_items_and_check_in_cart(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    catalog = CatalogPage(page)
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')
    basket = BasketPage(page)
    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')

def test_remove_item_from_cart(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    catalog = CatalogPage(page)
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    basket = BasketPage(page)
    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.remove_item('Sauce Labs Fleece Jacket')
    basket.expect_item_not_in_cart('Sauce Labs Fleece Jacket')

def test_remove_items_from_cart(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    catalog = CatalogPage(page)
    catalog.add_to_cart('Sauce Labs Backpack')
    catalog.add_to_cart('Test.allTheThings() T-Shirt (Red)')
    basket = BasketPage(page)
    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Backpack')
    basket.expect_item_in_cart('Test.allTheThings() T-Shirt (Red)')
    basket.remove_item('Sauce Labs Backpack')
    basket.remove_item('Test.allTheThings() T-Shirt (Red)')
    basket.expect_item_not_in_cart('Sauce Labs Backpack')
    basket.expect_item_not_in_cart('Test.allTheThings() T-Shirt (Red)')
