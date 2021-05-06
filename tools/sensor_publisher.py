import paho.mqtt.client as mqtt
import json

from random import random


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_publish(client, userdata, result):
    print(f"data published \nresult {result}")


def random_sensors():
    data = {}
    data['temperature'] = random()*100
    data['depth'] = random()*100
    data['voltage'] = random()*10
    data['current'] = random()*10

    return data


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect("localhost", 1883, 60)

    try:
        while True:
            input("Press Enter to continue...")
            client.publish("sensors/", json.dumps(random_sensors()))

    except KeyboardInterrupt:
        pass
