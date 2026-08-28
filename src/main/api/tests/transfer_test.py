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
    def test_transfer_one_user(self, api_manager, create_user_request):
        first_create_account = api_manager.user_steps.create_account(create_user_request)
        first_account_id = first_create_account.id
        second_create_account = api_manager.user_steps.create_account(create_user_request)
        second_account_id = second_create_account.id

        account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=1000.5)
        account_deposit = api_manager.user_steps.account_deposit(create_user_request, account_deposit_request)
        account_balance = account_deposit.balance

        transfer_request = TransferRequest(fromAccountId=first_account_id, toAccountId=second_account_id, amount=500)
        response = api_manager.user_steps.transfer(transfer_request, create_user_request)

        assert transfer_request.fromAccountId == response.fromAccountId
        assert transfer_request.toAccountId == response.toAccountId
        assert account_balance - transfer_request.amount == response.fromAccountIdBalance

    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        499,
        10001,
    ])
    def test_transfer_one_user_invalid(self, amount, api_manager, create_user_request):
        first_create_account = api_manager.user_steps.create_account(create_user_request)
        first_account_id = first_create_account.id
        second_create_account = api_manager.user_steps.create_account(create_user_request)
        second_account_id = second_create_account.id

        first_account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=9000)
        api_manager.user_steps.account_deposit(create_user_request, first_account_deposit_request)
        second_account_deposit_request = AccountDepositRequest(accountId=first_account_id, amount=9000)
        account_deposit = api_manager.user_steps.account_deposit(create_user_request, first_account_deposit_request)
        account_balance = account_deposit.balance

        transfer_request = TransferRequest(fromAccountId=first_account_id, toAccountId=second_account_id, amount=amount)
        api_manager.user_steps.invalid_transfer(transfer_request, create_user_request)

