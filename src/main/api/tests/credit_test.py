import pytest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequest



class TestCredit:
    @pytest.mark.api
    def test_credit(self, api_manager, create_credit_user_request, db_session):
        create_account = api_manager.user_steps.create_account(create_credit_user_request)
        account_id = create_account.id

        credit_request = CreditRequest(accountId=account_id, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit(credit_request, create_credit_user_request)

        assert credit_request.accountId == response.id
        assert credit_request.amount == response.amount
        assert credit_request.termMonths == response.termMonths
        assert credit_request.amount == response.balance

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId
        assert credit_from_db.account_id == account_id
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
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
