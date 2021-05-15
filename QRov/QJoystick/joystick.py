import sdl2
import sdl2.ext

from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot

from .mappings import XboxOneMapping
from .element import QJoystickAxis, QJoystickButton
from .signals import QJoystickSignals


class QJoystick(QObject):
    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)

        self.signals = QJoystickSignals()

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__timer.start(16)

    @property
    def name(self):
        return sdl2.SDL_JoystickName(self.__joystick).decode('utf8')

    @property
    def connected(self):
        if self.__joystick:
            return True

        return False

    def __open(self):
        self.__joystick = sdl2.SDL_JoystickOpen(0)
    
    def __close(self):
        sdl2.SDL_JoystickClose(self.__joystick)

    def __update(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.signals.axisChanged.emit(QJoystickAxis(event.jaxis.axis, event.jaxis.value))
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.signals.buttonChanged.emit(QJoystickButton(event.jbutton.button, event.jbutton.state))
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.signals.buttonChanged.emit(QJoystickButton(event.jbutton.button, event.jbutton.state))
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.signals.connected.emit(True)
                self.__open()
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.__close()
                self.signals.connected.emit(False)

    def get_button(self, button: int):
        return self.__buttons[button]

    def get_axis(self, axis: int):
        return self.__axes[axis]