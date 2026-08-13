import requests
import pytest

@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        assert login_admin_response.status_code == 200
        assert login_admin_response.json()["user"]["username"] == 'admin'
        assert login_admin_response.json()["user"]["role"] == 'ROLE_ADMIN'

    def test_login_user(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        assert login_admin_response.status_code == 200
        token = login_admin_response.json()["token"]

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Blake67",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        user_login_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Blake67",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        assert user_login_response.status_code == 200
        assert user_login_response.json()["user"]["username"] == 'Blake67'
        assert user_login_response.json()["user"]["role"] == 'ROLE_USER'

