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
    def test_credit_repay(self):
        create_user_request = CreateUserRequest(username="Credit244", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Credit244", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_create_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Credit244", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_created()
        ).post(credit_request)
        credit_id = credit_create_response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)
        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="Credit244", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        assert credit_repay_request.creditId == response.creditId
        assert credit_repay_request.amount == response.amountDeposited


    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        4999,
        5001,
    ])
    def test_credit_repay(self, amount):
        create_user_request = CreateUserRequest(username=f"Cred2t{amount}", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Cred2t{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        credit_create_response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Cred2t{amount}", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_created()
        ).post(credit_request)
        credit_id = credit_create_response.creditId

        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=amount)
        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Cred2t{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)