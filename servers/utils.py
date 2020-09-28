from django.contrib.auth.models import User

from servers.enums import CommandType, CommandResult
from servers.models import Command, Server


def log_command(
    command: CommandType, server: Server, creator: User, result: CommandResult
):
    Command.objects.create(
        command=command.name,
        server=server,
        creator=creator,
        result=result.name,
        server_status=server.server_status,
    )
