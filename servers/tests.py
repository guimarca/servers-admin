import pytest
from rest_framework import status

from servers.enums import CommandType, CommandResult, ServerStatus
from servers.models import Command, Server


@pytest.mark.django_db
class TestStart:
    def test_start_ok(self, api_client_admin, server_ps_stopped):
        response = api_client_admin.post(f"/server/{server_ps_stopped.id}/start/")
        assert response.status_code == status.HTTP_200_OK
        assert Server.objects.first().server_status == ServerStatus.RUNNING.name

        command = Command.objects.first()
        assert command.command == CommandType.START.name
        assert command.result == CommandResult.SUCCESS.name
        assert command.creator.username == "admin"
        assert command.server == server_ps_stopped

    def test_start_already_running(self, api_client_admin, server_ps_running):
        response = api_client_admin.post(f"/server/{server_ps_running.id}/start/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Server.objects.first().server_status == ServerStatus.RUNNING.name

        command = Command.objects.first()
        assert command.command == CommandType.START.name
        assert command.result == CommandResult.ERROR.name
        assert command.server == server_ps_running


@pytest.mark.django_db
class TestStart:
    def test_stop_ok(self, api_client_admin, server_ps_running):
        response = api_client_admin.post(f"/server/{server_ps_running.id}/stop/")
        assert response.status_code == status.HTTP_200_OK
        assert Server.objects.first().server_status == ServerStatus.STOPPED.name

        command = Command.objects.first()
        assert command.command == CommandType.STOP.name
        assert command.result == CommandResult.SUCCESS.name
        assert command.creator.username == "admin"
        assert command.server == server_ps_running

    def test_stop_not_running(self, api_client_admin, server_ps_stopped):
        response = api_client_admin.post(f"/server/{server_ps_stopped.id}/stop/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Server.objects.first().server_status == ServerStatus.STOPPED.name

        command = Command.objects.first()
        assert command.command == CommandType.STOP.name
        assert command.result == CommandResult.ERROR.name
        assert command.server == server_ps_stopped


@pytest.mark.django_db
class TestDelete:
    def test_delete(self, api_client_admin, server_ps_stopped):
        response = api_client_admin.delete(f"/server/{server_ps_stopped.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Server.objects.first().server_status == ServerStatus.DELETED.name

        command = Command.objects.first()
        assert command.command == CommandType.DELETE.name
        assert command.result == CommandResult.SUCCESS.name
        assert command.server == server_ps_stopped


@pytest.mark.django_db
class TestClone:
    def test_clone(self, api_client_admin, server_ps_running):
        response = api_client_admin.post(f"/server/{server_ps_running.id}/clone/")
        assert response.status_code == status.HTTP_200_OK

        servers = Server.objects.all()
        assert len(servers) == 2
        equal_fields = (
            "server_type",
            "server_flavor",
            "server_storage",
        )
        for field in equal_fields:
            assert getattr(servers[0], field) == getattr(servers[1], field)

        command = Command.objects.first()
        assert command.command == CommandType.CLONE.name
        assert command.result == CommandResult.SUCCESS.name
        assert command.creator.username == "admin"
        assert command.server == servers[1]
