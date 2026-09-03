import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_credit_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_account_request(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account_request = api_manager.user_steps.create_account(create_user_request)
    return account_request

@pytest.fixture
def create_credit_account_request(api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest):
    credit_account_request = api_manager.user_steps.create_account(create_credit_user_request)
    return credit_account_request

@pytest.fixture
def create_two_accounts_request(api_manager: ApiManager, create_user_request: CreateUserRequest):
    first_account = api_manager.user_steps.create_account(create_user_request)
    second_account = api_manager.user_steps.create_account(create_user_request)
    return first_account, second_account

@pytest.fixture
def transfer_accounts(api_manager, create_two_accounts_request, create_user_request):
    first_account, second_account = create_two_accounts_request
    deposit_request = AccountDepositRequest(accountId=first_account.id, amount=1000.5)
    first_account = api_manager.user_steps.account_deposit(create_user_request, deposit_request)
    return first_account, second_account

@pytest.fixture
def first_transfer_account(transfer_accounts):
    first_account, _ = transfer_accounts
    return first_account

@pytest.fixture
def second_transfer_account(transfer_accounts):
    _, second_account = transfer_accounts
    return second_account

@pytest.fixture
def invalid_transfer_accounts(api_manager, create_two_accounts_request, create_user_request):
    first_account, second_account = create_two_accounts_request
    first_deposit_request = AccountDepositRequest(accountId=first_account.id, amount=9000)
    api_manager.user_steps.account_deposit(create_user_request, first_deposit_request)
    second_deposit_request = AccountDepositRequest(accountId=first_account.id, amount=9000)
    first_account = api_manager.user_steps.account_deposit(create_user_request, second_deposit_request)
    return first_account, second_account

@pytest.fixture
def invalid_first_transfer_account(invalid_transfer_accounts):
    first_account, _ = invalid_transfer_accounts
    return first_account

@pytest.fixture
def invalid_second_transfer_account(invalid_transfer_accounts):
    _, second_account = invalid_transfer_accounts
    return second_account

@pytest.fixture
def credit_request(api_manager: ApiManager,create_credit_account_request, create_credit_user_request: CreateCreditUserRequest):
    credit_request = CreditRequest(accountId=create_credit_account_request.id, amount=5000, termMonths=12)
    credit_response = api_manager.user_steps.credit(credit_request, create_credit_user_request)
    return credit_response
