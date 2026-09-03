import random


class DataGenerator:
    @staticmethod
    def deposit_amount() -> float:
        return round(random.uniform(1000, 9000), 2)

    @staticmethod
    def credit_amount() -> float:
        return round(random.uniform(5000, 15000), 2)

    @staticmethod
    def credit_months() -> int:
        return random.randint(1, 12)

    @staticmethod
    def transfer_amount() -> float:
        return round(random.uniform(500, 1000), 2)