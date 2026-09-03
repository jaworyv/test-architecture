import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestTransfer:
    @pytest.mark.api
    def test_transfer_one_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session, first_transfer_account, second_transfer_account):
        transfer_request = TransferRequest(fromAccountId=first_transfer_account.id, toAccountId=second_transfer_account.id, amount=500)
        response = api_manager.user_steps.transfer(transfer_request, create_user_request)
        assert transfer_request.fromAccountId == response.fromAccountId, 'ОР: Аккаунт откуда в запросе = Аккаунт откуда в ответе, ФР: Аккаунт откуда в запросе != Аккаунт откуда в ответе'
        assert transfer_request.toAccountId == response.toAccountId, 'ОР: Аккаунт куда в запросе = Аккаунт куда в ответе, ФР: Аккаунт куда в запросе != Аккаунт куда в ответе'
        assert first_transfer_account.balance - transfer_request.amount == response.fromAccountIdBalance, 'ОР: Баланс аккаунта = Баланс в ответе, ФР: Баланс аккаунта != Баланс в ответе'

        transaction_from_db = Transaction.get_transaction_by_accounts(db_session, response.fromAccountId, response.toAccountId)
        assert transaction_from_db.from_account_id == response.fromAccountId, 'ОР: Аккаунт откуда в БД = Аккаунт откуда в ответе, ФР: Аккаунт откуда в БД != Аккаунт откуда в ответе'
        assert transaction_from_db.to_account_id == response.toAccountId, 'ОР: Аккаунт куда в БД = Аккаунт куда в ответе, ФР: Аккаунт куда в БД != Аккаунт куда в ответе'
        assert transaction_from_db.amount == transfer_request.amount, 'ОР: Сумма перевода в БД = Сумма перевода в ответе, ФР: Сумма перевода в БД != Сумма перевода в ответе'
# --------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        499,
        10001,
    ])
    def test_transfer_one_user_invalid(self, amount, api_manager: ApiManager, create_user_request: CreateUserRequest,invalid_first_transfer_account, invalid_second_transfer_account):
        transfer_request = TransferRequest(fromAccountId=invalid_first_transfer_account.id, toAccountId=invalid_second_transfer_account.id, amount=amount)
        api_manager.user_steps.invalid_transfer(transfer_request, create_user_request)

