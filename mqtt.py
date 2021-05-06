from QRov import QSensor
import threading
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal

import paho.mqtt.client as mqtt
import json


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    temperature = pyqtSignal(float)
    depth = pyqtSignal(float)
    voltage = pyqtSignal(float)
    current = pyqtSignal(float)


class MQTTWorker(QThread, mqtt.Client):
    '''
    Worker thread for MQTT updates.
    '''
    signals = WorkerSignals()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.connect("localhost", 1883, 60)
        self.subscribe("sensors/#")

        self._lock = threading.Lock()
        self.running = False

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        j = json.loads(msg.payload.decode())

        self.signals.temperature.emit(j["temperature"])
        self.signals.depth.emit(j["depth"])
        self.signals.voltage.emit(j["voltage"])
        self.signals.current.emit(j["current"])

    def run(self):
        with self._lock:
            self.running = True

        self.loop_forever()

    @pyqtSlot()
    def stop(self):
        with self._lock:
            self.running = False

        self.loop_stop()

    def add_sensor(self, sensor: QSensor):
        target = sensor.name.lower()
        if target == "temperature":
            self.signals.temperature.connect(
                sensor.update)
        elif target == "depth":
            self.signals.depth.connect(sensor.update)
        elif target == "voltage":
            self.signals.voltage.connect(sensor.update)
        elif target == "current":
            self.signals.current.connect(sensor.update)
