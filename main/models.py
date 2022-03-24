import uuid
from django.db import models


class Shuttle(models.Model):
    name = models.CharField(max_length=200)
    host = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    type = models.CharField(
        max_length=4,
        choices=[('SFTP', 'SFTP'), ('MQTT', 'MQTT'), ],
        default='SFTP',
    )

    def __str__(self):
        return self.username + "@" + self.host


class SftpSettings(models.Model):
    shuttle = models.OneToOneField(
        Shuttle,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    path = models.CharField(max_length=200)
    filename_pattern = models.CharField(max_length=200)
    poll_interval = models.CharField(max_length=200)

    def __str__(self):
        return self.path


class MqttSettings(models.Model):
    shuttle = models.OneToOneField(
        Shuttle,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    protocol = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    client_id = models.CharField(max_length=200)

    def __str__(self):
        return self.client_id


class RawdataStorage(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ParserType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Parser(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ParserType, on_delete=models.CASCADE)
    delimiter = models.CharField(max_length=200)
    exclude_headlines = models.IntegerField(default=0)
    exclude_footer = models.IntegerField(default=0)
    timestamp_field = models.IntegerField()
    timestamp_expression = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DatastoreType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Datastore(models.Model):
    label = models.CharField(max_length=200)
    type = models.ForeignKey(DatastoreType, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.label


class Datasource(models.Model):
    name = models.CharField(max_length=1000)
    serial_number = models.CharField(max_length=1000)
    description = models.CharField(max_length=4000)
    project = models.CharField(max_length=1000)
    contacts = models.CharField(max_length=1000)
    datasource_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    shuttle = models.ForeignKey(Shuttle, on_delete=models.CASCADE)
    rawdata_storage = models.ForeignKey(RawdataStorage, on_delete=models.CASCADE)
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE)
    datastore = models.ForeignKey(Datastore, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
