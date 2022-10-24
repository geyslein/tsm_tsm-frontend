import uuid
from django.contrib.auth.models import Group
from django.db import models


class MqttDeviceType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Thing(models.Model):
    name = models.CharField(max_length=1000)
    thing_id = models.UUIDField(
        'ID',
        default=uuid.uuid4,
        editable=False)
    datasource_type = models.CharField(
        'Ingest Type',
        max_length=4,
        choices=[('SFTP', 'SFTP'), ('MQTT', 'MQTT'), ],
        default='SFTP',
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Project')
    description = models.CharField(max_length=1000, blank=True, null=True)
    is_ready = models.BooleanField('Ready', default=False)
    sftp_uri = models.URLField('Fileserver URI', blank=True, null=True)
    sftp_username = models.CharField('Username', max_length=1000, blank=True, null=True)
    sftp_password = models.CharField('Password', max_length=1000, blank=True, null=True)
    sftp_filename_pattern = models.CharField('Filename pattern', max_length=200, blank=True, null=True)
    mqtt_uri = models.CharField('Broker URI', max_length=1000, blank=True, null=True)
    mqtt_username = models.CharField('Username', max_length=1000, blank=True, null=True)
    mqtt_password = models.CharField('Password', max_length=1000, blank=True, null=True)
    mqtt_hashed_password = models.CharField(max_length=256, blank=True, null=True)
    mqtt_topic = models.CharField('Topic', max_length=1000, blank=True, null=True)
    mqtt_device_type = models.ForeignKey(MqttDeviceType, verbose_name='Device Type', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Thing'
        verbose_name_plural = 'Things'


class Database(models.Model):
    url = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Project')

    def __str__(self):
        return self.username


class RawDataStorage(models.Model):
    bucket = models.CharField(max_length=63)
    access_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    thing = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.bucket


class Parser(models.Model):
    type = models.CharField('File type',
        max_length=100,
        choices=[('CsvParser', 'CSV'), ],
        default='CsvParser',
    )
    delimiter = models.CharField('Column delimiter', max_length=1, blank=True, null=True)
    exclude_headlines = models.PositiveIntegerField('Number of headlines to exclude', default=0, blank=True, null=True)
    exclude_footlines = models.PositiveIntegerField('Number of footlines to exclude', default=0, blank=True, null=True)
    timestamp_column = models.PositiveIntegerField(blank=True, null=True)
    timestamp_format = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' ' + self.type
