from PyQt5.QtCore import QObject, pyqtSignal

from .element import QJoystickAxis, QJoystickButton


class QJoystickSignals(QObject):
    connected = pyqtSignal(bool)
    axisChanged = pyqtSignal(QJoystickAxis)
    buttonChanged = pyqtSignal(QJoystickButton)