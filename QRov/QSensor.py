from PyQt5.QtCore import Qt, QObject, pyqtSlot
from PyQt5.QtWidgets import QLabel, QLCDNumber


class QSensor(QObject):
    def __init__(self, name: str, units: str) -> None:
        QObject.__init__(self)

        self.name = name
        self.value = 0
        self.units = units

        self.labelName = QLabel()
        self.labelName.setText(self.name+":")
        self.labelName.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.lcd = QLCDNumber()
        self.lcd.display(self.value)
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.labelUnits = QLabel()
        self.labelUnits.setText(self.units)
        self.labelUnits.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def __repr__(self) -> str:
        return f"{self.name}: {self.value} {self.units}"

    def __str__(self) -> str:
        return self.__repr__()

    @pyqtSlot(float)
    def update(self, value):
        self.value = value
        self.lcd.display(self.value)
