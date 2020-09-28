from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from servers.enums import ServerStatus, CommandType, CommandResult
from servers.models import Server, Command
from servers.serializers import ServerSerializer, CommandSerializer
from servers.utils import log_command


class ServerViewSet(viewsets.ModelViewSet):
    serializer_class = ServerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Server.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        log_command(
            CommandType.CREATE,
            serializer.instance,
            self.request.user,
            CommandResult.SUCCESS,
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        log_command(
            CommandType.MODIFY,
            serializer.instance,
            self.request.user,
            CommandResult.SUCCESS,
        )

    def perform_destroy(self, instance):
        if instance.server_status != ServerStatus.DELETED.name:
            instance.server_status = ServerStatus.DELETED.name
            instance.save()
            log_command(
                CommandType.DELETE, instance, self.request.user, CommandResult.SUCCESS,
            )
        else:
            log_command(
                CommandType.DELETE, instance, self.request.user, CommandResult.ERROR,
            )
            raise ValidationError("Server already deleted")

    @action(detail=True, methods=["post"])
    def start(self, request, pk):
        try:
            server = Server.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise NotFound()

        if server.server_status == ServerStatus.STOPPED.name:
            server.server_status = ServerStatus.RUNNING.name
            server.save()
            log_command(
                CommandType.START, server, self.request.user, CommandResult.SUCCESS
            )
            return Response()

        log_command(CommandType.START, server, self.request.user, CommandResult.ERROR)
        raise ValidationError(
            f"Cannot start the server because it is in status: {server.server_status}"
        )

    @action(detail=True, methods=["post"])
    def stop(self, request, pk):
        try:
            server = Server.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise NotFound()

        if server.server_status == ServerStatus.RUNNING.name:
            server.server_status = ServerStatus.STOPPED.name
            server.save()
            log_command(
                CommandType.STOP, server, self.request.user, CommandResult.SUCCESS
            )
            return Response()

        log_command(CommandType.STOP, server, self.request.user, CommandResult.ERROR)
        raise ValidationError(
            f"Cannot stop the server because it is in status: {server.server_status}"
        )

    @action(detail=True, methods=["post"])
    def clone(self, request, pk):
        try:
            server = Server.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise NotFound()

        if server.server_status not in [
            ServerStatus.IN_PROGRESS.name,
            ServerStatus.DELETED.name,
        ]:
            server.id = None
            server.server_status = ServerStatus.STOPPED.name
            server.created = timezone.now()
            server.save()
            log_command(
                CommandType.CLONE, server, self.request.user, CommandResult.SUCCESS
            )
            return Response(self.serializer_class(server).data)

        log_command(CommandType.CLONE, server, self.request.user, CommandResult.ERROR)
        raise ValidationError(
            f"Cannot clone the server because it is in status: {server.server_status}"
        )


class CommandAPIView(ListAPIView):
    serializer_class = CommandSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Command.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
