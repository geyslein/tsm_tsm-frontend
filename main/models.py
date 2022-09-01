import uuid
from django.db import models


class Database(models.Model):
    url = models.CharField(max_length=1000)
    schema = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.schema


class Thing(models.Model):
    name = models.CharField(max_length=1000)
    thing_id = models.CharField(max_length=1000)
    project = models.CharField(max_length=1000)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    datasource_type = models.CharField(
        max_length=4,
        choices=[('SFTP', 'SFTP'), ('MQTT', 'MQTT'), ],
        default='SFTP',
    )
    sftp_uri = models.CharField(max_length=1000, blank=True, null=True)
    sftp_username = models.CharField(max_length=1000, blank=True, null=True)
    sftp_password = models.CharField(max_length=1000, blank=True, null=True)
    sftp_filename_pattern = models.CharField(max_length=200, blank=True, null=True)
    mqtt_uri = models.CharField(max_length=1000, blank=True, null=True)
    mqtt_username = models.CharField(max_length=1000, blank=True, null=True)
    mqtt_password = models.CharField(max_length=1000, blank=True, null=True)
    mqtt_topic = models.CharField(max_length=1000, blank=True, null=True)


class Parser(models.Model):
    name = models.CharField(max_length=200)
    parser_type = models.CharField(
        max_length=10,
        choices=[('CSV', 'CSV'), ],
        default='CSV',
    )
    delimiter = models.CharField(max_length=200)
    exclude_headlines = models.IntegerField(default=0)
    time_column = models.IntegerField()
    timestamp_expression = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
