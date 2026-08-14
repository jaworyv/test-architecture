


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def auth_headers():
        ...