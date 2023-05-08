import re
import secrets
import string
from .models import Database, Parser, RawDataStorage, Thing
from django.contrib.auth.models import Group
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
        return f'postgresql://{db.username}:{db.password}@{db.url}/{db.name}'
    else:
        return '-'


def get_active_parser(thing: Thing):
    try:
        return Parser.objects.get(thing=thing.id, is_active=True)
    except:
        print(f"Cannot find active Parser for thing {thing.id}")


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
        f'{name[0:30].lower()}_{uuid.uuid4()}'
    )


def create_bucket_name(thing: Thing):
    group = thing.group.name.replace(' ', '')
    return re.sub(
        '[^a-z0-9_]+',
        '',
        f'{group[:26].lower()}_{thing.thing_id}'
    )


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
    }

    if thing.datasource_type == 'SFTP':
        config['properties'] = get_parser_properties(thing)

    if thing.datasource_type == 'MQTT':
        default_parser = thing.mqtt_device_type.name
        config['properties'] = {
            "default_parser": default_parser,
            "parsers": []
        }

        config['mqtt_authentication_credentials'] = {
            "username": thing.mqtt_username,
            "password_hash": thing.mqtt_hashed_password,
            "description": thing.mqtt_topic,
            "properties": thing.mqtt_uri,
        }

    return config
