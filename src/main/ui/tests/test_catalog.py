from playwright.sync_api import expect

from src.main.ui.pages.catalog_page import CatalogPage


def test_count_catalog(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    assert catalog.get_products_count() == 6

def test_sorted_by_name(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    catalog.sort_items('az')
    assert catalog.get_product_names() == sorted(catalog.get_product_names()), "Товары не отсортированы по имени A-Z"
    catalog.sort_items('za')
    assert catalog.get_product_names() == sorted(catalog.get_product_names(), reverse=True), "Товары не отсортированы по имени Z-A"

def test_sorted_by_price(page):
    catalog_page = CatalogPage(page)
    catalog_page.login('standard_user', 'secret_sauce')
    catalog_page.sort_items('lohi')
    assert catalog_page.get_product_prices() == sorted(catalog_page.get_product_prices()), "Товары не отсортированы по возрастанию цены"
    catalog_page.sort_items('hilo')
    assert catalog_page.get_product_prices() == sorted(catalog_page.get_product_prices(), reverse=True), "Товары не отсортированы по убыванию цены"


def test_add_to_cart(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    button = catalog.add_to_cart('Sauce Labs Bike Light')
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1

def test_add_to_cart_souce_labs_oneside(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    button = catalog.add_to_cart('Sauce Labs Onesie')
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1

def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"

def test_product_details_jacket(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"

def test_add_and_remove_t_shirt(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    button = catalog.add_to_cart('Test.allTheThings() T-Shirt (Red)')
    expect(button).to_have_text("Remove")
    button = catalog.remove_from_cart('Test.allTheThings() T-Shirt (Red)')
    expect(button).to_have_text("Add to cart")


def test_add_and_remove_onesie(page):
    catalog = CatalogPage(page)
    catalog.login('standard_user', 'secret_sauce')
    catalog.add_to_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 1
    catalog.remove_from_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 0