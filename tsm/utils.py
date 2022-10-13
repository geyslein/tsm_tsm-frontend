from typing import List
import re
import secrets
import string
from .models import Database, MqttConfig, Parser, RawDataStorage, SftpConfig, Thing
from django.contrib.auth.models import Group
import datetime
import uuid


def get_db_by_thing(thing: Thing):
    try:
        return Database.objects.get(group=thing.group)
    except Database.DoesNotExist:
        return None


def get_storage_by_thing(thing: Thing):
    try:
        return RawDataStorage.objects.get(thing_id=thing.id)
    except RawDataStorage.DoesNotExist:
        return None


def get_connection_string(thing: Thing):
    db = get_db_by_thing(thing)
    if db:
        return 'postgresql://{}:{}@{}/{}'.format(db.username, db.password, db.url, db.name)
    else:
        return '-'


def get_active_parser(thing: Thing):
    try:
        sftp_conf: SftpConfig = SftpConfig.objects.get(thing_id=thing.id)
        if sftp_conf:
            parsers = sftp_conf.parser_set.all()
            return select_parser_by_current_date(parsers)
    except RawDataStorage.DoesNotExist:
        return None


def get_mqtt_device(thing: Thing):
    try:
        mqtt_conf: MqttConfig = MqttConfig.objects.get(thing_id=thing.id)
        if mqtt_conf:
            return mqtt_conf.device_type.name
    except RawDataStorage.DoesNotExist:
        return None


def get_random_chars(length: int):
    chars = string.ascii_letters + string.digits
    result = ''

    for _ in range(length):
        result += secrets.choice(chars)

    return result


def create_db_username(group: Group):
    name = group.name.replace(' ', '')
    return re.sub(
        '[^a-z0-9_]+',
        '',
        '{shortname}_{uuid}'.format(shortname=name[0:30].lower(), uuid=str(uuid.uuid4()))
    )


def select_parser_by_current_date(parsers: List[Parser]):
    if len(parsers) == 1:
        return parsers[0]

    now = datetime.datetime.now

    for parser in parsers:
        if parser['start_time']:
            start = parser['start_time']
            if now.strftime('%Y-%m-%d %H:%M') >= start.strftime('%Y-%m-%d %H:%M'):
                return parser

        if parser['end_time']:
            end = parser['end_time']

            if now.strftime('%Y-%m-%d %H:%M') <= end.strftime('%Y-%m-%d %H:%M'):
                return parser


def get_parser_properties(thing: Thing):
    thing_parser: Parser = get_active_parser(thing)

    default_parser = thing_parser.type
    parser = {
        "type": default_parser,
        "settings": {
            "delimiter": thing_parser.delimiter,
            "footlines": thing_parser.exclude_footlines,
            "headlines": thing_parser.exclude_headlines,
            "timestamp": {
                "date": {
                    "pattern": thing_parser.timestamp_format,
                    "position": thing_parser.timestamp_column,
                    "replacement": thing_parser.timestamp_format
                },
                "time": {
                    "pattern": thing_parser.timestamp_format,
                    "position": thing_parser.timestamp_column,
                    "replacement": thing_parser.timestamp_format
                }
            }
        }
    }

    return {
            "default_parser": default_parser,
            "parsers": [
                parser
            ]
        }


def get_json_config(thing: Thing):
    storage: RawDataStorage = get_storage_by_thing(thing)

    properties = {}
    if thing.datasource_type == 'SFTP':
        properties = get_parser_properties(thing)

    if thing.datasource_type == 'MQTT':
        default_parser = get_mqtt_device(thing)
        properties = {
            "default_parser": default_parser,
            "parsers": [
                default_parser
            ]
        }

    db: Database = get_db_by_thing(thing)

    config = {
        "uuid": str(thing.thing_id),
        "name": thing.name,
        "database": {
            "username": db.username,
            "password": db.password,
            "url": get_connection_string(thing),
        },
        "project": {
            "name": thing.group.name,
            "uuid": str(uuid.uuid4()),
        },
        "raw_data_storage": {
            "bucket_name": storage.bucket,
            "username":  storage.access_key,
            "password": storage.secret_key
        },
        "description": thing.description,
        "properties": properties
    }
    return config
