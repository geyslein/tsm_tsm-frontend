import uuid
from django.conf import settings
from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=1000)
    thing_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    project = models.CharField(max_length=1000)
    datasource_type = models.CharField(
        max_length=4,
        choices=[('SFTP', 'SFTP'), ('MQTT', 'MQTT'), ],
        default='SFTP',
    )
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class SftpConfig(models.Model):
    uri = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    filename_pattern = models.CharField(max_length=200)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class MqttConfig(models.Model):
    uri = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000)
    device_type = models.CharField(
        max_length=100,
        choices=[('campbell_cr6', 'campbell_cr6'), ],
        default='campbell_cr6',
    )
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Database(models.Model):
    url = models.CharField(max_length=1000)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.username


class Parser(models.Model):
    parser_type = models.CharField(
        max_length=100,
        choices=[('CSV', 'CSV'),],
        default='CSV',
    )
    delimiter = models.CharField(max_length=1)
    exclude_headlines = models.IntegerField(default=0)
    time_column = models.IntegerField()
    timestamp_expression = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    sftp_config = models.ForeignKey(SftpConfig, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + self.parser_type
