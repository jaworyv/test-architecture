import requests
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.account_deposit_response import AccountDepositResponse
from src.main.api.requests.requester import Requester
from http import HTTPStatus

class AccountDepositRequester(Requester):
    def post(self, account_deposit_request: AccountDepositRequest) -> AccountDepositResponse:
        url=f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=account_deposit_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return AccountDepositResponse(**response.json())
        return response
