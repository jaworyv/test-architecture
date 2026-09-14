import allure
from ui.pages.basket_page import BasketPage
from playwright.sync_api import Page

class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(self.page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Переходим к Checkout")
    def checkout_button(self):
        self.basket.checkout()
        return self

    @allure.step("Удаляем {product_name} из корзины")
    def remove_item(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Проверяем, что {product_name} присутствует в корзине")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)
        return self

    @allure.step("Проверяем, что {product_name} отсутствует в корзине")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)
        return self

    @allure.step("Получаем список наименований продуктов")
    def get_item_names(self):
        return self.basket.get_item_names()

    @allure.step("Возвращает список цен всех товаров в корзине")
    def get_item_prices(self):
        return self.basket.get_item_prices()

    @allure.step("Возвращем сумму товаров в корзине")
    def get_items_total_price(self):
        return self.basket.get_items_total_price()
