import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_user_request, db_session):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'ID аккаунта нет в БД'
        assert account_from_db.balance is not None, 'Поле баланса для созданного аккунта нет в БД'
