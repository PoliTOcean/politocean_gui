import json
import sys
import os
from PyQt5.QtCore import QObject, pyqtSlot
import yaml
from yamlinclude import YamlIncludeConstructor

from .QJoystick import QJoystick, QJoystickButton, QJoystickAxis
from .QMQTT import QMQTTClient, MQTTStatus
from .sensor import QSensor
from .relay import QRelay


class QRovController(QObject):
    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)

        self.__configured = False
        self.__sensors = {}
        self.__relays = []
        self.__mqttClient = None

    @property
    def sensors(self):
        return self.__sensors.values()

    @property
    def relays(self):
        return self.__relays

    @property
    def configured(self):
        return self.__configured

    @property
    def depth_sensor(self):
        if not self.__configured:
            return None

        return self.__sensors['depth'] if 'depth' in self.__sensors else None

    @property
    def joystick(self):
        if not self.__configured:
            return None

        return self.__joystick

    def configure(self, path):
        if not os.path.isdir(path):
            sys.exit("config must be a dir")

        config_path = os.path.join(path, 'config.yaml')
        if not os.path.isfile(config_path):
            sys.exit("config dir must contains config.yaml")

        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader, base_dir=path)

        with open(config_path, 'r') as config_yaml:
            config = yaml.load(config_yaml, Loader=yaml.FullLoader)

            self.__init_sensors(config['sensors'])
            self.__init_relays(config['relays'])
            self.__init_joystick(config['joystick'])
            self.__init_mqtt(config['mqtt'])

        self.__configured = True

        return self.__configured

    def __init_sensors(self, config):
        self.__sensors = {s['id']: QSensor(
            s['id'], s['name'], s['units']) for s in config}

    def __init_relays(self, config):
        self.__relays = [QRelay(r['name'], False) for r in config]

    def __init_mqtt(self, config):
        self.__mqttClient = QMQTTClient(config['address'], config['port'])
        self.__mqttClient.statusChanged.connect(self.__on_mqttStatusChanged)
        self.__mqttClient.connect()

    def __init_joystick(self, config):
        self.__joystick = QJoystick()
        self.__commands = config
        self.__joystick.axisChanged.connect(self.__on_axisChange)
        self.__joystick.buttonChanged.connect(self.__on_buttonChange)

    def __on_mqttSensorMessage(self, str):
        j: dict[str, any] = json.loads(str)

        for key, val in j.items():
            if key in self.__sensors:
                self.__sensors[key].update(val)

    @pyqtSlot(QJoystickAxis)
    def __on_axisChange(self, axis: QJoystickAxis):
        data = {self.__commands['axes'][axis.id]: axis.value}
        self.__mqttClient.publish("axis/", json.dumps(data))

    @pyqtSlot(QJoystickButton)
    def __on_buttonChange(self, button: QJoystickButton):
        command = self.__commands['buttons'][button.id]['onPress'] if button.value else self.__commands['buttons'][button.id]['onRelease']
        if command:
            self.__mqttClient.publish('command/', command)

    @pyqtSlot(int)
    def __on_mqttStatusChanged(self, status: int) -> None:
        if status == MQTTStatus.Connected:
            self.__mqttClient.subscribe(
                "sensors/", self.__on_mqttSensorMessage)
