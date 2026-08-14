import requests
import pytest

from src.main.api.models import create_user_request
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestCreateUser:
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())
# --------------------------------------------------------
    def test_create_user_valid(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json()["token"]

        create_user_request = CreateUserRequest(username="Blake224", password="Pas!sw0rd", role="ROLE_USER")
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role
# --------------------------------------------------------
    @pytest.mark.parametrize(
        "username,password",
        [
            ("abв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Blake3", "Pas!sw0rд"),
            ("Blake4", "Pas!sw0"),
            ("Blake5", "pas!sw0rd"),
            ("Blake6", "PAS!SW0RD"),
            ("Blake3", "PAssw0rd"),
            ("Blake3", "PAs!sword"),
        ]
    )
    def test_create_user_invalid(self, username, password):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        token = login_admin_response.json()["token"]
        assert login_admin_response.status_code == 200

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 400