import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCredit:
    @pytest.mark.api
    def test_credit(self, api_manager, create_credit_user_request):
        create_account = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = create_account.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit(credit_request, create_credit_user_request)

        assert credit_request.accountId == response.id
        assert credit_request.amount == response.amount
        assert credit_request.termMonths == response.termMonths
        assert credit_request.amount == response.balance
# --------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        4999,
        15001,
    ])
    def test_credit_invalid(self,amount, api_manager, create_credit_user_request):
        create_account = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = create_account.id

        credit_request = CreditRequest(accountId=account_id, amount=amount, termMonths=12)
        response = api_manager.user_steps.invalid_credit(credit_request, create_credit_user_request)
