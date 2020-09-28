import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from servers.enums import ServerType, ServerFlavor, ServerStatus, ServerStorage
from servers.models import Server


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    user = User.objects.create(username="admin", email="admin@unicc.org")
    return user


@pytest.fixture
def api_client_admin(admin_user):
    api_client = APIClient()
    token = Token.objects.create(user=admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {str(token)}")
    return api_client


@pytest.fixture
def server_ps_running(admin_user):
    return Server.objects.create(
        server_type=ServerType.PS.name,
        server_flavor=ServerFlavor.C4_16GB.name,
        server_status=ServerStatus.RUNNING.name,
        server_storage=ServerStorage.TB10.name,
        creator=admin_user,
    )


@pytest.fixture
def server_ps_stopped(admin_user):
    return Server.objects.create(
        server_type=ServerType.PS.name,
        server_flavor=ServerFlavor.C4_16GB.name,
        server_status=ServerStatus.STOPPED.name,
        server_storage=ServerStorage.TB10.name,
        creator=admin_user,
    )
