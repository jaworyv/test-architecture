import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditRepay:
    @pytest.mark.api
    def test_credit_repay(self, api_manager, create_credit_user_request):
        create_account = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = create_account.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_create_response = api_manager.user_steps.credit(credit_request, create_credit_user_request)
        credit_id = credit_create_response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)
        response = api_manager.user_steps.credit_repay(credit_repay_request, create_credit_user_request)

        assert credit_repay_request.creditId == response.creditId
        assert credit_repay_request.amount == response.amountDeposited


# --------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        4999,
        5001,
    ])
    def test_invalid_credit_repay(self, amount, api_manager, create_credit_user_request):
        create_account = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = create_account.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_create_response = api_manager.user_steps.credit(credit_request, create_credit_user_request)
        credit_id = credit_create_response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=amount)
        response = api_manager.user_steps.invalid_credit_repay(credit_repay_request, create_credit_user_request)