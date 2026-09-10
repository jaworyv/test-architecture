from playwright.sync_api import expect

from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage
from src.main.ui.pages.login_page import LoginPage


def test_checkout_multiple_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)

    catalog .login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')
    basket_total = basket.get_items_total_price()
    basket.checkout()

    checkout.start_checkout("John", "Red", "125505")
    checkout_price_without_tax = checkout.get_item_total_after_continue()
    checkout_tax = checkout.get_tax_total()
    checkout_total = checkout.get_total()

    assert basket_total == checkout_price_without_tax
    assert checkout_price_without_tax + checkout_tax == checkout_total
    checkout.finish_checkout()
    assert checkout.get_success_text() == 'Thank you for your order!'

def test_checkout_without_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)

    catalog .login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')
    basket.checkout()

    checkout.start_checkout("John", "Red", "")
    assert checkout.get_error_text() == 'Error: Postal Code is required'
