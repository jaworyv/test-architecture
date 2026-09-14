import allure
from playwright.sync_api import Page

from ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(self.page)

    @allure.step("Заполняем все поля на форме checkout")
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.checkout.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step("Завершаем checkout")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Получаем текст ошибки на Checkout")
    def get_error_text(self):
        return self.checkout.get_error_text()

    @allure.step("Получаем текст после успешного Checkout")
    def get_success_text(self) -> str:
        return self.checkout.get_success_text()

    @allure.step("Получаем сумму товаров")
    def get_item_total(self) -> float:
        return self.checkout.get_item_total()

    @allure.step("Получаем сумму товаров после continue")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()

    @allure.step("Получаем налог")
    def get_tax_total(self) -> float:
        return self.checkout.get_tax_total()

    @allure.step("Получаем сумму с налогом")
    def get_total(self) -> float:
        return self.checkout.get_total()