import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session, create_account_request, deposit_amount: float):
        account_deposit_request = AccountDepositRequest(accountId=create_account_request.id, amount=deposit_amount)
        response = api_manager.user_steps.account_deposit(create_user_request, account_deposit_request)
        assert account_deposit_request.accountId == response.id, 'ОР: ID аккаунта в запросе = ID аккаунта в ответе, ФР: ID аккаунта в запросе != ID аккаунта в ответе'
        assert account_deposit_request.amount == response.balance, 'ОР: Баланс в запросе = Баланс в ответе, ФР: Баланс в запросе != Баланс в ответе'

        deposit_account_from_db = Transaction().get_transaction_by_id(db_session, response.id)
        assert deposit_account_from_db.to_account_id == response.id, 'ОР: ID аккаунта в БД = ID аккаунта в ответе, ФР: ID аккаунта в БД != ID аккаунта в ответе'
        assert deposit_account_from_db.amount == account_deposit_request.amount, 'ОР: Сумма пополнения в БД = Сумма пополнения в ответе, ФР: Сумма пополнения в БД != Сумма пополнения в ответе'
        balance_from_db = Account.get_account_by_id(db_session, response.id)
        assert balance_from_db.balance == response.balance, 'ОР: Баланс в БД = Баланс в ответе, ФР: Баланс в БД != Баланс в ответе'
# ---------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount, expected_error", [
        (999, "Amount must be between 1000 and 9000"),
        (9001, "Amount must be between 1000 and 9000")
    ])
    def test_account_deposit_invalid(self, amount, expected_error, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session, create_account_request):
        account_deposit_request = AccountDepositRequest(accountId=create_account_request.id, amount=amount)
        response = api_manager.user_steps.account_invalid_deposit(create_user_request, account_deposit_request)
        assert response.json()["error"] == expected_error
        balance_from_db = Account.get_account_by_id(db_session, create_account_request.id)
        assert balance_from_db.balance == 0, 'ОР: Баланс в БД = 0, ФР: Баланс в БД != 0'

