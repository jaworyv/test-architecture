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
    def test_credit(self):
        create_user_request = CreateUserRequest(username="Credit24", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Credit24", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Credit24", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_created()
        ).post(credit_request)


        assert credit_request.accountId == response.id
        assert credit_request.amount == response.amount
        assert credit_request.termMonths == response.termMonths
        assert credit_request.amount == response.balance

    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        4999,
        15001,
    ])
    def test_credit_invalid(self,amount):
        create_user_request = CreateUserRequest(username=f"Credit{amount}", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        account_create_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Credit{amount}", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = account_create_response.id

        credit_request = CreditRequest(accountId=account_id, amount=amount, termMonths=12)
        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username=f"Credit{amount}", password="Pas!sw0rd"),
            response_spec = ResponseSpecs.request_bad()
        ).post(credit_request)