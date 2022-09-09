import uuid
from django.contrib.auth.models import Group
from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=1000)
    thing_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    datasource_type = models.CharField(
        'Ingest Type',
        max_length=4,
        choices=[('SFTP', 'SFTP'), ('MQTT', 'MQTT'), ],
        default='SFTP',
    )
    group_id = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Project')
    is_ready = models.BooleanField('Ready', default=False)
    is_active = models.BooleanField('Active', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Thing'
        verbose_name_plural = 'Things'


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


class RawDataStorage(models.Model):
    bucket = models.CharField(max_length=1000)
    access_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.username


class Parser(models.Model):
    type = models.CharField(
        max_length=100,
        choices=[('CsvParser', 'CSV'), ],
        default='CsvParser',
    )
    delimiter = models.CharField(max_length=1)
    exclude_headlines = models.IntegerField(default=0)
    exclude_footlines = models.IntegerField(default=0)
    timestamp_column = models.IntegerField()
    timestamp_format = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    sftp_config = models.ForeignKey(SftpConfig, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + self.type


class MqttDeviceType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MqttConfig(models.Model):
    uri = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000)
    device_type = models.ForeignKey(MqttDeviceType, on_delete=models.CASCADE)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )
