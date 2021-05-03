from PyQt5.QtCore import Q_ENUMS, Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QSizePolicy, QVBoxLayout, QFrame, QWidget


class ComponentStatus:
    ON = 0
    OFF = 1


class QLedIndicator(QFrame):
    Q_ENUMS(ComponentStatus)

    def __init__(self, title, parent=None):
        QFrame.__init__(self, parent)

        self.status = ComponentStatus.OFF

        self.titleLabel = QLabel(title)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.statusLabel = QLabel(
            "On" if self.status == ComponentStatus.ON else "Off")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.titleLabel)
        self.vLayout.addWidget(self.statusLabel)
        self.vLayout.setAlignment(
            self.vLayout, Qt.AlignHCenter | Qt.AlignVCenter)

        self.setLayout(self.vLayout)

        self.opacityEffect = QGraphicsOpacityEffect(self)

        self.setObjectName("LedIndicatorFrame")
        self.setFrameStyle(QFrame.Box | QFrame.Panel)
        self.setStyleSheet(
            '#LedIndicatorFrame { border: 3px solid #FFFFFF; background-color: #304E6E; }')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.deactivate()

    def activate(self):
        self.status = ComponentStatus.ON
        self.opacityEffect.setOpacity(0.3)
        self.setGraphicsEffect(self.opacityEffect)

    def deactivate(self):
        self.status = ComponentStatus.OFF
        self.opacityEffect.setOpacity(0.3)
        self.setGraphicsEffect(self.opacityEffect)
