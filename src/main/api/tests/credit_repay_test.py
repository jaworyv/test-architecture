import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.credit_request import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

class TestCreditRepay:
    @pytest.mark.api
    def test_credit_repay(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest,db_session: Session, create_credit_account_request, credit_request: CreditRequest):
        credit_repay_request = CreditRepayRequest(creditId=credit_request.creditId, accountId=create_credit_account_request.id, amount=credit_request.amount)
        response = api_manager.user_steps.credit_repay(credit_repay_request, create_credit_user_request)
        assert credit_repay_request.creditId == response.creditId, 'ОР: ID кредита в запросе = ID кредита в ответе, ФР: ID кредита в запросе != ID кредита в ответе'
        assert credit_repay_request.amount == response.amountDeposited, 'ОР: Сумма пополнения в запросе = Сумма пополнения в ответе, ФР: Сумма пополнения в запросе != Сумма пополнения в ответе'

        credit_transaction_from_db = Transaction.get_credit_transaction_by_id(db_session, response.creditId)
        assert credit_transaction_from_db.credit_id == response.creditId, 'ОР: ID кредита в БД = ID кредита в ответе, ФР: ID кредита в БД != ID кредита в ответе'
        assert credit_transaction_from_db.amount == response.amountDeposited, 'ОР: Сумма пополнения в БД = Сумма пополнения в ответе, ФР: Сумма пополнения в БД != Сумма пополнения в ответе'
# --------------------------------------------------------
    @pytest.mark.api
    @pytest.mark.parametrize("amount, expected_error", [
        (4999, "The amount is not enough. Credit balance: -5000"),
        (5001, "Insufficient funds. Current balance: 5000.00, required: 5001.00")
    ])
    def test_invalid_credit_repay(self, amount, expected_error, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, db_session: Session, create_credit_account_request, invalid_credit_request: CreditRequest):
        credit_repay_request = CreditRepayRequest(creditId=invalid_credit_request.creditId, accountId=create_credit_account_request.id, amount=amount)
        response = api_manager.user_steps.invalid_credit_repay(credit_repay_request, create_credit_user_request)
        assert response.json()["error"] == expected_error
        credit_from_db = Credit.get_credit_by_id(db_session, invalid_credit_request.creditId)
        assert credit_from_db.balance == -invalid_credit_request.amount, 'ОР: Баланс кредита не изменился, ФР: Баланс кредита изменился'