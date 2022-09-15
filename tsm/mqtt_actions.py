import os
import json
import paho.mqtt.client as mqtt


# cat thing-event-msg.json | docker-compose exec -T mqtt-broker sh -c "mosquitto_pub -t thing_creation -u \$MQTT_USER -P \$MQTT_PASSWORD -s"
def publish_thing_config(thing_event_msg_json):
    mqtt_broker = os.environ.get("MQTT_BROKER")
    mqtt_user = os.environ.get("MQTT_USER")
    mqtt_password = os.environ.get("MQTT_PASSWORD")

    client = mqtt.Client("TSM-FRONTEND")
    client.username_pw_set(mqtt_user, mqtt_password)
    client.connect(mqtt_broker)

    print(thing_event_msg_json)

    config = json.dumps(thing_event_msg_json)
    client.publish("thing_creation", str(config), qos=2)
