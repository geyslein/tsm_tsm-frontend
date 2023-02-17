import logging
import os
import json
import socket
import sys

import paho.mqtt.client as mqtt

logger = logging.getLogger('django')


def on_connect(client, userdata, flags, reason_code, properties=None):
    logger.info(
        f"Connected to MQTT broker {(userdata['mqtt_config']).get('broker_host')} "
        f"port {(userdata['mqtt_config']).get('broker_port')}"
    )


def on_publish(client, userdata, mid, result=None, properties=None):
    logger.info("Message with id: {} published.".format(mid))


mqtt_config = {
    'broker_host': os.environ.get("MQTT_BROKER_HOST"),
    'broker_port': int(os.environ.get("MQTT_BROKER_PORT", 1883)),
    'user': os.environ.get("MQTT_USER"),
    'password': os.environ.get("MQTT_PASSWORD")
}

# Do not try to connect the mqtt broker when using the Django cli (manage.py)
if sys.argv[0] != 'manage.py':
    client = mqtt.Client(protocol=mqtt.MQTTv5, userdata={"mqtt_config": mqtt_config})
    client.username_pw_set(mqtt_config['user'], mqtt_config['password'])
    client.on_connect = on_connect
    client.on_publish = on_publish

    try:
        client.connect(host=mqtt_config['broker_host'], port=mqtt_config['broker_port'])
    except (socket.gaierror, ConnectionRefusedError) as e:
        raise Exception(f"Unable to connect to mqtt broker {mqtt_config['broker_host']} on port "
                        f"{mqtt_config['broker_port']}", e)

    client.loop_start()  # important to spawn a thread for receiving acks from broker when using qos>0!


def publish_thing_config(thing_event_msg_json):

    config = json.dumps(thing_event_msg_json)
    if client.is_connected():
        result = client.publish("thing_creation", str(config), qos=2)
        result.wait_for_publish(5)
        logger.info(f'thing published: {thing_event_msg_json}')
    else:
        raise Exception(
            f"Unable to publish mqtt message to broker at {mqtt_config['broker_host']}."
            f" Client not connected."
        )
