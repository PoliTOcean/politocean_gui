import sys
from typing import Any, Tuple
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication

import struct
import cv2
import numpy as np
import socket


class QCamera(QObject):
    MAX_DGRAM = 2 ** 16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64

    imageReady = pyqtSignal(QImage)
    connected = pyqtSignal(bool)

    def __init__(self, address: str = "127.0.0.1", port: int = None, fps: int = None, parent=None) -> None:
        QObject.__init__(self, parent)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = address
        self.__port = port
        self.__fps = fps

        self.__streaming = False
        self.__cleaned = False

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__readImage)

        if self.port is not None:
            self.__socket.bind((self.__address, self.port))

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port) -> None:
        self.__port = port
        self.__socket.bind((self.__address, self.__port))

    @property
    def address(self) -> str:
        return self.__address.toString()

    @address.setter
    def address(self, addr: str) -> None:
        self.__address = addr

        if self.__port is not None:
            self.__socket.bind((self.__address, self.__port))

    @property
    def fps(self) -> int:
        return self.__fps

    @fps.setter
    def fps(self, fps) -> None:
        self.__fps = fps

        if self.__streaming:
            self.stop()
            self.stream()

    @property
    def is_streaming(self) -> bool:
        return self.__streaming

    def close(self) -> None:
        self.__socket.close()

    def stop(self) -> None:
        if not self.__streaming:
            return

        self.__timer.stop()
        self.__streaming = False

    def stream(self):
        if self.__streaming:
            return

        self.__socket.settimeout(5 / self.__fps)
        self.__timer.start(1000 // self.__fps)
        self.__streaming = True

    def __readImage(self) -> None:
        data = b''
        i = 2
        try:
            if not self.__cleaned:
                self.__clean()

            while i > 1:
                i, seg = self.__read()
                data += seg

            frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
            image = QImage(
                frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()

            self.imageReady.emit(image)

            self.connected.emit(True)
        except socket.timeout:
            self.connected.emit(False)

    def __read(self) -> Tuple[int, bytes]:
        seg, _ = self.__socket.recvfrom(self.MAX_DGRAM)

        return struct.unpack("B", seg[0:1])[0], seg[1:]

    def __clean(self) -> None:
        i = 2
        while i > 1:
            i, seg = self.__read()

        print("finish emptying buffer")
        self.__cleaned = True


class QCameraView(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

        self.setAlignment(Qt.AlignCenter)

        self.__camera: QCamera = None

    def stop(self):
        if self.__camera is None:
            return

        self.__camera.stop()

    def play(self):
        if self.__camera is None:
            return

        self.__camera.stream()

    def setCamera(self, camera: QCamera) -> None:
        if self.__camera is not None and self.__camera.is_streaming:
            self.__camera.stop()

        self.__camera = camera
        self.__camera.imageReady.connect(self.setImage)

    @property
    def is_streaming(self) -> bool:
        if self.__camera is None:
            return False

        return self.__camera.is_streaming

    @pyqtSlot(QImage)
    def setImage(self, img):
        self.setPixmap(QPixmap.fromImage(img).scaled(
            self.width(), self.height()))
