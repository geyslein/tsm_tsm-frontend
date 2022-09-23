import os
import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with MQTT-Broker")


def on_publish(client, userdata, mid):
    print("Message with id: {} published.".format(mid))


def publish_thing_config(thing_event_msg_json):

    mqtt_broker = os.environ.get("MQTT_BROKER")
    mqtt_user = os.environ.get("MQTT_USER")
    mqtt_password = os.environ.get("MQTT_PASSWORD")

    client = mqtt.Client("TSM-FRONTEND")
    client.username_pw_set(mqtt_user, mqtt_password)
    client.connect(mqtt_broker)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.loop_start()  # important to spawn a thread for receiving acks from broker when using qos>0!

    config = json.dumps(thing_event_msg_json)
    client.publish("thing_creation", str(config), qos=2)

    print('thing published:')
    print(thing_event_msg_json)
    client.loop_stop()
