from PyQt5.QtCore import QObject, pyqtSignal


class SensorSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    temperature = pyqtSignal(float)
    pressure = pyqtSignal(float)
