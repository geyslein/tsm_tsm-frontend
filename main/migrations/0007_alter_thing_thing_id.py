# Generated by Django 4.0.7 on 2022-09-02 13:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_sftpconfig_thing_thing_mqtt_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='thing_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]