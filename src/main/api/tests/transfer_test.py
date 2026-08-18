import pytest

from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests.account_deposit_requester import AccountDepositRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs



class TestTransfer:
    @pytest.mark.api
    def test_transfer_one_user(self):
        create_user_request = CreateUserRequest(username="Transferuser2", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        first_account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Transferuser2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        first_account_id = first_account_create_response.id

        second_account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Transferuser2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        second_account_id = second_account_create_response.id

        account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=1000.5)
        account_deposit_response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username="Transferuser2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_deposit_request)
        account_balance = account_deposit_response.balance

        transfer_request = TransferRequest(fromAccountId=first_account_id, toAccountId=second_account_id, amount=500)
        response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username="Transferuser2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert transfer_request.fromAccountId == response.fromAccountId
        assert transfer_request.toAccountId == response.toAccountId
        assert account_balance - transfer_request.amount == response.fromAccountIdBalance

    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        499,
        10001,
    ])
    def test_transfer_one_user_invalid(self, amount):
        create_user_request = CreateUserRequest(username=f"Transf{amount}", password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        first_account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Transf{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        first_account_id = first_account_create_response.id

        second_account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Transf{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        second_account_id = second_account_create_response.id

        first_account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=9000)
        AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Transf{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(first_account_deposit_request)

        second_account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=9000)
        account_deposit_response = AccountDepositRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Transf{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(second_account_deposit_request)
        account_balance = account_deposit_response.balance

        transfer_request = TransferRequest(fromAccountId=first_account_id, toAccountId=second_account_id, amount=amount)
        response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Transf{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_request)


