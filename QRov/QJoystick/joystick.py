import json
import sdl2
import sdl2.ext

import os

from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot

from .element import QJoystickAxis, QJoystickButton


class QJoystick(QObject):
    connected = pyqtSignal(bool)
    axisChanged = pyqtSignal(QJoystickAxis)
    buttonChanged = pyqtSignal(QJoystickButton)

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update)
        self.__timer.start(16)

        self.__mapping = None

    @property
    def name(self):
        return sdl2.SDL_JoystickName(self.__joystick).decode('utf8')

    def __open(self):
        self.__joystick = sdl2.SDL_JoystickOpen(0)

        with open(os.path.join(self.__location__, "mappings.json")) as jmaps:
            mappings = json.load(jmaps)

            if self.name in mappings:
                self.__mapping = mappings[self.name]

    def __close(self):
        sdl2.SDL_JoystickClose(self.__joystick)

    def __update(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.axisChanged.emit(QJoystickAxis(
                    self.__mapping['axes'][event.jaxis.axis], event.jaxis.value))
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.buttonChanged.emit(QJoystickButton(
                    self.__mapping['buttons'][event.jbutton.button], event.jbutton.state))
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.buttonChanged.emit(QJoystickButton(
                    self.__mapping['buttons'][event.jbutton.button], event.jbutton.state))
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.connected.emit(True)
                self.__open()
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.__close()
                self.connected.emit(False)
