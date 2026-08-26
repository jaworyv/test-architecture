import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester



@pytest.mark.api
class TestCreateUser:

    def test_create_user_valid(self, api_manager):
        create_user_request = CreateUserRequest(username="Larl322", password="Pas!sw0rd", role="ROLE_USER")
        response = api_manager.admin_steps.create_user(create_user_request)
        
        assert create_user_request.username == response.username
        assert create_user_request.role == response.role
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
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)