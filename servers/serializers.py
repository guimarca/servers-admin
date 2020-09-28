from rest_framework import serializers

from servers.models import Server, Command


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server

        fields = "__all__"
        read_only_fields = ("creator",)


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command

        fields = "__all__"
        read_only_fields = ("creator",)
