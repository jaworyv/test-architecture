import requests
import pytest

@pytest.mark.api
class TestCreateUser:
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
        token = login_admin_response.json()["token"]
        assert login_admin_response.status_code == 200
# --------------------------------------------------------
    def test_create_user_valid(self):
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
                "username": "Blake2",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Blake1"
        assert create_user_response.json()["role"] == "ROLE_USER"
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
        token = login_admin_response.json()["token"]
        assert login_admin_response.status_code == 200

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": password,
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 400