from django.contrib import admin

from servers.models import Server, Command


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "server_type", "server_flavor", "server_storage", "server_status", "creator", "created")
    list_display_links = ("id",)
    list_filter = ("server_type", "server_flavor", "server_storage", "server_status",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "id")


@admin.register(Command)
class CredentialDefinitionAdmin(admin.ModelAdmin):
    list_display = ("id", "command", "server", "creator", "created")
    list_display_links = ("id",)
    list_filter = ("command", "server", "creator",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "name", "credential_json")