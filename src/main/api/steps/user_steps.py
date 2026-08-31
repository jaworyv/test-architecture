from src.main.api.foundation.endpoints import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models import create_user_request
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest, BaseCreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: BaseCreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def account_deposit(self, create_user_request: BaseCreateUserRequest, account_deposit_request: AccountDepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(account_deposit_request)
        return response

    def account_invalid_deposit(self, create_user_request: BaseCreateUserRequest, account_deposit_request: AccountDepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(account_deposit_request)
        return response

    def transfer(self, transfer_request: TransferRequest, create_user_request: BaseCreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def invalid_transfer(self, transfer_request: TransferRequest, create_user_request: BaseCreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer_request)
        return response
    def credit(self, credit_request: CreditRequest, create_credit_user_request: BaseCreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_credit_user_request.username, create_credit_user_request.password),
            Endpoint.CREDIT,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def invalid_credit(self, credit_request: CreditRequest, create_credit_user_request: BaseCreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_credit_user_request.username, create_credit_user_request.password),
            Endpoint.CREDIT,
            ResponseSpecs.request_bad()
        ).post(credit_request)
        return response

    def credit_repay(self, credit_repay_request: CreditRepayRequest, create_credit_user_request: BaseCreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_credit_user_request.username, create_credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def invalid_credit_repay(self, credit_repay_request: CreditRepayRequest, create_credit_user_request: BaseCreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_credit_user_request.username, create_credit_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
        return response