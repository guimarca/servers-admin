import uuid

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from servers.enums import (
    ServerStatus,
    ServerType,
    ServerFlavor,
    CommandType,
    ServerStorage,
    CommandResult,
)


class Server(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server_type = models.CharField(max_length=50, choices=ServerType.tuples())
    server_flavor = models.CharField(max_length=50, choices=ServerFlavor.tuples())
    server_status = models.CharField(max_length=50, choices=ServerStatus.tuples())
    server_storage = models.CharField(max_length=50, choices=ServerStorage.tuples())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="servers",)


class Command(TimeStampedModel):
    command = models.CharField(max_length=50, choices=CommandType.tuples())
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="server_commands",
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_commands",
    )
    result = models.CharField(max_length=50, choices=CommandResult.tuples())
    server_status = models.CharField(max_length=50, choices=ServerStatus.tuples())
