import sys
import os
import yaml
from yamlinclude import YamlIncludeConstructor


from .sensor import QSensor
from .relay import QRelay
from .mqtt import MQTTWorker

class QRovController:
    def __init__(self):
        self.__configured = False
        self.__sensors = []
        self.__relays = []
        self.__mqtt = None
    
    @property
    def sensors(self):
        return self.__sensors

    @property
    def relays(self):
        return self.__relays

    @property
    def configured(self):
        return self.__configured

    def configure(self, path):
        if not os.path.isdir(path):
            sys.exit("config must be a dir")

        config_path = os.path.join(path, 'config.yaml')
        if not os.path.isfile(config_path):
            sys.exit("config dir must contains config.yaml")

        YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=path)

        with open(config_path, 'r') as config_yaml:
            config = yaml.load(config_yaml, Loader=yaml.FullLoader)

            self.__init_sensors(config)
            self.__init_relays(config)

        self.__init_mqtt()

        self.__configured = True

        return self.__configured

    def __init_sensors(self, config):
        self.__sensors = [QSensor(s['id'], s['name'], s['units']) for s in config['sensors']]

    def __init_relays(self, config):
        self.__relays = [QRelay(r['name'], False) for r in config['relays']]

    def __init_mqtt(self):
        self.__mqtt = MQTTWorker("sensors/#")
        for s in self.__sensors:
            self.__mqtt.set_callback(s.id, s.update)
        self.__mqtt.start()

    @property
    def depth_sensor(self):
        return next((s for s in self.__sensors if s.id == 'depth'), None)