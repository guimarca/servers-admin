# Generated by Django 3.1.1 on 2020-09-28 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servers", "0002_command_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="command",
            name="server_status",
            field=models.CharField(
                choices=[
                    ("IN_PROGRESS", "A command is being processed"),
                    ("RUNNING", "VM up and running"),
                    ("STOPPED", "VM is stopped"),
                    ("DELETED", "VM deleted"),
                ],
                default="RUNNING",
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]
