from QCompass import QCompass
from PyQt5.QtGui import QCloseEvent
import numpy as np

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from Ui_MainWindow import Ui_MainWindow

from QRov import QRov
from QActivityMonitor import QActivityMonitor
from QLedIndicator import QLedIndicator
from QDepthTape import QDepthTape

import custom_types as t

from mqtt import MQTTWorker
from time import strftime


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

        self.mqttWorker = MQTTWorker()
        self.mqttWorker.start()

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
                self.mqttWorker.add_sensor(sensor)

                hLayout = QHBoxLayout(self)
                hLayout.addWidget(sensor.labelName)
                hLayout.addWidget(sensor.lcd)
                hLayout.addWidget(sensor.labelUnits)
                hLayout.setAlignment(hLayout, Qt.AlignHCenter)

                vLayout.addLayout(hLayout)

                self.setup_plots(sensor.name, sensor.units, i)

                i += 1

            self.ui.groupBoxSensorReadouts.setLayout(vLayout)

        if len(self.rov.relays) > 0:
            for relay in self.rov.relays:
                self.ui.groupBoxRelayButtons.layout().addWidget(relay.button)

        self.activityMonitor = QActivityMonitor(self.ui.teLog)
        self.activityMonitor.display("GUI started...", t.Message.INFO)

        self.ui.graphWidget.setBackground(self.palette().window().color())
        self.ui.graphWidget.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.ui.graphWidget.ci.layout.setSpacing(20)

        self.depthTape = QDepthTape()
        self.ui.gridLayoutHUD.addWidget(self.depthTape.container, 1, 0, 4, 1)

        self.compass = QCompass()
        self.ui.gridLayoutHUD.addWidget(self.compass.container, 0, 0, 1, 4)

        width = QApplication.primaryScreen().size().width()
        self.ui.splitterHorizontal.setSizes([width/8, width*5/8, width*2/8])

    def on_buttonClearLog_clicked(self):
        self.ui.teLog.clear()

    def on_buttonCopyLogToClipboard_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui.teLog.toPlainText())

    def setup_plots(self, title, units, position):
        graphColor = self.palette().highlight().color()
        graphColor.setAlpha(90)

        p = self.ui.graphWidget.addPlot(0, position, 1, 1)

        leftAxis = p.getAxis('left')
        leftAxis.setLabel(units=units)
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
        p.setTitle(title, color=titleColor,
                   size='12pt', bold=True)
        p.showAxis('top', True)
        p.showAxis('right', True)
        p.showGrid(x=True, y=True, alpha=0.2)
        p.setMouseEnabled(x=False, y=False)
        p.plot(y=3+np.random.normal(size=50),
               brush=graphColor, fillLevel=0)

    def update_time(self):
        self.ui.labCurrentTime.setText(strftime("%H"+":"+"%M"+":"+"%S"))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.mqttWorker.stop()
        self.mqttWorker.terminate()
        self.mqttWorker.wait()
