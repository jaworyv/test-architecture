from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.requester import Requester
import requests
from src.main.api.specs.request_specs import RequestSpecs
from http import HTTPStatus
from src.main.api.models.create_user_response import CreateUserResponse
from requests import Response

class LoginUserRequester(Requester):
    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse | Response:
        url=f"{self.base_url}/auth/token/login"
        response = requests.post(
            url=url,
            json=login_user_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        return LoginUserResponse(**response.json())