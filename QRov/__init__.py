from .QSensor import QSensor
from .QRelay import QRelay
from .QJoystick import QJoystick, QJoystickAxis, QJoystickButton

import yaml
from yamlinclude import YamlIncludeConstructor


class QRov:
    def __init__(self, config_path: str = "config/"):
        self.configured = False

        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader, base_dir=config_path)

        with open(config_path+'config.yaml', 'r') as config_yaml:
            config = yaml.load(config_yaml, Loader=yaml.FullLoader)
            self.sensors = [QSensor(s["name"], s["units"])
                            for s in config["sensors"]]
            self.relays = [QRelay(r["name"], False)
                           for r in config["relays"]]

            self.configured = True
