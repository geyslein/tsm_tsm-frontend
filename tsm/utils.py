import secrets
import string
from .models import Database, MqttConfig, RawDataStorage, SftpConfig, Thing


def get_db(thing: Thing):
    try:
        return Database.objects.get(thing_id=thing.id)
    except Database.DoesNotExist:
        return None


def get_storage(thing: Thing):
    try:
        return RawDataStorage.objects.get(thing_id=thing.id)
    except RawDataStorage.DoesNotExist:
        return None


def get_db_string(thing: Thing):
    db = get_db(thing)
    if db:
        return 'postgresql://' + db.username + ':' + db.password + '@' + db.url + '/rdm_tsm'
    else:
        return '-'


def get_active_parser(thing: Thing):
    try:
        sftp_conf: SftpConfig = SftpConfig.objects.get(thing_id=thing.id)
        if sftp_conf:
            return sftp_conf.parser_set.all()[0]
    except RawDataStorage.DoesNotExist:
        return None


def get_mqtt_device(thing: Thing):
    try:
        mqtt_conf: MqttConfig = MqttConfig.objects.get(thing_id=thing.id)
        if mqtt_conf:
            return mqtt_conf.device_type.name
    except RawDataStorage.DoesNotExist:
        return None


def generate_password(length: int):
    chars = string.ascii_letters + string.digits
    password = ''

    for _ in range(length):
        password += secrets.choice(chars)

    return password


def get_json_config(thing: Thing):
    storage = get_storage(thing)

    default_parser = ''
    parser = {}
    if thing.datasource_type == 'SFTP':
        thing_parser = get_active_parser(thing)

        default_parser = thing_parser.type
        parser = {
            "type": default_parser,
            "settings": {
                "timestamp_format": thing_parser.timestamp_format,
                "header": thing_parser.exclude_headlines,
                "delimiter": thing_parser.delimiter,
                "timestamp_column": thing_parser.timestamp_column,
                "skipfooter": thing_parser.exclude_footlines
            }
        }

    if thing.datasource_type == 'MQTT':
        default_parser = get_mqtt_device(thing)
        parser = {
            "type": default_parser
        }

    config = {
        "uuid": str(thing.thing_id),
        "name": thing.name,
        "database": {
            "username": '',
            "password": '',
            "url": get_db_string(thing),
        },
        "project": {
            "name": thing.group_id.name,
            "uuid": ''
        },
        "raw_data_storage": {
            "bucket_name": storage.bucket,
            "username":  storage.access_key,
            "password": storage.secret_key
        },
        "description": "automatically generated config",
        "properties": {
            "default_parser": default_parser,
            "parsers": [
                parser
            ]
        }
    }
    return config


def start_ingest(thing: Thing):
    thing.is_active = True
    thing.save()

    print(get_json_config(thing))
    # TODO post config to tsm-dispatcher
