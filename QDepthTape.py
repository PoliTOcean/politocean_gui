from PyQt5.QtGui import QColor
from PyQt5.QtQml import QQmlComponent
from PyQt5.QtQuick import QQuickView, QQuickItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QUrl, pyqtProperty, pyqtSignal, pyqtSlot


class QDepthTape(QWidget):
    def __init__(self, maxDepth=5, parent=None) -> None:
        QWidget.__init__(self, parent)

        self.maxDepth = maxDepth
        self.tickList = []
        self.lastChange = 0
        self.lastDepth = 0

        self.viewer = QQuickView()
        self.viewer.setSource(QUrl('resources/DepthTape.qml'))
        self.viewer.setResizeMode(QQuickView.SizeRootObjectToView)
        self.viewer.setColor(QColor(53, 53, 53))

        self.container = QWidget.createWindowContainer(self.viewer)
        self.container.setFixedWidth(70)
        self.container.setFocusPolicy(Qt.TabFocus)

        self.currentReadingComponent = QQmlComponent(
            self.viewer.engine(), QUrl("resources/DepthCurrentReading.qml"))

        self.currentReadingItem = self.currentReadingComponent.create()
        self.currentReadingItem.setParentItem(self.viewer.rootObject())

        self.currentReadingItem.setZ(5)

        for i in range(self.maxDepth + 1):
            tickComponent = QQmlComponent(
                self.viewer.engine(), QUrl("resources/DepthTick.qml"))

            tickItem = tickComponent.create()
            tickItem.setParentItem(self.viewer.rootObject())

            tickItem.text = str(i)

            self.tickList.append(tickItem)

        self.resetGraphics()

        self.viewer.widthChanged.connect(self.resetGraphics)
        self.viewer.heightChanged.connect(self.resetGraphics)

        self.container.show()

    def show(self) -> None:
        return self.container.show()

    def resetGraphics(self):
        self.currentReadingItem.setX(self.viewer.width() -
                                     self.currentReadingItem.width() + 2)
        self.currentReadingItem.setY(
            self.viewer.height()/2 - self.currentReadingItem.height()/2)

        for i, tickItem in enumerate(self.tickList, start=0):
            tickItem.setX(15 - tickItem.property("textX"))
            tickItem.setY(i*40 + self.viewer.height() /
                          2 - tickItem.height()/2)

        self.updateDepth(self.lastDepth)

    @pyqtSlot(float)
    def updateDepth(self, depth: float):
        print(depth)
        self.currentReadingItem.text = str(depth)
        change = depth * -40.0
        for tickItem in self.tickList:
            tickItem.setY(tickItem.y() + change)

        self.lastDepth = depth


class QDepthTick(QQuickItem):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        QQuickItem.__init__(self, parent)
        self._text = "0"

    @pyqtProperty(str, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.textChanged.emit(text)


class QDepthCurrentReading(QQuickItem):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        QQuickItem.__init__(self, parent)

        self._text = "0.0m"

    @pyqtProperty(str, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text+"m"
        self.textChanged.emit(text)
