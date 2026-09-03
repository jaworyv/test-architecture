import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [
            RandomModelGenerator.generate(CreateUserRequest),
        ]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)
        assert create_user_request.username == response.username, 'ОР: Пользователь в запросе = Пользователь в ответе, ФР: Пользователь в запросе != Пользователь в ответе'
        assert create_user_request.role == response.role, 'ОР: Роль в запросе = Роль в ответе, ФР: Роль в запросе != Роль в ответе'

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'ОР: Созданный пользователь есть в БД, ФР: Созданного пользователя нет в БД'
# --------------------------------------------------------
    @pytest.mark.parametrize(
        "username,password, expected_error",
        [
            ("abв", "Pas!sw0rd", "Username can only contain Latin letters and numbers"),
            ("ab", "Pas!sw0rd", "Username must be at least 3 characters long"),
            ("abv!", "Pas!sw0rd", "Username can only contain Latin letters and numbers"),
            ("Blake3", "Pas!sw0rд", "Password can only contain Latin letters, numbers and special characters"),
            ("Blake4", "Pas!sw0", "Password must be at least 8 characters long"),
            ("Blake5", "pas!sw0rd", "Password must contain at least one uppercase letter"),
            ("Blake6", "PAS!SW0RD", "Password must contain at least one lowercase letter"),
            ("Blake3", "PAssw0rd", "Password must contain at least one special character"),
            ("Blake3", "PAs!sword", "Password must contain at least one number"),
        ]
    )
    def test_create_user_invalid(self, username, password, expected_error, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        response = api_manager.admin_steps.create_invalid_user(create_user_request)
        assert response.json()["error"] == expected_error
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'ОР: Аккаунт не создан, ФР: Аккаунт создан'