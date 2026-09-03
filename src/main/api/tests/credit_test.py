import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest



class TestCredit:
    @pytest.mark.api
    def test_credit(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, db_session: Session, create_credit_account_request, credit_amount: float, credit_months: int):
        credit_request = CreditRequest(accountId=create_credit_account_request.id, amount=credit_amount, termMonths=credit_months)
        response = api_manager.user_steps.credit(credit_request, create_credit_user_request)

        assert credit_request.accountId == response.id, 'ОР: ID аккаунта в запросе = ID аккаунта в ответе, ФР: ID аккаунта в запросе != ID аккаунта в ответе'
        assert credit_request.amount == response.amount, 'ОР: Сумма пополнения в запросе = Сумма пополнения в ответе, ФР: Сумма пополнения в запросе != Сумма пополнения в ответе'
        assert credit_request.termMonths == response.termMonths, 'ОР: Срок кредита в запросе = Срок кредита в ответе, ФР: Срок кредита в запросе != Срок кредита в ответе'
        assert credit_request.amount == response.balance, 'ОР: Сумма пополнения = Сумма кредита в ответе, ФР: Сумма пополнения != Сумма кредита в ответе'

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId, 'ОР: ID кредита в БД = ID кредита в ответе, ФР: ID кредита в БД != ID кредита в ответе'
        assert credit_from_db.account_id == create_credit_account_request.id, 'ОР: ID аккаунта в БД = ID аккаунта в ответе, ФР: ID аккаунта в БД != ID аккаунта в ответе'
        assert credit_from_db.amount == credit_request.amount, 'ОР: Сумма пополнения БД = Сумма пополнения в ответе, ФР: Сумма пополнения в БД != Сумма пополнения в ответе'
        assert credit_from_db.term_months == credit_request.termMonths, 'ОР: Срок кредита в БД = Срок кредита в ответе, ФР: Срок кредита в БД != Срок кредита в ответе'
# --------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount, expected_error", [
        (4999, "Amount must be between 5000 and 15000"),
        (15001, "Amount must be between 5000 and 15000")
    ])
    def test_credit_invalid(self,amount, expected_error, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, create_credit_account_request, credit_months: int):
        credit_request = CreditRequest(accountId=create_credit_account_request.id, amount=amount, termMonths=credit_months)
        response = api_manager.user_steps.invalid_credit(credit_request, create_credit_user_request)
        assert response.json()["error"] == expected_error
