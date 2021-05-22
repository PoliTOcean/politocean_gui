from PyQt5.QtCore import QObject

class MQTTStatus(QObject):
    Disconected = 0
    Connecting = 1
    Connected = 2