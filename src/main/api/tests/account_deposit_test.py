import pytest
from src.main.api.models.account_deposit_request import AccountDepositRequest



@pytest.mark.api
class TestAccountDeposit:
    def test_account_deposit(self, api_manager, create_user_request):
        create_account = api_manager.user_steps.create_account(create_user_request)
        account_id = create_account.id
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=1000.5)
        response = api_manager.user_steps.account_deposit(create_user_request, account_deposit_request)

        assert account_deposit_request.accountId == response.id
        assert account_deposit_request.amount == response.balance

    @pytest.mark.api
    @pytest.mark.parametrize("amount", [
        999,
        9001
    ])
    def test_account_deposit_invalid(self, amount, api_manager, create_user_request):
        create_account = api_manager.user_steps.create_account(create_user_request)
        account_id = create_account.id
        account_deposit_request = AccountDepositRequest(accountId=account_id, amount=amount)
        api_manager.user_steps.account_invalid_deposit(create_user_request, account_deposit_request)