from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps


def test_checkout_multiple_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog .login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')
    basket_total = basket.get_items_total_price()
    basket.checkout_button()

    checkout.start_checkout("John", "Red", "125505")
    checkout_price_without_tax = checkout.get_item_total_after_continue()
    checkout_tax = checkout.get_tax_total()
    checkout_total = checkout.get_total()

    assert basket_total == checkout_price_without_tax
    assert checkout_price_without_tax + checkout_tax == checkout_total
    checkout.finish_checkout()
    assert checkout.get_success_text() == 'Thank you for your order!'

def test_checkout_without_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog .login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')
    basket.checkout_button()

    checkout.start_checkout("John", "Red", "")
    assert checkout.get_error_text() == 'Error: Postal Code is required'
