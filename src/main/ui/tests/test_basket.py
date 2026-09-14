
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_add_item_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Backpack')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Backpack')

def test_add_items_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')
    catalog.add_to_cart('Sauce Labs Bolt T-Shirt')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.expect_item_in_cart('Sauce Labs Bolt T-Shirt')

def test_remove_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Fleece Jacket')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Fleece Jacket')
    basket.remove_item('Sauce Labs Fleece Jacket')
    basket.expect_item_not_in_cart('Sauce Labs Fleece Jacket')

def test_remove_items_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart('Sauce Labs Backpack')
    catalog.add_to_cart('Test.allTheThings() T-Shirt (Red)')

    basket.open_cart()
    basket.expect_item_in_cart('Sauce Labs Backpack')
    basket.expect_item_in_cart('Test.allTheThings() T-Shirt (Red)')

    basket.remove_item('Sauce Labs Backpack')
    basket.remove_item('Test.allTheThings() T-Shirt (Red)')
    basket.expect_item_not_in_cart('Sauce Labs Backpack')
    basket.expect_item_not_in_cart('Test.allTheThings() T-Shirt (Red)')
