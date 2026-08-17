import pytest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_deposit_requester import AccountDepositRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_account_requester import CreateAccountRequester


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit(self):
        create_user_request = CreateUserRequest(username="Blake410", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Blake410", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=1000.5)
        response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Blake410", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)

        assert account_deposit_request.accountId == response.id
        assert account_deposit_request.amount == response.balance

    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        999,
        9001
    ])
    def test_account_deposit_invalid(self, amount):
        create_user_request = CreateUserRequest(username=f"Blake44{amount}", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Blake44{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=amount)
        response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Blake44{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(account_deposit_request)