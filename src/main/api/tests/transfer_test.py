import pytest
from src.main.api.models.account_deposit_request import AccountDepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestTransfer:
    @pytest.mark.api
    def test_transfer_one_user(self, api_manager, create_user_request, db_session):
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

        transaction_from_db = Transaction.get_transaction_by_accounts(db_session, response.fromAccountId, response.toAccountId)
        assert transaction_from_db.from_account_id == response.fromAccountId
        assert transaction_from_db.to_account_id == response.toAccountId
        assert transaction_from_db.amount == transfer_request.amount
# --------------------------------------------------------
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

