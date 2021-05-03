from SensorSignals import SensorSignals

from PyQt5.QtCore import QRunnable, pyqtSlot
import paho.mqtt.client as mqtt
import json


class MQTTWorker(QRunnable, mqtt.Client):
    '''
    Worker thread for MQTT updates.
    '''
    signals = SensorSignals()

    def __init__(self):
        super(MQTTWorker, self).__init__()
        self.connect("localhost", 1883, 60)
        self.subscribe("sensors/#")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        j = json.loads(msg.payload.decode())
        temp = j["temperature"]
        pres = j["pressure"]

        self.signals.temperature.emit(temp)
        self.signals.pressure.emit(pres)
        print(f"Temperature: {temp}")
        print(f"Pressure: {pres}")

    @pyqtSlot()
    def run(self):
        print("Thread run")

        self.loop_forever()
