from PyQt5.QtCore import QObject

class QJoystickElement(QObject):
    def __init__(self, id, value, parent=None) -> None:
        QObject.__init__(self, parent)

        self.id = id
        self.value = value


class QJoystickAxis(QJoystickElement):
    def __init__(self, id, value, parent=None) -> None:
        super().__init__(id, value, parent=parent)


class QJoystickButton(QJoystickElement):
    def __init__(self, id, value, parent=None) -> None:
        super().__init__(id, value, parent=parent)