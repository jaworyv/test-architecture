import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit(self, api_manager, create_user_request, db_session):
        create_account = api_manager.user_steps.create_account(create_user_request)
        account_id = create_account.id
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=1000.5)
        response = api_manager.user_steps.account_deposit(create_user_request, account_deposit_request)

        assert account_deposit_request.accountId == response.id
        assert account_deposit_request.amount == response.balance

        deposit_account_from_db = Transaction().get_transaction_by_id(db_session, response.id)
        assert deposit_account_from_db.to_account_id == response.id
        assert deposit_account_from_db.amount == account_deposit_request.amount
        balance_from_db = Account.get_account_by_id(db_session, response.id)
        assert balance_from_db.balance == response.balance
# ---------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        999,
        9001
    ])
    def test_account_deposit_invalid(self, amount, api_manager, create_user_request, db_session):
        create_account = api_manager.user_steps.create_account(create_user_request)
        account_id = create_account.id
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=amount)
        api_manager.user_steps.account_invalid_deposit(create_user_request, account_deposit_request)
        balance_from_db = Account.get_account_by_id(db_session, account_id)
        assert balance_from_db.balance == 0
