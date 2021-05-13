import sdl2
import sdl2.ext

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from .mappings import XboxOneMapping


class QJoystick(QObject):
    connected = pyqtSignal(bool)
    axisChanged = pyqtSignal()
    buttonChanged = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)

        self.__axes = []
        self.__buttons = []

        self.connect()

    def connect(self) -> bool:
        self.__joystick = sdl2.SDL_JoystickOpen(0)

        if self.__joystick:
            return True

        return False

    @property
    def name(self):
        return sdl2.SDL_JoystickName(self.__joystick).decode('utf8')

    def is_connected(self):
        if self.__joystick:
            return True

        return False

    def update(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.__axes[event.jaxis.axis] = event.jaxis.value
                self.axisChanged.emit()
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.__buttons[event.jbutton.button] = event.jbutton.state
                self.buttonChanged.emit()
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.__buttons[event.jbutton.button] = event.jbutton.state
                self.buttonChanged.emit()
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.connected.emit(True)
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.connected.emit(False)

    def loop_forever(self):
        while True:
            self.update()

    def get_button(self, button: int):
        return self.__buttons[button]

    def get_axis(self, axis: int):
        return self.__axes[axis]
