from PyQt5.QtGui import QBrush, QColor
import numpy as np

from QRov import QRov
from QLedIndicator import QLedIndicator
from pyqtgraph import PlotWidget
import custom_types as t

from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLCDNumber, QLabel, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import Qt
from Ui_MainWindow import Ui_MainWindow

from QActivityMonitor import QActivityMonitor


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Status Lights
        statusGrid = self.ui.groupBoxStatus.layout()

        statusLightCom = QLedIndicator("COM")
        # statusLightCom.setIndicatorTitle("COM")
        statusLightRpi = QLedIndicator("RPi")
        # statusLightRpi.setIndicatorTitle("RPi")
        statusLightJoystick = QLedIndicator("Joystick")
        # statusLightJoystick.setIndicatorTitle("RPi")
        statusLightLights = QLedIndicator("Lights")

        statusGrid.addWidget(statusLightCom, 0, 0, 1, 1)
        statusGrid.addWidget(statusLightRpi, 0, 1, 1, 1)
        statusGrid.addWidget(statusLightJoystick, 1, 0, 1, 1)
        statusGrid.addWidget(statusLightLights, 1, 1, 1, 1)

        # Sensor Readouts
        self.rov = QRov()

        if len(self.rov.sensors) > 0:
            vLayout = QVBoxLayout(self.ui.groupBoxSensorReadouts)
            i = 0
            for sensor in self.rov.sensors:
                labelName = QLabel(self)
                labelName.setText(sensor.name+":")
                labelName.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                lcd = QLCDNumber(self)
                lcd.display(sensor.value)
                lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
                labelUnits = QLabel(self)
                labelUnits.setText(sensor.units)
                labelUnits.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                hLayout = QHBoxLayout(self)
                hLayout.addWidget(labelName)
                hLayout.addWidget(lcd)
                hLayout.addWidget(labelUnits)
                hLayout.setAlignment(hLayout, Qt.AlignHCenter)

                vLayout.addLayout(hLayout)

                # Setup plots
                graphColor = self.palette().highlight().color()
                graphColor.setAlpha(90)

                p = self.ui.graphWidget.addPlot(0, i)

                leftAxis = p.getAxis('left')
                leftAxis.setLabel(units=sensor.units)
                leftAxis.setPen(self.palette().windowText().color())
                leftAxis.setTextPen(self.palette().windowText().color())

                topAxis = p.getAxis('top')
                topAxis.setPen(self.palette().windowText().color())
                topAxis.setTextPen(self.palette().windowText().color())
                topAxis.setStyle(showValues=False)

                rightAxis = p.getAxis('right')
                rightAxis.setPen(self.palette().windowText().color())
                rightAxis.setTextPen(self.palette().windowText().color())
                rightAxis.setStyle(showValues=False)

                bottomAxis = p.getAxis('bottom')
                bottomAxis.setPen(self.palette().windowText().color())
                bottomAxis.setTextPen(self.palette().windowText().color())
                bottomAxis.setStyle(showValues=False)

                titleColor = self.palette().windowText().color()
                p.setTitle(sensor.name, color=titleColor,
                           size='12pt', bold=True)
                p.showAxis('top', True)
                p.showAxis('right', True)
                p.showGrid(x=True, y=True, alpha=0.2)
                p.setMouseEnabled(x=False, y=False)
                p.plot(y=3+np.random.normal(size=50),
                       brush=graphColor, fillLevel=0)

                i += 1

            self.ui.groupBoxSensorReadouts.setLayout(vLayout)

        if len(self.rov.relays) > 0:
            for relay in self.rov.relays:
                pb = QPushButton(self)
                pb.setText(relay.name)
                pb.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                self.ui.groupBoxRelayButtons.layout().addWidget(pb)

        self.activityMonitor = QActivityMonitor(self.ui.teLog)
        self.activityMonitor.display("GUI started...", t.Message.INFO)

        self.ui.graphWidget.setBackground(self.palette().window().color())
        self.ui.graphWidget.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.ui.graphWidget.ci.layout.setSpacing(20)

    def on_buttonClearLog_clicked(self):
        self.ui.teLog.clear()

    def on_buttonCopyLogToClipboard_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.teLog.toPlainText())
