from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QLCDNumber


class QSensor(QObject):
    updated = pyqtSignal(float)

    def __init__(self, id: str, name: str, units: str) -> None:
        QObject.__init__(self)

        self.id = id
        self.name = name
        self.value = 0
        self.units = units

    def __repr__(self) -> str:
        return f"{self.name}: {self.value} {self.units}"

    def __str__(self) -> str:
        return self.__repr__()

    def update(self, value):
        self.value = value
        self.updated.emit(value)
