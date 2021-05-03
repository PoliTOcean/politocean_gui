import yaml
from yamlinclude import YamlIncludeConstructor


class QRovRelay:
    def __init__(self, name: str, enabled: bool) -> None:
        self.name = name
        self.enabled = enabled

    def __repr__(self) -> str:
        return f"{self.name}: Enabled" if self.enabled else f"{self.name}: Disabled"

    def __str__(self) -> str:
        return self.__repr__()


class QRovSensor:
    def __init__(self, name: str, value: float, units: str) -> None:
        self.name = name
        self.value = value
        self.units = units

    def __repr__(self) -> str:
        return f"{self.name}: {self.value} {self.units}"

    def __str__(self) -> str:
        return self.__repr__()


class QRov:
    def __init__(self, config_path: str = "config/"):
        self.configured = False

        YamlIncludeConstructor.add_to_loader_class(
            loader_class=yaml.FullLoader, base_dir=config_path)

        with open(config_path+'config.yaml', 'r') as config_yaml:
            config = yaml.load(config_yaml, Loader=yaml.FullLoader)
            self.sensors = [QRovSensor(s["name"], 0, s["units"])
                            for s in config["sensors"]]
            self.relays = [QRovRelay(r["name"], False)
                           for r in config["relays"]]

            self.configured = True


if __name__ == '__main__':
    rov = QRov()
    if rov.configured:
        print(rov.sensors)
        print(rov.relays)
