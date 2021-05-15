import threading
from typing import Any, Callable
import paho.mqtt.client as mqtt
import json

from PyQt5.QtCore import QThread, pyqtSlot
from .sensor import QSensor


class MQTTWorker(QThread, mqtt.Client):
    '''
    Worker thread for MQTT updates.
    '''

    def __init__(self, topic: str, address: str = "localhost", port=1883, parent=None):
        QThread.__init__(self, parent)
        self.connect(address, port, 60)
        self.subscribe(topic)

        self.__lock = threading.Lock()
        self.__running = False

        self.__callbacks = {}
        
    @property
    def running(self):
        return self.__running

    def set_callback(self, id: str, callback: Callable[[Any],None]):
        self.__callbacks[id] = callback

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        j = json.loads(msg.payload.decode())

        for key, val in j.items():
            if key in self.__callbacks:
                self.__callbacks[key](val)

    def run(self):
        with self.__lock:
            self.__running = True

        self.loop_forever()

    @pyqtSlot()
    def stop(self):
        with self.__lock:
            self.__running = False

        self.loop_stop()
